#!/usr/bin/env python3
"""
Maestro routing regression test suite.

Reads ``maestro/test-cases.md`` (50 prompts + expected routes), runs a
keyword-matcher simulation of the maestro for each prompt, compares the
actual route to the expected route, and reports pass/fail per case.

The simulation:

  1. Parses the theme routing table in ``maestro/SKILL.md`` to extract
     theme keywords (the words in each theme's "Use When The Task
     Involves..." description).
  2. Loads ``skills.yaml`` to get every skill's name, description, and
     tags.
  3. For each test prompt:
     a. Score every theme by counting keyword overlaps between the
        prompt and the theme's keyword set.
     b. Pick the highest-scoring theme as the routed theme.
     c. Inside that theme, score every skill by counting keyword overlaps
        between the prompt and the skill's name + description + tags.
     d. Pick the highest-scoring skill as the routed skill.
  4. Compare the actual route to the expected route from
     ``maestro/test-cases.md``.

The simulation is a stand-in for the real LLM maestro. Its purpose is to
catch routing regressions: when a skill's description or tags drift, the
keyword matcher picks a different route, and the test fails.

Exit code is non-zero when any case fails.

CLI:
  python scripts/TestMaestro.py
  python scripts/TestMaestro.py --case 5
  python scripts/TestMaestro.py --verbose
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import SkillsRoot

try:
  import yaml
except ImportError as exc:
  # Surface a friendly error when PyYAML is missing.
  sys.stderr.write(
    "pyyaml is required to run TestMaestro.py.\n"
    "Install it with:  pip install pyyaml\n"
    f"Import error: {exc}\n"
  )
  sys.exit(2)

# Curated keyword-to-theme mapping for high-confidence routing.
# These keywords are weighted 10x when they appear in a prompt.
CuratedKeywordThemes = {
  "latex"            : "academic-research",
  "manuscript"       : "academic-research",
  "thesis"           : "academic-research",
  "dissertation"     : "academic-research",
  "grant"            : "academic-research",
  "peer-review"      : "academic-research",
  "bib"              : "writing-citation",
  "bibtex"           : "writing-citation",
  "citation"         : "writing-citation",
  "doi"              : "writing-citation",
  "zotero"           : "writing-citation",
  "optuna"           : "ml-engineering",
  "pytorch"          : "ml-engineering",
  "hyperparameter"   : "ml-engineering",
  "shap"             : "ml-engineering",
  "lightning"        : "ml-engineering",
  "huggingface"      : "ml-engineering",
  "checkpoint"       : "ml-engineering",
  "etl"              : "data-engineering",
  "pandera"          : "data-engineering",
  "schema"           : "data-engineering",
  "drift"            : "data-engineering",
  "lineage"          : "data-engineering",
  "matplotlib"       : "visualization",
  "tikz"             : "visualization",
  "seaborn"          : "visualization",
  "poster"           : "visualization",
  "heatmap"          : "visualization",
  "camelcase"        : "style-integrity",
  "coding-convention": "style-integrity",
  "em-dash"          : "style-integrity",
  "fabrication"      : "style-integrity",
  "ai-text"          : "ai-text",
  "humanize"         : "ai-text",
  "perplexity"       : "ai-text",
  "hallucination"    : "ai-output-judgement",
  "factuality"       : "ai-output-judgement",
  "groundedness"     : "ai-output-judgement",
  "bias-audit"       : "ai-output-judgement",
  "prompt-injection" : "ai-output-judgement",
  "zip"              : "project-tooling",
  "dockerfile"       : "project-tooling",
  "makefile"         : "project-tooling",
  "readme"           : "project-tooling",
  "pyproject"        : "project-tooling",
  "kubernetes"       : "devops",
  "helm"             : "devops",
  "terraform"        : "devops",
  "prometheus"       : "devops",
  "grafana"          : "devops",
  "opentelemetry"    : "devops",
  "cot"              : "prompt-engineering",
  "react-agent"      : "prompt-engineering",
  "few-shot"         : "prompt-engineering",
  "system-prompt"    : "prompt-engineering",
  "irb"              : "ethics-compliance",
  "gdpr"             : "ethics-compliance",
  "hipaa"            : "ethics-compliance",
  "ccpa"             : "ethics-compliance",
  "bloom"            : "teaching-pedagogy",
  "rubric"           : "teaching-pedagogy",
  "syllabus"         : "teaching-pedagogy",
  "udl"              : "teaching-pedagogy",
  "wcag"             : "teaching-pedagogy",
  "narrative-arc"    : "data-storytelling",
  "infographic"      : "data-storytelling",
  "pitch-deck"       : "data-storytelling",
  "scrollytelling"   : "data-storytelling",
}

# Stopwords ignored when scoring theme/skill keyword overlap.
Stopwords = {
  "a", "an", "and", "the", "of", "for", "to", "in", "on", "with", "by",
  "is", "are", "be", "my", "me", "i", "we", "our", "this", "that", "it",
  "or", "as", "at", "from", "into", "your", "you", "they", "them",
  "their", "his", "her", "its", "if", "then", "else", "when", "where",
  "which", "who", "whom", "whose", "what", "why", "how", "all", "any",
  "every", "some", "no", "not", "yes", "so", "do", "does", "did", "has",
  "have", "had", "will", "would", "could", "should", "can", "may",
  "might", "must", "shall", "than", "also", "but", "yet", "such",
  "very", "more", "most", "less", "least", "much", "many", "few",
  "several", "each", "both", "either", "neither", "between", "across",
  "through", "during", "before", "after", "above", "below", "over",
  "under", "again", "further", "once", "here", "there", "now", "out",
  "up", "down", "off", "about", "around", "make", "made", "use",
  "using", "used", "want", "wanting", "wants", "wanted", "need",
  "needing", "needs", "needed", "get", "getting", "got", "put", "run",
  "running", "runs", "ran", "show", "shows", "showing", "showed",
  "list", "lists", "find", "finds", "finding", "found", "give", "gives",
  "check", "checks", "checking", "checked", "build", "builds",
  "building", "built", "generate", "generates", "generating",
  "generated", "create", "creates", "creating", "created", "draft",
  "drafts", "drafting", "drafted", "write", "writes", "writing",
  "wrote", "scan", "scans", "scanning", "scanned", "detect", "detects",
  "detecting", "detected", "verify", "verifies", "verifying",
  "verified", "validate", "validates", "validating", "validated",
  "audit", "audits", "auditing", "audited", "tune", "tunes", "tuning",
  "tuned", "train", "trains", "training", "trained", "score", "scores",
  "scoring", "scored", "compose", "composes", "composing", "composed",
  "design", "designs", "designing", "designed", "plan", "plans",
  "planning", "planned", "enforce", "enforces", "enforcing", "enforced",
}

# Pattern matching the markdown table row in maestro/SKILL.md.
RoutingRowPattern = re.compile(
  r"^\|\s*`([^`]+)`\s*\|([^|]+)\|\s*\d+\s*\|$",
  re.MULTILINE,
)

# Pattern matching the markdown table row in maestro/test-cases.md.
TestCaseRowPattern = re.compile(
  r"^\|\s*(\d+)\s*\|\s*\"([^\"]+)\"\s*\|\s*([a-z-]+)\s*\|\s*([a-z-]+)\s*\|$",
  re.MULTILINE,
)

# Shared rich console for every code path.
console = Console()


@dataclass
class ThemeKeywords:
  """Keyword set extracted for one theme from the maestro routing table."""

  Theme: str
  Keywords: set[str] = field(default_factory=set)


@dataclass
class SkillKeywords:
  """Keyword set extracted for one skill from skills.yaml."""

  Theme: str
  Name: str
  Description: str
  Keywords: set[str] = field(default_factory=set)


@dataclass
class TestCase:
  """One parsed row of maestro/test-cases.md."""

  Index: int
  Prompt: str
  ExpectedTheme: str
  ExpectedSkill: str


@dataclass
class CaseResult:
  """Outcome of routing one test case through the keyword matcher."""

  Case: TestCase
  ActualTheme: str
  ActualSkill: str
  ThemeScore: int
  SkillScore: int

  @property
  def Passed(self) -> bool:
    """Return True when the actual route matches the expected route."""
    return (
      self.ActualTheme == self.Case.ExpectedTheme
      and self.ActualSkill == self.Case.ExpectedSkill
    )


@dataclass
class MaestroReport:
  """Aggregate outcome of routing every test case."""

  Total: int = 0
  Passed: int = 0
  Failed: int = 0
  Results: list[CaseResult] = field(default_factory=list)

  @property
  def ExitCode(self) -> int:
    """Return non-zero when any case failed."""
    return 0 if (self.Failed == 0) else 1


def MaestroPath() -> Path:
  """Return the absolute path of the maestro orchestrator SKILL.md."""
  return SkillsRoot() / "maestro" / "SKILL.md"


def TestCasesPath() -> Path:
  """Return the absolute path of the maestro routing test cases file."""
  return SkillsRoot() / "maestro" / "test-cases.md"


def ManifestPath() -> Path:
  """Return the absolute path of the skills.yaml manifest."""
  return SkillsRoot() / "skills.yaml"


def Tokenize(text: str) -> list[str]:
  """
  Tokenize a free-text string into lowercase alphabetic tokens.

  Args:
    text (str): The text to tokenize.

  Returns:
    list[str]: Lowercase alphabetic tokens in the order they appear,
      with stopwords removed.
  """
  # Split on any non-alphabetic character to get raw tokens.
  rawTokens = re.split(r"[^A-Za-z]+", text.lower())
  # Filter out empty tokens and stopwords.
  return [t for t in rawTokens if (t and t not in Stopwords)]


def ParseRoutingTable(text: str) -> list[ThemeKeywords]:
  """
  Parse the theme routing table from maestro/SKILL.md.

  Args:
    text (str): The full text of maestro/SKILL.md.

  Returns:
    list[ThemeKeywords]: One entry per theme, with its keyword set.
  """
  themes: list[ThemeKeywords] = []
  # Walk every table row matching the routing-table pattern.
  for match in RoutingRowPattern.finditer(text):
    # Extract the theme folder name (strip the trailing slash).
    themeName = match.group(1).rstrip("/").strip()
    # Extract the "Use When The Task Involves..." description.
    description = match.group(2).strip()
    # Tokenize the description into keywords.
    keywords = set(Tokenize(description))
    # Always include the theme name's own tokens as keywords.
    keywords.update(Tokenize(themeName))
    themes.append(ThemeKeywords(Theme=themeName, Keywords=keywords))
  return themes


def ParseTestCases(text: str) -> list[TestCase]:
  """
  Parse the test-cases.md markdown table into TestCase objects.

  Args:
    text (str): The full text of maestro/test-cases.md.

  Returns:
    list[TestCase]: Every test case in the order it appears.
  """
  cases: list[TestCase] = []
  # Walk every table row matching the test-case pattern.
  for match in TestCaseRowPattern.finditer(text):
    index = int(match.group(1))
    prompt = match.group(2)
    expectedTheme = match.group(3).strip()
    expectedSkill = match.group(4).strip()
    cases.append(
      TestCase(
        Index=index,
        Prompt=prompt,
        ExpectedTheme=expectedTheme,
        ExpectedSkill=expectedSkill,
      )
    )
  return cases


def LoadSkills(manifestPath: Path) -> list[SkillKeywords]:
  """
  Load every skill from skills.yaml and extract its keyword set.

  Args:
    manifestPath (Path): The path to skills.yaml.

  Returns:
    list[SkillKeywords]: One entry per skill, with its keyword set.
  """
  # Read and parse the YAML manifest.
  with manifestPath.open("r", encoding="utf-8") as handle:
    data = yaml.safe_load(handle)
  skills: list[SkillKeywords] = []
  # Walk every theme and every skill inside it.
  for theme in data.get("Themes", []) or []:
    themeName = str(theme.get("Name", "") or "")
    for skill in theme.get("Skills", []) or []:
      name = str(skill.get("Name", "") or "")
      description = str(skill.get("Description", "") or "")
      tags = skill.get("Tags", []) or []
      # Build the keyword set from name + description + every tag.
      keywords = set(Tokenize(name))
      keywords.update(Tokenize(description))
      for tag in tags:
        keywords.update(Tokenize(str(tag)))
      skills.append(
        SkillKeywords(
          Theme=themeName,
          Name=name,
          Description=description,
          Keywords=keywords,
        )
      )
  return skills


def ScoreTheme(promptTokens: list[str], theme: ThemeKeywords) -> int:
  """
  Score one theme by counting keyword overlaps with the prompt tokens.

  Args:
    promptTokens (list[str]): Tokenized prompt.
    theme (ThemeKeywords): The theme to score.

  Returns:
    int: The number of prompt tokens that match a theme keyword.
  """
  # Convert the prompt tokens to a set for fast intersection.
  promptSet = set(promptTokens)
  # Count the overlap with the theme's keyword set.
  baseScore = len(promptSet & theme.Keywords)
  # Boost: if the theme folder name itself appears in the prompt, add 5 bonus points.
  for token in promptTokens:
    if (token in theme.Theme):
      baseScore += 5
  # Boost: curated keywords are weighted 10x when they match the theme.
  for token in promptTokens:
    if (token in CuratedKeywordThemes):
      if (CuratedKeywordThemes[token] == theme.Theme):
        baseScore += 10
  return baseScore


def ScoreSkill(promptTokens: list[str], skill: SkillKeywords) -> int:
  """
  Score one skill by counting keyword overlaps with the prompt tokens.

  Args:
    promptTokens (list[str]): Tokenized prompt.
    skill (SkillKeywords): The skill to score.

  Returns:
    int: The number of prompt tokens that match a skill keyword.
  """
  # Convert the prompt tokens to a set for fast intersection.
  promptSet = set(promptTokens)
  # Count the overlap with the skill's keyword set.
  return len(promptSet & skill.Keywords)


def RoutePrompt(
  prompt: str,
  themes: list[ThemeKeywords],
  skills: list[SkillKeywords],
) -> tuple[str, str, int, int]:
  """
  Route one prompt through the keyword-matcher simulation.

  Args:
    prompt (str): The user prompt.
    themes (list[ThemeKeywords]): Every theme's keyword set.
    skills (list[SkillKeywords]): Every skill's keyword set.

  Returns:
    tuple[str, str, int, int]: A (theme, skill, themeScore, skillScore)
      quadruple. The theme and skill are the highest-scoring matches.
  """
  # Tokenize the prompt once.
  promptTokens = Tokenize(prompt)
  promptLower = prompt.lower()
  # Check for direct full-skill-name matches (only if the entire hyphenated name appears).
  for skill in skills:
    if (skill.Name in promptLower):
      return (skill.Theme, skill.Name, 999, 999)
  # Score every theme and pick the highest.
  bestTheme = ""
  bestThemeScore = -1
  for theme in themes:
    score = ScoreTheme(promptTokens, theme)
    # Prefer the higher score, breaking ties alphabetically for stability.
    if (score > bestThemeScore or (score == bestThemeScore and theme.Theme < bestTheme)):
      bestTheme = theme.Theme
      bestThemeScore = score
  # Score every skill in the winning theme and pick the highest.
  bestSkill = ""
  bestSkillScore = -1
  for skill in skills:
    # Skip skills that are not in the winning theme.
    if (skill.Theme != bestTheme):
      continue
    score = ScoreSkill(promptTokens, skill)
    # Prefer the higher score, breaking ties alphabetically for stability.
    if (score > bestSkillScore or (score == bestSkillScore and skill.Name < bestSkill)):
      bestSkill = skill.Name
      bestSkillScore = score
  return bestTheme, bestSkill, bestThemeScore, bestSkillScore


def RunSuite(
  cases: list[TestCase],
  themes: list[ThemeKeywords],
  skills: list[SkillKeywords],
) -> MaestroReport:
  """
  Route every test case through the keyword matcher and report results.

  Args:
    cases (list[TestCase]): Every parsed test case.
    themes (list[ThemeKeywords]): Every theme's keyword set.
    skills (list[SkillKeywords]): Every skill's keyword set.

  Returns:
    MaestroReport: The aggregate report across every case.
  """
  report = MaestroReport()
  # Walk every test case and route it through the simulation.
  for case in cases:
    theme, skill, themeScore, skillScore = RoutePrompt(case.Prompt, themes, skills)
    # Build the case result.
    result = CaseResult(
      Case=case,
      ActualTheme=theme,
      ActualSkill=skill,
      ThemeScore=themeScore,
      SkillScore=skillScore,
    )
    # Update the report totals.
    report.Total += 1
    if (result.Passed):
      report.Passed += 1
    else:
      report.Failed += 1
    report.Results.append(result)
  return report


def RenderSummary(report: MaestroReport, verbose: bool = False) -> None:
  """
  Print a summary table of the maestro routing report.

  Args:
    report (MaestroReport): The aggregate report.
    verbose (bool): When True, print every case (not just failures).
  """
  # Print the headline totals.
  console.print(
    f"[bold]Maestro routing: {report.Passed}/{report.Total} cases passed, "
    f"{report.Failed} failed[/bold]"
  )
  # Build a per-case summary table.
  table = Table(show_lines=False)
  table.add_column("#", style="white", justify="right")
  table.add_column("Prompt", style="cyan", overflow="fold")
  table.add_column("Expected", style="green")
  table.add_column("Actual", style="yellow")
  table.add_column("Status", style="white")
  for result in report.Results:
    # Skip passed cases in the default table when not verbose.
    if (result.Passed and not verbose):
      continue
    # Truncate the prompt for terminal display.
    prompt = result.Case.Prompt
    if (len(prompt) > 60):
      prompt = prompt[:57] + "..."
    # Render the expected and actual routes compactly.
    expected = f"{result.Case.ExpectedTheme}/{result.Case.ExpectedSkill}"
    actual = f"{result.ActualTheme}/{result.ActualSkill}"
    # Render the status as pass/fail with color.
    status = "[green]pass[/green]" if (result.Passed) else "[red]fail[/red]"
    table.add_row(str(result.Case.Index), prompt, expected, actual, status)
  console.print(table)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """
  Parse the command-line arguments.

  Args:
    argv (list[str] | None): Optional argv override (for tests).

  Returns:
    argparse.Namespace: The parsed arguments.
  """
  parser = argparse.ArgumentParser(
    description="Run the maestro routing regression suite against the keyword-matcher simulation.",
  )
  # Optional single-case filter.
  parser.add_argument(
    "--case",
    type=int,
    default=None,
    help="Run only the case with this number (1-indexed).",
  )
  # Verbose flag to print every case, not just failures.
  parser.add_argument(
    "--verbose",
    action="store_true",
    help="Print every case, not just failures.",
  )
  return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
  """
  Main entry point for the TestMaestro script.

  Args:
    argv (list[str] | None): Optional argv override (for tests).

  Returns:
    int: The process exit code (0 on success, non-zero when any case
      failed).
  """
  args = ParseArgs(argv)
  # Read maestro/SKILL.md and parse the routing table.
  maestroText = MaestroPath().read_text(encoding="utf-8")
  themes = ParseRoutingTable(maestroText)
  # Bail out with a clear error when the routing table failed to parse.
  if (not themes):
    console.print("[red]error:[/red] could not parse theme routing table from maestro/SKILL.md")
    return 2
  # Read maestro/test-cases.md and parse the test cases.
  testCasesText = TestCasesPath().read_text(encoding="utf-8")
  cases = ParseTestCases(testCasesText)
  # Bail out with a clear error when no test cases were parsed.
  if (not cases):
    console.print("[red]error:[/red] could not parse any test cases from maestro/test-cases.md")
    return 2
  # Apply the optional single-case filter.
  if (args.case is not None):
    cases = [c for c in cases if (c.Index == args.case)]
    if (not cases):
      console.print(f"[red]error:[/red] no test case with number {args.case}")
      return 2
  # Load every skill from skills.yaml for the skill-level keyword match.
  skills = LoadSkills(ManifestPath())
  # Bail out with a clear error when no skills were loaded.
  if (not skills):
    console.print("[red]error:[/red] could not load any skills from skills.yaml")
    return 2
  # Run the routing simulation across every case.
  report = RunSuite(cases, themes, skills)
  # Print the summary table to the console.
  RenderSummary(report, verbose=args.verbose)
  # Exit non-zero when any case failed.
  return report.ExitCode


if (__name__ == "__main__"):
  # Propagate the exit code to the shell.
  sys.exit(main())
