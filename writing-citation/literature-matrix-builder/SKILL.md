---
name: literature-matrix-builder
description: Builds a paper-by-dimension literature matrix (rows = papers, columns = year, methodology, dataset, sample size, key findings, limitations, relevance) as a Markdown table or CSV, sorted by year or theme. Use when synthesizing a body of literature for a review, identifying clusters and gaps, or preparing the input for a systematic-review narrative.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [literature-review, matrix, synthesis, csv, gaps]
related: [writing-citation/annotated-bibliography-builder, writing-citation/research-methodology-designer]
prerequisites: []
outputs: [markdown, csv]
difficulty: beginner
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

# Literature Matrix Builder

## When To Use

- You need to compare 10+ papers across a fixed set of dimensions for a literature review.
- A grant proposal asks for a "gap analysis" table.
- You are preparing input for a scoping or systematic review.
- A thesis advisor wants to see the landscape of prior work before approving a contribution.

## Workflow

1. Confirm the dimensions the matrix must capture: year, methodology, dataset/sample, key findings, limitations,
   relevance, plus any user-specific columns (e.g., population, intervention, comparator).
2. Collect the candidate paper set (Zotero collection, `.bib`, or DOI list).
3. For each paper, extract the dimension values from the abstract, methods, and conclusions.
4. Normalize categorical values (e.g., "RCT," "randomized controlled trial," "randomised trial" → "RCT") so they group
   cleanly.
5. Build the matrix as a Markdown table for human reading and a CSV for downstream analysis.
6. Sort by year (descending) by default; offer a theme-based sort as an alternative.
7. Run a gap analysis: which dimension values are over-represented (clusters) and which are empty (gaps).
8. Emit a companion narrative paragraph that interprets the clusters and gaps.
9. Cross-check that every row's "relevance" cell ties to the user's research question.

## Inputs

- The list of papers (`.bib`, DOIs, or titles).
- The dimension schema (default: year, methodology, dataset, sample size, key findings, limitations, relevance).
- The user's research question or thesis topic.
- Sort preference (year descending vs. theme).

## Outputs

- `literature_matrix.md` — Markdown table.
- `literature_matrix.csv` — same content, machine-readable.
- `gap_analysis.md` — clusters, gaps, and a short narrative interpretation.
- `theme_index.md` — list of themes with the count of papers per theme.

## Key Rules

- Every cell must be sourced from the paper itself — never inferred or fabricated.
- Categorical values must be normalized to a controlled vocabulary before clustering.
- Each row must populate the relevance column with an explicit tie to the user's research question.
- The matrix must include every paper in the candidate set; exclusions require a stated reason.
- Cluster and gap claims must be backed by counts from the matrix.
- A paper with missing dimensions must be flagged `[MISSING]`, not silently left blank.

## Examples

```text
| Year | Author        | Method  | Dataset           | N      | Key finding                                     | Limitations                | Relevance to our work        |
|------|---------------|---------|-------------------|--------|-------------------------------------------------|----------------------------|------------------------------|
| 2023 | Wang et al.   | RCT     | MIMIC-IV          | 12,400 | 14% lower mortality with early intervention     | Single-center              | Validates our population     |
| 2022 | Lee et al.    | Cohort  | UK Biobank        | 88,000 | Long-term BP effect modest (3 mmHg)             | Self-reported adherence     | Bounds our expected effect   |
| 2021 | Smith et al.  | Cross-sec.| NHANES          | 6,200  | Prevalence of stage 2 HTN 18.4%                 | No causal claims possible   | Defines our target segment   |
```

```text
Gap analysis excerpt:
  Cluster: 6 of 9 papers use MIMIC-IV → over-reliance on US ICU data.
  Gap: 0 of 9 papers address pediatric populations → pediatric gap.
  Gap: 0 of 9 papers report outcomes beyond 24 months → long-term gap.
  Narrative: The literature converges on short-term adult ICU outcomes,
  leaving pediatric and long-term effects as open research directions.
```

## Common Pitfalls

- Leaving cells blank instead of marking `[MISSING]` — silent gaps distort the gap analysis.
- Failing to normalize categorical values, so "RCT" and "randomized controlled trial" count as two distinct
  methodologies.
- Inferring cells from abstracts alone — for methods and limitations, the full PDF is often required.
- Forcing a paper into a theme where it does not fit; an "Other" theme is better than misclassification.
- Claiming clusters or gaps without backing counts — every claim must trace to matrix data.

## References

- Garrard, J. (2013). *Health Sciences Literature Review Made Easy*. Jones & Bartlett — on the matrix method.
- PRISMA 2020 statement: https://www.prisma-statement.org/ — for systematic-review reporting.
- Booth, A., Papaioannou, D., & Sutton, A. (2012). *Systematic Approaches to a Successful Literature Review*. SAGE.
- Arksey, H., & O'Malley, L. (2005). Scoping studies: Towards a methodological framework. *International Journal of
  Social Research Methodology*, 8(1), 19-32.
- Tricco, A. C., et al. (2018). PRISMA extension for scoping reviews (PRISMA-ScR). *Annals of Internal Medicine*, 169
  (7), 467-473.
- Covidence systematic review software: https://www.covidence.org/ — for collaborative matrix building.
