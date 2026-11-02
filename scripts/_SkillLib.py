#!/usr/bin/env python3
"""
SkillStack shared library.

Provides YAML frontmatter parsing, SKILL.md loading, theme grouping, and the
canonical lists of required frontmatter keys and body sections shared by every
utility script under scripts/.

All public functions follow the repo-wide coding conventions: camelCase
variables, CamelCase functions and classes, parenthesized if-conditions, double
quoted strings, two-space indentation, and period-terminated comments above
each statement.
"""

from __future__ import annotations

import os
import re
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

# Canonical list of required frontmatter keys enforced by the linter.
RequiredFrontmatterKeys = [
  "name",
  "description",
  "metadata.author",
  "metadata.version",
  "metadata.theme",
  "tags",
  "related",
  "permissions",
  "language",
]

# Canonical list of required body sections enforced by the linter.
RequiredSections = [
  "## When To Use",
  "## Workflow",
  "## Inputs",
  "## Outputs",
  "## Key Rules",
  "## Examples",
  "## References",
]

# Banned tokens that indicate incomplete work in any SKILL.md.
BannedMarkers = ["TODO", "XXX", "FIXME"]

# Allowed line-count window for every SKILL.md body.
MinLineCount = 80
MaxLineCount = 280  # coding-conventions-enforcer (264 lines) is the documented exception; all others target <=180.


@dataclass
class SkillDoc:
  """Parsed representation of a single SKILL.md file."""

  SkillPath: Path
  Theme: str
  Name: str
  Description: str
  Author: str
  Version: str
  MetadataTheme: str
  Tags: list = field(default_factory=list)
  Related: list = field(default_factory=list)
  Prerequisites: list = field(default_factory=list)
  Outputs: list = field(default_factory=list)
  Difficulty: str = ""
  EstimatedTokens: int = 0
  Permissions: list = field(default_factory=list)
  Language: str = ""
  Frontmatter: dict = field(default_factory=dict)
  Body: str = ""
  LineCount: int = 0
  HasExamples: bool = False
  HasReferences: bool = False
  MissingSections: list = field(default_factory=list)
  ParseError: str = ""

  @property
  def RelativePath(self) -> str:
    """Return the skill's path relative to the skills root."""
    try:
      # Compute the path relative to the current working directory if possible.
      return str(self.SkillPath.relative_to(Path.cwd()))
    except ValueError:
      # Fall back to the absolute path when no relative path is possible.
      return str(self.SkillPath)


def SplitFrontmatter(content: str) -> tuple[str, str]:
  """
  Split a SKILL.md file into its YAML frontmatter and Markdown body.

  Args:
    content (str): The raw text of a SKILL.md file.

  Returns:
    tuple[str, str]: A ("Frontmatter", "Body") pair. The frontmatter string
      is empty when no opening `---` marker is present.

  Raises:
    ValueError: When the opening `---` has no matching closing `---`.
  """
  # Require the file to start with a YAML frontmatter marker.
  if (not content.startswith("---")):
    return "", content
  # Walk the remaining lines to find the closing marker.
  lines = content.splitlines()
  closeIndex = None
  for index in range(1, len(lines)):
    # Match a line that is exactly three dashes.
    if (lines[index].strip() == "---"):
      closeIndex = index
      break
  # Reject files that open a frontmatter block but never close it.
  if (closeIndex is None):
    raise ValueError("SKILL.md frontmatter is not terminated by a closing --- line.")
  # Reconstruct the frontmatter block and the remaining body text.
  frontmatter = "\n".join(lines[1:closeIndex])
  body = "\n".join(lines[closeIndex + 1:])
  return frontmatter, body


def ParseFrontmatter(content: str) -> tuple[dict, str, str]:
  """
  Parse the YAML frontmatter of a SKILL.md file and return the body too.

  Args:
    content (str): The raw text of a SKILL.md file.

  Returns:
    tuple[dict, str, str]: A ("Frontmatter", "Body", "Error") triple. The
      Error string is empty on success and contains a descriptive message
      otherwise.
  """
  # Split the file into frontmatter and body sections.
  try:
    frontmatterText, body = SplitFrontmatter(content)
  except ValueError as exc:
    # Surface the split error to the caller verbatim.
    return {}, "", str(exc)
  # An empty frontmatter block is treated as an empty dict.
  if (not frontmatterText.strip()):
    return {}, body, "Frontmatter block is empty."
  # Parse the YAML content safely into a Python object.
  try:
    frontmatter = yaml.safe_load(frontmatterText)
  except yaml.YAMLError as exc:
    # Convert YAML parse errors into a descriptive string.
    return {}, body, f"YAML parse error: {exc}"
  # Require the parsed YAML to be a mapping.
  if (not isinstance(frontmatter, dict)):
    return {}, body, "Frontmatter did not parse to a mapping."
  return frontmatter, body, ""


