---
name: academic-plotting-pipeline
description: Route academic figures into the correct rendering track (matplotlib for numerical data, diagrams for boxes-and-arrows). Trigger when building a complete paper figure suite, ablation charts, confusion matrices, or system diagrams.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: visualization
tags: [matplotlib, academic, figures, pipeline, routing]
related: [visualization/publication-figure-maker, visualization/confusion-matrix-plotter]
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

# Academic Plotting Pipeline

## When To Use
- Producing the full figure set for a research paper in one consistent pass.
- Selecting the right chart type from a data shape (curve, matrix, ablation table).
- Separating system diagrams from data plots so each uses the best tool.
- Auto-dispatching figure generation from a single metadata file.

## Workflow
1. Read a figure manifest listing every figure in the paper.
2. Classify each figure as `data` or `diagram` based on whether axes are numerical.
3. For `data` figures, inspect the array shape to pick line, bar, scatter, or heatmap.
4. For `diagram` figures, hand off to TikZ or image-generation tooling.
5. Render data figures with matplotlib/seaborn using the publication setup.
6. Render diagrams with the TikZ framework diagrammer or a vector tool.
7. Write each artifact to the paper's `figures/` directory.
8. Emit a LaTeX `\input{}` file that lists every figure for the manuscript.

## Inputs
- A figure manifest (JSON/YAML) mapping figure IDs to type, data path, and caption.
- Data files (CSV, NPZ, parquet) and a labels dictionary.
- Style configuration (journal, font sizes, palette).

## Outputs
- Per-figure PDF/PNG files under `figures/`.
- A `figures.tex` include file for the manuscript.
- A log mapping each figure ID to the renderer chosen.

## Key Rules
- If the figure has numerical axes, use matplotlib/seaborn.
- If the figure is boxes plus arrows, use TikZ or diagram tooling.
- Training curves always render as line plots.
- Confusion matrices always render as heatmaps.
- Ablation tables render as grouped bar charts when shown graphically.
- Keep one renderer per figure; never mix matplotlib and TikZ in one file.

## Examples
```python
# Pick a renderer from the shape of the data array.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def SelectChartType(dataArray):
  # Decide chart family from array rank and intent.
  shape = np.asarray(dataArray).shape
  if (len(shape) == 1):
    return "line"
  if (len(shape) == 2 and shape[0] == shape[1]):
    return "heatmap"
  if (len(shape) == 2):
    return "grouped_bar"
  return "scatter"

def RenderDataFigure(dataArray, outputPath):
  # Dispatch to the right matplotlib routine.
  chart = SelectChartType(dataArray)
  fig, ax = plt.subplots(figsize=(3.35, 2.6), constrained_layout=True)
  if (chart == "heatmap"):
    sns.heatmap(dataArray, annot=True, fmt="d", cmap="Blues", ax=ax)
  elif (chart == "line"):
    ax.plot(dataArray, linewidth=1.0)
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```

## References
- AI-Research-SKILLs plotting recipes: https://github.com/Orchestra-Research/AI-Research-SKILLs
