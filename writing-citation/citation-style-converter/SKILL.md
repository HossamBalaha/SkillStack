---
name: citation-style-converter
description: Converts bibliographies and inline citations between IEEE, APA, Chicago, Vancouver, and MLA styles while keeping citekeys and the bibliography in sync. Use when a manuscript is retargeted to a journal with a different citation style, or when an existing `.bib` or inline citations must be reformatted wholesale.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [citation, ieee, apa, chicago, vancouver]
related: [writing-citation/bibtex-citation-manager, writing-citation/reference-list-formatter]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Citation Style Converter

## When To Use

- The same manuscript is being submitted to two journals with different citation styles (e.g., IEEE numbered vs. APA
  author-date).
- You inherited a draft with mixed citation conventions and need to unify it.
- A `.bib` exists but the bibliography style file (`.bst`/`.bbx`) is misaligned with the inline `\cite{}` macros.
- A co-author added references in MLA style and you write in a biblatex/IEEE project.

## Workflow

1. Identify the source style by inspecting the inline citations and a sample bibliography entry.
2. Identify the target style from the journal's author guide.
3. Normalize the bibliography to a canonical `.bib` if the source was inline citations (parse author, year, title,
   container, pages, DOI).
4. Map inline citation macros to the target style:
    - IEEE → `\cite{}` with numbered output `[1]`.
    - APA → `\citep{}` / `\citet{}` rendering `(Author, Year)`.
    - Chicago notes-bibliography → `\autocite{}` producing a footnote.
    - Vancouver → numbered `[1]` (biomedical).
    - MLA → `(Author Page)`.
5. Switch the biblatex style: `style=ieee`, `style=apa`, `style=chicago` (authoryear), etc.
6. Re-render the bibliography and confirm ordering (alphabetical for APA/MLA/Chicago; citation order for
   IEEE/Vancouver).
7. Diff the source and target outputs to confirm no entry was dropped or duplicated.
8. Emit the converted `.tex`, the new `.bib`, and a side-by-side style comparison.

## Inputs

- Source `.tex` and `.bib` (or a Markdown/DOCX draft with inline citations).
- Target style declaration (one of: IEEE, APA, Chicago notes, Chicago author-date, Vancouver, MLA).
- Optional journal-specific style file (`.bst` or `.bbx`).

## Outputs

- `manuscript_<target_style>.tex` — converted manuscript.
- `references_<target_style>.bib` — bibliography aligned with the target style.
- `style_diff.md` — before/after table for spot-check entries.

## Key Rules

- The bibliography style and the inline citation macros must be the same family (biblatex with biblatex-style, or BibTeX
  with `.bst`).
- Numbered styles (IEEE, Vancouver) sort by citation order; author-date styles (APA, Chicago author-date, MLA) sort
  alphabetically — do not preserve source order blindly.
- Page references in MLA `(Author 23)` must be preserved when converting from another style that loses page specificity.
- Citekeys must remain stable across the conversion — only rendering changes.
- A re-rendered bibliography must contain exactly the same set of entries as the source (no drops, no duplicates).
- When converting TO a numbered style, the first-cited entry receives `[1]`.

## Examples

```text
Source (APA):
  Inline: (Smith & Patel, 2021)
  Bibliography: Smith, J., & Patel, R. (2021). A survey of federated learning.
                ACM Computing Surveys, 54(2), 1-38.

After conversion to IEEE:
  Inline: [1]
  Bibliography: [1] J. Smith and R. Patel, "A survey of federated learning,"
                ACM Comput. Surv., vol. 54, no. 2, pp. 1-38, 2021.

After conversion to MLA:
  Inline: (Smith and Patel 12)
  Bibliography: Smith, J., and R. Patel. "A Survey of Federated Learning."
                ACM Computing Surveys, vol. 54, no. 2, 2021, pp. 1-38.

After conversion to Vancouver:
  Inline: [1]
  Bibliography: 1. Smith J, Patel R. A survey of federated learning.
                ACM Comput Surv. 2021;54(2):1-38.
```

```text
biblatex switch (LaTeX preamble):
  % Source:
  \usepackage[style=apa]{biblatex}
  % Target (IEEE):
  \usepackage[style=ieee]{biblatex}
  \addbibresource{references.bib}
```

## References

- biblatex style options: `style=ieee`, `style=apa`, `style=chicago`, `style=mla`, `style=numeric` (for Vancouver-like).
- IEEE Editorial Style Manual.
- APA Style and Grammar Guidelines: https://apastyle.apa.org/.
- Chicago Manual of Style Online: https://www.chicagomanualofstyle.org/.
