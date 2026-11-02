#!/usr/bin/env python3
"""
Export every cited paper across every SkillStack skill as a BibTeX file.

Walks every SKILL.md, extracts every arXiv identifier (``\\d{4}\\.\\d{4,5}``)
and every DOI (``10\\.\\d{4,}/...``), queries Crossref's REST API for the
full citation metadata of each DOI (and constructs an arXiv-flavoured
BibTeX entry for every arXiv identifier), deduplicates the entries, and
writes them to ``export/citations.bib``.

The exporter is polite: it pauses ``PolitePauseSeconds`` between successive
HTTP requests, caps retries at ``MaxRetries`` per identifier, and sends a
``User-Agent`` that identifies SkillStack to Crossref.

CLI:
  python scripts/ExportCollection.py
  python scripts/ExportCollection.py --out export/citations.bib
  python scripts/ExportCollection.py --timeout 10 --pause 0.2
"""

from __future__ import annotations

import argparse
import json
import re
import requests
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  EnsureDir,
  ExtractArxivIds,
  ExtractDois,
  IterateSkills,
  RelativeToSkills,
  SkillsRoot,
)

# Per-request timeout in seconds for the Crossref API.
RequestTimeout = 10
# Maximum number of HTTP attempts per identifier.
MaxRetries = 3
# Number of seconds to pause between successive Crossref requests.
PolitePauseSeconds = 0.2
# User-Agent string sent on every Crossref request (Crossref asks for one).
UserAgent = "SkillStack-CollectionExporter/1.0 (mailto:h3ossam@gmail.com)"
# Crossref REST API endpoint for a single work by DOI.
CrossrefApiUrl = "https://api.crossref.org/works/{doi}"
# arXiv BibTeX URL pattern (the canonical export endpoint).
ArxivBibUrl = "https://arxiv.org/bibtex/{arxivId}"

# Shared rich console for every code path.
console = Console()


@dataclass
class Citation:
  """A single deduplicated citation entry."""

  Kind: str  # "arxiv" or "doi"
  Value: str
  SkillName: str
  SkillPath: str
  BibEntry: str = ""
  Error: str = ""

  @property
  def CiteKey(self) -> str:
    """Return a stable BibTeX citekey derived from kind and value."""
    # Replace every non-alphanumeric character with an underscore for a
    # citekey that survives BibTeX's strict parser.
    raw = f"{self.Kind}_{self.Value}"
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", raw)
    return cleaned.strip("_")


@dataclass
class ExportReport:
  """Aggregate result of exporting every citation across every skill."""

  Total: int = 0
  Resolved: int = 0
  Failed: int = 0
  Citations: list[Citation] = field(default_factory=list)
  CiteKeys: set[str] = field(default_factory=set)

  @property
  def ExitCode(self) -> int:
    """Return non-zero when any citation failed to resolve."""
    return 0 if (self.Failed == 0) else 1


def CollectCitations(rootPath: Path | None = None) -> list[Citation]:
  """
  Walk every SKILL.md and collect every arXiv ID and DOI referenced.

  Args:
    rootPath (Path | None): Optional skills root override.

  Returns:
    list[Citation]: One Citation per (kind, value) pair, in first-seen
      order. Skills that reference the same identifier contribute only
      one Citation (the first skill that mentions it).
  """
  # Default to the auto-detected skills root.
  root = rootPath or SkillsRoot()
  # Walk every skill and accumulate (kind, value, skillName, skillPath).
  seen: dict[tuple[str, str], Citation] = {}
  for doc in IterateSkills(root):
    # Read the raw file text so the extractor sees every line.
    rawText = doc.SkillPath.read_text(encoding="utf-8")
    # Extract arXiv identifiers and DOIs from the full file body.
    for arxivId in ExtractArxivIds(rawText):
      key = ("arxiv", arxivId)
      # Skip identifiers we have already captured from a prior skill.
      if (key in seen):
        continue
      seen[key] = Citation(
        Kind="arxiv",
        Value=arxivId,
        SkillName=doc.Name,
        SkillPath=RelativeToSkills(doc.SkillPath),
      )
    for doi in ExtractDois(rawText):
      key = ("doi", doi)
      # Skip identifiers we have already captured from a prior skill.
      if (key in seen):
        continue
      seen[key] = Citation(
        Kind="doi",
        Value=doi,
        SkillName=doc.Name,
        SkillPath=RelativeToSkills(doc.SkillPath),
      )
  # Materialize the deduplicated citations in first-seen order.
  return list(seen.values())


