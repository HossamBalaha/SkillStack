---
name: surface-plotter
description: Plot 3D surfaces with proper view angles, colourbars, and a 2D contour overlay for loss landscapes. Trigger when visualising loss landscapes, response surfaces, or any scalar field over two variables.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [3d, surface, contour, loss-landscape, matplotlib]
related: [visualization/training-curve-visualizer, visualization/publication-figure-maker]
prerequisites: []
outputs: [python, svg, pdf]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Surface Plotter

## When To Use

- Visualising a loss landscape over two parameters.
- Plotting a response surface from a DOE study.
- Inspecting a 2-D scalar field with height and colour.
- Producing both a 3-D surface and a 2-D contour for a paper.

## Workflow

1. Build a meshgrid from the two parameter axes.
2. Evaluate the scalar field on the grid to get `Z`.
3. Create a 3-D axis with `mpl_toolkits.mplot3d.Axes3D`.
4. Plot the surface with `ax.plot_surface(X, Y, Z, cmap="viridis")`.
5. Set the view angle via `ax.view_init(elev=30, azim=45)`.
6. Add a colourbar and label axes with units.
7. Produce a 2-D contour overlay for the same field.
8. Save both views as PDF for the manuscript.

## Inputs

- Two 1-D arrays `x` and `y` defining the grid.
- A callable `Z = f(x, y)` or a precomputed 2-D array.
- Axis labels with units and an optional colourbar label.

## Outputs

- A PDF with the 3-D surface.
- A PDF with the 2-D contour overlay.
- A JSON record of the view angle and colour map for reproducibility.

## Key Rules

- Use `ax.view_init(elev=30, azim=45)` as the default camera.
- Always include a colourbar labelled with the quantity and units.
- Label axes with units, not bare variable names.
- Produce a 2-D contour overlay for loss landscapes.
- Keep `constrained_layout=True` so the colourbar fits.
- Use `cmap="viridis"` or another perceptually uniform map.

## Examples

```python
# Plot a 3-D surface and a 2-D contour for the same field.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d import Axes3D

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def PlotSurface(x, y, zFunc, outputPath):
  # Build a meshgrid and evaluate the field.
  X, Y = np.meshgrid(x, y)
  Z = zFunc(X, Y)
  fig = plt.figure(figsize=(6.8, 3.2), constrained_layout=True)
  # Left panel: 3-D surface.
  ax3d = fig.add_subplot(1, 2, 1, projection="3d")
  surf = ax3d.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
  ax3d.view_init(elev=30, azim=45)
  ax3d.set_xlabel("Parameter A (a.u.)")
  ax3d.set_ylabel("Parameter B (a.u.)")
  ax3d.set_zlabel("Loss")
  # Right panel: 2-D contour overlay.
  ax2d = fig.add_subplot(1, 2, 2)
  cf = ax2d.contourf(X, Y, Z, levels=20, cmap="viridis")
  ax2d.set_xlabel("Parameter A (a.u.)")
  ax2d.set_ylabel("Parameter B (a.u.)")
  # Shared colourbar placed outside the axes.
  cbar = fig.colorbar(cf, ax=ax2d, shrink=0.8)
  cbar.set_label("Loss")
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```
