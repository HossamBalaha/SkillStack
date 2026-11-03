---
name: supplementary-materials-organizer
description: Organize supplementary materials (math derivations, additional figures, full tables, code release, dataset, model weights, video demos) and cross-reference every supplementary item from the main text. Use when the user is finalizing a journal submission and needs the supplementary package structured, indexed, and cross-referenced from the main manuscript.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [supplementary, appendix, cross-reference, multimedia, code-release]
related: [academic-research/journal-manuscript-writer, style-integrity/cross-reference-validator, academic-research/reproducibility-checklist-author]
prerequisites: []
outputs: [latex, markdown]
difficulty: intermediate
estimated_tokens: 820
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Supplementary Materials Organizer

## When To Use

- The user asks to "organize supplementary", "what goes in the appendix", or "cross-reference supplementary".
- The user is finalizing a journal submission with an appendix, code release, dataset, weights, or video demos.
- The user needs every supplementary item referenced from the main text.
- Trigger keywords: supplementary, appendix, supplementary code, model weights, video demo, cross-reference.

## Workflow

1. Inventory all candidate supplementary artifacts: derivations, extra figures, full tables, code, dataset, weights,
   video demos.
2. Categorize: Supplementary Document (LaTeX, single PDF), Supplementary Code (GitHub+Zenodo), Supplementary Data
   (Zenodo/Figshare), Supplementary Multimedia (MP4 on Figshare/YouTube).
3. Assign every item a stable ID: S1, S2, S3, ... Tables: ST1, ST2; Figures: SF1, SF2; Equations: SE1; Code: SC1; Data:
   SD1; Video: SV1.
4. For each item, draft a one-line description and a permanent URL or DOI.
5. Cross-reference every item from the main text: "(see Supplementary Equation SE1)" or "(see Supplementary Table ST2)".
6. Build a Supplementary Index table at the top of the supplementary PDF listing every item with its ID and URL.
7. For math derivations, structure them as numbered supplementary equations referenced from the main text.
8. For full tables, ensure column headers match the main text conventions; mark significant results with the same stars.
9. For code/data/weights, link to the DOI-minted archive; include SHA-256 checksums.
10. For video demos, embed a thumbnail in the supplementary PDF and link to the hosted MP4.
11. Run a cross-reference audit: every ID appears at least once in the main text; every main-text reference resolves to
    an existing ID.

## Inputs

- Main manuscript draft (for cross-reference insertion).
- List of supplementary artifacts with descriptions.
- Code repository URL and DOI.
- Dataset archive DOI.
- Optional: video demo files.

## Outputs

- `supplementary.tex` — single supplementary PDF source with index, equations, figures, tables.
- `supplementary_index.md` — ID, type, description, URL/DOI table.
- `cross_reference_audit.md` — main-text mentions vs. supplementary IDs.
- `code_release.md`, `data_release.md`, `weights_release.md` — DOI links and checksums.
- `video_demo.md` — video metadata and hosting link.

## Key Rules

- Every supplementary item has a stable ID (S1, SF1, ST1, SE1, SC1, SD1, SV1).
- Every ID is referenced at least once from the main text.
- Supplementary PDF opens with an Index table listing every item and its URL/DOI.
- Tables and figures in supplementary reuse main-text conventions (column headers, stars, color palette).
- Code/data/weights have DOIs and SHA-256 checksums.
- Video demos have a thumbnail and caption in the supplementary PDF.

## Examples

```text
Supplementary Index (excerpt):
  ID  | Type     | Description                          | URL/DOI
  SF1 | Figure   | Per-site topology descriptor plots   | supplementary.pdf#SF1
  ST1 | Table    | Full ablation (2^3 factorial)        | supplementary.pdf#ST1
  SE1 | Equation | Derivation of topology regularizer   | supplementary.pdf#SE1
  SC1 | Code     | Reproducible code release             | 10.5281/zenodo.1234567
  SD1 | Data     | Multi-site MRI benchmark               | 10.5281/zenodo.7654321
  SV1 | Video    | Demo: training dynamics over epochs    | https://figshare.com/...
```

```text
Main-text cross-reference (excerpt):
  "The topology regularizer (Supplementary Equation SE1) is derived by
   integrating persistent-homology descriptors across scales. Full per-site
   descriptors are shown in Supplementary Figure SF1, and the complete
   2^3 ablation is reported in Supplementary Table ST1."
```

## Notes

- Re-run the cross-reference audit every time the main text or the supplementary PDF changes.
- Keep supplementary table styles consistent with the main paper so reviewers can compare rows directly.
- Cap each video at the venue's recommended length and host a downloadable MP4 alongside streaming embeds.
