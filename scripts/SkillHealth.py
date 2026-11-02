#!/usr/bin/env python3
"""
Generate the SkillStack health dashboard.

Produces docs/health.html with a per-skill card showing:

  * name, theme, line count
  * has-examples (yes/no)
  * has-references (yes/no)
  * link-check status (when a cached report is available)
  * last-modified timestamp

Styling is provided by embedded CSS; no external dependencies are required.
Uses ``jinja2`` when available, otherwise falls back to string formatting.

CLI:
  python scripts/SkillHealth.py
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  EnsureDir,
  IterateSkills,
  MinLineCount,
  SkillDoc,
  SkillsRoot,
)


# Attempt to import jinja2; degrade gracefully when missing.
try:
  import jinja2
  HasJinja2 = True
except ImportError:
  HasJinja2 = False


@dataclass
class HealthCard:
  """One card in the health dashboard."""

  Theme: str
  Name: str
  LineCount: int
  HasExamples: bool
  HasReferences: bool
  UnderMinLines: bool
  LinkCheckStatus: str
  LastModified: str


def LoadLinkCheckStatus(rootPath: Path) -> dict[str, str]:
  """
  Load the cached link-check status from ``.cache/link-check.json`` when present.

  Args:
    rootPath (Path): The skills repository root.

  Returns:
    dict[str, str]: Mapping of skill name to status string ("ok" or "broken").
  """
  cachePath = rootPath / ".cache" / "link-check.json"
  # Return an empty mapping when the cache file does not exist.
  if (not cachePath.is_file()):
    return {}
  try:
    return json.loads(cachePath.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
    return {}


def BuildCards(rootPath: Path) -> list[HealthCard]:
  """
  Build one HealthCard per skill, sorted by theme then name.

  Args:
    rootPath (Path): The skills repository root.

  Returns:
    list[HealthCard]: Cards sorted by theme then name.
  """
  # Load any cached link-check status by skill name.
  linkStatus = LoadLinkCheckStatus(rootPath)
  cards = []
  for doc in IterateSkills(rootPath):
    # Compute the last-modified timestamp from the file's mtime.
    mtime = doc.SkillPath.stat().st_mtime
    lastModified = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
    # Look up the cached link-check status, defaulting to "unknown".
    status = linkStatus.get(doc.Name, "unknown")
    cards.append(HealthCard(
      Theme=doc.Theme,
      Name=doc.Name or doc.SkillPath.parent.name,
      LineCount=doc.LineCount,
      HasExamples=doc.HasExamples,
      HasReferences=doc.HasReferences,
      UnderMinLines=(doc.LineCount < MinLineCount),
      LinkCheckStatus=status,
      LastModified=lastModified,
    ))
  # Sort cards by theme then name for stable dashboard layout.
  cards.sort(key=lambda c: (c.Theme, c.Name))
  return cards


# Embedded CSS for the dashboard, kept inline to avoid external dependencies.
EmbeddedCss = """
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0;
  padding: 2rem;
  background: #f7f8fa;
  color: #1f2933;
}
header {
  margin-bottom: 1.5rem;
}
header h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.75rem;
}
header p {
  margin: 0;
  color: #52606d;
}
.theme-block {
  margin-bottom: 2rem;
}
.theme-block h2 {
  border-bottom: 2px solid #cbd2d9;
  padding-bottom: 0.25rem;
  font-size: 1.25rem;
  color: #243b53;
}
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.75rem;
}
.card {
  background: #ffffff;
  border: 1px solid #e4e7eb;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
.card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #1f2933;
}
.card .row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  margin: 0.15rem 0;
}
.card .row .label { color: #52606d; }
.card .row .value { color: #1f2933; font-weight: 600; }
.card .badge {
  display: inline-block;
  padding: 0.05rem 0.4rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  margin-left: 0.25rem;
}
.badge.ok { background: #c8f0d4; color: #1c6332; }
.badge.broken { background: #ffd6d6; color: #8d1f1f; }
.badge.unknown { background: #e4e7eb; color: #52606d; }
.badge.yes { background: #c8f0d4; color: #1c6332; }
.badge.no { background: #ffd6d6; color: #8d1f1f; }
.badge.warn { background: #fff1c8; color: #6b4f00; }
"""


def RenderWithJinja(cards: list[HealthCard], generatedAt: str) -> str:
  """
  Render the dashboard HTML using jinja2.

  Args:
    cards (list[HealthCard]): Cards to render.
    generatedAt (str): ISO timestamp for the generated-at footer.

  Returns:
    str: HTML document string.
  """
  # Build a jinja2 environment with a string template loader.
  env = jinja2.Environment(autoescape=True, loader=jinja2.BaseLoader())
  template = env.from_string(HTML_TEMPLATE)
  # Group cards by theme for sectioned rendering.
  byTheme: dict[str, list[HealthCard]] = {}
  for card in cards:
    byTheme.setdefault(card.Theme, []).append(card)
  themes = sorted(byTheme.keys())
  return template.render(Css=EmbeddedCss, GeneratedAt=generatedAt, Themes=themes, ByTheme=byTheme)


def RenderWithString(cards: list[HealthCard], generatedAt: str) -> str:
  """
  Render the dashboard HTML using plain string formatting (fallback path).

  Args:
    cards (list[HealthCard]): Cards to render.
    generatedAt (str): ISO timestamp for the generated-at footer.

  Returns:
    str: HTML document string.
  """
  # Group cards by theme for sectioned rendering.
  byTheme: dict[str, list[HealthCard]] = {}
  for card in cards:
    byTheme.setdefault(card.Theme, []).append(card)
  themes = sorted(byTheme.keys())
  parts = []
  # Open the HTML document with the embedded CSS.
  parts.append("<!DOCTYPE html>")
  parts.append("<html lang=\"en\">")
  parts.append("<head>")
  parts.append("<meta charset=\"utf-8\">")
  parts.append("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
  parts.append("<title>SkillStack Health Dashboard</title>")
  parts.append("<style>")
  parts.append(EmbeddedCss)
  parts.append("</style>")
  parts.append("</head>")
  parts.append("<body>")
  parts.append("<header>")
  parts.append("<h1>SkillStack Health Dashboard</h1>")
  parts.append(f"<p>Generated {html.escape(generatedAt)} | {len(cards)} skills</p>")
  parts.append("</header>")
  # Render each theme as its own block of cards.
  for theme in themes:
    parts.append("<section class=\"theme-block\">")
    parts.append(f"<h2>{html.escape(theme)} ({len(byTheme[theme])} skills)</h2>")
    parts.append("<div class=\"cards\">")
    for card in byTheme[theme]:
      parts.append(RenderCardHtml(card))
    parts.append("</div>")
    parts.append("</section>")
  parts.append("</body>")
  parts.append("</html>")
  return "\n".join(parts)


def RenderCardHtml(card: HealthCard) -> str:
  """
  Render one health card as an HTML fragment.

  Args:
    card (HealthCard): The card to render.

  Returns:
    str: HTML fragment for one card.
  """
  # Compute badge classes for each boolean flag.
  examplesBadge = "yes" if (card.HasExamples) else "no"
  referencesBadge = "yes" if (card.HasReferences) else "no"
  lineBadge = "warn" if (card.UnderMinLines) else "ok"
  # Normalize the link-check status into a known badge class.
  statusClass = card.LinkCheckStatus if (card.LinkCheckStatus in ("ok", "broken")) else "unknown"
  # Escape all user-controlled text to prevent HTML injection.
  safeName = html.escape(card.Name)
  safeTheme = html.escape(card.Theme)
  safeModified = html.escape(card.LastModified)
  safeStatus = html.escape(card.LinkCheckStatus or "unknown")
  return (
    f"<div class=\"card\">"
    f"<h3>{safeName}</h3>"
    f"<div class=\"row\"><span class=\"label\">Theme</span><span class=\"value\">{safeTheme}</span></div>"
    f"<div class=\"row\"><span class=\"label\">Lines</span><span class=\"value\">{card.LineCount} <span class=\"badge {lineBadge}\">{('short' if card.UnderMinLines else 'ok')}</span></span></div>"
    f"<div class=\"row\"><span class=\"label\">Examples</span><span class=\"value\"><span class=\"badge {examplesBadge}\">{('yes' if card.HasExamples else 'no')}</span></span></div>"
    f"<div class=\"row\"><span class=\"label\">References</span><span class=\"value\"><span class=\"badge {referencesBadge}\">{('yes' if card.HasReferences else 'no')}</span></span></div>"
    f"<div class=\"row\"><span class=\"label\">Link check</span><span class=\"value\"><span class=\"badge {statusClass}\">{safeStatus}</span></span></div>"
    f"<div class=\"row\"><span class=\"label\">Modified</span><span class=\"value\">{safeModified}</span></div>"
    f"</div>"
  )


# Jinja2 template used when jinja2 is available. The structure mirrors the
# string-formatting fallback so both renderers produce equivalent HTML.
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SkillStack Health Dashboard</title>
<style>{{ Css|safe }}</style>
</head>
<body>
<header>
<h1>SkillStack Health Dashboard</h1>
<p>Generated {{ GeneratedAt }} | {{ Themes | length }} themes</p>
</header>
{% for theme in Themes %}
<section class="theme-block">
<h2>{{ theme }} ({{ ByTheme[theme] | length }} skills)</h2>
<div class="cards">
{% for card in ByTheme[theme] %}
<div class="card">
<h3>{{ card.Name }}</h3>
<div class="row"><span class="label">Theme</span><span class="value">{{ card.Theme }}</span></div>
<div class="row"><span class="label">Lines</span><span class="value">{{ card.LineCount }} <span class="badge {{ 'warn' if card.UnderMinLines else 'ok' }}">{{ 'short' if card.UnderMinLines else 'ok' }}</span></span></div>
<div class="row"><span class="label">Examples</span><span class="value"><span class="badge {{ 'yes' if card.HasExamples else 'no' }}">{{ 'yes' if card.HasExamples else 'no' }}</span></span></div>
<div class="row"><span class="label">References</span><span class="value"><span class="badge {{ 'yes' if card.HasReferences else 'no' }}">{{ 'yes' if card.HasReferences else 'no' }}</span></span></div>
<div class="row"><span class="label">Link check</span><span class="value"><span class="badge {{ card.LinkCheckStatus if card.LinkCheckStatus in ('ok', 'broken') else 'unknown' }}">{{ card.LinkCheckStatus }}</span></span></div>
<div class="row"><span class="label">Modified</span><span class="value">{{ card.LastModified }}</span></div>
</div>
{% endfor %}
</div>
</section>
{% endfor %}
</body>
</html>
"""


def RenderHtml(cards: list[HealthCard], generatedAt: str) -> str:
  """
  Render the dashboard HTML using jinja2 when available, else string formatting.

  Args:
    cards (list[HealthCard]): Cards to render.
    generatedAt (str): ISO timestamp for the generated-at footer.

  Returns:
    str: HTML document string.
  """
  # Pick the renderer based on jinja2 availability.
  if (HasJinja2):
    return RenderWithJinja(cards, generatedAt)
  return RenderWithString(cards, generatedAt)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Generate docs/health.html with per-skill health cards.",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  parser.add_argument(
    "--output",
    default=str(SkillsRoot() / "docs" / "health.html"),
    help="Destination HTML path (default: <root>/docs/health.html).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the health dashboard generator.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; always zero on success.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  outputPath = Path(args.output).resolve()
  console = Console()
  # Build the per-skill cards from the parsed skills.
  cards = BuildCards(rootPath)
  # Render the dashboard HTML.
  generatedAt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
  htmlText = RenderHtml(cards, generatedAt)
  # Ensure the parent directory exists before opening the file.
  EnsureDir(outputPath.parent)
  outputPath.write_text(htmlText, encoding="utf-8")
  # Print a one-line summary using the active renderer name.
  renderer = "jinja2" if (HasJinja2) else "string-format"
  console.print(f"[green]wrote[/green] {outputPath} ({len(cards)} skills, renderer={renderer})")
  return 0


if (__name__ == "__main__"):
  sys.exit(Main())