def IssueGet(url: str, timeout: int, retries: int) -> tuple[int, str, str]:
  """
  Issue a GET request with retries and return (status, body, error).

  Args:
    url (str): The URL to fetch.
    timeout (int): Per-request timeout in seconds.
    retries (int): Maximum number of attempts.

  Returns:
    tuple[int, str, str]: A (status, body, error) triple. Status is 0 on
      transport failure; error carries the exception message.
  """
  # Set the polite User-Agent header for every request.
  headers = {"User-Agent": UserAgent, "Accept": "application/json"}
  lastError = ""
  # Retry up to the configured maximum, sleeping briefly between attempts.
  for attempt in range(retries):
    try:
      response = requests.get(url, headers=headers, timeout=timeout)
      # Return the status and body on any HTTP response (even a 4xx/5xx).
      return response.status_code, response.text, ""
    except requests.RequestException as exc:
      # Capture the exception message for the caller.
      lastError = str(exc)
      # Sleep briefly before retrying to be polite to the upstream API.
      time.sleep(PolitePauseSeconds)
  # All retries exhausted; surface the last error to the caller.
  return 0, "", lastError


def ResolveArxiv(citation: Citation, timeout: int) -> Citation:
  """
  Resolve one arXiv identifier to a BibTeX entry via the arXiv bibtex endpoint.

  Args:
    citation (Citation): The arXiv citation to resolve.
    timeout (int): Per-request timeout in seconds.

  Returns:
    Citation: The same citation with ``BibEntry`` populated on success
      or ``Error`` populated on failure.
  """
  # Build the arXiv bibtex URL for this identifier.
  url = ArxivBibUrl.format(arxivId=citation.Value)
  status, body, error = IssueGet(url, timeout, MaxRetries)
  # Surface any transport error to the caller.
  if (status == 0):
    citation.Error = f"transport error: {error}"
    return citation
  # Surface any non-200 status to the caller.
  if (status != 200):
    citation.Error = f"HTTP {status}"
    return citation
  # Trim leading/trailing whitespace from the bibtex body.
  entry = body.strip()
  # Reject empty responses (rare but possible).
  if (not entry):
    citation.Error = "empty bibtex body"
    return citation
  # Replace the auto-generated citekey with our stable one for dedup.
  entry = re.sub(r"@\w+\{[^,]+,", f"@misc{{{citation.CiteKey},", entry, count=1)
  citation.BibEntry = entry
  return citation


def ResolveDoi(citation: Citation, timeout: int) -> Citation:
  """
  Resolve one DOI to a BibTeX entry via the Crossref REST API.

  Args:
    citation (Citation): The DOI citation to resolve.
    timeout (int): Per-request timeout in seconds.

  Returns:
    Citation: The same citation with ``BibEntry`` populated on success
      or ``Error`` populated on failure.
  """
  # Build the Crossref REST API URL for this DOI.
  url = CrossrefApiUrl.format(doi=citation.Value)
  status, body, error = IssueGet(url, timeout, MaxRetries)
  # Surface any transport error to the caller.
  if (status == 0):
    citation.Error = f"transport error: {error}"
    return citation
  # Surface any non-200 status to the caller.
  if (status != 200):
    citation.Error = f"HTTP {status}"
    return citation
  # Parse the Crossref JSON response to extract the citation metadata.
  try:
    payload = json.loads(body)
  except json.JSONDecodeError as exc:
    citation.Error = f"JSON decode error: {exc}"
    return citation
  message = payload.get("message", {})
  # Synthesize a BibTeX entry from the Crossref metadata.
  entry = SynthesizeBibtex(message, citation.CiteKey)
  # Reject empty entries (rare but possible).
  if (not entry):
    citation.Error = "no bibtex synthesized"
    return citation
  citation.BibEntry = entry
  return citation


