---
name: executive-dashboard-designer
description: Design executive dashboards that surface the right KPI hierarchy, encode state with restrained colour, annotate thresholds, and offer drill-down paths that hold up on mobile. Use when the user is building a leadership-facing dashboard, fixing a cluttered KPI wall, or wiring annotations and drill-downs into a Streamlit, Dash, or Power BI view.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [dashboard, kpi, executive, drill-down, mobile-responsive]
related: [data-storytelling/data-annotation-writer, data-storytelling/audience-tailor, visualization/dashboard-builder]
prerequisites: []
outputs: [python, html, yaml, markdown]
difficulty: intermediate
estimated_tokens: 1450
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Executive Dashboard Designer

## When To Use

- The user says "build me a leadership dashboard" or "fix my KPI wall".
- An existing dashboard has too many tiles, no thresholds, and executives cannot find the action.
- The user must add drill-down paths from a headline number to its drivers.
- The dashboard has to stay readable on a phone or a tablet.
- Trigger keywords: executive dashboard, KPI hierarchy, drill-down, threshold, mobile.

## Workflow

1. List the three to five questions an executive will ask at 7 a.m. and at 4 p.m.; each becomes a tile.
2. Build a KPI tree: a single north-star metric, two to three driver metrics, and supporting detail.
3. For each metric, define the target, the alert threshold, and the comparison baseline (last week, last year).
4. Map colour to state only: green for on-track, amber for watch, red for breach; no decorative colour.
5. Place KPI cards top-left, supporting charts below, and drill-down tables reachable via click-through.
6. Annotate every chart with the threshold line and a one-line caption naming the action it implies.
7. Wire drill-down: click a KPI card to filter the charts to that segment and reveal the next layer.
8. Verify on a 360-pixel-wide viewport: cards stack, fonts stay above 14 pt, no horizontal scroll.
9. Add a "last refreshed" stamp and a data-quality flag tied to the ingestion job.
10. Smoke-test the alert state by injecting a breach value and confirming the colour flips.

## Inputs

- Metric definitions with formulas and data source columns.
- Targets, alert thresholds, and comparison baselines per metric.
- Audience device mix (mobile share, tablet share, desktop share).
- Available dashboard framework (Streamlit, Dash, Gradio, Power BI, Tableau).

## Outputs

- `dashboard_spec.yaml` — KPI tree, thresholds, drill-down map, colour rules.
- `app.py` — Streamlit or Dash skeleton wired to the spec.
- `kpi_cards.html` — standalone card components for embedding.
- `annotation_layer.md` — captions and threshold lines per chart.
- `mobile_qa_checklist.md` — viewport, font, and scroll checks.

## Key Rules

- A dashboard answers questions; it does not display data. Every tile ties to a question.
- Colour encodes state, never decoration; reserve red for breaches only.
- Maximum five KPI cards above the fold; everything else is a drill-down.
- Every chart has a one-line caption naming the action it implies.
- Targets and thresholds are visible on the chart, not hidden in a tooltip.
- Mobile layout is designed first, then scaled up; desktop is not the default.
- "Last refreshed" stamp is mandatory; stale data is worse than no data.

## Examples

```python
# Streamlit executive dashboard: KPI cards with state colour + drill-down.
import pandas as pd
import streamlit as st

STATE_COLOUR = {"on-track": "#1a7f37", "watch": "#bf8700", "breach": "#cf222e"}

def StateFor(value, target, watchPct, breachPct):
  ratio = value / target
  if (ratio < breachPct):
    return "breach"
  if (ratio < watchPct):
    return "watch"
  return "on-track"

def BuildCards(kpiFrame):
  cols = st.columns(len(kpiFrame))
  for (i, row) in kpiFrame.iterrows():
    state = StateFor(row["value"], row["target"], row["watch"], row["breach"])
    with cols[i]:
      st.metric(row["name"], f"{row['value']:,.0f}", delta=f"{row['delta']:+.1%}")
      st.markdown(
        f'<div style="height:6px;background:{STATE_COLOUR[state]};border-radius:3px"></div>',
        unsafe_allow_html=True,
      )
      if (st.button("Drill down", key=row["name"])):
        st.session_state["drill"] = row["name"]
```

```yaml
# dashboard_spec.yaml (excerpt)
north_star: monthly_recurring_revenue
drivers: [new_logos, expansion, churn]
cards:
  - name: MRR
    target: 1200000
    watch: 0.95
    breach: 0.90
    drill_down: segments/mrr_by_plan.csv
  - name: Churn
    target: 0.020
    watch: 1.05
    breach: 1.15
    drill_down: segments/churn_by_cohort.csv
```
