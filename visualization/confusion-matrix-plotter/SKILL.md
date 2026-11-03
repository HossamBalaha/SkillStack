---
name: confusion-matrix-plotter
description: Plot raw-count and row-normalized confusion matrices side by side with cell annotations and accuracy/F1 in a side panel. Trigger when evaluating a classifier, comparing models on class-wise performance, or reporting per-class errors.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [confusion-matrix, classifier, accuracy, f1, evaluation]
related: [visualization/roc-pr-curve-plotter, visualization/results-table-formatter]
prerequisites: []
outputs: [python, svg]
difficulty: beginner
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

# Confusion Matrix Plotter

## When To Use

- Reporting classification results with per-class accuracy.
- Comparing two classifiers on their error patterns.
- Diagnosing systematic confusion between similar classes.
- Producing a figure for a paper's results section.

## Workflow

1. Compute the confusion matrix from predicted and true labels.
2. Build the row-normalized variant by dividing each row by its sum.
3. Create a two-panel figure with `plt.subplots(1, 2)`.
4. Render each matrix with `seaborn.heatmap(annot=True, fmt="d", cmap="Blues")`.
5. Rotate long class labels by 45 degrees on the x-axis.
6. Add accuracy, macro-F1, and weighted-F1 in a side text panel.
7. Save as PDF for the manuscript and PNG for quick inspection.

## Inputs

- Predicted labels and ground-truth labels (lists or 1-D arrays).
- Class name list aligned with label indices.
- Optional sample weights for weighted metrics.

## Outputs

- A two-panel PDF/PNG with raw and normalized matrices.
- A small JSON file recording accuracy, macro-F1, and weighted-F1.

## Key Rules

- Always show raw counts AND row-normalized variants.
- Annotate every cell with its count using `annot=True`.
- Use `fmt="d"` for integer counts and `fmt=".2f"` for normalized values.
- Rotate long class labels to 45 degrees to avoid overlap.
- Report accuracy and F1 either in the title or a side panel.
- Use `constrained_layout=True` and keep legends outside when present.

## Examples

```python
# Plot raw and normalized confusion matrices side by side.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.metrics import confusion_matrix, f1_score

# Register fonts so Chinese class names render correctly.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def PlotConfusion(yTrue, yPred, classNames, outputPath):
  # Compute raw counts and the row-normalized variant.
  cm = confusion_matrix(yTrue, yPred)
  cmNorm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
  acc = float(np.mean(np.asarray(yTrue) == np.asarray(yPred)))
  f1 = float(f1_score(yTrue, yPred, average="macro"))
  # Two-panel figure with shared layout.
  fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.4), constrained_layout=True)
  sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
              xticklabels=classNames, yticklabels=classNames, ax=axes[0])
  axes[0].set_title("Counts", fontsize=9)
  sns.heatmap(cmNorm, annot=True, fmt=".2f", cmap="Blues",
              xticklabels=classNames, yticklabels=classNames, ax=axes[1])
  axes[1].set_title("Normalised", fontsize=9)
  for (ax) in axes:
    # Rotate long labels for readability.
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
  # Headline metrics in the super title.
  fig.suptitle(f"Accuracy={acc:.3f}  Macro-F1={f1:.3f}", fontsize=10)
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```
