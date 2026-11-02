---
name: cross-reference-validator
description: Verify that every `\label{}` in a LaTeX manuscript has a corresponding `\ref{}`, and vice versa, that every float and equation is cross-referenced, and that punctuation sits outside the closing brace. Use when finalizing a LaTeX manuscript, debugging undefined-reference warnings, or auditing cross-reference integrity before submission.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [latex, cross-reference, label, ref, floats]
related: [style-integrity/latex-style-guard, style-integrity/notation-consistency-checker, academic-research/supplementary-materials-organizer]
prerequisites: []
outputs: [latex, markdown]
difficulty: intermediate
estimated_tokens: 860
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Cross-Reference Validator

## When To Use

- A LaTeX manuscript reports `undefined reference` or `multiply defined` warnings.
- A pre-submission check requires every equation, table, figure, and algorithm to be cross-referenced.
- A reviewer may challenge an uncited float.
- Punctuation conventions on `\ref{}` need enforcement.

## Workflow

1. Parse the `.tex` source for every `\label{...}` declaration. Collect into a set `Labels`.
2. Parse the source for every `\ref{...}`, `\eqref{...}`, `\autoref{...}`, and `\cref{...}` call. Collect the referenced
   keys into a set `Referenced`.
3. Compute `Labels \ Referenced` (defined but never referenced) — these are unused labels.
4. Compute `Referenced \ Labels` (referenced but never defined) — these are broken references.
5. For every float environment (`figure`, `table`, `algorithm`) and every numbered equation, confirm a `\label{}` exists
   inside.
6. For every float/equation with a label, confirm at least one `\ref{}`-style call cites it in the text.
7. Audit punctuation: any `.` `,` `;` `:` immediately inside a `\ref{}` closing brace is a violation. Move it outside.
8. Audit non-breaking space: ensure `Figure~\ref{...}`, `Table~\ref{...}`, `Equation~\ref{...}` (tilde before `\ref`).
9. Report findings: unused labels, broken references, missing labels on floats, missing cross-references, punctuation
   violations.
10. Apply minimal fixes: add labels where missing, add cross-references where missing, move punctuation outside braces.
11. Re-run the scan to confirm zero violations remain.

## Inputs

- LaTeX manuscript source (`.tex`) and any included files.
- Optional compiled `.aux` file (for sanity-checking against the LaTeX engine's own reports).

## Outputs

- A validation report with five tables: unused labels, broken references, unlabeled floats, uncross-referenced floats,
  punctuation violations.
- The revised `.tex` file with fixes applied.

## Key Rules

- Every `\label{}` must have at least one corresponding `\ref{}` in the text.
- Every `\ref{}` must point to a defined `\label{}`.
- Every `figure`, `table`, `algorithm`, and numbered `equation` must carry a `\label{}` and be cross-referenced at least
  once.
- Punctuation goes OUTSIDE the closing brace: `Figure~\ref{fig:x}.` not `Figure~\ref{fig:x.}`.
- Non-breaking space (`~`) precedes `\ref{}` for figure, table, equation, and section references.

## Examples

Before:

```latex
\begin{figure}[!htb]
\centering
\includegraphics{plot}
\caption{Results.}
% no label
\end{figure}

As shown in Figure~\ref{fig:results.}, the curve plateaus.
See Figure~\ref{fig:missing} for details.
```

After:

```latex
\begin{figure}[!htb]
\centering
\includegraphics{plot}
\caption{Results.}
\label{fig:results}
\end{figure}

As shown in Figure~\ref{fig:results}, the curve plateaus.
% Reference to fig:missing removed: no such label exists.
```

Validation report:

```
Unused labels:      (none)
Broken references:  fig:missing  (removed)
Unlabeled floats:   figure (added \label{fig:results})
Uncross-referenced: (none)
Punctuation violations: 1 (moved '.' outside \ref{} brace)
```

## References

- LaTeX `hyperref` and `cleveref` package documentation on cross-references.
- TeX Stack Exchange canonical answers on `undefined reference` warnings.
- The `chktex` static checker for LaTeX: https://www.nongnu.org/chktex/
