---
name: claim-source-tracer
description: Map every factual claim in a manuscript to its originating binder, page, line, and citation, producing a verification table and a separate unverified-sources list. Use when auditing a paper against a research binder, checking whether every claim has a traceable origin, or preparing for editorial review.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [verification, claims, citations, binder, traceability]
related: [style-integrity/zero-fabrication-guard, style-integrity/cross-reference-validator, academic-research/supplementary-materials-organizer]
prerequisites: []
outputs: [markdown, json]
difficulty: advanced
estimated_tokens: 810
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Claim Source Tracer

## When To Use

- User submits a manuscript plus a research binder (PDFs, notes, annotated PDFs) and asks to verify every claim.
- An editor or co-author requests a "claim-to-source" traceability matrix.
- A pre-submission audit requires every factual statement to have a citable origin.
- A reviewer challenge is anticipated and the team needs the exact quote and page number.

## Workflow

1. Parse the manuscript into atomic factual claims (one claim per row).
2. Number each claim sequentially: `C001`, `C002`, …, in document order.
3. For each claim, identify the cited reference (BibTeX key) if present.
4. Open the corresponding binder file (PDF, Markdown, plain text).
5. Locate the supporting quote: record `BinderName`, `BinderPage`, `BinderLine`, `ExactBinderQuote`.
6. Compare the manuscript's phrasing against the binder's exact quote. Mark `IsMatching` as `Yes`, `Partial`, or `No`.
7. If no binder entry supports the claim, record it in the "Unverified or Missing Sources" table.
8. For numerical claims, confirm the number, the metric, the unit, and the experimental setting match the binder's table
   or text.
9. Produce two tables: (a) the verification matrix and (b) the unverified-sources list.
10. Append a Planning Note summarizing claims that need additional sourcing.

## Inputs

- Manuscript source text (`.tex`, `.md`, or plain text).
- Research binder: a directory of source PDFs, notes, and BibTeX file (`.bib`).
- Optional index file mapping BibTeX keys to binder filenames.

## Outputs

- **Verification Table** with columns: `IndexNumber`, `BibtexKeyword`, `Authors`, `StudyTitle`, `Journal`,
  `ManuscriptCitedSection`, `CitedTextOrResults`, `BinderName`, `BinderPage`, `BinderLine`, `ExactBinderQuote`,
  `IsMatching`.
- **Unverified or Missing Sources** table with columns: `IndexNumber`, `ClaimText`, `ManuscriptCitedSection`,
  `ReasonMissing`.
- A Planning Note at the end listing what the user must provide to close each gap.

## Key Rules

- Every factual claim gets exactly one row in the verification table.
- Claims without a binder match go to the "Unverified or Missing Sources" table — never silently dropped.
- The `ExactBinderQuote` must be a verbatim copy from the binder, with ellipses for elisions and brackets for
  insertions.
- `IsMatching` accepts only three values: `Yes`, `Partial`, `No`.
- Numerical claims must cite the binder page AND the exact cell or sentence.
- A claim is treated as atomic: one claim per row, never multiple claims merged.
- The `ManuscriptCitedSection` uses the section number plus paragraph index for precise location.
- Verbatim quotes preserve the binder's original spelling and punctuation.

## Examples

Verification Table (excerpt):

| IndexNumber | BibtexKeyword | Authors   | StudyTitle    | Journal | ManuscriptCitedSection | CitedTextOrResults          | BinderName    | BinderPage | BinderLine | ExactBinderQuote                          | IsMatching      |
|-------------|---------------|-----------|---------------|---------|------------------------|-----------------------------|---------------|------------|------------|-------------------------------------------|-----------------|
| C001        | smith2024     | Smith, J. | Deep features | NeurIPS | Sec. 3.1               | 94.2% accuracy              | smith2024.pdf | 7          | 12         | "Our model reaches 94.2% top-1 accuracy." | Yes             |
| C002        | lee2023       | Lee, K.   | Edge cases    | ICML    | Sec. 4                 | failure rate 2.1%           | lee2023.pdf   | 11         | 4          | "failure rate of 2.1% under noise."       | Yes             |
| C003        | —             | —         | —             | —       | Sec. 5                 | "commonly used in practice" | —             | —          | —          | —                                         | No (unverified) |

Unverified or Missing Sources:

| IndexNumber | ClaimText                   | ManuscriptCitedSection | ReasonMissing                         |
|-------------|-----------------------------|------------------------|---------------------------------------|
| C003        | "commonly used in practice" | Sec. 5                 | No binder entry or citation provided. |

Planning Note (appended):

```
Planning Note:
- C003 needs a supporting reference or removal. Suggested candidate:
  jones2022 (not in binder). Request the BibTeX entry from the user.
- C002 marked Partial on second read: the binder's setting is "noise
  level 0.1" while the manuscript omits the noise level. Add the
  qualifier to the manuscript sentence.
```