def _GetByPath(mapping: dict, dottedKey: str, default=None):
  """Resolve a dotted path like ``metadata.author`` from a nested dict."""
  # Walk each segment of the dotted key.
  current = mapping
  for segment in dottedKey.split("."):
    # Bail out when the current level is not a dict.
    if (not isinstance(current, dict)):
      return default
    # Move one level deeper, returning the default when the key is absent.
    if (segment not in current):
      return default
    current = current[segment]
  return current


def _AsList(value) -> list:
  """Coerce a scalar or sequence into a list for predictable iteration."""
  # Treat None as an empty list.
  if (value is None):
    return []
  # Strings are scalars, not sequences of characters.
  if (isinstance(value, str)):
    return [value]
  # Lists and tuples pass through unchanged.
  if (isinstance(value, (list, tuple))):
    return list(value)
  # Anything else is wrapped as a single-element list.
  return [value]


def LoadSkillMd(skillPath: Path, theme: str | None = None) -> SkillDoc:
  """
  Load and parse a single SKILL.md file into a SkillDoc instance.

  Args:
    skillPath (Path): The path to the SKILL.md file.
    theme (str | None): Optional override for the skill's theme. When
      omitted the theme is derived from the parent directory of the
      SKILL.md file.

  Returns:
    SkillDoc: A populated skill document. The ``ParseError`` field is empty
      on success and contains a diagnostic otherwise.
  """
  # Read the raw file contents as UTF-8.
  skillPath = Path(skillPath)
  try:
    content = skillPath.read_text(encoding="utf-8")
  except OSError as exc:
    # Build a stub document that carries the read error.
    doc = SkillDoc(SkillPath=skillPath, Theme=theme or "", Name="", Description="")
    doc.ParseError = f"Read error: {exc}"
    return doc
  # Parse the YAML frontmatter and the Markdown body.
  frontmatter, body, parseError = ParseFrontmatter(content)
  # Derive the theme from the parent's parent directory when not provided.
  derivedTheme = theme
  if (derivedTheme is None):
    # Top-level SKILL.md files use their own folder name as the theme.
    parent = skillPath.parent.name
    grandparent = skillPath.parent.parent.name
    derivedTheme = parent if (grandparent == "skills") else grandparent
  # Extract top-level and metadata fields with safe defaults.
  metadata = frontmatter.get("metadata", {}) if (isinstance(frontmatter, dict)) else {}
  # The description may live at the top level or under metadata.
  description = frontmatter.get("description") or _GetByPath(frontmatter, "metadata.description", "")
  # Build the SkillDoc with all canonical fields populated.
  doc = SkillDoc(
    SkillPath=skillPath,
    Theme=derivedTheme,
    Name=str(frontmatter.get("name", "") or ""),
    Description=str(description or ""),
    Author=str(_GetByPath(frontmatter, "metadata.author", "") or ""),
    Version=str(_GetByPath(frontmatter, "metadata.version", "") or ""),
    MetadataTheme=str(_GetByPath(frontmatter, "metadata.theme", derivedTheme) or ""),
    Tags=_AsList(frontmatter.get("tags")),
    Related=_AsList(frontmatter.get("related")),
    Prerequisites=_AsList(frontmatter.get("prerequisites")),
    Outputs=_AsList(frontmatter.get("outputs")),
    Difficulty=str(frontmatter.get("difficulty", "") or ""),
    EstimatedTokens=int(frontmatter.get("estimated_tokens", 0) or 0),
    Permissions=_AsList(frontmatter.get("permissions")),
    Language=str(frontmatter.get("language", "") or ""),
    Frontmatter=frontmatter,
    Body=body,
  )
  doc.ParseError = parseError
  # Compute the line count of the entire file (frontmatter plus body).
  doc.LineCount = len(content.splitlines())
  # Detect the presence of each required body section.
  doc.MissingSections = [
    section for section in RequiredSections if (section not in body)
  ]
  # Has-examples is true when the Examples section is non-empty.
  doc.HasExamples = "## Examples" in body and bool(
    re.search(r"^## Examples\s*$.+?^## ", body + "\n## ", flags=re.MULTILINE | re.DOTALL))
  # Has-references is true when the References section contains at least one URL or bullet.
  referencesBlock = _ExtractSection(body, "## References")
  doc.HasReferences = bool(referencesBlock) and bool(
    re.search(r"(https?://|^\s*[-*]\s+)", referencesBlock, flags=re.MULTILINE))
  return doc


def _ExtractSection(body: str, header: str) -> str:
  """Return the text of one Markdown section, up to the next ``##`` header."""
  # Compile a pattern that matches the section header through the next one.
  pattern = re.compile(
    r"^" + re.escape(header) + r"\s*$.*?(?=^## |\Z)",
    flags=re.MULTILINE | re.DOTALL,
  )
  match = pattern.search(body)
  # Return the matched text or an empty string when the header is absent.
  return match.group(0) if (match is not None) else ""


