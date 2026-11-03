---
name: roc-pr-curve-plotter
description: Plot ROC and Precision-Recall curves with AUC in the legend, baseline references, and bootstrap 95% CI bands. Trigger when evaluating binary or multi-class classifiers on imbalanced data, or when reporting AUC values for a paper.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [roc, pr-curve, auc, classifier, imbalance]
related: [visualization/confusion-matrix-plotter, visualization/training-curve-visualizer]
prerequisites: []
outputs: [python, pdf, svg]
difficulty: intermediate
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# ROC / PR Curve Plotter

## When To Use

- Reporting ROC-AUC and average precision for a classifier.
- Comparing several models on the same evaluation set.
- Dealing with class imbalance where PR curves are more informative.
- Adding bootstrap confidence bands around a curve.

## Workflow

1. Collect predicted probabilities and binary labels for the test set.
2. Compute ROC and PR curves plus AUC via `sklearn.metrics`.
3. Bootstrap the test set N times to estimate 95% CI bands.
4. Add the ROC diagonal and the PR prevalence baseline references.
5. For multi-class, iterate one-vs-rest per class with distinct colours.
6. Place the AUC value in the legend and the band outside the curve.
7. Save as PDF with legends outside the axes via `bbox_to_anchor`.

## Inputs

- Predicted probabilities (1-D for binary, 2-D for multi-class).
- True labels (1-D integer array).
- Number of bootstrap iterations (default 1000).

## Outputs

- A PDF/PNG with ROC and PR curves side by side.
- A JSON file recording AUC, average precision, and CI bounds.

## Key Rules

- Always include the ROC diagonal and PR prevalence baselines.
- Bootstrap 95% CI bands use at least 1000 resamples.
- Multi-class uses one-vs-rest with a distinct colour per class.
- AUC must appear in the legend, not the title only.
- Use `constrained_layout=True` and place legends outside the axes.
- Report average precision alongside the PR curve.

## Examples

```python
# Plot ROC and PR curves with bootstrap CI bands.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def BootstrapRoc(yTrue, yScore, nIter=1000):
  # Bootstrap the ROC curve and AUC for 95% CI bands.
  rng = np.random.default_rng(0)
  baseFpr, _, _ = roc_curve(yTrue, yScore)
  tprs = []
  aucs = []
  n = len(yTrue)
  for (i) in range(nIter):
    # Resample indices with replacement.
    idx = rng.integers(0, n, size=n)
    fpr, tpr, _ = roc_curve(yTrue[idx], yScore[idx])
    tprs.append(np.interp(baseFpr, fpr, tpr))
    aucs.append(auc(fpr, tpr))
  tprs = np.asarray(tprs)
  meanTpr = tprs.mean(axis=0)
  lower = np.percentile(tprs, 2.5, axis=0)
  upper = np.percentile(tprs, 97.5, axis=0)
  return baseFpr, meanTpr, lower, upper, float(np.mean(aucs))

def PlotRocPr(yTrue, yScore, outputPath):
  # Side-by-side ROC and PR curves with CI bands.
  fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.4), constrained_layout=True)
  fpr, tpr, _ = roc_curve(yTrue, yScore)
  aucVal = auc(fpr, tpr)
  bFpr, mTpr, lo, hi, _ = BootstrapRoc(yTrue, yScore)
  # ROC panel with diagonal baseline and CI band.
  axes[0].plot([0, 1], [0, 1], "--", color="grey", lw=0.8)
  axes[0].plot(fpr, tpr, color="#1f77b4", label=f"AUC={aucVal:.3f}")
  axes[0].fill_between(bFpr, lo, hi, color="#1f77b4", alpha=0.15)
  axes[0].set_xlabel("False positive rate")
  axes[0].set_ylabel("True positive rate")
  # PR panel with prevalence baseline.
  prec, rec, _ = precision_recall_curve(yTrue, yScore)
  ap = average_precision_score(yTrue, yScore)
  prev = float(np.mean(yTrue))
  axes[1].plot([0, 1], [prev, prev], "--", color="grey", lw=0.8)
  axes[1].plot(rec, prec, color="#d62728", label=f"AP={ap:.3f}")
  axes[1].set_xlabel("Recall")
  axes[1].set_ylabel("Precision")
  for (ax) in axes:
    ax.legend(bbox_to_anchor=(1.02, 1.0), loc="upper left", fontsize=8)
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```
