---
name: latex-style-guard-lite
description: Enforce strict LaTeX typography and structural formatting rules on manuscripts before submission. Use when editing .tex files, reviewing equations, figures, tables, algorithms, or normalizing quote styles and float placements for camera-ready papers.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity

lite: true
full_version: latex-style-guard/SKILL.md
language: en
---

# LaTeX Style Guard (Lite)

> Condensed version. Load `latex-style-guard/SKILL.md` for the full workflow.

Enforces strict LaTeX typography, blank-line, quote-style, and float-placement rules on `.tex` manuscripts before
camera-ready submission.

## Top 3 Workflow Steps

1. Read the entire `.tex` source end-to-end before editing; verify exactly one blank line after each `\section{}`/
   `\subsection{}` and one blank line before AND after every float/equation/table/figure/algorithm block.
2. Insert `% ====================== %` separator lines on their own line immediately before AND after each equation,
   table, figure, and algorithm block (NEVER around `\section{}`); normalize quotes (`` ``...'' `` double, `` `...' ``
   single; straight quotes forbidden).
3. Replace every `\subsubsection{Title}` with inline `\textbf{Title.}`; move punctuation OUTSIDE `\ref{}`/`\cite{}`
   braces; redefine `\fps@figure` and `\fps@table` to `!htb` in the preamble; re-read the patched file and report
   transformation counts.

## Top 3 Key Rules

1. **Blank lines**: exactly ONE after `\section{}`/`\subsection{}`; ONE before AND after every float/equation
   environment. **Separators** (`% ====================== %`) wrap equations, tables, figures, algorithms ONLY — never
   section commands.
2. **Quotes and emphasis**: `` ``...'' `` for double quotes, `` `...' `` for single quotes; `\textit{}
   ` is forbidden entirely; `\textbf{}` reserved for structural hierarchy only.
3. **No `\subsubsection{}`** — use inline `\textbf{Inline Heading.}`. **Punctuation sits OUTSIDE** closing brace of
   `\ref{}`, `\cite{}`, `\eqref{}`. **Float placement defaults to `[!htb]`** via `\fps@...` redefinitions, not per-float
   overrides.