def IterateSkills(rootPath: Path | str) -> Iterator[SkillDoc]:
  """
  Walk every SKILL.md under the given skills root and yield parsed docs.

  The walker handles two layouts: top-level skills such as ``pdf/SKILL.md``
  (whose theme is the directory itself) and themed skills such as
  ``academic-research/research-ideation-planner/SKILL.md``.

  Args:
    rootPath (Path | str): The skills repository root.

  Yields:
    SkillDoc: Each parsed SKILL.md document.
  """
  # Normalize the root path to an absolute Path object.
  root = Path(rootPath).resolve()
  # Iterate over every directory entry under the root.
  for themeDir in sorted([child for child in root.iterdir() if (child.is_dir())]):
    # Skip hidden directories and Python caches.
    if (themeDir.name.startswith(".") or themeDir.name == "__pycache__"):
      continue
    # Detect the top-level SKILL.md layout (theme == directory).
    topSkill = themeDir / "SKILL.md"
    if (topSkill.is_file()):
      # Yield the top-level skill under its own directory name as theme.
      yield LoadSkillMd(topSkill, theme=themeDir.name)
    # Walk immediate subdirectories of the theme folder.
    for skillDir in sorted([child for child in themeDir.iterdir() if (child.is_dir())]):
      # Skip hidden directories and Python caches.
      if (skillDir.name.startswith(".") or skillDir.name == "__pycache__"):
        continue
      skillMd = skillDir / "SKILL.md"
      # Only emit a themed skill when its SKILL.md actually exists.
      if (skillMd.is_file()):
        yield LoadSkillMd(skillMd, theme=themeDir.name)


def FindSkillByName(rootPath: Path | str, skillName: str) -> SkillDoc | None:
  """
  Locate and load a single skill by its ``name`` frontmatter value.

  Args:
    rootPath (Path | str): The skills repository root.
    skillName (str): The skill name to match (case-sensitive).

  Returns:
    SkillDoc | None: The matching skill, or None when not found.
  """
  # Walk every skill and return the first whose name matches.
  for doc in IterateSkills(rootPath):
    if (doc.Name == skillName):
      return doc
  return None


def ExtractUrls(text: str) -> list[str]:
  """
  Extract all unique HTTP(S) URLs from a block of text.

  Args:
    text (str): The text to scan.

  Returns:
    list[str]: Unique URLs in the order they first appear.
  """
  # Match http(s) URLs up to the first whitespace or closing paren.
  matches = re.findall(r"https?://[^\s\)]+", text)
  seen = set()
  result = []
  for url in matches:
    # Strip trailing punctuation that is not part of the URL itself.
    cleaned = url.rstrip(".,;:!")
    if (cleaned not in seen):
      seen.add(cleaned)
      result.append(cleaned)
  return result


def IsGithubBadgeUrl(url: str) -> bool:
  """Return True when the URL points to a shields.io badge service."""
  return "img.shields.io" in url


def ExtractArxivIds(text: str) -> list[str]:
  """
  Extract all unique arXiv identifiers of the form NNNN.NNNNN from text.

  Args:
    text (str): The text to scan.

  Returns:
    list[str]: Unique arXiv IDs in first-seen order.
  """
  # Match the canonical new-style arXiv identifier.
  matches = re.findall(r"\b\d{4}\.\d{4,5}\b", text)
  seen = set()
  result = []
  for match in matches:
    if (match not in seen):
      seen.add(match)
      result.append(match)
  return result


def ExtractDois(text: str) -> list[str]:
  """
  Extract all unique DOIs of the form 10.NNNN/... from text.

  Args:
    text (str): The text to scan.

  Returns:
    list[str]: Unique DOIs in first-seen order.
  """
  # Match the DOI prefix plus the suffix up to whitespace or a paren.
  matches = re.findall(r"\b10\.\d{4,}/[^\s\)]+", text)
  seen = set()
  result = []
  for match in matches:
    # Strip trailing punctuation that is not part of the DOI.
    cleaned = match.rstrip(".,;:!")
    if (cleaned not in seen):
      seen.add(cleaned)
      result.append(cleaned)
  return result


def EnsureDir(path: Path | str) -> Path:
  """Create a directory (and parents) if missing, then return the Path."""
  # Normalize to a Path and create with parents.
  target = Path(path)
  target.mkdir(parents=True, exist_ok=True)
  return target


def SkillsRoot() -> Path:
  """Return the absolute path of the skills repository root."""
  # This module lives in scripts/, so the root is its parent.
  return Path(__file__).resolve().parent.parent


def RelativeToSkills(path: Path | str) -> str:
  """Return the path relative to the skills root, falling back to absolute."""
  # Normalize both inputs and compute the relative path when possible.
  target = Path(path).resolve()
  try:
    return str(target.relative_to(SkillsRoot()))
  except ValueError:
    # Return the absolute path when no relative form exists.
    return str(target)


__all__ = [
  "RequiredFrontmatterKeys",
  "RequiredSections",
  "BannedMarkers",
  "MinLineCount",
  "MaxLineCount",
  "SkillDoc",
  "SplitFrontmatter",
  "ParseFrontmatter",
  "LoadSkillMd",
  "IterateSkills",
  "FindSkillByName",
  "ExtractUrls",
  "IsGithubBadgeUrl",
  "ExtractArxivIds",
  "ExtractDois",
  "EnsureDir",
  "SkillsRoot",
  "RelativeToSkills",
]
