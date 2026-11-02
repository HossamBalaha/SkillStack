#!/usr/bin/env python3
"""
Generate the SkillStack skill dependency graph as SVG.

Builds a directed graph where nodes are skills and edges come from each
skill's ``related`` and ``prerequisites`` frontmatter fields. Nodes are
grouped by theme and colored by theme. Uses the ``graphviz`` Python
package when available; otherwise falls back to a manual SVG writer with
a simple column layout (one column per theme).

CLI:
  python scripts/graphviz_chains.py
"""

from __future__ import annotations

import argparse
import html
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _SkillLib import EnsureDir, IterateSkills, SkillDoc, SkillsRoot


# Attempt to import the graphviz Python package; degrade gracefully.
try:
  import graphviz as gv
  HasGraphviz = True
except ImportError:
  HasGraphviz = False


# Stable color palette assigned to themes in alphabetical order.
ThemePalette = [
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#bcbd22",
  "#17becf",
  "#aec7e8",
  "#ffbb78",
  "#98df8a",
  "#ff9896",
  "#c5b0d5",
  "#c49c94",
  "#f7b6d2",
  "#c7c7c7",
  "#dbdb8d",
  "#9edae5",
  "#393b79",
  "#637939",
  "#8c6d31",
  "#843c39",
  "#7b4173",
  "#bd9e39",
  "#e7969c",
  "#5254a3",
]


@dataclass
class GraphNode:
  """One node in the skill dependency graph."""

  Name: str
  Theme: str
  Color: str


@dataclass
class GraphEdge:
  """One directed edge in the skill dependency graph."""

  Source: str
  Target: str
  Kind: str  # "related" or "prerequisite"


@dataclass
class SkillGraph:
  """Aggregate graph data: nodes, edges, and theme color mapping."""

  Nodes: list[GraphNode] = field(default_factory=list)
  Edges: list[GraphEdge] = field(default_factory=list)
  ThemeColors: dict[str, str] = field(default_factory=dict)


def BuildGraph(rootPath: Path) -> SkillGraph:
  """
  Build the skill dependency graph from every skill's frontmatter.

  Args:
    rootPath (Path): The skills repository root.

  Returns:
    SkillGraph: The populated graph.
  """
  # Load every skill once to map names to docs.
  docs: list[SkillDoc] = list(IterateSkills(rootPath))
  # Build a set of known skill names for edge target validation.
  knownNames = {doc.Name for doc in docs if (doc.Name)}
  # Assign one palette color per theme in alphabetical order.
  themes = sorted({doc.Theme for doc in docs})
  themeColors = {theme: ThemePalette[index % len(ThemePalette)] for index, theme in enumerate(themes)}
  graph = SkillGraph(ThemeColors=themeColors)
  # Create one node per known skill.
  for doc in docs:
    if (not doc.Name):
      continue
    graph.Nodes.append(GraphNode(
      Name=doc.Name,
      Theme=doc.Theme,
      Color=themeColors[doc.Theme],
    ))
  # Create edges from each skill's related and prerequisites fields.
  for doc in docs:
    if (not doc.Name):
      continue
    # Add an edge for every related skill that exists in the graph.
    for related in doc.Related:
      target = str(related).split("/", 1)[-1] if ("/" in str(related)) else str(related)
      if (target in knownNames and target != doc.Name):
        graph.Edges.append(GraphEdge(Source=doc.Name, Target=target, Kind="related"))
    # Add an edge for every prerequisite skill that exists in the graph.
    for prerequisite in doc.Prerequisites:
      target = str(prerequisite).split("/", 1)[-1] if ("/" in str(prerequisite)) else str(prerequisite)
      if (target in knownNames and target != doc.Name):
        graph.Edges.append(GraphEdge(Source=doc.Name, Target=target, Kind="prerequisite"))
  return graph


