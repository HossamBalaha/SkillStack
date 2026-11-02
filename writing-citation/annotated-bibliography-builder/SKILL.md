---
name: annotated-bibliography-builder
description: Builds annotated bibliographies where each entry combines a full citation, a 2-4 sentence summary (what the paper did, its method, and key finding), and an assessment of strengths, limitations, and relevance to the user's work. Use when preparing a literature review, a grant proposal's background section, or a thesis's state-of-the-art chapter.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [bibliography, annotated, summary, literature-review, citation]
related: [writing-citation/literature-matrix-builder, writing-citation/bibtex-citation-manager, writing-citation/reference-list-formatter]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
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

# Annotated Bibliography Builder

## When To Use

- A grant proposal requires a 1-page annotated bibliography of the most relevant prior work.
- A thesis chapter needs a synthesis-ready set of paper notes grouped by theme.
- You are starting a systematic review and need a structured note per candidate paper.
- A course assignment explicitly calls for an annotated bibliography.

## Workflow

1. Collect the candidate references (a `.bib` file, a Zotero collection, or a list of DOIs).
2. For each reference, retrieve the abstract and the methods/findings sections (from the PDF or the publisher page).
3. Write a 2-4 sentence summary covering: what the paper did, the method it used, and its key finding.
4. Write an assessment covering: strengths, limitations, and explicit relevance to the user's research question.
5. Format the full citation in the target style (APA, IEEE, Chicago, etc.) at the top of the entry.
6. Group entries by theme (e.g., "Federated optimization," "Privacy attacks," "Personalization") rather than
   alphabetically.
7. Within each theme, sort entries by year (descending) so the most recent work leads.
8. Produce both a Markdown report and a CSV row-per-entry version for downstream synthesis.
9. Cross-check that every entry's "relevance" statement ties back to the user's stated research question.

## Inputs

- A reference list (`.bib`, Zotero export, or DOIs).
- The user's research question or thesis topic.
- Target citation style.
- Optional theme list (if the user has predefined categories).

## Outputs

- `annotated_bibliography.md` — grouped, styled entries with summary + assessment per paper.
- `annotated_bibliography.csv` — flat table: citekey, year, theme, summary, strengths, limitations, relevance.
- `theme_index.md` — list of themes with the count of entries per theme.

## Key Rules

- Each summary must be 2-4 sentences — no longer, no shorter.
- Each assessment must contain explicit strengths, limitations, and relevance statements.
- Entries must be grouped by theme, not by author or by year.
- Relevance statements must explicitly connect the paper to the user's research question.
- Citations must be in the chosen style and must be consistent.
- Never fabricate findings — if the source PDF is unavailable, mark the summary as "unverified."

## Examples

```text
Theme: Privacy attacks on federated learning

Geiping, J., Bauermeister, H., Dröge, H., & Moeller, M. (2020). Inverting
gradients — how easy is it to recover private data in deep learning?
Advances in Neural Information Processing Systems, 33, 15737-15747.

Summary: The authors demonstrate that raw training samples can be
reconstructed from shared gradients via a distance-minimization attack
that matches synthetic inputs to the observed gradient. They evaluated
the attack on image classification and language-modeling tasks,
showing pixel-perfect recovery on small-batch regimes.

Assessment: Strengths include a clean mathematical formulation and a
public reproduction codebase. Limitations are the reliance on small
batch sizes (≤ 8) and shallow model depths, which overstate risk in
production settings. Relevance: this paper directly motivates the
gradient-noise defense we propose in Chapter 3.

Theme: Federated optimization
Li, T., Sahu, A. K., Zaheer, M., Sanjabi, M., Talwalkar, A., & Smith, V.
(2020). Federated optimization in heterogeneous networks. MLSys, 2, 429-444.
Summary: ...
Assessment: ...
```

```text
CSV row example:
citekey,year,theme,summary,strengths,limitations,relevance
Geiping2020Inverting,2020,Privacy attacks,"Reconstructs training data from shared gradients via distance-minimization.","Clean formulation; reproducible code","Assumes small batches (≤8)","Motivates our gradient-noise defense (Ch.3)"
```

## References

- Cornell University Library guide to annotated
  bibliographies: https://guides.library.cornell.edu/annotatedbibliography.
- Purdue OWL: https://owl.purdue.edu/owl/general_writing/common_writing_assignments/annotated_bibliographies/index.html.
- The CRAAP test for source assessment (Currency, Relevance, Authority, Accuracy, Purpose).
