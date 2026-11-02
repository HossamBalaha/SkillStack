---
name: tikz-framework-diagrammer
description: Build publication-ready TikZ pipeline diagrams with solid grouping boxes, concise node labels, and explicit anchor connections. Trigger when drawing system architectures, data-flow pipelines, or workflow diagrams for a LaTeX manuscript.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [tikz, latex, diagrams, architecture]
related: [visualization/publication-figure-maker, academic-research/journal-manuscript-writer]
prerequisites: [style-integrity/latex-style-guard]
outputs: [latex]
difficulty: advanced
estimated_tokens: 2100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# TikZ Framework Diagrammer

## When To Use

- Drawing a system architecture or data-flow pipeline for a paper.
- Producing a workflow diagram that must scale to a column width.
- Composing a multi-stage framework where each stage has sub-blocks.
- Embedding the figure as native LaTeX so the fonts match the body text.
- Reusing the same diagram in slides, posters, and the manuscript.

## Workflow

1. List every pipeline stage and the blocks inside each stage.
2. Assign a short identifier per block (for example, `Conv2D, k=3`).
3. Choose a subtle colour per stage from a perceptually uniform palette.
4. Lay out nodes on a grid with generous horizontal and vertical spacing.
5. Wrap each stage in a solid grouping box (never dashed).
6. Connect blocks with arrows anchored explicitly via `.east` and `.west`.
7. Wrap the full diagram in `\resizebox{\linewidth}{!}{...}`.
8. Compile to PDF and verify node text stays legible at column width.
9. Check that the compiled PDF uses the same font family as the body text.

## Inputs

- A pipeline specification listing stages, blocks, and connections.
- A colour palette mapping stage names to fills.
- Optional caption text for the figure environment.

## Outputs

- A `.tex` file containing a `tikzpicture` environment.
- A compiled PDF preview for the manuscript.
- A standalone `.tex` for reuse in slides or posters.

## Key Rules

- Node labels must be concise identifiers, never dense math formulations.
- Grouping boxes use SOLID lines; never dashed.
- Every arrow uses explicit anchors (`.east`, `.west`, `.north`, `.south`).
- Reserve subtle colour coding for pipeline stages, not for emphasis.
- Wrap the whole picture in `\resizebox{\linewidth}{!}{...}`.
- Keep padding generous; never let boxes touch arrows or text.

## Examples

```latex
% TikZ pipeline diagram with solid grouping boxes.
\documentclass[tikz,border=2mm]{standalone}
\usetikzlibrary{positioning,arrows.meta,fit,backgrounds}
\begin{document}
\begin{tikzpicture}[
  font=\small,
  block/.style={draw, rounded corners, fill=stageblue!15,
                minimum width=18mm, minimum height=8mm, inner sep=2mm},
  group/.style={draw, solid, rounded corners, inner sep=3mm},
  >={Stealth[length=2mm]}
]
  % Stage one: feature extraction.
  \node[block] (conv) {Conv2D, $k=3$};
  \node[block, right=8mm of conv] (pool) {MaxPool, $2\times2$};
  % Stage two: classification head.
  \node[block, right=12mm of pool] (fc) {FC, $d=128$};
  \node[block, right=8mm of fc] (sm) {Softmax};
  % Explicit anchor connections keep arrows tidy.
  \draw[->] (conv.east) -- (pool.west);
  \draw[->] (pool.east) -- (fc.west);
  \draw[->] (fc.east) -- (sm.west);
  % Solid grouping boxes around each stage.
  \begin{scope}[on background layer]
    \node[group, fit=(conv) (pool), fill=stageblue!5] {};
    \node[group, fit=(fc) (sm),   fill=stageorange!5] {};
  \end{scope}
\end{tikzpicture}
\end{document}
```

## References

- TikZ & PGF manual: https://ctan.org/pkg/pgf