def SynthesizeBibtex(message: dict, citeKey: str) -> str:
  """
  Synthesize a BibTeX entry from a Crossref message payload.

  Args:
    message (dict): The ``message`` block of a Crossref work response.
    citeKey (str): The stable citekey to use for the entry.

  Returns:
    str: A BibTeX ``@article`` (or ``@misc``) entry as a single string.
  """
  # Extract the bibliographic type (defaults to "journal-article").
  kind = str(message.get("type", "misc") or "misc")
  # Map Crossref types to BibTeX entry types.
  bibtexType = "article"
  if (kind in ["book", "monograph"]):
    bibtexType = "book"
  elif (kind in ["proceedings-article", "conference-paper"]):
    bibtexType = "inproceedings"
  elif (kind in ["report", "report-component"]):
    bibtexType = "techreport"
  # Extract the title (Crossref returns a list).
  titles = message.get("title", []) or []
  title = titles[0] if (titles) else ""
  # Extract the authors.
  authors = FormatAuthors(message.get("author", []) or [])
  # Extract the container title (journal name).
  containers = message.get("container-title", []) or []
  journal = containers[0] if (containers) else ""
  # Extract the year from the issued date parts.
  issued = message.get("issued", {}).get("date-parts", [[]]) or [[]]
  year = ""
  if (issued and issued[0]):
    year = str(issued[0][0])
  # Extract the volume, issue, page, and publisher.
  volume = str(message.get("volume", "") or "")
  issueNumber = str(message.get("issue", "") or "")
  page = str(message.get("page", "") or "")
  publisher = str(message.get("publisher", "") or "")
  doi = str(message.get("DOI", "") or "")
  # Build the BibTeX entry line by line.
  lines = [f"@{bibtexType}{{{citeKey},"]
  if (authors):
    lines.append(f"  author = {{{authors}}},")
  if (title):
    lines.append(f"  title = {{{title}}},")
  if (journal):
    lines.append(f"  journal = {{{journal}}},")
  if (year):
    lines.append(f"  year = {{{year}}},")
  if (volume):
    lines.append(f"  volume = {{{volume}}},")
  if (issueNumber):
    lines.append(f"  number = {{{issueNumber}}},")
  if (page):
    lines.append(f"  pages = {{{page}}},")
  if (publisher):
    lines.append(f"  publisher = {{{publisher}}},")
  if (doi):
    lines.append(f"  doi = {{{doi}}},")
  # Close the entry.
  lines.append("}")
  return "\n".join(lines)


def FormatAuthors(authors: list) -> str:
  """
  Format a Crossref author list as a BibTeX "and"-separated string.

  Args:
    authors (list): The Crossref ``author`` array.

  Returns:
    str: Authors joined by " and " (BibTeX convention).
  """
  formatted: list[str] = []
  for author in authors:
    # Crossref splits family and given names.
    family = str(author.get("family", "") or "")
    given = str(author.get("given", "") or "")
    # Compose "Family, Given" for BibTeX.
    if (family and given):
      formatted.append(f"{family}, {given}")
    elif (family):
      formatted.append(family)
    elif (given):
      formatted.append(given)
  return " and ".join(formatted)


def ResolveAll(
  citations: list[Citation],
  timeout: int,
  pause: float,
) -> ExportReport:
  """
  Resolve every citation in the list, pausing politely between requests.

  Args:
    citations (list[Citation]): The citations to resolve.
    timeout (int): Per-request timeout in seconds.
    pause (float): Seconds to pause between successive requests.

  Returns:
    ExportReport: An aggregate report with every citation updated in
      place and totals computed.
  """
  report = ExportReport()
  # Track citekeys we have already resolved so duplicates are skipped.
  for citation in citations:
    # Skip duplicates by citekey (rare but possible across arXiv/DOI).
    if (citation.CiteKey in report.CiteKeys):
      continue
    report.Total += 1
    # Resolve the citation based on its kind.
    if (citation.Kind == "arxiv"):
      ResolveArxiv(citation, timeout)
    else:
      ResolveDoi(citation, timeout)
    # Update the totals based on whether resolution succeeded.
    if (citation.BibEntry):
      report.Resolved += 1
    else:
      report.Failed += 1
    # Track the citekey so duplicates are skipped on subsequent iterations.
    report.CiteKeys.add(citation.CiteKey)
    # Append the citation to the report.
    report.Citations.append(citation)
    # Pause politely between requests to be a good upstream citizen.
    time.sleep(pause)
  return report


