---
name: journal-manuscript-writer-lite
description: Draft publication-ready journal sections in LaTeX with strict structural style: only \section and \subsection (no \subsubsection), separator comments around floats, IEEE citation style, and mandatory back-matter sections. Use when the user asks to write, format, or polish a journal article draft for IEEE, Elsevier, or comparable venues.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
  lite: true
  full_version: journal-manuscript-writer/SKILL.md
---

# Journal Manuscript Writer (Lite)

> Condensed version. Load `journal-manuscript-writer/SKILL.md` for the full workflow.

Drafts publication-ready LaTeX journal sections for IEEE/Elsevier-style venues with strict structural style and mandatory back-matter.

## Top 3 Workflow Steps
1. Confirm target venue, document class (`IEEEtran`, `elsarticle`), and bibliography style; draft the 150-250 word abstract followed by 4-6 keywords in venue-required format.
2. Outline and write Introduction, Related Work, Methodology, Experiments, Discussion, Conclusion using ONLY `\section{}` and `\subsection{}` (never `\subsubsection`); insert a blank line after every sectioning command.
3. Wrap every float/equation/table/figure/algorithm with `% ====================== %` separators; use LaTeX-style quotes (`` ``...'' ``, `` `...' ``); cite via IEEE numbered `\cite{}` grouped and sorted ascending; append mandatory back-matter (CRediT, Funding, IRB, Informed Consent, Data Availability, Conflicts, Abbreviations); compile-check labels/refs and run an orphaned-subsection pass.

## Top 3 Key Rules
1. **Only `\section` and `\subsection`** — never `\subsubsection`; one blank line after every sectioning command; `% ====================== %` separators wrap every float/equation/table/figure/algorithm.
2. **Quotes & emphasis**: `` ``...'' `` double and `` `...' `` single only (no straight quotes); `\textit{}` forbidden everywhere — switch to `\emph{}` only when semantics demand; `\textbf{}` restricted to structural hierarchy.
3. **IEEE numbered citations** grouped as `\cite{a, b, c}` sorted ascending; **mandatory back-matter present even if "Not applicable"**; **4-6 keywords immediately after the abstract**; every `\label{}` must have a matching `\ref{}`/`\eqref{}`.
