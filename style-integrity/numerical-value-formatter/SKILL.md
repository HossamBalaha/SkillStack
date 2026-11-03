---
name: numerical-value-formatter
description: Wrap every standalone numerical value in body text with the `\ineq{}` LaTeX macro, replace the `PIP` token with `\ineq{pip}`, normalize en-dash-minus variants to hyphen, and fix `etc.etc.` duplicates. Use when finalizing a LaTeX manuscript for consistent number typesetting and to ensure all in-text numerals route through a single macro.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [latex, numerical, ineq-macro, typography, formatting]
related: [style-integrity/latex-style-guard, style-integrity/math-symbol-auditor, style-integrity/notation-consistency-checker]
prerequisites: []
outputs: [latex]
difficulty: intermediate
estimated_tokens: 800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Numerical Value Formatter

## When To Use

- A LaTeX manuscript mixes raw `32`, `3.14`, and `1e-4` directly in body prose.
- The token `PIP` appears in body text and should be normalized to `\ineq{pip}`.
- Unicode `‒` (figure dash / en-dash minus variant) appears in place of the ASCII hyphen `-`.
- A typo such as `etc.etc.` appears and should collapse to `etc.` or `, and`.
- A pre-submission pass wants every numeral to route through a single macro for global restyling.

## Workflow

1. Ensure the preamble defines the macro:
   ```latex
   \newcommand{\ineq}[1]{\ensuremath{#1}}
   ```
2. Scan the body text (NOT inside code blocks, verbatim, lstlisting, or minted environments).
3. For every standalone integer or decimal (`32`, `3.14`, `1.5e-3`, `1000`), wrap as `\ineq{32}`, `\ineq{3.14}`.
4. Skip numerals that are part of identifiers, version strings (`v2.0`), section numbers (`Section~\ref{...}`), or
   citation keys.
5. Replace every occurrence of the literal token `PIP` (case-sensitive, whole token) with `\ineq{pip}`.
6. Replace every `‒` (U+2012 figure dash) and every en-dash used as a minus variant with the ASCII hyphen `-`.
7. Replace every `etc.etc.` (with or without spaces) with `etc.` when it closes a list, or with `, and` when joining the
   final item.
8. Re-scan to confirm no raw standalone numerals remain in body text.
9. Verify the macro is defined exactly once in the preamble.
10. Produce a change report: count of numerals wrapped, PIP replacements, dash normalizations, `etc.etc.` fixes.

## Inputs

- LaTeX manuscript source (`.tex`) including preamble.
- Optional allow-list of identifiers that should NOT be wrapped (e.g., `v2.0`, `B100`).

## Outputs

- Revised `.tex` file with all body numerals wrapped in `\ineq{}`.
- Macro `\newcommand{\ineq}[1]{\ensuremath{#1}}` defined once in the preamble.
- Change report with counts.

## Key Rules

- Every standalone integer or decimal in body prose is wrapped in `\ineq{}`.
- Numerals inside code blocks, `verbatim`, `lstlisting`, identifiers, version strings, and `\ref{}` arguments are NOT
  wrapped.
- `PIP` is replaced with `\ineq{pip}` everywhere in body text.
- `‒` (figure dash) and en-dash-minus variants are normalized to ASCII hyphen `-`.
- `etc.etc.` collapses to `etc.` (terminal) or `, and` (joining).
- The `\ineq{}` macro is defined exactly once in the preamble.

## Examples

Before:

```latex
We trained for 100 epochs with a learning rate of 0.001 and a batch size
of 32. The model has 1.2e7 parameters. See Section~\ref{sec:results} for
the PIP metric. We used layers of sizes 128‒256‒10, etc.etc.
```

After:

```latex
We trained for \ineq{100} epochs with a learning rate of \ineq{0.001}
and a batch size of \ineq{32}. The model has \ineq{1.2e7} parameters.
See Section~\ref{sec:results} for the \ineq{pip} metric. We used layers
of sizes \ineq{128}-\ineq{256}-\ineq{10}, etc.
```

Change report:

```
Numerals wrapped:      6
PIP replaced:          1
‒ normalized to -:     2
etc.etc. collapsed:    1
Macro defined:         once (verified)
```
