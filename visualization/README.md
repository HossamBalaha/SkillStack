# 📊 Visualization — Figures, TikZ & Posters

> Produce publication-ready figures, multi-panel composites, TikZ framework diagrams, scientific posters, and
> interactive dashboards. From color-palette selection through confusion matrices, ROC/PR curves, attention maps, and
> embedding projectors, this theme covers every visual artifact a paper or talk needs. Output is vector-first (PDF /
> SVG)
> with a paired caption.

## Theme Overview

This folder contains **18 skills** in the `visualization/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                 | Description                                                                                                                                    | Difficulty   | Tags                                                                   | Related                                                                                                                     |
|----|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| 1  | [`academic-plotting-pipeline`](academic-plotting-pipeline/SKILL.md)   | Route academic figures into the correct rendering track (matplotlib for numerical data, diagrams for boxes-and-arrows).                        | intermediate | `matplotlib`, `academic`, `figures`, `pipeline`, `routing`             | `visualization/publication-figure-maker`, `visualization/confusion-matrix-plotter`                                          |
| 2  | [`attention-map-visualizer`](attention-map-visualizer/SKILL.md)       | Visualize transformer attention weights as per-head and per-layer heatmaps with token overlay.                                                 | intermediate | `attention`, `transformer`, `heatmaps`, `nlp`, `visualization`         | `visualization/embedding-projector`, `visualization/training-curve-visualizer`                                              |
| 3  | [`color-palette-selector`](color-palette-selector/SKILL.md)           | Select colorblind-friendly palettes (viridis, cividis, ColorBrewer, Wong's palette) and verify them with simulators.                           | beginner     | `color`, `palette`, `colorblind`, `viridis`, `accessibility`           | `visualization/publication-figure-maker`, `visualization/dashboard-builder`                                                 |
| 4  | [`confusion-matrix-plotter`](confusion-matrix-plotter/SKILL.md)       | Plot raw-count and row-normalized confusion matrices side by side with cell annotations and accuracy/F1 in a side panel.                       | beginner     | `confusion-matrix`, `classifier`, `accuracy`, `f1`, `evaluation`       | `visualization/roc-pr-curve-plotter`, `visualization/results-table-formatter`                                               |
| 5  | [`dashboard-builder`](dashboard-builder/SKILL.md)                     | Build interactive dashboards with Streamlit, Dash, or Gradio, featuring sidebar controls, metric cards, charts, and real-time callbacks.       | intermediate | `streamlit`, `dash`, `gradio`, `dashboard`                             | `visualization/interactive-plot-builder`                                                                                    |
| 6  | [`embedding-projector`](embedding-projector/SKILL.md)                 | Project high-dimensional embeddings to 2D or 3D using PCA, t-SNE, or UMAP with label coloring.                                                 | intermediate | `embeddings`, `tsne`, `umap`, `pca`, `latent-space`                    | `visualization/attention-map-visualizer`, `visualization/interactive-plot-builder`                                          |
| 7  | [`figure-caption-writer`](figure-caption-writer/SKILL.md)             | Write publication-ready figure captions explaining what the figure shows, how the methodology produced it, and why it validates the framework. | beginner     | `caption`, `manuscript`, `figure`, `publication`, `writing`            | `visualization/publication-figure-maker`, `visualization/multi-panel-figure-composer`                                       |
| 8  | [`infographic-summarizer`](infographic-summarizer/SKILL.md)           | Convert dense reports into single-page infographics with visual hierarchy, key-stat callouts, and a limited color palette.                     | intermediate | `infographic`, `summary`, `design`, `hierarchy`, `callouts`            | `visualization/scientific-poster-designer`, `visualization/dashboard-builder`                                               |
| 9  | [`interactive-plot-builder`](interactive-plot-builder/SKILL.md)       | Build interactive plots with hover, zoom, and click using Plotly, Bokeh, or Holoviews/Datashader.                                              | intermediate | `plotly`, `bokeh`, `holoviews`, `interactive`, `datashader`            | `visualization/dashboard-builder`, `visualization/embedding-projector`                                                      |
| 10 | [`multi-panel-figure-composer`](multi-panel-figure-composer/SKILL.md) | Compose multi-panel matplotlib figures with shared axes, panel labels (a), (b), (c), and constrained layout.                                   | intermediate | `matplotlib`, `multi-panel`, `subplots`, `publication`, `panel-labels` | `visualization/publication-figure-maker`, `visualization/figure-caption-writer`                                             |
| 11 | [`network-graph-visualizer`](network-graph-visualizer/SKILL.md)       | Visualize network graphs with layout algorithms, node sizing by degree, community coloring, and edge widths by weight.                         | intermediate | `network`, `graph`, `layout`, `community`, `citation-graph`            | `visualization/embedding-projector`, `visualization/interactive-plot-builder`                                               |
| 12 | [`publication-figure-maker`](publication-figure-maker/SKILL.md)       | Produce journal-ready matplotlib and seaborn figures sized to exact column widths.                                                             | intermediate | `matplotlib`, `publication`, `figures`, `journal`                      | `visualization/figure-caption-writer`, `visualization/results-table-formatter`, `visualization/multi-panel-figure-composer` |
| 13 | [`results-table-formatter`](results-table-formatter/SKILL.md)         | Format experimental results tables in booktabs style with significance markers, confidence intervals, and bold best entries.                   | intermediate | `table`, `booktabs`, `significance`, `ci`, `ablation`                  | `visualization/figure-caption-writer`, `visualization/publication-figure-maker`                                             |
| 14 | [`roc-pr-curve-plotter`](roc-pr-curve-plotter/SKILL.md)               | Plot ROC and Precision-Recall curves with AUC in the legend, baseline references, and bootstrap 95% CI bands.                                  | intermediate | `roc`, `pr-curve`, `auc`, `classifier`, `imbalance`                    | `visualization/confusion-matrix-plotter`, `visualization/training-curve-visualizer`                                         |
| 15 | [`scientific-poster-designer`](scientific-poster-designer/SKILL.md)   | Design A0 scientific posters with IMRAD layout and one-meter readability.                                                                      | advanced     | `poster`, `a0`, `imrad`, `conference`, `readability`                   | `visualization/infographic-summarizer`, `visualization/multi-panel-figure-composer`                                         |
| 16 | [`surface-plotter`](surface-plotter/SKILL.md)                         | Plot 3D surfaces with proper view angles, colorbars, and a 2D contour overlay for loss landscapes.                                             | intermediate | `3d`, `surface`, `contour`, `loss-landscape`, `matplotlib`             | `visualization/training-curve-visualizer`, `visualization/publication-figure-maker`                                         |
| 17 | [`tikz-framework-diagrammer`](tikz-framework-diagrammer/SKILL.md)     | Build publication-ready TikZ pipeline diagrams with solid grouping boxes, concise node labels, and explicit anchor connections.                | advanced     | `tikz`, `latex`, `diagrams`, `architecture`                            | `visualization/publication-figure-maker`, `academic-research/journal-manuscript-writer`                                     |
| 18 | [`training-curve-visualizer`](training-curve-visualizer/SKILL.md)     | Plot train and validation loss and accuracy over epochs with dual y-axes, overfit shading, and a best-epoch marker.                            | beginner     | `training`, `loss`, `accuracy`, `overfit`, `convergence`               | `visualization/roc-pr-curve-plotter`, `visualization/confusion-matrix-plotter`                                              |

## Difficulty Breakdown

Across **18** skills in this theme, the difficulty distribution is:

- **Beginner** — 4 skill(s)
- **Intermediate** — 12 skill(s)
- **Advanced** — 2 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`matplotlib` (4), `publication` (3), `accuracy` (2), `classifier` (2), `figures` (2), `3d` (1), `a0` (1), `ablation`
(1), `academic` (1), `accessibility` (1), `architecture` (1), `attention` (1), `auc` (1), `bokeh` (1), `booktabs` (1),
`callouts` (1), `caption` (1), `ci` (1), `citation-graph` (1), `color` (1), `colorblind` (1), `community` (1),
`conference` (1), `confusion-matrix` (1), `contour` (1), `convergence` (1), `dash` (1), `dashboard` (1), `datashader`
(1), `design` (1), `diagrams` (1), `embeddings` (1), `evaluation` (1), `f1` (1), `figure` (1), `gradio` (1), `graph`
(1), `heatmaps` (1), `hierarchy` (1), `holoviews` (1), `imbalance` (1), `imrad` (1), `infographic` (1), `interactive`
(1), `journal` (1), `latent-space` (1), `latex` (1), `layout` (1), `loss` (1), `loss-landscape` (1), `manuscript` (1),
`multi-panel` (1), `network` (1), `nlp` (1), `overfit` (1), `palette` (1), `panel-labels` (1), `pca` (1), `pipeline`
(1), `plotly` (1), `poster` (1), `pr-curve` (1), `readability` (1), `roc` (1), `routing` (1), `significance` (1),
`streamlit` (1), `subplots` (1), `summary` (1), `surface` (1), `table` (1), `tikz` (1), `training` (1), `transformer`
(1), `tsne` (1), `umap` (1), `viridis` (1), `visualization` (1), `writing` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`publication-figure-maker` → `figure-caption-writer` → `results-table-formatter`** — Figure + caption + table
  bundle.
- **`academic-plotting-pipeline` → `tikz-framework-diagrammer` → `multi-panel-figure-composer` →
  `figure-caption-writer`** — Pipeline → diagram → panels → caption.
- **`confusion-matrix-plotter` → `roc-pr-curve-plotter` → `training-curve-visualizer` → `embedding-projector`** —
  Classification evaluation suite.
- **`color-palette-selector` → `publication-figure-maker` → `multi-panel-figure-composer` → `figure-caption-writer`** —
  Color → figures → panels → caption.

## Cross-Theme Connections

Skills in `visualization/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../academic-research/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../ml-engineering/README.md`](ml-engineering/README.md) — training curves, confusion matrices, and attention maps
  visualize ML outputs.
- [`../academic-research/README.md`](academic-research/README.md) — publication figures and posters back the manuscript.
- [`../data-engineering/README.md`](data-engineering/README.md) — distribution plots and drift charts visualize data
  quality.
- [`../style-integrity/README.md`](style-integrity/README.md) — figure captions respect LaTeX and prose style rules.

## Back to Master

← [Back to SkillStack README](../README.md)
