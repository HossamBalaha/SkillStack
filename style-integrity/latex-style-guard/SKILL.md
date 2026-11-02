---
name: latex-style-guard
description: Enforce strict LaTeX typography and structural formatting rules on manuscripts before submission. Use when editing .tex files, reviewing equations, figures, tables, algorithms, or normalizing quote styles and float placements for camera-ready papers.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: style-integrity
tags: [latex, typography, manuscript, formatting, camera-ready]
related: [style-integrity/cross-reference-validator, style-integrity/notation-consistency-checker, academic-research/journal-manuscript-writer]
prerequisites: []
outputs: [latex, markdown]
difficulty: advanced
estimated_tokens: 880
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# LaTeX Style Guard

## When To Use
- User submits a `.tex` file and asks for "formatting cleanup", "style check", or "camera-ready preparation".
- A manuscript has inconsistent blank lines around floats, equations, or section commands.
- Inline quotes appear as straight `"text"` or `"text"` rather than LaTeX-style ``text''.
- The body uses `\subsubsection{}` instead of inline bold headings.
- Equations or floats lack separator comment lines.

## Workflow
1. Read the entire `.tex` source file end-to-end before editing.
2. Verify there is exactly one blank line after every `\section{}` and `\subsection{}` command.
3. Confirm exactly one blank line before AND after each floating environment: `table`, `figure`, `algorithm`, and any `equation`/`align` block.
4. Insert `% ====================== %` separator lines on their own line immediately before AND after each equation, table, figure, and algorithm block. Do NOT add separators around `\section{}` commands.
5. Replace all double quotes with `` `` `` open and `''` close, and single quotes with `` ` `` open and `'` close.
6. Audit `\textbf{}` usage: keep only for structural hierarchy (section-like emphasis). Remove decorative bolding from inline prose.
7. Delete every `\textit{}` occurrence. If emphasis is essential, restructure the sentence instead.
8. Replace every `\subsubsection{Title}` with `\textbf{Title.}` rendered inline at the start of the following paragraph.
9. Move punctuation OUTSIDE `\ref{}` and `\cite{}` closing braces: write `Figure~\ref{fig:x}.` not `Figure~\ref{fig:x.}`.
10. Redefine default float placement in the preamble:
    ```latex
    \makeatletter
    \renewcommand{\fps@figure}{!htb}
    \renewcommand{\fps@table}{!htb}
    \makeatother
    ```
11. Re-read the patched file to confirm all rules hold consistently.
12. Report the count of each transformation applied.

## Inputs
- Path to one or more `.tex` files (single-file or multi-file project via `\input{}`/`\include{}`).
- Target venue style guide if available (overrides defaults where it conflicts).
- Any existing preamble macros the user wants preserved.

## Outputs
- Modified `.tex` file(s) with all rules applied.
- A short summary table: rule name, occurrences found, occurrences fixed.

## Key Rules
- Exactly ONE blank line after every `\section{}` and `\subsection{}`.
- Exactly ONE blank line before AND after every float/equation environment.
- `% ====================== %` separators wrap equations, tables, figures, algorithms ONLY, never section commands.
- `` ``text'' `` for double quotes, `` `text' `` for single quotes. Straight quotes are forbidden.
- `\textbf{}` is reserved for structural hierarchy; `\textit{}` is forbidden entirely.
- `\subsubsection{}` is forbidden. Use `\textbf{Inline Heading.}` inline.
- Punctuation sits OUTSIDE the closing brace of `\ref{}`, `\cite{}`, `\eqref{}`.
- Float placement defaults to `[!htb]` via `\fps@...` redefinitions, not per-float overrides.

## Examples

Before:
```latex
\subsection{Method}
We define the loss as:
\begin{equation}
L = (y - \hat{y})^2
\end{equation}
The "standard" approach is shown in Figure~\ref{fig:x.}.
```

After:
```latex
\subsection{Method}

We define the loss as:

% ====================== %
\begin{equation}
L = (y - \hat{y})^2
\end{equation}
% ====================== %

The ``standard'' approach is shown in Figure~\ref{fig:x}.
```

## References
- Leslie Lamport, *LaTeX: A Document Preparation System* (2nd ed.).
- The TeX FAQ on float placement: https://texfaq.org/FAQ-floats
- `amsmath` user guide (AMS) for equation environments.
