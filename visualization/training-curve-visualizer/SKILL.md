---
name: training-curve-visualizer
description: Plot train and validation loss and accuracy over epochs with dual y-axes, overfit shading, and a best-epoch marker. Trigger when monitoring model training, comparing optimisers, or reporting convergence behaviour in a paper.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [training, loss, accuracy, overfit, convergence]
related: [visualization/roc-pr-curve-plotter, visualization/confusion-matrix-plotter]
prerequisites: []
outputs: [python, svg]
difficulty: beginner
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Training Curve Visualizer

## When To Use
- Monitoring training and validation loss across epochs.
- Spotting the epoch where validation diverges (overfit onset).
- Comparing optimisers or learning-rate schedules.
- Producing a convergence figure for a manuscript appendix.

## Workflow
1. Load epoch logs containing train/val loss and accuracy.
2. Detect the best validation epoch by lowest loss or highest accuracy.
3. Identify the overfit region where val loss rises while train loss falls.
4. Build a single figure with two y-axes if loss and accuracy differ in scale.
5. Shade the overfit region and draw a vertical line at the best epoch.
6. Place legends outside the axes via `bbox_to_anchor`.
7. Save the figure as PDF for the paper.

## Inputs
- A training log (CSV or JSON) with columns `epoch`, `trainLoss`, `valLoss`, `trainAcc`, `valAcc`.
- Optional metric choice to drive the best-epoch selection.
- A title string identifying the run.

## Outputs
- A PDF figure with train/val curves and annotations.
- A JSON file recording the best epoch and overfit onset.

## Key Rules
- Use two y-axes when loss and accuracy have different scales.
- Shade the overfit region where validation diverges from training.
- Mark the best validation epoch with a vertical line.
- Save as PDF; never as JPG for line plots.
- Legends sit outside the axes via `bbox_to_anchor`.
- Use `constrained_layout=True` so labels do not collide.

## Examples
```python
# Plot training and validation curves with overfit shading.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def PlotTrainingCurve(log, outputPath):
  # Unpack the log arrays.
  epochs = np.asarray(log["epoch"])
  trainLoss = np.asarray(log["trainLoss"])
  valLoss = np.asarray(log["valLoss"])
  bestEpoch = int(epochs[np.argmin(valLoss)])
  # Detect the overfit onset after the best epoch.
  onset = bestEpoch
  for (i) in range(bestEpoch + 1, len(epochs)):
    if (valLoss[i] > valLoss[bestEpoch] and trainLoss[i] < trainLoss[bestEpoch]):
      onset = int(epochs[i])
      break
  # Dual-axis figure for loss and accuracy.
  fig, axL = plt.subplots(figsize=(3.5, 2.8), constrained_layout=True)
  axR = axL.twinx()
  axL.plot(epochs, trainLoss, color="#1f77b4", label="Train loss")
  axL.plot(epochs, valLoss, color="#d62728", label="Val loss")
  # Shade the overfit region.
  axL.axvspan(onset, epochs[-1], color="grey", alpha=0.12)
  # Vertical line at the best validation epoch.
  axL.axvline(bestEpoch, color="black", linestyle=":", lw=0.8)
  axL.set_xlabel("Epoch")
  axL.set_ylabel("Loss")
  axR.set_ylabel("Accuracy")
  # Legends collected outside the axes.
  linesL, labelsL = axL.get_legend_handles_labels()
  axL.legend(linesL, labelsL, bbox_to_anchor=(1.08, 1.0), loc="upper left", fontsize=7)
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```

## References
- matplotlib twinx docs: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.twinx.html
