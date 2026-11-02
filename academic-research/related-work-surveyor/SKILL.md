---
name: related-work-surveyor
description: Survey related work and build thematic comparison tables (paper x dimension matrix) grouped by methodology, not chronology, and identify the gap your work fills. Use when the user is drafting a Related Work section, preparing a state-of-the-art comparison table, or sharpening the novelty claim.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [related-work, comparison-table, novelty, gap-analysis, literature]
related: [academic-research/literature-review-synthesizer, academic-research/citation-network-mapper, academic-research/journal-manuscript-writer]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 820
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: false
language: en
---

# Related Work Surveyor

## When To Use

- The user asks to "write related work", "compare prior methods", or "build a SOTA table".
- The user wants a methodology-grouped comparison matrix, not a chronological list.
- The user needs to articulate the research gap explicitly.
- Trigger keywords: related work, related work survey, SOTA table, comparison matrix, gap statement.

## Workflow

1. Take the candidate paper list (from the literature-review-synthesizer step or user input).
2. Group papers by methodology family, not by year. Reject chronological narrative.
3. Define 5-8 comparison dimensions (e.g., "Aggregator type", "Topology-aware", "Public code", "Datasets used",
   "Backbone").
4. Build a paper × dimension matrix. Mark unknown cells with "Not reported" rather than leaving them blank.
5. For each methodology family, write a 4-6 sentence synthesis paragraph (not a paper-by-paper walk).
6. Identify the intersection of weaknesses: which dimensions are under-addressed across families.
7. Draft the Gap Statement: 2-3 sentences naming the exact gap and how the proposed work fills it.
8. Map each gap dimension back to a Specific Aim or contribution.
9. Add a forward pointer: "Our work (Section 3) addresses this gap by..."
10. Output the matrix and synthesis as LaTeX-ready content.

## Inputs

- Candidate paper list with BibTeX or DOIs.
- Proposed work's aims and contributions.
- Comparison dimensions (or let the skill propose them).
- Target venue and section length budget.

## Outputs

- `methodology_groups.md` — papers grouped by methodology family.
- `comparison_matrix.tex` — paper × dimension LaTeX table.
- `synthesis_paragraphs.md` — one paragraph per methodology family.
- `gap_statement.md` — 2-3 sentence gap statement.
- `gap_to_aim_map.md` — gap dimensions mapped to Specific Aims.

## Key Rules

- Group by methodology, never by year.
- Never leave matrix cells blank; use "Not reported".
- One synthesis paragraph per methodology family; no paper-by-paper walk.
- Gap Statement names the dimension and the proposed contribution.
- Every gap dimension maps to at least one Specific Aim.
- Cite each paper with a stable BibTeX key.

## Examples

```text
Methodology groups (Federated MRI segmentation):
  Group A — Aggregation-only methods: FedAvg, FedBN, FedProx.
  Group B — Adversarial alignment methods: DANN-FL, FedDG.
  Group C — Topology-aware methods: TopoNet (closest prior art).

Comparison matrix (excerpt):
  Method      | Aggregator | Topo-aware | Public code | Datasets
  FedAvg      | Mean       | No         | Yes         | 2
  FedBN       | Mean+BN    | No         | Yes         | 3
  FedDG       | Mean+Adv   | No         | No          | 3
  TopoNet     | Mean+TL    | Yes        | No          | 2
```

```text
Gap statement:
  Existing federated MRI segmentation methods either ignore topology (Group A/B)
  or address it with limited public benchmarks and no released code (TopoNet).
  Our work fills this gap by introducing a topology-regularized aggregator
  with open code and a 4-dataset benchmark (Aims 2 and 3).
```

## References

- ACM Computing Surveys review methodology: https://dl.acm.org/journal/csur
- "Writing a related-work section that gets cited" (Jensen 2019): https://doi.org/10.1038/d41586-019-02962-9
- Connected Papers for graphing prior art: https://www.connectedpapers.com/
- Semantic Scholar API: https://api.semanticscholar.org/

## Notes

- Keep each synthesis paragraph focused on the methodology family's shared assumption, then highlight divergences.
- If a paper spans two methodology families, list it under both with a cross-reference note.
- Re-run the gap audit after every new paper added to the candidate list.
