#!/usr/bin/env python3
"""
Export SkillStack skills to Anthropic Agent Skills format.

Each skill becomes a single Markdown file under
``export/anthropic/<theme>/<skill-name>.md`` with frontmatter converted to
Anthropic's format:

  ---
  name: <skill-name>
  description: <description>
  ---

The body is the original SKILL.md body verbatim.

CLI:
  python scripts/ExportAnthropic.py
  python scripts/ExportAnthropic.py --out export/anthropic
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import EnsureDir, IterateSkills, SkillDoc, SkillsRoot


def BuildAnthropicFrontmatter(doc: SkillDoc) -> str:
  """
  Build the Anthropic-format YAML frontmatter for one skill.

  Args:
    doc (SkillDoc): The parsed skill document.

  Returns:
    str: A YAML frontmatter block delimited by ``---`` lines.
  """
  # Compose the two Anthropic-mandated keys: name and description.
  # Use a manual two-line block to control escaping without pulling in PyYAML twice.
  lines = ["---"]
  # Emit the name field verbatim.
  lines.append(f"name: {doc.Name}")
  # Emit the description with YAML safe-quoting when it contains a colon or leading quote.
  description = doc.Description.strip()
  if (":" in description or description.startswith('"')):
    # Wrap in double quotes and escape any internal double quotes.
    escaped = description.replace('"', '\\"')
    lines.append(f'description: "{escaped}"')
  else:
    lines.append(f"description: {description}")
  lines.append("---")
  return "\n".join(lines)


def SanitizeName(name: str) -> str:
  """
  Sanitize a skill name for use as a filename component.

  Args:
    name (str): The raw skill name.

  Returns:
    str: A safe filename component with no path separators.
  """
  # Replace any path separators to prevent directory traversal.
  safe = name.replace("/", "-").replace("\\", "-")
  return safe


def ExportOne(doc: SkillDoc, outRoot: Path) -> Path:
  """
  Export one skill to an Anthropic-format Markdown file.

  Args:
    doc (SkillDoc): The parsed skill document.
    outRoot (Path): The export root directory.

  Returns:
    Path: The destination file path.
  """
  # Build the destination path under <outRoot>/<theme>/<skill-name>.md.
  themeDir = outRoot / SanitizeName(doc.Theme)
  destination = themeDir / f"{SanitizeName(doc.Name)}.md"
  # Ensure the theme directory exists before opening the file.
  EnsureDir(destination.parent)
  # Read the original body and prepend the Anthropic frontmatter.
  body = doc.Body.lstrip("\n")
  frontmatter = BuildAnthropicFrontmatter(doc)
  text = frontmatter + "\n\n" + body
  destination.write_text(text, encoding="utf-8")
  return destination


def ExportAll(rootPath: Path, outRoot: Path) -> list[Path]:
  """
  Export every skill under the skills root to Anthropic format.

  Args:
    rootPath (Path): The skills repository root.
    outRoot (Path): The export root directory.

  Returns:
    list[Path]: Destination paths in iteration order.
  """
  destinations = []
  # Iterate every skill and export each one in turn.
  for doc in IterateSkills(rootPath):
    if (not doc.Name):
      continue
    destination = ExportOne(doc, outRoot)
    destinations.append(destination)
  return destinations


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Export SkillStack skills to Anthropic Agent Skills format.",
  )
  parser.add_argument(
    "--out",
    default="export/anthropic",
    help="Destination export root (default: export/anthropic).",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the Anthropic exporter.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; always zero on success.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  # Resolve the output directory relative to the skills root when not absolute.
  outRoot = Path(args.out)
  if (not outRoot.is_absolute()):
    outRoot = rootPath / outRoot
  outRoot = outRoot.resolve()
  console = Console()
  # Export every skill and capture the destination paths.
  destinations = ExportAll(rootPath, outRoot)
  console.print(f"[green]exported[/green] {len(destinations)} skills to {outRoot}")
  return 0


if (__name__ == "__main__"):
  sys.exit(Main())
