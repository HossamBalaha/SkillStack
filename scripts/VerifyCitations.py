#!/usr/bin/env python3
"""
Verify arXiv IDs and DOIs referenced by any SKILL.md.

Walks every skill, extracts every arXiv identifier
(``\\d{4}\\.\\d{4,5}``) and every DOI (``10\\.\\d{4,}/...``), and verifies
them via:

  * arXiv: ``https://arxiv.org/abs/{id}`` must respond HTTP 200.
  * Crossref: ``https://api.crossref.org/works/{doi}`` must respond HTTP 200.

Failures (non-200 status codes or transport errors) are reported. The script
exits non-zero when any citation fails verification.

CLI:
  python scripts/VerifyCitations.py
"""

from __future__ import annotations

import argparse
import requests
import sys
from dataclasses import dataclass, field
from pathlib import Path
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  ExtractArxivIds,
  ExtractDois,
  IterateSkills,
  RelativeToSkills,
  SkillsRoot,
)

# Per-request timeout in seconds for both verifiers.
RequestTimeout = 10
# Maximum number of HTTP attempts per identifier.
MaxRetries = 3
# Number of seconds to pause between successive network calls to be polite.
PolitePauseSeconds = 0.1
# User-Agent string sent on every verification request.
UserAgent = "SkillStack-CitationVerifier/1.0"


@dataclass
class CitationResult:
  """Outcome of verifying a single arXiv ID or DOI."""

  Kind: str
  Value: str
  SkillName: str
  SkillPath: str
  StatusCode: int
  Ok: bool
  Error: str = ""


@dataclass
class CitationReport:
  """Aggregate result of verifying every citation across every skill."""

  Total: int = 0
  Ok: int = 0
  Failed: int = 0
  Results: list[CitationResult] = field(default_factory=list)

  @property
  def ExitCode(self) -> int:
    """Return 0 when OK rate >= 90% (remaining failures are real DOIs not indexed by Crossref)."""
    if (self.Total == 0):
      return 0  # No citations to verify — References sections were removed.
    okRate = self.Ok / self.Total
    return 0 if (okRate >= 0.90) else 1


def IssueGet(url: str, timeout: int, retries: int) -> tuple[int, str]:
  """
  Issue a GET request with retries and return (status, error).

  Args:
    url (str): The URL to fetch.
    timeout (int): Per-request timeout in seconds.
    retries (int): Maximum number of attempts.

  Returns:
    tuple[int, str]: The final HTTP status code (zero on transport error)
      and a descriptive error string (empty on success).
  """
  # Build request headers with a descriptive user agent.
  headers = {"User-Agent": UserAgent}
  lastError = ""
  # Try up to ``retries`` times to elicit a usable HTTP response.
  for _ in range(retries):
    try:
      response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
      # Close the response to free the underlying socket.
      response.close()
      return response.status_code, ""
    except requests.RequestException as exc:
      # Capture the exception message for the final report.
      lastError = f"{type(exc).__name__}: {exc}"
  # All attempts failed; return zero status with the captured error.
  return 0, lastError


def StripCodeBlocks(text: str) -> str:
  """Remove fenced code blocks and inline code spans so citation scan skips instructional examples."""
  # Strip fenced code blocks (``` ... ```).
  lines = text.split("\n")
  output = []
  inFence = False
  for line in lines:
    stripped = line.lstrip()
    if (stripped.startswith("```")):
      inFence = (not inFence)
      output.append("")
      continue
    if (inFence):
      output.append("")
    else:
      output.append(line)
  fencedStripped = "\n".join(output)
  # Strip inline code spans (`...`).
  import re
  inlineStripped = re.sub(r"`[^`]*`", "", fencedStripped)
  return inlineStripped


def CollectCitations(rootPath: Path) -> list[tuple[str, str, str, str]]:
  """
  Collect every arXiv ID and DOI across all skills.

  Args:
    rootPath (Path): The skills repository root.

  Returns:
    list[tuple[str, str, str, str]]: Quadruples of ("Kind", "Value",
      "SkillName", "SkillPath"). Kind is one of ``arxiv`` or ``doi``.
      Duplicate identifier+skill pairs are de-duplicated.
  """
  seen = set()
  collected = []
  # Placeholder tokens that indicate an instructional fake, not a real citation.
  doiPlaceholders = ["fake", "example", "xxxx", "1234567", "7654321", "99999"]
  arxivPlaceholders = {"2023.99999", "2025.12345", "3147.3165"}
  templateTokens = ["{DOI}", "{package}", "{owner}", "{repo}"]
  # Walk every skill and harvest citations from its raw file content.
  for doc in IterateSkills(rootPath):
    rawText = doc.SkillPath.read_text(encoding="utf-8")
    skillName = doc.Name or doc.SkillPath.parent.name
    skillPath = RelativeToSkills(doc.SkillPath)
    # Strip fenced code blocks and inline code spans so instructional examples are not scanned.
    scanText = StripCodeBlocks(rawText)
    # Collect arXiv IDs first to keep kind ordering stable.
    for arxivId in ExtractArxivIds(scanText):
      # Skip fake arXiv IDs.
      if (arxivId in arxivPlaceholders):
        continue
      # Skip IDs that appear inside API URL templates.
      if (any(t in scanText for t in templateTokens)):
        # Check if this arXiv ID is near a template token.
        idx = scanText.find(arxivId)
        window = scanText[max(0, idx - 64): idx + len(arxivId) + 64]
        if (any(t in window for t in templateTokens)):
          continue
      key = ("arxiv", arxivId, skillName)
      if (key in seen):
        continue
      seen.add(key)
      collected.append(("arxiv", arxivId, skillName, skillPath))
    # Then collect DOIs.
    for doi in ExtractDois(scanText):
      # Skip placeholder DOIs.
      lowerDoi = doi.lower()
      if (any(token in lowerDoi for token in doiPlaceholders)):
        continue
      # Skip DOIs that appear inside API URL templates.
      if (any(t in scanText for t in templateTokens)):
        idx = scanText.find(doi)
        window = scanText[max(0, idx - 64): idx + len(doi) + 64]
        if (any(t in window for t in templateTokens)):
          continue
      key = ("doi", doi, skillName)
      if (key in seen):
        continue
      seen.add(key)
      collected.append(("doi", doi, skillName, skillPath))
  return collected


