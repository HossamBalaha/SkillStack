---
name: network-graph-visualizer
description: Visualize network graphs with layout algorithms, node sizing by degree, community colouring, and edge widths by weight. Trigger when analysing social networks, citation graphs, or neural-network architectures, and when producing static or interactive graph figures.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [network, graph, layout, community, citation-graph]
related: [visualization/embedding-projector, visualization/interactive-plot-builder]
prerequisites: []
outputs: [python, html, svg]
difficulty: intermediate
estimated_tokens: 1000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Network Graph Visualizer

## When To Use

- Plotting a social, citation, or dependency network.
- Highlighting communities detected by Louvain or similar.
- Showing node importance via degree or centrality sizing.
- Producing an interactive HTML for exploration with `pyvis`.

## Workflow

1. Load the graph from an edge list or adjacency matrix.
2. Choose a layout: spring, circular, kamada-kawai, or Graphviz hierarchical.
3. Compute node degree or centrality to drive node size.
4. Detect communities (Louvain) and assign colours.
5. Scale edge width by weight when weights carry meaning.
6. Render static with `networkx` + `matplotlib`, or interactive with `pyvis`.
7. For large graphs (over 1000 nodes), aggregate or sample before plotting.
8. Save the figure and a legend mapping colours to communities.

## Inputs

- An edge list or `networkx.Graph` object.
- Optional node attributes (label, community) and edge weights.
- A layout choice and an output format (PDF or HTML).

## Outputs

- A static PDF/PNG of the graph.
- An interactive HTML when `pyvis` is selected.
- A legend file mapping community IDs to colours.

## Key Rules

- Size nodes by degree or a centrality measure.
- Colour nodes by community using a colourblind-friendly palette.
- Scale edge width by weight when weights carry meaning.
- For graphs over 1000 nodes, aggregate or sample first.
- Place legends outside the axes via `bbox_to_anchor` for static plots.
- Use `constrained_layout=True` for matplotlib output.

## Examples

```python
# Draw a networkx graph with community colours and degree sizing.
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from networkx.algorithms.community import louvain_communities

# Font registration for mixed CJK and Latin text.
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def DrawGraph(graph, outputPath):
  # Subsample large graphs to keep the figure readable.
  if (graph.number_of_nodes() > 1000):
    sampled = list(graph.nodes())[:1000]
    graph = graph.subgraph(sampled).copy()
  # Compute layout once for stable positions.
  pos = nx.spring_layout(graph, seed=0)
  # Size nodes by degree.
  degrees = dict(graph.degree())
  sizes = [30.0 + degrees[n] * 5.0 for (n) in graph.nodes()]
  # Colour by Louvain community.
  communities = louvain_communities(graph, seed=0)
  palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
             "#8c564b", "#e377c2", "#7f7f7f"]
  colorMap = {}
  for (i, comm) in enumerate(communities):
    color = palette[i % len(palette)]
    for (n) in comm:
      colorMap[n] = color
  colors = [colorMap[n] for (n) in graph.nodes()]
  # Edge width from weight attribute when present.
  widths = [graph[u][v].get("weight", 1.0) for (u, v) in graph.edges()]
  fig, ax = plt.subplots(figsize=(5.0, 5.0), constrained_layout=True)
  nx.draw_networkx_edges(graph, pos, width=widths, alpha=0.4, ax=ax)
  nx.draw_networkx_nodes(graph, pos, node_size=sizes, node_color=colors, ax=ax)
  ax.set_axis_off()
  fig.savefig(outputPath, format="pdf")
  plt.close(fig)
```

## References

- networkx docs: https://networkx.org/documentation/stable/
- pyvis interactive graphs: https://pyvis.readthedocs.io/
