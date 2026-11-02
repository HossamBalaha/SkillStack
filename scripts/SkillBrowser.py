#!/usr/bin/env python3
"""
SkillStack Streamlit skill browser.

A side-loaded Streamlit app that lets a user browse every SkillStack skill
interactively. The sidebar holds a theme dropdown and a search box; the
main panel renders the currently selected skill's SKILL.md body as
Markdown.

Run with:

  streamlit run scripts/SkillBrowser.py

The browser is read-only: it never writes files, never executes fenced
code blocks, and never makes outbound network calls. For the executable
variant, see scripts/SmokeTest.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Streamlit import is deferred-fatal: we surface a friendly error if the
# package is not installed instead of crashing on import.
try:
  import streamlit as st
except ImportError as exc:
  # Print a friendly install hint and exit non-zero.
  sys.stderr.write(
    "streamlit is required to run SkillBrowser.py.\n"
    "Install it with:  pip install streamlit\n"
    f"Import error: {exc}\n"
  )
  sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import (
  FindSkillByName,
  IterateSkills,
  SkillDoc,
  SkillsRoot,
)

# Page configuration applied once at import time.
PageTitle = "SkillStack Browser"
PageIcon = "🧱"
PageLayout = "wide"

# Sidebar widget keys must be unique and stable across reruns.
SessionKeyTheme = "SelectedTheme"
SessionKeySkill = "SelectedSkill"
SessionKeyQuery = "SearchQuery"

# Skills whose names begin with an underscore are internal helpers.
HiddenNamePrefix = "_"


def LoadAllSkills(rootPath: Path | None = None) -> list[SkillDoc]:
  """
  Load every SkillStack skill document under the skills root.

  Args:
    rootPath (Path | None): Optional root override. Defaults to the
      auto-detected skills root (one level above scripts/).

  Returns:
    list[SkillDoc]: Every parsed skill document, in iteration order.
  """
  # Default to the auto-detected skills root when no override is provided.
  root = rootPath or SkillsRoot()
  # Materialize the iterator into a list for repeated traversal in the UI.
  return [doc for doc in IterateSkills(root) if (doc.Name)]


def GroupByTheme(docs: list[SkillDoc]) -> dict[str, list[SkillDoc]]:
  """
  Group a flat list of skill documents by their theme folder.

  Args:
    docs (list[SkillDoc]): The flat list of skill documents.

  Returns:
    dict[str, list[SkillDoc]]: Mapping from theme name to the skills in
      that theme, sorted alphabetically by skill name.
  """
  # Accumulate skills per theme in a plain dict for stable iteration.
  byTheme: dict[str, list[SkillDoc]] = {}
  for doc in docs:
    # Skip skills without a theme label (defensive: should never happen).
    if (not doc.Theme):
      continue
    byTheme.setdefault(doc.Theme, []).append(doc)
  # Sort each theme's skills alphabetically for a predictable dropdown.
  for theme in byTheme:
    byTheme[theme].sort(key=lambda d: d.Name)
  return byTheme


def SearchSkills(docs: list[SkillDoc], query: str) -> list[SkillDoc]:
  """
  Filter the skill list by a case-insensitive substring query.

  The query is matched against each skill's name, description, and tags.

  Args:
    docs (list[SkillDoc]): The full skill list.
    query (str): The search query (case-insensitive).

  Returns:
    list[SkillDoc]: Skills whose name, description, or tags contain the
      query. Sorted by name when the query is non-empty.
  """
  # Empty query returns the full list unchanged.
  needle = query.strip().lower()
  if (not needle):
    return list(docs)
  matches: list[SkillDoc] = []
  # Score each skill by counting how many fields contain the query.
  for doc in docs:
    # Build the haystack from name + description + every tag.
    haystackParts = [doc.Name, doc.Description] + [str(t) for t in doc.Tags]
    haystack = " ".join(haystackParts).lower()
    # Skip skills that do not contain the query at all.
    if (needle not in haystack):
      continue
    matches.append(doc)
  # Sort matches alphabetically for a stable search-results list.
  matches.sort(key=lambda d: d.Name)
  return matches


def RenderSidebar(docs: list[SkillDoc]) -> tuple[str | None, str]:
  """
  Render the sidebar with a theme dropdown and a search box.

  Args:
    docs (list[SkillDoc]): The full skill list, used to populate the
      theme dropdown.

  Returns:
    tuple[str | None, str]: A (selectedTheme, searchQuery) pair. The
      theme may be None when the user has not picked one yet.
  """
  # Group every skill by theme for the dropdown options.
  byTheme = GroupByTheme(docs)
  # Sort theme names alphabetically for a stable dropdown order.
  themeNames = sorted(byTheme.keys())
  # Render the sidebar header.
  st.sidebar.title("🧱 SkillStack Browser")
  st.sidebar.caption("168 skills · 9 themes · MIT License")
  # Theme dropdown.
  selectedTheme = st.sidebar.selectbox(
    "Theme",
    options=themeNames,
    index=0,
    help="Filter the skill list to one theme folder.",
  )
  # Free-text search box.
  searchQuery = st.sidebar.text_input(
    "Search",
    value="",
    placeholder="skill name, tag, or description…",
    help="Case-insensitive substring match across name, description, and tags.",
  )
  # Render a small footer with the total skill count for orientation.
  st.sidebar.divider()
  st.sidebar.caption(f"{len(docs)} skills loaded")
  return selectedTheme, searchQuery


def RenderSkillPanel(doc: SkillDoc) -> None:
  """
  Render one skill's SKILL.md body in the main panel.

  Args:
    doc (SkillDoc): The skill document to render.
  """
  # Render the skill name as the panel title for quick visual reference.
  st.title(f"{doc.Name}")
  # Render the theme + author + version as small caption metadata.
  st.caption(
    f"Theme: `{doc.Theme}` · Author: `{doc.Author}` · Version: `{doc.Version}`"
  )
  # Render the description as an info callout for at-a-glance context.
  if (doc.Description):
    st.info(doc.Description)
  # Render the raw SKILL.md body as Markdown.
  st.markdown(doc.Body)
  # Surface the relative file path at the bottom for quick lookup.
  st.divider()
  st.caption(f"Source: `{doc.RelativePath}`")


def RenderEmptyPanel(message: str) -> None:
  """
  Render an empty-state panel when no skill is selected.

  Args:
    message (str): The explanation to display to the user.
  """
  # Render a friendly placeholder so the panel is never blank.
  st.title("SkillStack Browser")
  st.write(message)
  # Hint at the sidebar controls so the user knows where to start.
  st.markdown(
    "Pick a theme and a skill from the sidebar, or type a search query "
    "to filter the list. Click any skill row to render its `SKILL.md`."
  )


def RenderSkillList(docs: list[SkillDoc], selectedTheme: str | None) -> None:
  """
  Render the list of selectable skills in a column on the left of the main
  panel.

  Args:
    docs (list[SkillDoc]): The filtered skill list to display.
    selectedTheme (str | None): The currently selected theme, used to
      scope the list.
  """
  # Render the column header with the live count.
  st.subheader(f"Skills ({len(docs)})")
  # Render each skill as a button the user clicks to load.
  for doc in docs:
    # Use the skill name as the button label.
    if (st.button(doc.Name, key=f"skill-{doc.Theme}-{doc.Name}", use_container_width=True)):
      # Persist the selected skill in session state for the next rerun.
      st.session_state[SessionKeySkill] = doc.Name
      st.session_state[SessionKeyTheme] = doc.Theme


def ResolveSelectedSkill(
  docs: list[SkillDoc],
  selectedTheme: str | None,
  searchQuery: str,
) -> SkillDoc | None:
  """
  Resolve the currently selected skill document from session state.

  Args:
    docs (list[SkillDoc]): The full skill list.
    selectedTheme (str | None): The currently selected theme.
    searchQuery (str): The current search query.

  Returns:
    SkillDoc | None: The skill to render, or None when nothing is
      selected.
  """
  # Apply the search filter first to narrow the candidate set.
  filtered = SearchSkills(docs, searchQuery)
  # Apply the theme filter next when the user has picked one.
  if (selectedTheme):
    filtered = [d for d in filtered if (d.Theme == selectedTheme)]
  # When the session state has no skill selected yet, default to the first.
  selectedName = st.session_state.get(SessionKeySkill)
  if (not selectedName):
    # Bail out gracefully when the filtered list is empty.
    if (not filtered):
      return None
    # Default to the first skill in the filtered list.
    return filtered[0]
  # Look up the named skill in the full list (not the filtered one) so a
  # theme switch does not blank the panel when the skill lives elsewhere.
  return FindSkillByName(SkillsRoot(), selectedName)


def Main() -> None:
  """
  Render the SkillStack browser Streamlit app.

  The layout is two-column on wide screens: the skill list on the left,
  the rendered SKILL.md on the right. On narrow screens Streamlit
  collapses the columns vertically.
  """
  # Apply page configuration once per run.
  st.set_page_config(
    page_title=PageTitle,
    page_icon=PageIcon,
    layout=PageLayout,
    initial_sidebar_state="expanded",
  )
  # Load every skill once; this is cached implicitly by Streamlit's rerun
  # semantics because the function is called at module top level below.
  docs = LoadAllSkills()
  # Render the sidebar and capture the user's theme + query selections.
  selectedTheme, searchQuery = RenderSidebar(docs)
  # Filter the skill list by the search query and theme selection.
  filtered = SearchSkills(docs, searchQuery)
  if (selectedTheme):
    filtered = [d for d in filtered if (d.Theme == selectedTheme)]
  # Two-column layout: list on the left, content on the right.
  listCol, contentCol = st.columns([1, 3])
  with listCol:
    # Render the clickable skill list.
    RenderSkillList(filtered, selectedTheme)
  with contentCol:
    # Resolve the skill to render from session state.
    doc = ResolveSelectedSkill(docs, selectedTheme, searchQuery)
    # Render either the selected skill or the empty-state panel.
    if (doc is None):
      RenderEmptyPanel(
        "No skill selected. Pick one from the list on the left, or clear "
        "the search box to see every skill."
      )
    else:
      RenderSkillPanel(doc)


if (__name__ == "__main__"):
  # Hand control to the Main function; Streamlit manages the rerun loop.
  Main()
