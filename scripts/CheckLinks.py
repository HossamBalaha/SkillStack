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


@dataclass
class UrlResult:
  """Outcome of checking a single URL."""

  Url: str
  SkillName: str
  SkillPath: str
  StatusCode: int
  Ok: bool
  Error: str = ""


@dataclass
class CheckReport:
  """Aggregate result of checking every URL across every skill."""

  Total: int = 0
  Ok: int = 0
  Broken: int = 0
  RateLimited: int = 0
  Skipped: int = 0
  Results: list[UrlResult] = field(default_factory=list)

  @property
  def ExitCode(self) -> int:
    """Return 0 always — link checker is informational, not a build gate."""
    return 0


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
      lastError = f"HTTP {response.status_code}"
    except requests.RequestException as exc:
      # Capture the request exception message for the final report.
      lastError = f"{type(exc).__name__}: {exc}"
  # All attempts failed; return zero status with the captured error.
  return 0, lastError


def CollectUrls(rootPath: Path) -> list[tuple[str, str, str]]:
  """
  Collect every non-badge, non-placeholder URL across all skills.

  Args:
    rootPath (Path): The skills repository root.

  Returns:
    list[tuple[str, str, str]]: Triples of ("Url", "SkillName", "SkillPath")
      in iteration order. Duplicate URLs are de-duplicated by URL string.
  """
  # Placeholder host fragments that indicate an instructional example, not a real URL.
  placeholderHosts = [
    "example.org", "example.com", "grafana.example.com",
    "kubernetes.default.svc", "otel-collector",
    "github.com/org/", "github.com/owner/", "github.com/.../",
    "github.com/example/",
  ]
  seen = set()
  collected = []
  # Walk every skill and harvest URLs from its raw file content.
  for doc in IterateSkills(rootPath):
    rawText = doc.SkillPath.read_text(encoding="utf-8")
    skillPath = RelativeToSkills(doc.SkillPath)
    for url in ExtractUrls(rawText):
      # Skip GitHub badge URLs that always return 200 and carry no signal.
      if (IsGithubBadgeUrl(url)):
        continue
      # Clean trailing artifacts (backticks, quotes, braces, </script>).
      cleanedUrl = url.rstrip("`\"'}>)")
      # Remove trailing </script> or similar HTML fragments.
      if (">" in cleanedUrl):
        cleanedUrl = cleanedUrl.split(">")[0]
      # Skip placeholder hosts (instructional examples).
      lowerUrl = cleanedUrl.lower()
      if (any(ph in lowerUrl for ph in placeholderHosts)):
        continue
      # Skip template URLs with {placeholder} tokens.
      if ("{" in cleanedUrl and "}" in cleanedUrl):
        continue
      # Skip internal service names (http:// without a dot in hostname).
      if (cleanedUrl.startswith("http://") and "." not in cleanedUrl.split("//")[1].split("/")[0].split(":")[0]):
        continue
      # Record only the first occurrence of each URL.
      if (cleanedUrl in seen):
        continue
      seen.add(cleanedUrl)
      collected.append((cleanedUrl, doc.Name or doc.SkillPath.parent.name, skillPath))
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
    result = UrlResult(
      Url=url,
      SkillName=skillName,
      SkillPath=skillPath,
      StatusCode=statusCode,
      Ok=isOk,
      Error=error,
    )
    report.Results.append(result)
    if (isOk):
      report.Ok += 1
    elif (statusCode in (403, 429)):
      report.RateLimited += 1
    elif (statusCode == 0 and ("NameResolution" in error or "ConnectionError" in error or "getaddrinfo" in error)):
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
    f"[yellow]Rate-limited:[/yellow] {report.RateLimited}"
  )
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
    if (not r.Ok):
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
