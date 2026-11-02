---
name: interactive-plot-builder
description: Build interactive plots with hover, zoom, and click using Plotly, Bokeh, or Holoviews/Datashader. Trigger when embedding interactive visuals in dashboards, reports, or notebooks, or when datasets are too large for static matplotlib.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [plotly, bokeh, holoviews, interactive, datashader]
related: [visualization/dashboard-builder, visualization/embedding-projector]
prerequisites: []
outputs: [python, html]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Interactive Plot Builder

## When To Use

- Adding hover tooltips and zoom to a chart for exploration.
- Embedding a chart in a dashboard or HTML report.
- Rendering large datasets where matplotlib would choke.
- Producing a self-contained HTML artefact for sharing.

## Workflow

1. Pick the library: Plotly (hover, zoom, click), Bokeh (server-backed), or Holoviews/Datashader (large data).
2. Build the figure object with the chosen library.
3. Configure tooltips, axis labels, and colour scales.
4. If data is large, aggregate with Datashader before rendering.
5. Export as a standalone HTML file.
6. Optionally embed the HTML in a dashboard or report.
7. Smoke-test that interactivity works in a plain browser (no server needed).

## Inputs

- Data frame or arrays plus column metadata for tooltips.
- A library choice and an interaction feature list.
- An optional theme colour palette.

## Outputs

- A standalone HTML file containing the interactive plot.
- A PNG export for static fallback when requested.
- A small snippet to embed the HTML in a parent page.

## Key Rules

- Export as standalone HTML so no server is required to view it.
- Configure tooltips for every meaningful data column.
- Aggregate with Datashader when rows exceed roughly 100k.
- Keep colour scales colourblind-friendly.
- Embed via iframe when dropping the HTML into a larger page.
- Test in a vanilla browser without extra dependencies.

## Examples

```python
# Build a Plotly scatter with custom tooltips and export HTML.
import plotly.express as px
import pandas as pd

def BuildScatter(df, outputPath):
  # Plotly express gives hover, zoom, and pan out of the box.
  fig = px.scatter(
    df,
    x="FeatureA",
    y="FeatureB",
    color="Label",
    hover_data=["SampleId", "Score"],
    title="Interactive scatter",
    color_discrete_sequence=px.colors.qualitative.Safe
  )
  # Tidy layout and font sizes for embedding.
  fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(x=1.02, y=1.0)
  )
  # Standalone HTML means anyone can open it in a browser.
  fig.write_html(outputPath, include_plotlyjs="cdn")

def BuildLargeScatter(df, outputPath):
  # For large data, aggregate with Datashader first.
  import datashader as ds
  import datashader.transfer_functions as tf
  cvs = ds.Canvas(plot_width=800, plot_height=600)
  agg = cvs.points(df, x="FeatureA", y="FeatureB")
  img = tf.shade(agg, cmap=["white", "#1f77b4"])
  img.to_pil().save(outputPath)
```

## References

- Plotly Python docs: https://plotly.com/python/
- Bokeh docs: https://docs.bokeh.org/
- Datashader docs: https://datashader.org/
