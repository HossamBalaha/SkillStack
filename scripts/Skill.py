#!/usr/bin/env python3
"""
SkillStack skill CLI.

Subcommands:

  list            List every skill name grouped by theme.
  search <query>  Search skill names, descriptions, and tags; show top 10.
  show <name>     Print the full SKILL.md for the named skill.
  validate <nm>   Run the linter on one skill.
  graph           Print a Markdown table of related/prerequisite chains.
  tags            Print a tag cloud (tag -> skill count).
  health          Run the coverage report and print a summary.

Uses ``rich`` for colored output and ``click`` for subcommand dispatch.

CLI:
  python scripts/skill.py <command> [args]
"""

from __future__ import annotations

import subprocess
import sys
from collections import Counter
from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  FindSkillByName,
  IterateSkills,
  RequiredSections,
  SkillDoc,
  SkillsRoot,
)


# Shared rich console for every subcommand.
console = Console()


def LoadAll(rootPath: Path | None = None) -> list[SkillDoc]:
  """
  Load every skill document under the skills root.

  Args:
    rootPath (Path | None): Optional root override.

  Returns:
    list[SkillDoc]: Every parsed skill document, in iteration order.
  """
  # Default to the auto-detected skills root.
  root = rootPath or SkillsRoot()
  # Materialize the iterator into a list for repeated traversal.
  return list(IterateSkills(root))


@click.group(help="SkillStack skill command-line interface.")
def Cli() -> None:
  """Top-level click group."""
  # No-op; subcommands carry the actual behavior.
  pass


@Cli.command("list", help="List every skill name grouped by theme.")
def ListCommand() -> None:
  """List every skill name grouped by theme."""
  # Load every skill once.
  docs = LoadAll()
  # Group skills by their theme folder.
  byTheme: dict[str, list[SkillDoc]] = {}
  for doc in docs:
    byTheme.setdefault(doc.Theme, []).append(doc)
  # Render each theme block with its skill count.
  for themeName in sorted(byTheme.keys()):
    themeDocs = sorted(byTheme[themeName], key=lambda d: d.Name)
    console.print(
      Panel.fit(
        f"[bold magenta]{themeName}[/bold magenta] ({len(themeDocs)} skills)",
        style="magenta",
      )
    )
    # Print each skill name on its own line.
    for doc in themeDocs:
      console.print(f"  [cyan]{doc.Name}[/cyan]")


@Cli.command("search", help="Search skills by name, description, or tags.")
@click.argument("query", required=True)
def SearchCommand(query: str) -> None:
  """
  Search skills by name, description, and tags.

  Args:
    query (str): The search query (case-insensitive substring).
  """
  # Lowercase the query for case-insensitive matching.
  needle = query.lower()
  docs = LoadAll()
  matches: list[tuple[int, SkillDoc]] = []
  # Score each skill by counting how many fields contain the query.
  for doc in docs:
    haystackParts = [doc.Name, doc.Description] + [str(t) for t in doc.Tags]
    haystack = " ".join(haystackParts).lower()
    # Skip skills that do not contain the query at all.
    if (needle not in haystack):
      continue
    # Score by the number of occurrences of the needle.
    score = haystack.count(needle)
    matches.append((score, doc))
  # Sort matches by descending score then by name for stable output.
  matches.sort(key=lambda pair: (-pair[0], pair[1].Name))
  # Limit to the top 10 results.
  top = matches[:10]
  # Print a friendly header.
  console.print(f"[bold]Top {len(top)} matches for[/bold] '{query}':")
  # Build a table of the top matches.
  table = Table(show_lines=False)
  table.add_column("Skill", style="cyan")
  table.add_column("Theme", style="magenta")
  table.add_column("Description", style="white", overflow="fold")
  for score, doc in top:
    # Truncate long descriptions for terminal display.
    description = doc.Description
    if (len(description) > 120):
      description = description[:117] + "..."
    table.add_row(doc.Name, doc.Theme, description)
  console.print(table)


@Cli.command("show", help="Print the full SKILL.md for the named skill.")
@click.argument("skillname", required=True)
def ShowCommand(skillname: str) -> None:
  """
  Print the full SKILL.md content for a named skill.

  Args:
    skillname (str): The skill name (matching the frontmatter ``name``).
  """
  # Locate the skill by its frontmatter name.
  doc = FindSkillByName(SkillsRoot(), skillname)
  if (doc is None):
    # Surface a clear error when the skill name is unknown.
    console.print(f"[red]error:[/red] no skill named '{skillname}'")
    sys.exit(2)
  # Read the raw file content for faithful display.
  rawText = doc.SkillPath.read_text(encoding="utf-8")
  # Render the Markdown document with rich formatting.
  console.print(Markdown(rawText))


