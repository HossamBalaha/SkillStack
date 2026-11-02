---
name: embedding-projector
description: Project high-dimensional embeddings to 2D or 3D using PCA, t-SNE, or UMAP with label colouring. Trigger when inspecting latent spaces, comparing encoders, or producing a t-SNE scatter for a paper.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [embeddings, tsne, umap, pca, latent-space]
related: [visualization/attention-map-visualizer, visualization/interactive-plot-builder]
prerequisites: []
outputs: [python, html, svg]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Embedding Projector

## When To Use

- Inspecting the latent space of a trained encoder.
- Comparing clusters across two embedding methods.
- Producing a t-SNE or UMAP scatter for a paper's analysis section.
- Building an interactive projector for exploratory analysis.

## Workflow

1. Load the embedding matrix and the label vector.
2. Choose a projector: PCA (fast, linear), t-SNE (local structure, slow), or UMAP (local plus global).
3. Subsample if the dataset exceeds a few thousand points to keep t-SNE tractable.
4. Project to 2-D (or 3-D) and store the coordinates.
5. Colour points by label using a colourblind-friendly palette.
6. Save a static PDF and optionally an interactive HTML via plotly.
7. Optionally export TensorBoard Projector checkpoints for exploration.

## Inputs

- Embedding matrix of shape `[nSamples, nDims]` with `nDims >= 3`.
- Label array of shape `[nSamples]`.
- Choice of projector and target dimensionality.

## Outputs

- A static PDF/PNG scatter with a colour legend.
- An interactive HTML (plotly) when requested.
- TensorBoard Projector variable and metadata files when requested.

## Key Rules

- Use PCA for a fast linear baseline before non-linear methods.
- Subsample before t-SNE when the dataset exceeds a few thousand points.
- Colour points by label using a colourblind-friendly palette.
- Report the projector, perplexity (t-SNE), or `n_neighbors` (UMAP) in the caption.
- Always set a random seed for reproducibility.
- Place legends outside the axes via `bbox_to_anchor`.

## Examples

```python
# Project embeddings with PCA, t-SNE, or UMAP and plot a scatter.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def ProjectEmbeddings(embeddings, labels, method="pca", outputPath="emb.pdf"):
  # Select the projector based on the method flag.
  if (method == "pca"):
    model = PCA(n_components=2, random_state=0)
  elif (method == "tsne"):
    model = TSNE(n_components=2, perplexity=30.0, random_state=0, init="pca")
  else:
    # Defer to umap-learn when available.
    from umap import UMAP
    model = UMAP(n_components=2, n_neighbors=15, random_state=0)
  coords = model.fit_transform(embeddings)
  # Scatter coloured by label.
  fig, ax = plt.subplots(figsize=(3.5, 3.0), constrained_layout=True)
  for (lab) in np.unique(labels):
    mask = np.asarray(labels) == lab
    ax.scatter(coords[mask, 0], coords[mask, 1], s=6, label=str(lab), alpha=0.7)
  ax.set_xlabel(f"{method.upper()} 1")
  ax.set_ylabel(f"{method.upper()} 2")
  # Legend placed outside the axes.
  ax.legend(bbox_to_anchor=(1.02, 1.0), loc="upper left", fontsize=7, markerscale=2)
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```

## References

- sklearn PCA: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- sklearn TSNE: https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
- umap-learn: https://umap-learn.readthedocs.io/