def WriteBibtex(report: ExportReport, outPath: Path) -> Path:
  """
  Write the resolved BibTeX entries to the output file.

  Args:
    report (ExportReport): The aggregate report with resolved entries.
    outPath (Path): The output file path.

  Returns:
    Path: The absolute output file path that was written.
  """
  # Ensure the parent directory exists before opening the file.
  EnsureDir(outPath.parent)
  # Open the output file in write mode with UTF-8 encoding.
  with outPath.open("w", encoding="utf-8") as handle:
    # Write a header comment explaining the file's origin.
    handle.write("% SkillStack BibTeX export.\n")
    handle.write("% Auto-generated by scripts/ExportCollection.py.\n")
    handle.write(f"% Total entries: {report.Resolved} of {report.Total}.\n")
    handle.write("% Do not edit by hand; rerun the script to refresh.\n\n")
    # Write each resolved entry separated by a blank line.
    for citation in report.Citations:
      # Skip citations that failed to resolve.
      if (not citation.BibEntry):
        continue
      handle.write(citation.BibEntry)
      handle.write("\n\n")
  return outPath


def RenderSummary(report: ExportReport, outPath: Path) -> None:
  """
  Print a summary table of the export report.

  Args:
    report (ExportReport): The aggregate report.
    outPath (Path): The output file path that was written.
  """
  # Print the headline totals.
  console.print(
    f"[bold]Exported {report.Resolved} of {report.Total} citations to "
    f"{outPath}[/bold]"
  )
  # Build a table of the per-citation results.
  table = Table(show_lines=False)
  table.add_column("Kind", style="magenta")
  table.add_column("Value", style="cyan")
  table.add_column("First Skill", style="white")
  table.add_column("Status", style="green")
  table.add_column("Error", style="red")
  for citation in report.Citations:
    # Truncate long error messages for terminal display.
    error = citation.Error
    if (len(error) > 60):
      error = error[:57] + "..."
    status = "ok" if (citation.BibEntry) else "fail"
    table.add_row(citation.Kind, citation.Value, citation.SkillName, status, error)
  console.print(table)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """
  Parse the command-line arguments.

  Args:
    argv (list[str] | None): Optional argv override (for tests).

  Returns:
    argparse.Namespace: The parsed arguments.
  """
  parser = argparse.ArgumentParser(
    description="Export every cited paper across every SkillStack skill as a BibTeX file.",
  )
  # The output file path defaults to export/citations.bib under the repo root.
  parser.add_argument(
    "--out",
    type=Path,
    default=SkillsRoot() / "export" / "citations.bib",
    help="Output .bib file path (default: export/citations.bib).",
  )
  # Per-request timeout in seconds.
  parser.add_argument(
    "--timeout",
    type=int,
    default=RequestTimeout,
    help=f"Per-request timeout in seconds (default: {RequestTimeout}).",
  )
  # Polite pause between successive requests.
  parser.add_argument(
    "--pause",
    type=float,
    default=PolitePauseSeconds,
    help=f"Seconds to pause between requests (default: {PolitePauseSeconds}).",
  )
  return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
  """
  Main entry point for the ExportCollection script.

  Args:
    argv (list[str] | None): Optional argv override (for tests).

  Returns:
    int: The process exit code (0 on success, non-zero when any
      citation failed to resolve).
  """
  args = ParseArgs(argv)
  # Collect every citation referenced by every skill.
  citations = CollectCitations(SkillsRoot())
  # Surface a friendly message when no citations were found at all.
  if (not citations):
    console.print("[yellow]No arXiv IDs or DOIs found in any SKILL.md.[/yellow]")
    return 0
  # Resolve every citation via the upstream APIs.
  report = ResolveAll(citations, args.timeout, args.pause)
  # Write the resolved entries to the output .bib file.
  outPath = WriteBibtex(report, args.out)
  # Print the summary table to the console.
  RenderSummary(report, outPath)
  # Exit non-zero when any citation failed to resolve.
  return report.ExitCode


if (__name__ == "__main__"):
  # Propagate the exit code to the shell.
  sys.exit(main())
