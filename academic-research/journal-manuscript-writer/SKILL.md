---
name: journal-manuscript-writer
description: 'Draft publication-ready journal sections in LaTeX with strict structural style: only \section and \subsection (no \subsubsection), separator comments around floats, IEEE citation style, and mandatory back-matter sections. Use when the user asks to write, format, or polish a journal article draft for IEEE, Elsevier, or comparable venues.'
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: academic-research
tags: [latex, manuscript, journal, imrad, writing]
related: [style-integrity/latex-style-guard, academic-research/related-work-surveyor, academic-research/supplementary-materials-organizer]
prerequisites: [style-integrity/latex-style-guard]
outputs: [latex]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Journal Manuscript Writer

## When To Use
- The user asks to "write the manuscript", "draft Section 3", or "format my paper in LaTeX".
- The target is a journal (IEEE TPAMI, Medical Image Analysis, Nature Scientific Reports, Elsevier).
- The user needs mandatory back-matter (CRediT, Funding, IRB, Data Availability, Conflicts, Abbreviations).
- Trigger keywords: manuscript, LaTeX draft, IEEEtran, elsevier, back-matter, keywords, citations.

## Workflow
1. Confirm target venue, document class (e.g., `IEEEtran`, `elsarticle`), and bibliography style (e.g., `IEEEtran`, `elsarticle-num`).
2. Draft the abstract (150-250 words). Append 4-6 keywords after the abstract in venue-required format.
3. Outline Introduction, Related Work, Methodology, Experiments, Discussion, Conclusion.
4. Write each section using only `\section{}` and `\subsection{}`. Never use `\subsubsection`.
5. Insert a blank line after every `\section` and `\subsection` command.
6. Wrap every float, equation, table, figure, and algorithm with `% ====================== %` separator lines.
7. Use LaTeX-style quotes: ``double'' and `single'. Never use straight quotes.
8. Restrict `\textbf{}` to structural hierarchy (section heads, table column headers). Never use `\textit{}`; switch to `\emph{}` only when semantics demand emphasis.
9. Cite using `\cite{}` (IEEE numbered style). Group multiple citations as `\cite{a, b, c}` sorted ascending.
10. Append mandatory back-matter: CRediT author contributions, Funding, IRB/ethics approval, Informed Consent, Data Availability, Conflicts of Interest, Abbreviations.
11. Compile-check mentally: every `\label{}` has a matching `\ref{}` or `\eqref{}`.
12. Run a final pass for orphaned subsections (no `\subsection` without an enclosing `\section`).

## Inputs
- Target venue and document class.
- Project plan / executive summary from the ideation step.
- Figures, tables, equations (as LaTeX source or descriptions).
- Bibliography file (`refs.bib`) or list of DOIs to format.
- Author list with affiliations and CRediT roles.

## Outputs
- `main.tex` — single root file or `\input{}` includes per section.
- `sections/01_intro.tex`, `02_related.tex`, `03_method.tex`, `04_experiments.tex`, `05_discussion.tex`, `06_conclusion.tex`.
- `backmatter.tex` — CRediT, Funding, IRB, Informed Consent, Data Availability, Conflicts, Abbreviations.
- `refs.bib` — IEEE-style bibliography entries.
- Compilation checklist (labels, refs, floats, citations).

## Key Rules
- Only `\section` and `\subsection`. Never `\subsubsection`.
- Blank line after every sectioning command.
- `% ====================== %` around every float, equation, table, figure, algorithm.
- Use ``...'' and `...' for quotes; never straight quotes.
- No `\textit{}` anywhere; `\textbf{}` only for structural hierarchy.
- IEEE numbered citations grouped and sorted.
- Mandatory back-matter present even if some fields say "Not applicable".
- 4-6 keywords immediately after the abstract.

## Examples
```latex
% ====================== %
\section{Methodology}
% ====================== %

\subsection{Problem Formulation}

Let $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{N}$ denote the training set. The objective
is to minimize the empirical risk

% ====================== %
\begin{equation}
\label{eq:empirical_risk}
\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f_\theta(x_i), y_i).
\end{equation}
% ====================== %

As shown in Fig.~\ref{fig:pipeline}, the proposed model ``FedTopo'' combines
topology regularization with batch-norm-aware aggregation.
```
```latex
% ====================== %
\section*{Data Availability}
% ====================== %
The multi-site MRI dataset used in this study is available from
\url{https://example.org/data} under the CC-BY-NC 4.0 license. Code
and trained weights are released at \url{https://github.com/...}.
```

## References
- IEEEtran template and author guide: https://journals.ieeeauthorcenter.ieee.org/
- Elsevier elsarticle class: https://www.ctan.org/pkg/elsarticle
- CRediT taxonomy: https://credit.niso.org/
- LaTeX float placement guide (Overleaf): https://www.overleaf.com/learn/latex/Positioning_images_and_tables
