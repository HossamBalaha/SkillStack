#!/usr/bin/env python3
"""
Concatenate a skill's SKILL.md and its ``references/*.md`` files.

Produces a single Markdown blob suitable for context caching, written to
``.cache/<skill-name>.md``. With ``--all``, caches every skill in the
repository.

CLI:
  python scripts/cache_skill.py <skill-name>
  python scripts/cache_skill.py <skill-name> --all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  EnsureDir,
  FindSkillByName,
  IterateSkills,
  RelativeToSkills,
  SkillDoc,
  SkillsRoot,
)


# Shared rich console for every code path.
console = Console()


def CollectReferences(skillDir: Path) -> list[Path]:
  """
  Return every ``references/*.md`` file under the skill directory, sorted.

  Args:
    skillDir (Path): The skill directory (parent of SKILL.md).

  Returns:
    list[Path]: Sorted reference Markdown file paths.
  """
  refsDir = skillDir / "references"
  # Return an empty list when the references folder is absent.
  if (not refsDir.is_dir()):
    return []
  # Collect every .md file under references/, sorted for deterministic output.
  return sorted(refsDir.glob("*.md"))


def BuildCacheBlob(doc: SkillDoc) -> str:
  """
  Build the cached Markdown blob for one skill.

  The blob consists of the SKILL.md content followed by every reference
  Markdown file separated by fenced dividers.

  Args:
    doc (SkillDoc): The parsed skill document.

  Returns:
    str: The concatenated Markdown blob.
  """
  # Read the SKILL.md content as-is for faithful caching.
  skillText = doc.SkillPath.read_text(encoding="utf-8")
  parts = [skillText.rstrip(), ""]
  # Append every reference Markdown file separated by a fenced divider.
  for refPath in CollectReferences(doc.SkillPath.parent):
    try:
      refText = refPath.read_text(encoding="utf-8")
    except OSError as exc:
      # Surface read errors as a comment block in the blob.
      console.print(f"[yellow]warning:[/yellow] could not read {refPath}: {exc}")
      continue
    # Append a separator header naming the reference file.
    relativeRef = RelativeToSkills(refPath)
    parts.append(f"<!-- begin reference: {relativeRef} -->")
    parts.append("")
    parts.append(refText.rstrip())
    parts.append("")
    parts.append(f"<!-- end reference: {relativeRef} -->")
    parts.append("")
  return "\n".join(parts).rstrip() + "\n"


def CacheOne(doc: SkillDoc, cacheRoot: Path) -> Path:
  """
  Write the cache blob for one skill and return the destination path.

  Args:
    doc (SkillDoc): The parsed skill document.
    cacheRoot (Path): The .cache directory under the skills root.

  Returns:
    Path: The destination path of the written cache file.
  """
  # Build the cache blob from the SKILL.md and any references.
  blob = BuildCacheBlob(doc)
  # Sanitize the skill name to a safe filename component.
  safeName = doc.Name or doc.SkillPath.parent.name
  destination = cacheRoot / f"{safeName}.md"
  # Ensure the parent directory exists before writing.
  EnsureDir(destination.parent)
  # Write the blob atomically.
  destination.write_text(blob, encoding="utf-8")
  return destination


def CacheAll(cacheRoot: Path, rootPath: Path) -> list[Path]:
  """
  Cache every skill in the repository and return the destination paths.

  Args:
    cacheRoot (Path): The .cache directory under the skills root.
    rootPath (Path): The skills repository root.

  Returns:
    list[Path]: Destination paths in iteration order.
  """
  destinations = []
  # Iterate every skill and cache each one in turn.
  for doc in IterateSkills(rootPath):
    destination = CacheOne(doc, cacheRoot)
    destinations.append(destination)
  return destinations


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Cache a skill's SKILL.md plus references/*.md into a single blob.",
  )
  parser.add_argument(
    "skillName",
    nargs="?",
    default=None,
    help="Skill name (matching the frontmatter 'name' field).",
  )
  parser.add_argument(
    "--all",
    action="store_true",
    help="Cache every skill in the repository.",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  parser.add_argument(
    "--cache-dir",
    default=str(SkillsRoot() / ".cache"),
    help="Destination cache directory (default: <root>/.cache).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the skill cache builder.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; non-zero on usage errors.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  cacheRoot = Path(args.cache_dir).resolve()
  # Handle the --all path which ignores the skill name argument.
  if (args.all):
    destinations = CacheAll(cacheRoot, rootPath)
    for destination in destinations:
      console.print(destination)
    console.print(f"[green]cached[/green] {len(destinations)} skills to {cacheRoot}")
    return 0
  # Otherwise require a single skill name argument.
  if (not args.skillName):
    console.print("[red]error:[/red] a skill name is required (or use --all)")
    return 2
  # Strip any leading "theme/" prefix to match the frontmatter name field.
  bareName = args.skillName.split("/", 1)[-1] if ("/" in args.skillName) else args.skillName
  # Locate the skill by its frontmatter name.
  doc = FindSkillByName(rootPath, bareName)
  if (doc is None):
    console.print(f"[red]error:[/red] no skill named '{bareName}'")
    return 2
  # Cache the single skill and print its destination path.
  destination = CacheOne(doc, cacheRoot)
  console.print(str(destination))
  return 0


if (__name__ == "__main__"):
  sys.exit(Main())