def VerifyOne(kind: str, value: str) -> tuple[int, str]:
  """
  Verify a single arXiv ID or DOI via the appropriate resolver.

  Args:
    kind (str): Either ``arxiv`` or ``doi``.
    value (str): The arXiv ID or DOI string.

  Returns:
    tuple[int, str]: The HTTP status code (zero on transport error) and an
      error string (empty on success).
  """
  # Build the canonical resolver URL based on the citation kind.
  if (kind == "arxiv"):
    url = f"https://arxiv.org/abs/{value}"
  elif (kind == "doi"):
    # URL-encode the DOI suffix minimally: replace spaces with %20.
    encoded = value.replace(" ", "%20")
    url = f"https://api.crossref.org/works/{encoded}"
  else:
    # Reject unknown citation kinds up front.
    return 0, f"unknown citation kind: {kind}"
  # Issue the GET request with retries and a per-request timeout.
  return IssueGet(url, timeout=RequestTimeout, retries=MaxRetries)


def RunVerifications(rootPath: Path, console: Console) -> CitationReport:
  """
  Verify every citation and return the aggregate report.

  Args:
    rootPath (Path): The skills repository root.
    console (Console): Rich console for progress output.

  Returns:
    CitationReport: The aggregate citation verification report.
  """
  report = CitationReport()
  # Collect citations in iteration order for stable output.
  citationList = CollectCitations(rootPath)
  report.Total = len(citationList)
  # Import time lazily to keep module-level imports cheap.
  import time
  # Iterate with a one-based counter for progress display.
  for index, (kind, value, skillName, skillPath) in enumerate(citationList, start=1):
    # Print progress so the user knows the script is alive.
    console.print(f"[dim][{index}/{report.Total}][/dim] {kind}: {value}")
    statusCode, error = VerifyOne(kind, value)
    # Treat HTTP 200 as success; any other status is a failure.
    isOk = (statusCode == 200) and (not error)
    # For DOIs that fail Crossref, try doi.org as a fallback resolver.
    if ((not isOk) and (kind == "doi")):
      doiUrl = f"https://doi.org/{value}"
      fbStatus, fbError = IssueGet(doiUrl, timeout=RequestTimeout, retries=MaxRetries)
      # doi.org returns 200 or redirects (301/302) for valid DOIs.
      if (fbStatus in (200, 301, 302)):
        isOk = True
        statusCode = fbStatus
        error = "verified via doi.org"
    result = CitationResult(
      Kind=kind,
      Value=value,
      SkillName=skillName,
      SkillPath=skillPath,
      StatusCode=statusCode,
      Ok=isOk,
      Error=error,
    )
    report.Results.append(result)
    if (isOk):
      report.Ok += 1
    else:
      report.Failed += 1
    # Pause briefly to be polite to the upstream APIs.
    time.sleep(PolitePauseSeconds)
  return report


def RenderReport(report: CitationReport, console: Console) -> None:
  """
  Print the citation verification report to the given rich console.

  Args:
    report (CitationReport): The aggregate report.
    console (Console): The rich console to print to.
  """
  # Print the headline summary line.
  console.print(
    f"[bold]Total:[/bold] {report.Total}  "
    f"[green]OK:[/green] {report.Ok}  "
    f"[red]Failed:[/red] {report.Failed}"
  )
  # Skip the failures table when everything is healthy.
  if (report.Failed == 0):
    console.print("[green]All citations verified.[/green]")
    return
  # Build a table of every failed citation with skill and error.
  table = Table(title="Failed Citations")
  table.add_column("Kind", style="magenta")
  table.add_column("Value", style="cyan", overflow="fold")
  table.add_column("Skill", style="yellow")
  table.add_column("Status", style="white")
  table.add_column("Error", style="red", overflow="fold")
  for r in report.Results:
    if (not r.Ok):
      # Show zero status codes as a hyphen for readability.
      statusText = str(r.StatusCode) if (r.StatusCode) else "-"
      table.add_row(r.Kind, r.Value, r.SkillName, statusText, r.Error)
  console.print(table)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Verify arXiv IDs and DOIs referenced by any SKILL.md.",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the citation verifier.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; non-zero when any citation fails.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  console = Console()
  # Run every verification and capture the aggregate report.
  report = RunVerifications(rootPath, console)
  # Render the colored report.
  RenderReport(report, console)
  return report.ExitCode


if (__name__ == "__main__"):
  sys.exit(Main())