@Cli.command("validate", help="Run the linter on one skill.")
@click.argument("skillname", required=True)
def ValidateCommand(skillname: str) -> None:
  """
  Run the linter on a single named skill.

  Args:
    skillname (str): The skill name (matching the frontmatter ``name``).
  """
  # Locate the skill by its frontmatter name.
  doc = FindSkillByName(SkillsRoot(), skillname)
  if (doc is None):
    # Surface a clear error when the skill name is unknown.
    console.print(f"[red]error:[/red] no skill named '{skillname}'")
    sys.exit(2)
  # Delegate to lint_skills.py via subprocess to reuse its full logic.
  scriptPath = Path(__file__).resolve().parent / "lint_skills.py"
  command = [sys.executable, str(scriptPath), str(doc.SkillPath)]
  # Run the linter and propagate its exit code.
  completed = subprocess.run(command)
  sys.exit(completed.returncode)


@Cli.command("graph", help="Print a Markdown table of skill chains.")
def GraphCommand() -> None:
  """Print a Markdown table of every skill's related and prerequisite chains."""
  docs = LoadAll()
  # Build a quick lookup table from skill name to SkillDoc for cross-reference.
  byName = {doc.Name: doc for doc in docs if (doc.Name)}
  # Build the Markdown table header.
  header = (
    "| Skill | Theme | Related | Prerequisites |\n"
    "|---|---|---|---|\n"
  )
  lines = [header]
  # Emit one table row per skill, sorted by theme then name.
  for doc in sorted(docs, key=lambda d: (d.Theme, d.Name)):
    if (not doc.Name):
      continue
    # Render the related list as comma-separated names or em-dash.
    related = ", ".join(doc.Related) if (doc.Related) else "---"
    # Render the prerequisites list as comma-separated names or em-dash.
    prerequisites = ", ".join(doc.Prerequisites) if (doc.Prerequisites) else "---"
    lines.append(f"| {doc.Name} | {doc.Theme} | {related} | {prerequisites} |\n")
  # Render the assembled Markdown to the console.
  console.print(Markdown("".join(lines)))


@Cli.command("tags", help="Print a tag cloud (tag -> skill count).")
def TagsCommand() -> None:
  """Print a tag cloud showing how many skills reference each tag."""
  docs = LoadAll()
  # Count tag occurrences across every skill.
  counter: Counter = Counter()
  for doc in docs:
    for tag in doc.Tags:
      # Normalize tags to lower case for a stable cloud.
      counter[str(tag).lower()] += 1
  # Sort by descending count then alphabetically.
  ordered = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
  # Print the tag cloud header.
  console.print("[bold]Tag cloud[/bold]")
  # Build a two-column table of tags and counts.
  table = Table(show_lines=False)
  table.add_column("Tag", style="cyan")
  table.add_column("Skill count", style="magenta", justify="right")
  for tag, count in ordered:
    table.add_row(tag, str(count))
  console.print(table)


@Cli.command("health", help="Run the coverage report and print a summary.")
def HealthCommand() -> None:
  """Run the coverage report and print the headline summary."""
  # Delegate to coverage_report.py via subprocess to reuse its full logic.
  scriptPath = Path(__file__).resolve().parent / "coverage_report.py"
  command = [sys.executable, str(scriptPath)]
  # Run the coverage report and capture its exit code.
  completed = subprocess.run(command)
  if (completed.returncode != 0):
    # Surface any non-zero exit code from the coverage report.
    console.print(f"[red]coverage report exited with code {completed.returncode}[/red]")
    sys.exit(completed.returncode)
  # Read the generated coverage Markdown and print its summary block.
  coveragePath = SkillsRoot() / "docs" / "coverage.md"
  if (not coveragePath.is_file()):
    console.print(f"[red]error:[/red] coverage report not found at {coveragePath}")
    sys.exit(2)
  text = coveragePath.read_text(encoding="utf-8")
  # Extract the summary section between the heading and the next level-2 heading.
  start = text.find("## Summary")
  end = text.find("## ", start + 1) if (start != -1) else -1
  if (start == -1):
    console.print("[red]error:[/red] summary section not found in coverage report")
    sys.exit(2)
  # Slice the summary block from the document.
  summary = text[start:end if (end != -1) else None]
  console.print(Markdown(summary))


if (__name__ == "__main__"):
  # Hand control to click; no need to wrap with sys.exit because click does it.
  Cli()