def RenderWithGraphviz(graph: SkillGraph, outputPath: Path) -> Path:
  """
  Render the graph to SVG using the graphviz Python package.

  Args:
    graph (SkillGraph): The populated graph.
    outputPath (Path): Destination SVG file path.

  Returns:
    Path: The destination SVG file path.
  """
  # Create a directed graph with left-to-right layout.
  dot = gv.Digraph("SkillStack", format="svg")
  dot.attr(rankdir="LR", bgcolor="white", fontname="Helvetica")
  dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="10")
  dot.attr("edge", fontname="Helvetica", fontsize="9")
  # Add one cluster per theme for visual grouping.
  themes = sorted(graph.ThemeColors.keys())
  for theme in themes:
    with dot.subgraph(name=f"cluster_{theme}") as cluster:
      cluster.attr(label=theme, color=graph.ThemeColors[theme], style="rounded")
      # Add nodes belonging to this theme.
      for node in graph.Nodes:
        if (node.Theme == theme):
          cluster.node(node.Name, label=node.Name, fillcolor=node.Color, fontcolor="white")
  # Add edges after all nodes have been declared.
  for edge in graph.Edges:
    # Use a dashed line for related and a solid arrow for prerequisites.
    style = "dashed" if (edge.Kind == "related") else "solid"
    dot.edge(edge.Source, edge.Target, label=edge.Kind, style=style, color="#666666")
  # Ensure the parent directory exists before rendering.
  EnsureDir(outputPath.parent)
  # Render the graph to disk without opening it.
  renderedPath = dot.render(filename=str(outputPath.with_suffix("")), cleanup=True)
  return Path(renderedPath)


def RenderManualSvg(graph: SkillGraph, outputPath: Path) -> Path:
  """
  Render the graph to SVG manually using a column-per-theme layout.

  Args:
    graph (SkillGraph): The populated graph.
    outputPath (Path): Destination SVG file path.

  Returns:
    Path: The destination SVG file path.
  """
  # Group nodes by theme in alphabetical order.
  themes = sorted(graph.ThemeColors.keys())
  nodesByTheme: dict[str, list[GraphNode]] = {theme: [] for theme in themes}
  for node in graph.Nodes:
    nodesByTheme[node.Theme].append(node)
  # Sort nodes within each theme alphabetically.
  for theme in themes:
    nodesByTheme[theme].sort(key=lambda n: n.Name)
  # Compute canvas dimensions based on the tallest column.
  columnWidth = 240
  rowHeight = 36
  padding = 24
  headerHeight = 28
  maxRows = max((len(nodesByTheme[t]) for t in themes), default=1)
  canvasWidth = padding * 2 + columnWidth * len(themes)
  canvasHeight = padding * 2 + headerHeight + rowHeight * maxRows
  # Build a lookup from skill name to (x, y) center for edge routing.
  positions: dict[str, tuple[float, float]] = {}
  for columnIndex, theme in enumerate(themes):
    x = padding + columnIndex * columnWidth + columnWidth / 2
    for rowIndex, node in enumerate(nodesByTheme[theme]):
      y = padding + headerHeight + rowIndex * rowHeight + rowHeight / 2
      positions[node.Name] = (x, y)
  # Compose the SVG document as a list of strings.
  parts = []
  parts.append(f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{canvasWidth}\" height=\"{canvasHeight}\" viewBox=\"0 0 {canvasWidth} {canvasHeight}\">")
  parts.append("<style>")
  parts.append(".node { font-family: Helvetica, Arial, sans-serif; font-size: 11px; }")
  parts.append(".theme { font-family: Helvetica, Arial, sans-serif; font-size: 13px; font-weight: bold; }")
  parts.append(".edge { stroke: #666666; stroke-width: 1px; fill: none; }")
  parts.append(".edge-related { stroke-dasharray: 4 2; }")
  parts.append(".edge-label { font-family: Helvetica, Arial, sans-serif; font-size: 9px; fill: #888888; }")
  parts.append("</style>")
  # Draw one theme header per column.
  for columnIndex, theme in enumerate(themes):
    x = padding + columnIndex * columnWidth + columnWidth / 2
    parts.append(f"<text class=\"theme\" x=\"{x:.0f}\" y=\"{padding + 16:.0f}\" text-anchor=\"middle\" fill=\"{graph.ThemeColors[theme]}\">{html.escape(theme)}</text>")
  # Draw each node as a colored rectangle with a label.
  for theme in themes:
    color = graph.ThemeColors[theme]
    for node in nodesByTheme[theme]:
      x, y = positions[node.Name]
      rectX = x - 80
      rectY = y - 12
      parts.append(f"<rect class=\"node\" x=\"{rectX:.0f}\" y=\"{rectY:.0f}\" width=\"160\" height=\"24\" rx=\"4\" ry=\"4\" fill=\"{color}\" stroke=\"#333333\" stroke-width=\"1\"/>")
      parts.append(f"<text class=\"node\" x=\"{x:.0f}\" y=\"{y + 4:.0f}\" text-anchor=\"middle\" fill=\"white\">{html.escape(node.Name)}</text>")
  # Draw each edge as a straight line between node centers.
  for edge in graph.Edges:
    src = positions.get(edge.Source)
    dst = positions.get(edge.Target)
    if (src is None or dst is None):
      continue
    cls = "edge edge-related" if (edge.Kind == "related") else "edge"
    parts.append(f"<line class=\"{cls}\" x1=\"{src[0]:.0f}\" y1=\"{src[1]:.0f}\" x2=\"{dst[0]:.0f}\" y2=\"{dst[1]:.0f}\"/>")
    # Place a tiny label at the midpoint of the edge.
    midX = (src[0] + dst[0]) / 2
    midY = (src[1] + dst[1]) / 2
    parts.append(f"<text class=\"edge-label\" x=\"{midX:.0f}\" y=\"{midY - 2:.0f}\" text-anchor=\"middle\">{html.escape(edge.Kind)}</text>")
  parts.append("</svg>")
  # Ensure the parent directory exists before writing.
  EnsureDir(outputPath.parent)
  outputPath.write_text("\n".join(parts), encoding="utf-8")
  return outputPath


