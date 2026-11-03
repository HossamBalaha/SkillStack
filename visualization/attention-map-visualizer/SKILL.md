---
name: attention-map-visualizer
description: Visualize transformer attention weights as per-head and per-layer heatmaps with token overlay. Trigger when debugging attention patterns, comparing heads, or explaining model behaviour in an NLP or vision-transformer paper.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [attention, transformer, heatmaps, nlp, visualization]
related: [visualization/embedding-projector, visualization/training-curve-visualizer]
prerequisites: []
outputs: [python, svg]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Attention Map Visualizer

## When To Use

- Inspecting per-head attention patterns in a transformer.
- Comparing attention across layers for a single example.
- Overlaying attention weights on input tokens for interpretability.
- Producing a figure for a model analysis section.

## Workflow

1. Extract attention weights from the model's attention modules.
2. Align token strings with the row and column indices of the matrix.
3. Build a grid of per-head heatmaps for one layer.
4. If the head count is large, average across heads for a summary panel.
5. Overlay attention on tokens by colouring the token text.
6. Use `viridis` or a seaborn heatmap with cell annotations off.
7. Save as PDF for the manuscript plus PNG for quick inspection.

## Inputs

- Attention tensor of shape `[nLayers, nHeads, seqLen, seqLen]`.
- Token list aligned with `seqLen`.
- Optional layer and head indices to spotlight.

## Outputs

- A multi-panel PDF with per-head heatmaps.
- A summary PNG averaging across heads when the head count is large.
- A token-overlay HTML file colouring tokens by attention weight.

## Key Rules

- Use `cmap="viridis"` or `seaborn.heatmap` for the heatmap.
- Average across heads when there are too many to display individually.
- Align row and column ticks with token strings.
- Rotate long token labels to avoid overlap.
- Keep `constrained_layout=True` and legends outside the axes.
- Do not annotate every cell when sequence length exceeds 20.

## Examples

```python
# Plot per-head attention heatmaps for one transformer layer.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def PlotHeads(attention, tokens, outputPath, layerIdx=0):
  # attention shape: [nHeads, seqLen, seqLen].
  nHeads = attention.shape[0]
  # Average across heads if the grid would be too wide.
  if (nHeads > 8):
    fig, ax = plt.subplots(figsize=(3.4, 3.0), constrained_layout=True)
    sns.heatmap(attention.mean(axis=0), cmap="viridis",
                xticklabels=tokens, yticklabels=tokens, ax=ax, cbar=False)
    ax.set_title(f"Layer {layerIdx} (avg heads)", fontsize=9)
  else:
    cols = min(4, nHeads)
    rows = int(np.ceil(nHeads / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(3.4 * cols, 3.0 * rows),
                             constrained_layout=True)
    axes = np.atleast_1d(axes).ravel()
    for (h) in range(nHeads):
      sns.heatmap(attention[h], cmap="viridis",
                  xticklabels=tokens, yticklabels=tokens,
                  ax=axes[h], cbar=False)
      axes[h].set_title(f"Head {h}", fontsize=9)
      # Rotate long tokens to prevent overlap.
      axes[h].set_xticklabels(axes[h].get_xticklabels(), rotation=45, ha="right")
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```
