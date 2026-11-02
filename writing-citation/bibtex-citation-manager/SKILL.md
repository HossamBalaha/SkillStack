---
name: bibtex-citation-manager
description: Manages BibTeX bibliography databases by generating stable citekeys, deduplicating entries, validating required fields, and enforcing IEEE citation style. Use when curating a .bib file, cleaning up duplicate or malformed entries, or aligning citation keys with the LaTeX `\cite{}` and `\bibitem{}` commands.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [bibtex, citations, latex, ieee]
related: [writing-citation/doi-verifier, writing-citation/citation-style-converter, writing-citation/reference-list-formatter, style-integrity/cross-reference-validator]
prerequisites: []
outputs: [latex, bash]
difficulty: intermediate
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# BibTeX Citation Manager

## When To Use

- You are handed a `.bib` file with inconsistent citekeys (e.g., `smith2021a`, `Smith_21`, `paper1`) and need to
  normalize them.
- The same DOI appears under two different entries and must be merged without losing fields.
- A LaTeX build reports "undefined references" or "multiply defined" citekeys.
- The target venue requires IEEE numbered citation style `[1]` and you must reformat the bibliography.
- A reviewer flagged missing required fields (volume, pages, year) on specific entries.

## Workflow

1. Parse the input `.bib` file into structured entries (entry type, fields, citekey).
2. Normalize field names to canonical BibTeX (e.g., `journal` not `journalname`; `pages` not `page-range`).
3. Generate stable citekeys using the pattern `Author + Year + FirstContentWord` (e.g., `Wang2023Federated`); append
   `a`, `b`, `c` for same-author/same-year collisions.
4. Detect duplicates by DOI, then by (title + first-author + year); merge fields giving priority to the entry with the
   most complete record.
5. Validate required fields per entry type: `@article` needs author, title, journal, year, volume, pages;
   `@inproceedings` needs author, title, booktitle, year; `@book` needs author/editor, title, publisher, year.
6. Cross-check that every `\bibitem{X}` in the bibliography is referenced by at least one `\cite{X}` (or variant
   `\citep`, `\citet`) in the `.tex` source.
7. Apply IEEE style transformation to each entry: `[N] A. B. Author, "Title," Journal, vol. X, no. Y, pp. Z–W, Year.`
8. Emit a cleaned `.bib`, a report of merged/removed entries, and a list of orphan citekeys.

## Inputs

- One or more `.bib` files.
- Optionally the `.tex` manuscript to test cite-key usage.
- Target style declaration (default: IEEE numbered).

## Outputs

- `references_clean.bib` — normalized, deduplicated bibliography.
- `citation_report.md` — table of actions taken per entry (kept, merged, renamed, dropped).
- `ieee_style_bibliography.tex` — formatted `\begin{thebibliography}` block ready to paste.

## Key Rules

- Citekeys must be ASCII, start with a letter, and contain no spaces.
- Never drop a field during merge — union the fields, preferring the more complete source.
- A DOI is the strongest duplicate signal; (title + first-author + year) is the fallback.
- Orphan `\bibitem`s that are never cited must be flagged, not silently removed.
- Required-field violations are errors, not warnings; surface them explicitly.
- Preserve original citekeys in the report so the author can audit renames.

## Examples

```text
Before:
@article{paper1,
  author = {John Smith and Wei Zhang},
  title = {Federated learning at scale},
  journal = {IEEE TPAMI},
  year = {2023}
}
@article{Smith2023Federated,
  author = {J. Smith and W. Zhang},
  title = {Federated Learning at Scale},
  journal = {IEEE Trans. Pattern Anal. Mach. Intell.},
  year = {2023},
  volume = {45},
  pages = {1024--1038},
  doi = {10.1109/TPAMI.2023.123456}
}

After (merged, IEEE formatted):
[1] J. Smith and W. Zhang, "Federated learning at scale," IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, pp. 1024–1038, 2023.
```

```text
Validation report excerpt:
  @article{Lee2022Sparse}  — MISSING: volume, pages  -> ERROR
  @inproceedings{Ng2021}    — OK
  Citekey 'Brown2020Survey' is defined but never \cite'd  -> ORPHAN
```

## References

- LaTeX bibliography management
  overview: https://resources.latex-cloud-studio.com/learn/latex/bibliography/bibliography-management-bibtex
- IEEE Editorial Style Manual (citation format reference).
- `biblatex` package documentation for field-name normalization.
