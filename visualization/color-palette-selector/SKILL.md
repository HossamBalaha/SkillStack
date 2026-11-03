---
name: color-palette-selector
description: Select colourblind-friendly palettes (viridis, cividis, ColorBrewer, Wong's palette) and verify them with simulators. Trigger when choosing colours for figures, dashboards, or diagrams that must be readable by viewers with colour vision deficiencies.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [color, palette, colorblind, viridis, accessibility]
related: [visualization/publication-figure-maker, visualization/dashboard-builder]
prerequisites: []
outputs: [python]
difficulty: beginner
estimated_tokens: 1000
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Color Palette Selector

## When To Use

- Choosing a colour scheme for a paper figure or dashboard.
- Encoding categorical labels without relying on red/green pairs.
- Building sequential or diverging maps for heatmaps.
- Validating that a palette survives colourblind simulation.

## Workflow

1. Decide whether the data is categorical, sequential, or diverging.
2. For categorical, prefer Wong's palette or ColorBrewer qualitative.
3. For sequential or diverging, prefer viridis, cividis, or ColorBrewer.
4. Cap the categorical count at eight; switch to a lightness gradient above that.
5. Avoid red/green encoding that fails deuteranopia and protanopia.
6. Run the palette through a simulator (Coblis or similar) to verify.
7. Lock the palette in a project config so figures stay consistent.

## Inputs

- Data kind: categorical, sequential, or diverging.
- Number of distinct colours required.
- Optional brand constraints (forbidden colours, contrast target).

## Outputs

- A palette definition file (JSON) with hex codes and names.
- A PNG swatch preview plus a simulated colourblind preview.
- A matplotlib snippet registering the palette as a custom cmap.

## Key Rules

- Never use red and green as the sole encoding pair.
- Categorical palettes cap at eight distinct colours.
- Prefer perceptually uniform maps (viridis, cividis) for sequential data.
- For more than eight categories, switch to a lightness gradient.
- Validate every palette with a colourblind simulator.
- Register the chosen palette once and reuse across figures.

## Examples

```python
# Define Wong's palette and validate it for colourblind safety.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import ListedColormap

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

WONG_PALETTE = [
  "#000000", "#E69F00", "#56B4E9", "#009E73",
  "#F0E442", "#0072B2", "#D55E00", "#CC79A7"
]

def RegisterWongCmap(name="wong"):
  # Register Wong's palette as a discrete matplotlib cmap.
  cmap = ListedColormap(WONG_PALETTE, name=name)
  # Register only if not already present.
  if (name not in plt.colormaps()):
    plt.register_cmap(name=name, cmap=cmap)
  return cmap

def ValidatePalette(palette):
  # Simulate deuteranopia by removing the red-green channel contrast.
  rgb = [plt.matplotlib.colors.to_rgb(c) for c in palette]
  grey = [0.299 * r + 0.587 * g + 0.114 * b for (r, g, b) in rgb]
  # If any two greys are too close, the palette is unsafe.
  for (i) in range(len(grey)):
    for (j) in range(i + 1, len(grey)):
      if (abs(grey[i] - grey[j]) < 0.05):
        return False
  return True

def PlotSwatch(palette, outputPath):
  # Render a swatch strip for documentation.
  fig, ax = plt.subplots(figsize=(3.5, 0.6), constrained_layout=True)
  for (i, color) in enumerate(palette):
    ax.bar(i, 1.0, color=color)
  ax.set_xticks(range(len(palette)))
  ax.set_xticklabels([str(i) for i in range(len(palette))], fontsize=7)
  ax.set_yticks([])
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```
