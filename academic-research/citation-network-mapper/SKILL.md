---
name: citation-network-mapper
description: Map citation networks using tools like Connected Papers, Semantic Scholar, and Inciteful to identify influential/bridge papers, research lineages, and emerging trends, and output a citation graph (nodes = papers, edges = citations). Use when the user wants to visualize the literature landscape, find seminal works, or trace a research lineage.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [ citations, literature, network-graph, semantic-scholar, connected-papers ]
related: [ academic-research/literature-review-synthesizer, academic-research/related-work-surveyor, style-integrity/zero-fabrication-guard ]
prerequisites: [ ]
outputs: [ json, markdown ]
difficulty: intermediate
estimated_tokens: 860
cost_warning: "Optional: Connected Papers / Semantic Scholar / Inciteful APIs may have rate limits or paid tiers."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: [ ]
---

# Citation Network Mapper

## When To Use

- The user asks to "map citations", "find bridge papers", "visualize the literature", or "trace the lineage" of a topic.
- The user wants influential or trending papers around a seed paper.
- The user needs a citation graph (nodes = papers, edges = citations).
- Trigger keywords: citation network, Connected Papers, Semantic Scholar, Inciteful, lineage, bridge papers,
  influential.

## Workflow

1. Take a seed paper (DOI or Semantic Scholar paperId) from the user.
2. Query Connected Papers, Semantic Scholar, and Inciteful for forward and backward citations.
3. Normalize across sources: deduplicate by DOI, prefer Semantic Scholar paperId as the canonical key.
4. Build the edge list: every (citing_paper, cited_paper) directed pair.
5. Compute node metrics: in-degree (times cited), out-degree (references), betweenness centrality (bridge score),
   PageRank.
6. Identify three classes of papers: influential (top PageRank), bridges (top betweenness), emerging (recent + rising
   in-degree).
7. Detect research lineages by tracing the longest citation path through bridge papers from the earliest seminal work to
   the seed.
8. Cluster nodes by methodology (reuse related-work-surveyor groups) and color the graph accordingly.
9. Output a Graphviz DOT file and a tabular summary.
10. Draft a 2-paragraph interpretation: where the seed sits in the network, what the lineage implies for novelty
    positioning.

## Inputs

- Seed paper DOI or Semantic Scholar paperId.
- Depth of expansion (1-hop or 2-hop).
- Time window filter (optional).
- Methodology cluster labels (optional, from related-work-surveyor).

## Outputs

- `citation_graph.dot` — Graphviz source (nodes + directed edges).
- `node_metrics.csv` — paperId, in-degree, out-degree, betweenness, PageRank.
- `influential_papers.md` — top PageRank papers with metadata.
- `bridge_papers.md` — top betweenness papers.
- `lineage.md` — earliest seminal work → seed path.
- `interpretation.md` — 2-paragraph positioning narrative.

## Key Rules

- Deduplicate by DOI before computing metrics.
- Use a single canonical key (Semantic Scholar paperId) across all outputs.
- Betweenness centrality identifies bridges; PageRank identifies influence.
- Emerging papers = published in last 3 years with rising in-degree.
- Every graph node carries metadata: title, year, methodology cluster.
- Cite the API or tool that produced the data (no fabricated edges).

## Examples

```text
Seed: McMahan et al. 2017 "Communication-Efficient Learning of Deep Networks
       from Decentralized Data" (FedAvg).

Influential (top PageRank):
  - McMahan 2017 (FedAvg)              PR=0.18
  - Bonawitz 2019 (Secure Aggregation) PR=0.09
  - Li 2020 (FedProx)                  PR=0.07

Bridge (top betweenness):
  - Li 2020 (FedProx) — connects foundational and personalization branches.
  - Acar 2021 (FedDyn) — bridges optimization and convergence theory.

Lineage: McMahan 2017 → Bonawitz 2019 → Li 2020 → Acar 2021 → seed.
```

```text
DOT excerpt:
digraph citation_network {
  rankdir=LR;
  mcmahan2017 [label="FedAvg (2017)"];
  bonawitz2019 [label="SecAgg (2019)"];
  li2020 [label="FedProx (2020)", color=orange];
  mcmahan2017 -> bonawitz2019;
  bonawitz2019 -> li2020;
  li2020 -> acar2021;
}
```
