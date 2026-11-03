---
name: reference-list-formatter
description: Formats reference lists in any citation style from a `.bib` source, applying author-name order, italics, punctuation, and abbreviated-vs-full journal-name rules. Use when producing the final bibliography block for a manuscript, or when a journal's copyeditor has requested style-compliant reference formatting.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [bibliography, reference-list, citation-style, italics, bibtex]
related: [writing-citation/bibtex-citation-manager, writing-citation/citation-style-converter]
prerequisites: []
outputs: [latex, markdown]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Reference List Formatter

## When To Use

- The manuscript is final and the bibliography must be rendered in the exact journal style.
- The journal requires abbreviated journal names (e.g., ISO 4 / NLM) but your `.bib` has full names.
- You need a plain-text reference list (no LaTeX) for a non-LaTeX submission portal.
- A copyeditor flagged inconsistent italics or punctuation across reference entries.

## Workflow

1. Load the `.bib` and the list of citekeys actually cited in the manuscript (from the `.aux` file or a manual scan).
2. Filter the bibliography: keep only entries that appear at least once in the manuscript; flag orphans.
3. Apply author-name formatting per style (IEEE: initials before surname; APA: surname first, then initials; MLA:
   surname, first name).
4. Apply container formatting (italicize journal title for APA/MLA; italicize volume only for some styles).
5. Convert journal names to the abbreviated form if the style requires it (ISO 4 via the ISSN List of Title Word
   Abbreviations).
6. Apply punctuation rules: comma vs. period between fields, en-dash for page ranges, and trailing period.
7. Order the list per the style: alphabetical (APA, MLA, Chicago author-date), citation order (IEEE, Vancouver).
8. Render either as a LaTeX `\begin{thebibliography}...\end{thebibliography}` block or as a plain-text list.
9. Cross-check every cited key against the rendered list; report any missing entries.

## Inputs

- The `.bib` file.
- The cited-keys list (from `.aux` or a manual extraction).
- Target style declaration (IEEE, APA, Chicago, Vancouver, MLA, journal-specific).
- Journal abbreviation preference: full names, ISO 4 abbreviations, or NLM abbreviations.

## Outputs

- `references_formatted.tex` — the `\begin{thebibliography}` block (LaTeX path).
- `references_formatted.txt` — the plain-text reference list (non-LaTeX path).
- `formatting_report.md` — entry-by-entry log of name order, italicization, and abbreviation decisions.
- `orphan_report.md` — entries in the `.bib` that were never cited.

## Key Rules

- Every entry in the rendered list must be cited at least once in the manuscript.
- Page ranges use an en-dash (–), not a hyphen (-).
- Journal-name abbreviation must be consistent across the entire list.
- Author surname must precede initials for the first author in author-date styles; subsequent authors may be "first name
  initial + surname" per style.
- Italics applied to journal title (APA) or volume number (some biomedical styles) must be consistent.
- The list must be sorted exactly as the style mandates; alphabetical sort must use the first author's surname.

## Examples

```text
Before (.bib entry):
@article{Chronis2024Survey,
  author = {Christos Chronis and Iraklis Varlamis and Yassine Himeur and Ahmed N. Sayed and Tarek M. Al-Hasan and Aneeba Nhlabatsi and George Dimitrakopoulos},
  title = {A survey on the use of federated learning in privacy-preserving recommender systems},
  journal = {IEEE Open Journal of the Computer Society},
  year = {2024},
  volume = {5},
  pages = {227--247},
  doi = {10.1109/OJCS.2024.3396344}
}

After (IEEE LaTeX block):
\begin{thebibliography}{99}
\bibitem{Chronis2024Survey}
C. Chronis, I. Varlamis, Y. Himeur, A. N. Sayed, T. M. Al-Hasan, A. Nhlabatsi, and G. Dimitrakopoulos, ``A survey on the use of federated learning in privacy-preserving recommender systems,''
\emph{IEEE OJCS}, vol. 5, pp. 227--247, 2024.
\end{thebibliography}

After (APA plain text):
Chronis, C., Varlamis, I., Himeur, Y., Sayed, A. N., Al-Hasan, T. M., Nhlabatsi, A., ... & Dimitrakopoulos, G. (2024). A survey on the use of federated learning in privacy-preserving recommender systems. IEEE Open Journal of the Computer Society, 5, 227-247. https://doi.org/10.1109/OJCS.2024.3396344

After (Vancouver, abbreviated journal):
Chronis C, Varlamis I, Himeur Y, et al. A survey on the use of federated learning in privacy-preserving recommender systems. IEEE OJCS.
2021;54(2):1-38.
```

```text
Orphan report:
  @inproceedings{Brown2020Old} — defined in .bib but never \cite'd.
  Action: flagged for author review (do not auto-remove).
```
