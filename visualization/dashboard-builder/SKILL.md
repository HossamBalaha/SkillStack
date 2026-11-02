---
name: dashboard-builder
description: Build interactive dashboards with Streamlit, Dash, or Gradio, featuring sidebar controls, metric cards, charts, and real-time callbacks. Trigger when prototyping an ML demo, sharing model results with stakeholders, or building an internal analytics tool.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: visualization
tags: [streamlit, dash, gradio, dashboard]
related: [visualization/interactive-plot-builder]
prerequisites: []
outputs: [python, html]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Dashboard Builder

## When To Use
- Prototyping an ML model demo for stakeholders.
- Sharing interactive results internally without a front-end team.
- Building an analytics view over a dataset with live filters.
- Comparing Streamlit, Dash, or Gradio for a new project.

## Workflow
1. Choose the framework: Streamlit (Python-native, quick), Dash (Plotly, control), or Gradio (ML demos).
2. Define the layout: sidebar controls, metric cards, charts, and a data table.
3. Wire callbacks so controls refresh the charts without a full page reload.
4. Cache expensive computations so the dashboard stays responsive.
5. Style with a consistent palette and spacing system.
6. Deploy as a local app or containerise for cloud hosting.
7. Smoke-test every control path before sharing the link.

## Inputs
- A dataset (CSV/parquet) or a model artefact.
- A specification of controls (sliders, dropdowns, file uploaders).
- A list of metric cards and charts to render.

## Outputs
- A runnable Python app (`app.py`) plus a requirements file.
- A container image spec when cloud deployment is required.
- A short README describing how to launch the dashboard.

## Key Rules
- Sidebar holds controls; the main area holds metrics, charts, and tables.
- Use framework caching for expensive computations.
- Every control must drive a callback; no dead widgets.
- Keep metric cards on a single row above the charts.
- Limit charts to three or four per page for responsiveness.
- Choose Streamlit for speed, Dash for control, Gradio for ML demos.

## Examples
```python
# Streamlit dashboard with sidebar controls and metric cards.
import pandas as pd
import streamlit as st

@st.cache_data
def LoadData(path):
  # Cache the dataset load so reruns are instant.
  return pd.read_csv(path)

def BuildApp(dataPath):
  st.set_page_config(page_title="Model Dashboard", layout="wide")
  df = LoadData(dataPath)
  # Sidebar controls.
  with st.sidebar:
    dataset = st.selectbox("Dataset", df["dataset"].unique())
    topK = st.slider("Top-K", 1, 20, 5)
  # Metric cards across the top.
  filtered = df[df["dataset"] == dataset].nlargest(topK, "accuracy")
  cols = st.columns(3)
  cols[0].metric("Rows", len(filtered))
  cols[1].metric("Best Acc", f"{filtered['accuracy'].max():.3f}")
  cols[2].metric("Mean Acc", f"{filtered['accuracy'].mean():.3f}")
  # Charts and a data table below the cards.
  st.bar_chart(filtered.set_index("model")["accuracy"])
  st.dataframe(filtered, use_container_width=True)

if (__name__ == "__main__"):
  BuildApp("results.csv")
```

## References
- Streamlit docs: https://streamlit.io
- Dash docs: https://dash.plotly.com
- Gradio docs: https://gradio.app
