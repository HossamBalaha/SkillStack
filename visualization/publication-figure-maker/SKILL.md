---
name: publication-figure-maker
description: Produce journal-ready matplotlib and seaborn figures sized to exact column widths. Trigger when building figures for Nature, PRL, IEEE, or any manuscript submission, when DPI/vector format matters, or when LaTeX sizing would corrupt fonts.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [matplotlib, publication, figures, journal]
related: [visualization/figure-caption-writer, visualization/results-table-formatter, visualization/multi-panel-figure-composer]
prerequisites: []
outputs: [python, pdf, svg]
difficulty: intermediate
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Publication Figure Maker

## When To Use

- Generating a final figure for a journal submission (Nature, Science, PRL, IEEE, NeurIPS camera-ready).
- Matching a strict column width in millimetres and avoiding LaTeX-side resizing.
- Mixing vector (PDF/EPS) and raster (PNG) output formats in one pipeline.
- Ensuring font sizes survive the editorial typesetting pipeline.

## Workflow

1. Determine the target journal and its column width in millimetres.
2. Convert millimetres to inches using `ONE_MM = 1 / 25.4`.
3. Pick the minimum font size per journal policy (Nature 7pt, PRL 8pt).
4. Build the figure with `plt.subplots(figsize=..., constrained_layout=True)`.
5. Register the Chinese font plus DejaVu Sans fallback.
6. Plot data, label axes with units, and apply a journal stylesheet (SciencePlots or custom).
7. Place legends outside the axes using `bbox_to_anchor`.
8. Save vector format (PDF/EPS) for line art and PNG at 300-600 DPI for raster content.
9. Verify that the saved file is NOT resized downstream by LaTeX.

## Inputs

- Data arrays (numpy/pandas) and metadata (axis labels, units, legends).
- Journal name plus column specification (single or double column).
- Optional style sheet path (SciencePlots `.mplstyle`).

## Outputs

- One standalone figure file (PDF/EPS/PNG) per figure.
- A small JSON manifest recording journal, width, DPI, and font size for reproducibility.

## Key Rules

- ONE figure file per figure; never compose multiple figures with `\includegraphics`.
- Never let LaTeX resize via `\includegraphics[width=\textwidth]`; size in matplotlib instead.
- Use vector formats (PDF/EPS) for line plots and raster (PNG 300-600 DPI) for images/heatmaps.
- Minimum font size obeys the journal policy (Nature 7pt, PRL 8pt).
- Always use `constrained_layout=True`; do not call `plt.tight_layout()` afterwards.
- Legends must sit outside the axes via `bbox_to_anchor`.

## Examples

```python
# Publication figure sized to a PRL double column.
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Register fonts so Chinese glyphs and minus signs render correctly.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Conversion constant.
ONE_MM = 1 / 25.4.

def MakeJournalFigure(xData, yData, outputPath):
  # Size to PRL double column (178 mm) at 8 pt body text.
  widthIn = 178. * ONE_MM
  figHeight = widthIn * 0.62
  fig, ax = plt.subplots(figsize=(widthIn, figHeight), constrained_layout=True)
  # Plot the curve with a thin line for print fidelity.
  ax.plot(xData, yData, linewidth=1.0, color="#1f77b4", label="Model")
  # Label axes with units at the journal minimum size.
  ax.set_xlabel("Frequency (Hz)", fontsize=8)
  ax.set_ylabel("Amplitude (a.u.)", fontsize=8)
  # Legend placed outside so it never overlaps data.
  ax.legend(bbox_to_anchor=(1.02, 1.0), loc="upper left", fontsize=7)
  # Vector output preserves crisp strokes at any zoom level.
  fig.savefig(outputPath, format="pdf")
  fig.savefig(outputPath.replace(".pdf", ".png"), dpi=600)
  plt.close(fig)
```

## References

- SciencePlots matplotlib stylesheets: https://github.com/garrettj403/SciencePlots
- Matplotlib paper tips: https://allanchain.github.io/blog/post/mpl-paper-tips
