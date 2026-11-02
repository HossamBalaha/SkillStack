#!/usr/bin/env python3
"""
SkillStack invocation audit log.

Records skill invocations to ``.audit-log.jsonl`` as append-only JSON lines
with the following schema:

  {"Timestamp": "...", "Skill": "...", "InputFiles": [...],
   "OutputFiles": [...], "PermissionsUsed": [...]}

Subcommands:

  log <skill> [--input f1 ...] [--output f2 ...]
      Append a new audit entry for the named skill.
  show
      Print the last 50 audit entries as a table.
  stats
      Print the top-10 most-used skills.

CLI:
  python scripts/Audit.py log <skill> [--input f] [--output f]
  python scripts/Audit.py show
  python scripts/Audit.py stats
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import EnsureDir, FindSkillByName, SkillsRoot


# Shared rich console for every subcommand.
console = Console()


def AuditLogPath() -> Path:
  """Return the absolute path of the JSONL audit log file."""
  return SkillsRoot() / ".audit-log.jsonl"


def AppendEntry(entry: dict) -> None:
  """
  Append one entry to the JSONL audit log.

  Args:
    entry (dict): The entry to append; must be JSON-serializable.
  """
  # Ensure the parent directory exists before opening the file.
  logPath = AuditLogPath()
  EnsureDir(logPath.parent)
  # Open in append mode with UTF-8 encoding for portable text.
  with logPath.open("a", encoding="utf-8") as handle:
    # Serialize the entry as a single JSON line.
    handle.write(json.dumps(entry, ensure_ascii=False))
    handle.write("\n")


def ReadEntries() -> list[dict]:
  """
  Read every entry from the JSONL audit log.

  Returns:
    list[dict]: Parsed entries, oldest first. Lines that fail to parse
      are skipped with a warning printed to the console.
  """
  logPath = AuditLogPath()
  # Return an empty list when the log file does not yet exist.
  if (not logPath.is_file()):
    return []
  entries = []
  # Read the file line by line to handle large logs efficiently.
  with logPath.open("r", encoding="utf-8") as handle:
    for lineNumber, rawLine in enumerate(handle, start=1):
      # Skip blank lines without complaint.
      stripped = rawLine.strip()
      if (not stripped):
        continue
      try:
        entry = json.loads(stripped)
      except json.JSONDecodeError as exc:
        # Surface malformed lines to the user without aborting the read.
        console.print(f"[yellow]warning:[/yellow] line {lineNumber} not JSON: {exc}")
        continue
      entries.append(entry)
  return entries


def ResolveSkillPermissions(skillName: str) -> list[str]:
  """
  Look up the named skill's declared permissions from its SKILL.md.

  Accepts both bare skill names (``research-ideation-planner``) and
  theme-prefixed names (``academic-research/research-ideation-planner``).

  Args:
    skillName (str): The skill name, optionally prefixed with its theme.

  Returns:
    list[str]: A flat list of permission strings, or an empty list when
      the skill is unknown or declares no permissions.
  """
  # Strip any leading "theme/" prefix to match the frontmatter name field.
  bareName = skillName.split("/", 1)[-1] if ("/" in skillName) else skillName
  # Locate the skill by its frontmatter name.
  doc = FindSkillByName(SkillsRoot(), bareName)
  if (doc is None):
    return []
  # Normalize the permissions into a flat string list. Permissions may be
  # a list of strings, a single dict, or a one-element list wrapping a dict.
  permissions = doc.Permissions
  if (isinstance(permissions, list) and len(permissions) == 1 and isinstance(permissions[0], dict)):
    # Unwrap a single dict that was wrapped by the loader.
    permissions = permissions[0]
  if (isinstance(permissions, dict)):
    # Booleans become the key name when truthy.
    return [str(key) for key, value in permissions.items() if (value)]
  return [str(p) for p in permissions]


@click.group(help="SkillStack invocation audit log.")
def Cli() -> None:
  """Top-level click group."""
  # No-op; subcommands carry the actual behavior.
  pass


@Cli.command("log", help="Append a new audit entry for a skill invocation.")
@click.argument("skill", required=True)
@click.option("--input", "inputFiles", multiple=True, help="Input file used by the skill.")
@click.option("--output", "outputFiles", multiple=True, help="Output file produced by the skill.")
def LogCommand(skill: str, inputFiles: tuple[str, ...], outputFiles: tuple[str, ...]) -> None:
  """
  Append one audit entry recording a skill invocation.

  Args:
    skill (str): The skill name that was invoked.
    inputFiles (tuple[str, ...]): Input file paths supplied by the caller.
    outputFiles (tuple[str, ...]): Output file paths produced by the skill.
  """
  # Resolve the skill's declared permissions when available.
  permissionsUsed = ResolveSkillPermissions(skill)
  # Compose the audit entry using CamelCase dict keys.
  entry = {
    "Timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "Skill": skill,
    "InputFiles": list(inputFiles),
    "OutputFiles": list(outputFiles),
    "PermissionsUsed": permissionsUsed,
  }
  # Append the entry to the JSONL log.
  AppendEntry(entry)
  console.print(
    f"[green]logged[/green] invocation of '{skill}' "
    f"({len(inputFiles)} inputs, {len(outputFiles)} outputs)"
  )


@Cli.command("show", help="Print the last 50 audit entries.")
def ShowCommand() -> None:
  """Print the last 50 audit entries as a rich table."""
  # Read every entry then trim to the last 50.
  entries = ReadEntries()
  last = entries[-50:]
  if (not last):
    console.print("[yellow]no audit entries yet[/yellow]")
    return
  # Build a table with the canonical columns.
  table = Table(title=f"Last {len(last)} audit entries")
  table.add_column("#", style="dim", justify="right")
  table.add_column("Timestamp", style="cyan")
  table.add_column("Skill", style="magenta")
  table.add_column("Inputs", style="white", overflow="fold")
  table.add_column("Outputs", style="white", overflow="fold")
  table.add_column("Permissions", style="yellow", overflow="fold")
  # Number entries relative to the trimmed window for readability.
  for index, entry in enumerate(last, start=1):
    table.add_row(
      str(index),
      str(entry.get("Timestamp", "")),
      str(entry.get("Skill", "")),
      ", ".join(entry.get("InputFiles", []) or []) or "---",
      ", ".join(entry.get("OutputFiles", []) or []) or "---",
      ", ".join(entry.get("PermissionsUsed", []) or []) or "---",
    )
  console.print(table)


@Cli.command("stats", help="Print the top-10 most-used skills.")
def StatsCommand() -> None:
  """Print a table of the top-10 most-invoked skills."""
  # Read every entry and count invocations per skill.
  entries = ReadEntries()
  if (not entries):
    console.print("[yellow]no audit entries yet[/yellow]")
    return
  counter: Counter = Counter()
  for entry in entries:
    skill = str(entry.get("Skill", ""))
    if (skill):
      counter[skill] += 1
  # Sort by descending count then by skill name for stable output.
  ordered = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
  top = ordered[:10]
  # Build a two-column table of skill names and invocation counts.
  table = Table(title="Top-10 most-used skills")
  table.add_column("Skill", style="magenta")
  table.add_column("Invocations", style="cyan", justify="right")
  for skill, count in top:
    table.add_row(skill, str(count))
  console.print(table)


if (__name__ == "__main__"):
  # Hand control to click.
  Cli()