def RenderSvg(graph: SkillGraph, outputPath: Path) -> Path:
  """
  Render the graph using graphviz when available, else manual SVG.

  Args:
    graph (SkillGraph): The populated graph.
    outputPath (Path): Destination SVG file path.

  Returns:
    Path: The destination SVG file path.
  """
  # Pick the renderer based on graphviz availability.
  if (HasGraphviz):
    return RenderWithGraphviz(graph, outputPath)
  return RenderManualSvg(graph, outputPath)


def ParseArgs(argv: list[str] | None = None) -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(
    description="Generate docs/skill-graph.svg showing skill dependency chains.",
  )
  parser.add_argument(
    "--root",
    default=str(SkillsRoot()),
    help="Path to the skills repository root (default: auto-detected).",
  )
  parser.add_argument(
    "--output",
    default=str(SkillsRoot() / "docs" / "skill-graph.svg"),
    help="Destination SVG path (default: <root>/docs/skill-graph.svg).",
  )
  return parser.parse_args(argv)


def Main(argv: list[str] | None = None) -> int:
  """
  Entry point for the skill graph generator.

  Args:
    argv (list[str] | None): Optional argv override for tests.

  Returns:
    int: Process exit code; always zero on success.
  """
  args = ParseArgs(argv)
  rootPath = Path(args.root).resolve()
  outputPath = Path(args.output).resolve()
  console = Console()
  # Build the skill dependency graph from parsed skill documents.
  graph = BuildGraph(rootPath)
  # Render the graph to SVG.
  finalPath = RenderSvg(graph, outputPath)
  renderer = "graphviz" if (HasGraphviz) else "manual-svg"
  console.print(
    f"[green]wrote[/green] {finalPath} "
    f"({len(graph.Nodes)} nodes, {len(graph.Edges)} edges, renderer={renderer})"
  )
  return 0


if (__name__ == "__main__"):
  sys.exit(Main())
