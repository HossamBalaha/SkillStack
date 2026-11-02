#!/usr/bin/env python3
"""
Lint every SKILL.md in the SkillStack repository.

Checks each skill for:

  * Parseable YAML frontmatter.
  * Required frontmatter keys: ``name``, ``description``,
    ``metadata.author``, ``metadata.version``, ``metadata.theme``,
    ``tags``, ``related``, ``permissions``, ``language``.
  * All seven required body sections: ``## When To Use``, ``## Workflow``,
    ``## Inputs``, ``## Outputs``, ``## Key Rules``, ``## Examples``,
    ``## References``.
  * Body line count between 80 and 250 lines (inclusive).
  * No banned markers (``TODO``, ``XXX``, ``FIXME``) anywhere in the file.

Output is colored via ``rich``. The script exits non-zero when any
violation is reported.

CLI:
  python scripts/LintSkills.py             # lint all skills
  python scripts/LintSkills.py <path>     # lint one skill (dir or file)
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  BannedMarkers,
  LoadSkillMd,
  MaxLineCount,
  MinLineCount,
  RequiredFrontmatterKeys,
  RequiredSections,
  SkillDoc,
  SkillsRoot,
)


@dataclass
class Violation:
  """A single linter finding."""

  SkillPath: Path
  SkillName: str
  Theme: str
  Rule: str
  Detail: str


@dataclass
class LintReport:
  """Aggregate result of linting one or more skills."""

  Checked: int = 0
  Passed: int = 0
  Failed: int = 0
  Violations: list[Violation] = field(default_factory=list)

  @property
  def ExitCode(self) -> int:
    """Return the process exit code: zero only when no skill failed."""
    return 0 if (self.Failed == 0) else 1


def _ResolveByPath(frontmatter: dict, dottedKey: str):
  """Resolve a dotted key like ``metadata.author`` from a nested mapping."""
  # Walk each segment of the dotted key path.
  current = frontmatter
  for segment in dottedKey.split("."):
    if (not isinstance(current, dict)):
      return None
    if (segment not in current):
      return None
    current = current[segment]
  return current


def LintOne(doc: SkillDoc) -> list[Violation]:
  """
  Run all linter checks against a single parsed skill.

  Args:
    doc (SkillDoc): The parsed skill document.

  Returns:
    list[Violation]: All violations found for this skill.
  """
  violations: list[Violation] = []
  # Helper to append a violation with consistent metadata.
  def Add(rule: str, detail: str) -> None:
    violations.append(Violation(
      SkillPath=doc.SkillPath,
      SkillName=doc.Name or doc.SkillPath.parent.name,
      Theme=doc.Theme,
      Rule=rule,
      Detail=detail,
    ))
  # Surface any parse error from the loader before semantic checks.
  if (doc.ParseError):
    Add("frontmatter.parse", doc.ParseError)
    return violations
  # Verify each required frontmatter key is present and non-empty.
  for key in RequiredFrontmatterKeys:
    value = _ResolveByPath(doc.Frontmatter, key)
    # Treat None, empty string, empty list, or empty dict as missing.
    if (value is None or (isinstance(value, str) and not value.strip())):
      Add("frontmatter.required", f"missing required field: {key}")
  # Verify all seven required body sections appear.
  for section in RequiredSections:
    if (section not in doc.Body):
      Add("body.required-section", f"missing section: {section}")
  # Verify the body length is within the allowed window.
  if (doc.LineCount < MinLineCount):
    Add("body.line-count", f"only {doc.LineCount} lines (minimum {MinLineCount})")
  if (doc.LineCount > MaxLineCount):
    Add("body.line-count", f"{doc.LineCount} lines exceeds maximum {MaxLineCount}")
  # Scan for banned markers anywhere in the raw file.
  rawText = doc.SkillPath.read_text(encoding="utf-8")
  for marker in BannedMarkers:
    if (marker in rawText):
      Add("body.banned-marker", f"contains banned marker: {marker}")
  return violations


def ResolveTargets(rootPath: Path, skillArg: str | None) -> list[SkillDoc]:
  """
  Resolve the user-supplied argument into a list of SkillDoc targets.

  Args:
    rootPath (Path): The skills repository root.
    skillArg (str | None): A directory path, SKILL.md path, or None to
      lint all skills.

  Returns:
    list[SkillDoc]: The parsed skill documents to lint.
  """
  # When no argument is provided, lint every skill in the repo.
  if (skillArg is None):
    return list(_IterateAllSkills(rootPath))
  target = Path(skillArg).resolve()
  # Reject paths that do not exist on disk.
  if (not target.exists()):
    raise FileNotFoundError(f"target does not exist: {target}")
  # When given a directory, prefer its SKILL.md but fall back to all skills.
  if (target.is_dir()):
    skillMd = target / "SKILL.md"
    if (skillMd.is_file()):
      theme = target.parent.name if (target.parent.parent.name != "skills") else target.name
      return [LoadSkillMd(skillMd, theme=theme)]
    # Treat the directory itself as a theme to lint recursively.
    docs = []
    for skillDir in sorted([c for c in target.iterdir() if (c.is_dir())]):
      candidate = skillDir / "SKILL.md"
      if (candidate.is_file()):
        docs.append(LoadSkillMd(candidate, theme=target.name))
    return docs
  # When given a file, treat it as a SKILL.md path.
  if (target.is_file()):
    parent = target.parent
    theme = parent.parent.name if (parent.parent.name != "skills") else parent.name
    return [LoadSkillMd(target, theme=theme)]
  return []


def _IterateAllSkills(rootPath: Path):
  """Yield every parsed skill under the root (local import to avoid cycle)."""
  # Imported here to keep the module-level surface narrow.
  from _SkillLib import IterateSkills
  yield from IterateSkills(rootPath)


def RenderReport(report: LintReport, console: Console) -> None:
  """
  Print the lint report to the given rich console.

  Args:
    report (LintReport): The aggregate lint result.
    console (Console): The rich console to print to.
  """
  # Print a summary panel with totals.
  summaryText = (
    f"[bold]Checked:[/bold] {report.Checked}  "
    f"[green]Passed:[/green] {report.Passed}  "
    f"[red]Failed:[/red] {report.Failed}"
  )
  console.print(Panel(summaryText, title="SkillStack Lint Report", expand=False))
  # Skip the violations table when there are no findings.
  if (not report.Violations):
    console.print("[green]No violations found.[/green]")
    return
  # Build a table of all violations, grouped by skill.
  table = Table(title="Violations", show_lines=False)
  table.add_column("Skill", style="cyan", no_wrap=True)
  table.add_column("Theme", style="magenta")
  table.add_column("Rule", style="yellow")
  table.add_column("Detail", style="white")
  # Sort violations by theme then skill name for stable output.
  for v in sorted(report.Violations, key=lambda x: (x.Theme, x.SkillName, x.Rule)):
    table.add_row(v.SkillName, v.Theme, v.Rule, v.Detail)
  console.print(table)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Lint SkillStack SKILL.md files for required fields, sections, and banned markers.",
  )
  parser.add_argument(
    "skillPath",
    nargs="?",
    default=None,
    help="Optional path to a skill directory or SKILL.md file (omit to lint all).",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the linter.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; non-zero when any violation is found.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  console = Console()
  report = LintReport()
  # Resolve the list of skills to lint from the user argument.
  try:
    docs = ResolveTargets(rootPath, args.skillPath)
  except FileNotFoundError as exc:
    console.print(f"[red]error:[/red] {exc}")
    return 2
  # Lint each parsed skill document.
  for doc in docs:
    report.Checked += 1
    violations = LintOne(doc)
    if (violations):
      report.Failed += 1
      report.Violations.extend(violations)
    else:
      report.Passed += 1
  # Render the rich report to the console.
  RenderReport(report, console)
  return report.ExitCode


if (__name__ == "__main__"):
  sys.exit(Main())
