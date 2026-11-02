---
name: multi-panel-figure-composer
description: Compose multi-panel matplotlib figures with shared axes, panel labels (a), (b), (c), and constrained layout. Trigger when combining several subplots into a single publication figure, sharing axes, or labelling panels for a paper.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: visualization
tags: [matplotlib, multi-panel, subplots, publication, panel-labels]
related: [visualization/publication-figure-maker, visualization/figure-caption-writer]
prerequisites: []
outputs: [python, pdf, svg]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Multi-Panel Figure Composer

## When To Use
- Combining several subplots into one publication figure.
- Sharing x or y axes across panels to ease comparison.
- Labelling panels with (a), (b), (c) for cross-reference.
- Laying out an ablation grid or a results-at-a-glance view.

## Workflow
1. Decide the grid size (`nrows`, `ncols`) from the number of panels.
2. Create the figure with `plt.subplots(nrows, ncols, figsize=..., constrained_layout=True)`.
3. Set `sharex=True` and/or `sharey=True` when axes are comparable.
4. Plot each panel and apply consistent axis labels.
5. Add panel labels via `ax.text(-0.1, 1.05, "(a)", transform=ax.transAxes)`.
6. Hide redundant tick labels on shared inner axes.
7. Place legends outside the axes via `bbox_to_anchor`.
8. Save as PDF for the manuscript.

## Inputs
- A list of plotting callables, one per panel.
- The grid shape and shared-axis flags.
- A figure size matching the target journal column.

## Outputs
- A single PDF/PNG containing every panel.
- A LaTeX caption referencing each panel label.
- A small JSON manifest recording the grid and labels.

## Key Rules
- Use `constrained_layout=True`; never combine with `tight_layout()`.
- Share axes with `sharex` and `sharey` when scales are comparable.
- Panel labels use `ax.text(-0.1, 1.05, "(a)", transform=ax.transAxes)`.
- Hide redundant inner tick labels on shared axes.
- Legends sit outside the axes via `bbox_to_anchor`.
- One combined caption is acceptable; each panel may also have its own.

## Examples
```python
# Compose a two-by-two multi-panel figure with shared axes and labels.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def AddPanelLabel(ax, label):
  # Place a panel label in the upper-left of the axes.
  ax.text(-0.1, 1.05, label, transform=ax.transAxes,
          fontsize=10, fontweight="bold", va="bottom", ha="right")

def ComposeFigure(panels, outputPath):
  # panels is a 2x2 list of callables: f(ax) -> None.
  fig, axes = plt.subplots(2, 2, figsize=(6.8, 5.2),
                           sharex=True, sharey=True,
                           constrained_layout=True)
  labels = [["(a)", "(b)"], ["(c)", "(d)"]]
  for (i) in range(2):
    for (j) in range(2):
      ax = axes[i][j]
      panels[i][j](ax)
      AddPanelLabel(ax, labels[i][j])
      # Hide inner tick labels on shared axes.
      if (i < 1):
        ax.set_xticklabels([])
      if (j > 0):
        ax.set_yticklabels([])
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```

## References
- matplotlib subplots docs: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
- matplotlib constrained_layout guide: https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html
