#!/usr/bin/env python3
"""
Smoke test harness for every SkillStack skill.

For each skill in the repository the harness:

  1. Parses the YAML frontmatter (re-uses ``_SkillLib.LoadSkillMd``).
  2. Checks the body contains all 7 required sections.
  3. Extracts every fenced ``python`` code block in the body.
  4. Executes each fenced code block in a subprocess with a 10-second
     timeout and reports pass/fail.

The harness is read-only: it never writes files and never makes outbound
network calls of its own. The fenced code blocks may make network calls
(some skills' examples fetch live URLs); the 10-second timeout catches
slow or hanging calls.

Exit code is non-zero when any skill fails any of the three checks.

CLI:
  python scripts/SmokeTest.py
  python scripts/SmokeTest.py --timeout 15
  python scripts/SmokeTest.py --skill hyperparameter-tuner
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  IterateSkills,
  RequiredSections,
  SkillDoc,
  SkillsRoot,
)

# Per-fenced-block subprocess timeout in seconds.
DefaultTimeout = 10
# Marker written to stderr when a fenced block exceeds the timeout.
TimeoutMarker = "TIMEOUT"
# Pattern matching the opening fence of a Python code block.
PythonFence = re.compile(r"^```python\s*$", re.MULTILINE)
# Pattern matching the closing fence of any code block.
CloseFence = re.compile(r"^```\s*$", re.MULTILINE)

# Shared rich console for every code path.
console = Console()


@dataclass
class BlockResult:
  """Outcome of executing one fenced Python code block."""

  Index: int
  ExitCode: int
  Stdout: str
  Stderr: str
  Duration: float
  TimedOut: bool
  Error: str = ""


@dataclass
class SkillResult:
  """Aggregate outcome of smoke-testing one skill."""

  SkillName: str
  Theme: str
  ParseError: str = ""
  MissingSections: list = field(default_factory=list)
  BlockResults: list[BlockResult] = field(default_factory=list)

  @property
  def Passed(self) -> bool:
    """Return True when the skill passed every smoke-test check."""
    # Fail when the frontmatter did not parse.
    if (self.ParseError):
      return False
    # Fail when any required section is missing.
    if (self.MissingSections):
      return False
    # Fail when any fenced block exited non-zero or timed out.
    for block in self.BlockResults:
      if (block.TimedOut):
        return False
      if (block.ExitCode != 0):
        return False
    return True


@dataclass
class SmokeReport:
  """Aggregate outcome of smoke-testing every skill in the repository."""

  Total: int = 0
  Passed: int = 0
  Failed: int = 0
  Results: list[SkillResult] = field(default_factory=list)

  @property
  def ExitCode(self) -> int:
    """Return non-zero when any skill failed any check."""
    return 0 if (self.Failed == 0) else 1


def ExtractPythonBlocks(body: str) -> list[str]:
  """
  Extract every fenced ``python`` code block from a Markdown body.

  Args:
    body (str): The Markdown body of a SKILL.md file (without frontmatter).

  Returns:
    list[str]: Each fenced Python block's source code, in order.
  """
  blocks: list[str] = []
  # Walk every line of the body to find opening fences.
  lines = body.splitlines()
  inBlock = False
  current: list[str] = []
  for line in lines:
    if (not inBlock):
      # Detect the opening fence of a Python block.
      if (PythonFence.match(line)):
        inBlock = True
        current = []
      continue
    # We are inside a block; check for the closing fence.
    if (CloseFence.match(line)):
      # Append the accumulated source to the blocks list.
      blocks.append("\n".join(current))
      inBlock = False
      current = []
      continue
    # Accumulate the source line.
    current.append(line)
  # Tolerate an unterminated block by appending whatever we accumulated.
  if (inBlock and current):
    blocks.append("\n".join(current))
  return blocks


def ExecuteBlock(source: str, timeout: int) -> BlockResult:
  """
  Execute one Python source block in a subprocess with a timeout.

  Args:
    source (str): The Python source to execute.
    timeout (int): Per-block timeout in seconds.

  Returns:
    BlockResult: The outcome of the execution.
  """
  # Write the source to a temporary file so the subprocess can run it.
  with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".py",
    delete=False,
    encoding="utf-8",
  ) as handle:
    handle.write(source)
    tempPath = Path(handle.name)
  # Construct the subprocess command using the current Python interpreter.
  command = [sys.executable, "-I", str(tempPath)]
  # Run the subprocess and capture its output.
  try:
    completed = subprocess.run(
      command,
      timeout=timeout,
      capture_output=True,
      text=True,
    )
    # Build the result for a successful (possibly non-zero) execution.
    return BlockResult(
      Index=0,
      ExitCode=completed.returncode,
      Stdout=completed.stdout or "",
      Stderr=completed.stderr or "",
      Duration=0.0,
      TimedOut=False,
    )
  except subprocess.TimeoutExpired as exc:
    # Build the result for a timed-out execution.
    return BlockResult(
      Index=0,
      ExitCode=-1,
      Stdout=(exc.stdout or "") if (isinstance(exc.stdout, str)) else "",
      Stderr=(exc.stderr or "") if (isinstance(exc.stderr, str)) else "",
      Duration=float(timeout),
      TimedOut=True,
      Error=TimeoutMarker,
    )
  finally:
    # Always remove the temporary file, even on failure.
    try:
      tempPath.unlink(missing_ok=True)
    except OSError:
      pass


def SmokeTestSkill(doc: SkillDoc, timeout: int) -> SkillResult:
  """
  Smoke-test one skill: parse, sections, and every fenced Python block.

  Args:
    doc (SkillDoc): The parsed skill document.
    timeout (int): Per-block subprocess timeout in seconds.

  Returns:
    SkillResult: The aggregate outcome for the skill.
  """
  result = SkillResult(SkillName=doc.Name, Theme=doc.Theme)
  # Surface the parse error from the loader (if any).
  if (doc.ParseError):
    result.ParseError = doc.ParseError
    return result
  # Check that every required section is present in the body.
  result.MissingSections = [
    section for section in RequiredSections if (section not in doc.Body)
  ]
  # Extract every fenced Python block from the body.
  blocks = ExtractPythonBlocks(doc.Body)
  # Execute each block in turn and append the result.
  for index, source in enumerate(blocks):
    blockResult = ExecuteBlock(source, timeout)
    # Override the index to reflect the position in the skill.
    blockResult.Index = index
    result.BlockResults.append(blockResult)
  return result


def SmokeTestAll(timeout: int, skillFilter: str | None = None) -> SmokeReport:
  """
  Smoke-test every skill in the repository.

  Args:
    timeout (int): Per-block subprocess timeout in seconds.
    skillFilter (str | None): Optional skill-name substring filter.

  Returns:
    SmokeReport: The aggregate report across every skill.
  """
  report = SmokeReport()
  # Walk every skill and run the smoke test.
  for doc in IterateSkills(SkillsRoot()):
    # Skip skills without a name (defensive: should never happen).
    if (not doc.Name):
      continue
    # Apply the optional name-substring filter.
    if (skillFilter and (skillFilter.lower() not in doc.Name.lower())):
      continue
    # Smoke-test the skill.
    result = SmokeTestSkill(doc, timeout)
    # Update the report totals.
    report.Total += 1
    if (result.Passed):
      report.Passed += 1
    else:
      report.Failed += 1
    report.Results.append(result)
  # Sort the results by theme then name for stable output.
  report.Results.sort(key=lambda r: (r.Theme, r.SkillName))
  return report


def RenderSummary(report: SmokeReport) -> None:
  """
  Print a summary table of the smoke-test report.

  Args:
    report (SmokeReport): The aggregate report.
  """
  # Print the headline totals.
  console.print(
    f"[bold]Smoke test: {report.Passed}/{report.Total} skills passed, "
    f"{report.Failed} failed[/bold]"
  )
  # Build a per-skill summary table.
  table = Table(show_lines=False)
  table.add_column("Theme", style="magenta")
  table.add_column("Skill", style="cyan")
  table.add_column("Sections", style="white")
  table.add_column("Blocks", style="white")
  table.add_column("Status", style="green")
  for result in report.Results:
    # Render the section count as ok/missing.
    sectionCount = len(RequiredSections) - len(result.MissingSections)
    sections = f"{sectionCount}/{len(RequiredSections)}"
    # Render the block count as ok/total.
    totalBlocks = len(result.BlockResults)
    okBlocks = sum(1 for b in result.BlockResults if (not b.TimedOut and b.ExitCode == 0))
    blocks = f"{okBlocks}/{totalBlocks}"
    # Render the status as pass/fail.
    status = "pass" if (result.Passed) else "fail"
    table.add_row(result.Theme, result.SkillName, sections, blocks, status)
  console.print(table)
  # Print detail lines for every failed skill.
  for result in report.Results:
    if (result.Passed):
      continue
    console.print(f"[red]FAILED[/red] {result.Theme}/{result.SkillName}")
    if (result.ParseError):
      console.print(f"  parse error: {result.ParseError}")
    for section in result.MissingSections:
      console.print(f"  missing section: {section}")
    for block in result.BlockResults:
      if (block.TimedOut):
        console.print(f"  block #{block.Index}: timed out after {block.Duration}s")
      elif (block.ExitCode != 0):
        # Truncate long stderr for terminal display.
        stderr = block.Stderr.strip()
        if (len(stderr) > 200):
          stderr = stderr[:197] + "..."
        console.print(f"  block #{block.Index}: exit {block.ExitCode} - {stderr}")


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """
  Parse the command-line arguments.

  Args:
    argv (list[str] | None): Optional argv override (for tests).

  Returns:
    argparse.Namespace: The parsed arguments.
  """
  parser = argparse.ArgumentParser(
    description="Smoke test every SkillStack skill: parse, sections, and fenced Python blocks.",
  )
  # Per-block subprocess timeout in seconds.
  parser.add_argument(
    "--timeout",
    type=int,
    default=DefaultTimeout,
    help=f"Per-block subprocess timeout in seconds (default: {DefaultTimeout}).",
  )
  # Optional skill-name substring filter.
  parser.add_argument(
    "--skill",
    type=str,
    default=None,
    help="Optional skill-name substring filter (case-insensitive).",
  )
  return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
  """
  Main entry point for the SmokeTest script.

  Args:
    argv (list[str] | None): Optional argv override (for tests).

  Returns:
    int: The process exit code (0 on success, non-zero when any skill
      failed any check).
  """
  args = ParseArgs(argv)
  # Run the smoke test across every skill in the repository.
  report = SmokeTestAll(args.timeout, args.skill)
  # Print the summary table to the console.
  RenderSummary(report)
  # Exit non-zero when any skill failed any check.
  return report.ExitCode


if (__name__ == "__main__"):
  # Propagate the exit code to the shell.
  sys.exit(main())
