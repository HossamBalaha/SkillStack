---
name: data-annotation-writer
description: Write chart annotations that highlight the right data points, add contextual labels, draw narrative arrows, and place callouts so a reader lands the finding without the prose. Use when the user must annotate a chart for a report, a slide, or an article and the annotation, not the legend, has to carry the meaning.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [annotation, callout, contextual-label, narrative-arrow, chart-craft]
related: [data-storytelling/narrative-arc-designer, visualization/figure-caption-writer, visualization/publication-figure-maker]
prerequisites: []
outputs: [python, svg, markdown]
difficulty: beginner
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Data Annotation Writer

## When To Use

- The user says "annotate this chart" or "make the finding pop on the figure".
- A chart currently relies on its caption to make the point and the reader skims past it.
- The user needs arrows, labels, or callouts that direct the eye to the surprise.
- The chart is going into a slide or an article where prose cannot follow every reader.
- Trigger keywords: annotation, callout, contextual label, narrative arrow, highlight.

## Workflow

1. Read the chart and write the one-sentence finding the annotation must deliver.
2. Identify the data point or region that proves the finding; that is the anchor.
3. Choose an annotation style: direct label, leader line, callout box, or shaded region.
4. Write a short label (five to ten words) that states what the reader is looking at.
5. Add a narrative arrow only when direction matters (trend, before/after, deviation).
6. Place a reference line when a threshold, target, or baseline clarifies the finding.
7. Tone down the rest of the chart so the annotation wins the eye: mute colours, thin axes.
8. Verify the annotation does not overlap data; if it does, move the label, not the data.
9. Emit a Python annotation script (matplotlib or Plotly) and a Markdown annotation brief.

## Inputs

- The chart (PNG, SVG, or matplotlib script) and the dataset behind it.
- The single finding the annotation must deliver.
- Optional: target line, baseline, or comparison region.

## Outputs

- `annotate.py` — matplotlib or Plotly script that overlays the annotation.
- `annotated_chart.svg` — vector output for embedding.
- `annotation_brief.md` — per-annotation label, anchor, and rationale.

## Key Rules

- Every annotation delivers one finding in five to ten words; longer is prose, not a label.
- Annotation wins the eye: surrounding data is muted, axes are thin.
- Leader lines point precisely at the anchor, not at a region.
- Reference lines are labelled at the right edge with the value and the unit.
- Callout boxes do not cover data; if they would, use a leader line to place them outside.
- Narrative arrows carry direction only when direction is part of the finding.
- Annotations replace the legend where possible; direct labels beat colour keys.

## Examples

```python
# matplotlib annotation: highlight a spike with a callout and a target line.
import matplotlib.pyplot as plt

def AnnotateSpike(ax, xSpike, ySpike, targetY, label):
  ax.axhline(targetY, color="#999", linestyle="--", linewidth=1)
  ax.text(ax.get_xlim()[1], targetY, f" target {targetY}",
          va="center", ha="left", color="#666", fontsize=9)
  ax.annotate(
    label,
    xy=(xSpike, ySpike),
    xytext=(xSpike + 1, ySpike + 20),
    fontsize=11, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#cf222e", lw=1.5),
  )
  ax.spines[["top", "right"]].set_visible(False)

fig, ax = plt.subplots(figsize=(8, 4.5))
# (plot calls elided)
AnnotateSpike(ax, xSpike=2, ySpike=232, targetY=120,
              label="Q2 spike: 2x target, post-protocol gap")
fig.savefig("annotated_chart.svg", bbox_inches="tight")
```

```text
Annotation brief (excerpt):
- Anchor: 2024-Q2 bar, value 232 readmissions.
- Label: "Q2 spike: 2x target, post-protocol gap".
- Style: callout with leader arrow, colour #cf222e.
- Reference line: dashed at y=120, labelled "target 120".
- Rationale: target line shows breach magnitude; callout names the cause.
```

## References

- Tufte, E. R. (2001). The Visual Display of Quantitative Information, 2nd ed. Graphics Press, Chapters on data-ink and
  annotation. https://www.edwardtufte.com/tufte/books_vdqi
- Knaflic, C. N. (2015). Storytelling with Data. Wiley, Chapters 4-5 on focusing attention.
- Cairo, A. (2016). The Truthful Art. New Riders, Chapter 8 on annotation.
- matplotlib annotation tutorial: https://matplotlib.org/stable/tutorials/text/annotations.html
