#!/usr/bin/env python3
"""
Check every URL referenced by any SKILL.md in the SkillStack repository.

Walks all skills, extracts every ``https?://`` URL, skips GitHub badge
URLs hosted at ``img.shields.io``, and HEAD-requests each remaining URL
with retries and a per-request timeout. Prints a summary of total/OK/broken
URLs and a list of broken URLs. Exits non-zero when any URL is broken.

CLI:
  python scripts/CheckLinks.py
  python scripts/CheckLinks.py --timeout 5
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
  ExtractUrls,
  IsGithubBadgeUrl,
  IterateSkills,
  RelativeToSkills,
  SkillsRoot,
)

# Number of HTTP attempts per URL.
MaxRetries = 3
# Default seconds to wait for each HTTP response.
DefaultTimeout = 5
# User-Agent string sent on every HEAD request.
UserAgent = "SkillStack-LinkChecker/1.0"
# Trailing artifacts stripped from extracted URLs before checking.
TrailingArtifacts = ["`", "\"", "}", ")", "</script>", '">']
# Placeholder host fragments that indicate an instructional URL, not a real one.
PlaceholderHostFragments = [
  "example.org",
  "example.com",
  "grafana.example.com",
  "kubernetes.default.svc",
  "otel-collector",
  "github.com/org/",
  "github.com/owner/",
  "github.com/.../",
  "github.com/example/",
]
# HTTP status codes treated as rate-limited rather than broken.
RateLimitedStatusCodes = {403, 429}


def StripTrailingArtifact(url: str) -> str:
  """Strip trailing punctuation artifacts that are not part of the URL itself.

  Args:
    url (str): The URL candidate to clean.

  Returns:
    str: The URL with trailing backticks, quotes, braces, and HTML tags removed.
  """
  # Iterate until no artifact remains at the end.
  cleaned = url
  while (True):
    previous = cleaned
    # Try every documented artifact as a trailing suffix.
    for artifact in TrailingArtifacts:
      if (cleaned.endswith(artifact)):
        cleaned = cleaned[: -len(artifact)]
        break
    # Stop when no artifact was stripped in this pass.
    if (cleaned == previous):
      return cleaned


def IsPlaceholderUrl(url: str) -> bool:
  """Return True when a URL uses a placeholder host fragment or is a template URL."""
  # Lowercase once for case-insensitive host comparisons.
  lowered = url.lower()
  # Match any documented placeholder host fragment.
  for fragment in PlaceholderHostFragments:
    if (fragment in lowered):
      return True
  # Skip template URLs that contain Mustache/REST placeholders.
  if ("{" in url or "}" in url):
    return True
  # Skip http:// (not https://) URLs whose hostname has no dot (internal service name).
  if (lowered.startswith("http://") and not lowered.startswith("http://localhost")):
    rest = lowered[len("http://"):]
    # Take everything up to the first slash, colon, or at-sign.
    host = rest.split("/", 1)[0].split(":", 1)[0].split("@", 1)[-1]
    if ("." not in host):
      return True
  return False


def IsRateLimited(statusCode: int) -> bool:
  """Return True when an HTTP status code indicates rate-limiting rather than a broken URL."""
  return statusCode in RateLimitedStatusCodes


@dataclass
class UrlResult:
  """Outcome of checking a single URL."""

  Url: str
  SkillName: str
  SkillPath: str
  StatusCode: int
  Ok: bool
  Error: str = ""
  RateLimited: bool = False
  Skipped: bool = False


@dataclass
class CheckReport:
  """Aggregate result of checking every URL across every skill."""

  Total: int = 0
  Ok: int = 0
  Broken: int = 0
  Skipped: int = 0
  RateLimited: int = 0
  Results: list[UrlResult] = field(default_factory=list)

  @property
  def ExitCode(self) -> int:
    """Return non-zero when any broken URL was found."""
    return 0 if (self.Broken == 0) else 1


def CheckOneUrl(url: str, timeout: int, retries: int) -> tuple[int, str]:
  """
  Issue a HEAD request to the given URL with retries.

  Args:
    url (str): The URL to check.
    timeout (int): Per-request timeout in seconds.
    retries (int): Maximum number of attempts.

  Returns:
    tuple[int, str]: A ("StatusCode", "Error") pair. Error is empty on
      success. StatusCode is zero when an exception was raised.
  """
  # Build request headers with a descriptive user agent.
  headers = {"User-Agent": UserAgent}
  lastError = ""
  # Track the most recent HTTP status so callers can classify 403/429 as rate-limited.
  lastStatus = 0
  # Try up to ``retries`` times to elicit a usable HTTP response.
  for attempt in range(1, retries + 1):
    try:
      # Issue a HEAD request first to save bandwidth.
      response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
      # Some servers reject HEAD with 405; retry as GET in that case.
      if (response.status_code == 405):
        response = requests.get(url, headers=headers, timeout=timeout, stream=True, allow_redirects=True)
        # Close the streaming connection immediately to free the socket.
        response.close()
      # Treat any 2xx or 3xx status as success.
      if (200 <= response.status_code < 400):
        return response.status_code, ""
      # Otherwise record the status code and try again.
      lastStatus = response.status_code
      lastError = f"HTTP {response.status_code}"
    except requests.RequestException as exc:
      # Capture the request exception message for the final report.
      lastStatus = 0
      lastError = f"{type(exc).__name__}: {exc}"
  # All attempts failed; return the last status code (zero on transport error) with the captured error.
  return lastStatus, lastError


def CollectUrls(rootPath: Path) -> list[tuple[str, str, str]]:
  """
  Collect every non-badge URL across all skills.

  Args:
    rootPath (Path): The skills repository root.

  Returns:
    list[tuple[str, str, str]]: Triples of ("Url", "SkillName", "SkillPath")
      in iteration order. Duplicate URLs are de-duplicated by URL string.
  """
  seen = set()
  collected = []
  # Walk every skill and harvest URLs from its raw file content.
  for doc in IterateSkills(rootPath):
    rawText = doc.SkillPath.read_text(encoding="utf-8")
    skillPath = RelativeToSkills(doc.SkillPath)
    for rawUrl in ExtractUrls(rawText):
      # Strip trailing artifacts (backticks, quotes, braces, HTML tags) before checking.
      url = StripTrailingArtifact(rawUrl)
      # Skip GitHub badge URLs that always return 200 and carry no signal.
      if (IsGithubBadgeUrl(url)):
        continue
      # Skip placeholder hosts and template URLs that are instructional examples.
      if (IsPlaceholderUrl(url)):
        continue
      # Record only the first occurrence of each URL.
      if (url in seen):
        continue
      seen.add(url)
      collected.append((url, doc.Name or doc.SkillPath.parent.name, skillPath))
  return collected


def RunChecks(rootPath: Path, timeout: int, console: Console) -> CheckReport:
  """
  Run every URL check and return the aggregate report.

  Args:
    rootPath (Path): The skills repository root.
    timeout (int): Per-request timeout in seconds.
    console (Console): Rich console for progress output.

  Returns:
    CheckReport: The aggregate URL check report.
  """
  report = CheckReport()
  # Collect every URL once, in deterministic order.
  urlList = CollectUrls(rootPath)
  report.Total = len(urlList)
  # Iterate with a one-based counter for progress display.
  for index, (url, skillName, skillPath) in enumerate(urlList, start=1):
    # Print progress so the user knows the script is alive.
    console.print(f"[dim][{index}/{report.Total}][/dim] {url}")
    statusCode, error = CheckOneUrl(url, timeout=timeout, retries=MaxRetries)
    # Treat status codes below 400 as successful.
    isOk = (200 <= statusCode < 400) and (not error)
    # 403 and 429 indicate rate-limiting, not a broken URL.
    isRateLimited = (not isOk) and IsRateLimited(statusCode)
    result = UrlResult(
      Url=url,
      SkillName=skillName,
      SkillPath=skillPath,
      StatusCode=statusCode,
      Ok=isOk,
      Error=error,
      RateLimited=isRateLimited,
    )
    report.Results.append(result)
    if (isOk):
      report.Ok += 1
    elif (isRateLimited):
      report.RateLimited += 1
    else:
      report.Broken += 1
  return report


def RenderReport(report: CheckReport, console: Console) -> None:
  """
  Print the link-check report to the given rich console.

  Args:
    report (CheckReport): The aggregate report.
    console (Console): The rich console to print to.
  """
  # Print the headline summary line with color-coded counts.
  console.print(
    f"[bold]Total:[/bold] {report.Total}  "
    f"[green]OK:[/green] {report.Ok}  "
    f"[red]Broken:[/red] {report.Broken}  "
    f"[yellow]Rate-limited:[/yellow] {report.RateLimited}  "
    f"[blue]Skipped:[/blue] {report.Skipped}"
  )
  # Print a separate section for rate-limited URLs (warnings, not broken).
  rateLimitedRows = [r for r in report.Results if (r.RateLimited)]
  if (rateLimitedRows):
    rlTable = Table(title="Rate-limited (not broken)")
    rlTable.add_column("URL", style="yellow", overflow="fold")
    rlTable.add_column("Skill", style="cyan")
    rlTable.add_column("Status", style="white")
    for r in rateLimitedRows:
      statusText = str(r.StatusCode) if (r.StatusCode) else "-"
      rlTable.add_row(r.Url, r.SkillName, statusText)
    console.print(rlTable)
  # Skip the broken-URLs table when everything is healthy.
  if (report.Broken == 0):
    console.print("[green]All URLs are reachable.[/green]")
    return
  # Build a table listing each broken URL with its skill and error.
  table = Table(title="Broken URLs")
  table.add_column("URL", style="red", overflow="fold")
  table.add_column("Skill", style="cyan")
  table.add_column("Status", style="yellow")
  table.add_column("Error", style="white", overflow="fold")
  for r in report.Results:
    if (r.Ok or r.RateLimited or r.Skipped):
      continue
    # Show zero status codes as a hyphen for readability.
    statusText = str(r.StatusCode) if (r.StatusCode) else "-"
    table.add_row(r.Url, r.SkillName, statusText, r.Error)
  console.print(table)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Check every URL referenced in any SKILL.md file.",
  )
  parser.add_argument(
    "--timeout",
    type=int,
    default=DefaultTimeout,
    help=f"Per-request timeout in seconds (default: {DefaultTimeout}).",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the URL link checker.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; non-zero when any URL is broken.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  console = Console()
  # Run every URL check and capture the aggregate report.
  report = RunChecks(rootPath, args.timeout, console)
  # Render the colored report.
  RenderReport(report, console)
  return report.ExitCode


if (__name__ == "__main__"):
  sys.exit(Main())
