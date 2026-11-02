---
name: notation-consistency-checker
description: Audit a mathematical manuscript for one-to-one symbol-to-concept mapping and enforce a Nomenclature table when symbol count exceeds fifteen. Use when reviewing LaTeX math notation, detecting symbol reuse, or normalizing calligraphic-font conventions for sets and spaces.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [notation, symbols, nomenclature, latex, math]
related: [style-integrity/math-symbol-auditor, style-integrity/abbreviation-consistency-checker, style-integrity/latex-style-guard]
prerequisites: []
outputs: [latex, markdown]
difficulty: advanced
estimated_tokens: 810
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Notation Consistency Checker

## When To Use

- User submits a math-heavy manuscript (machine learning, physics, statistics) and asks for "notation check" or "symbol
  audit".
- A symbol appears to mean two different things in two sections.
- The manuscript defines more than fifteen distinct math symbols.
- Sets, feature spaces, or graphs use inconsistent font conventions.

## Workflow

1. Scan the full `.tex` source for math-mode symbols: Greek letters, calligraphic, blackboard-bold, Roman, operators,
   and indexed forms.
2. Build a symbol → concept map by reading each definition site (typically the sentence immediately following the first
   equation using the symbol).
3. Flag any symbol that maps to more than one concept. Report each conflict with section and line numbers.
4. Flag any concept that uses more than one symbol.
5. Apply calligraphic-font conventions: `\mathcal{D}` for datasets, `\mathcal{X}` for feature spaces, `\mathcal{Y}` for
   label spaces, `\mathcal{V}` for vertices, `\mathcal{E}` for edges, `\mathcal{N}` for neighbor sets.
6. Apply blackboard-bold for standard number domains: `\mathbb{R}`, `\mathbb{Z}`, `\mathbb{N}`.
7. Count distinct symbols. If the count exceeds fifteen, mandate a "Nomenclature" table immediately after the abstract.
   The table lists each symbol, its definition, and its physical/clinical unit (or "dimensionless" if applicable).
8. Rewrite conflicting definitions to enforce one-to-one mapping. Prefer the original definition site as canonical.
9. Re-scan to confirm all conflicts are resolved.
10. Output the symbol table and the conflict-resolution report.

## Inputs

- LaTeX manuscript source (`.tex`) and any included math macro files.
- Field-specific conventions if known (e.g., physics vs. ML conventions for vectors).

## Outputs

- Revised manuscript with consistent notation.
- A Nomenclature table (if >15 symbols) ready for insertion after the abstract.
- A conflict report listing every original conflict and its resolution.

## Key Rules

- One symbol maps to exactly one concept across the entire manuscript.
- Calligraphic fonts reserved for sets and spaces (`\mathcal{D}`, `\mathcal{X}`, etc.).
- Blackboard-bold reserved for number domains.
- More than fifteen distinct symbols mandates a Nomenclature table.
- Every symbol must be defined in prose immediately after its first appearance.
- Units must accompany every physical or clinical quantity in the Nomenclature table.
- Bold is reserved for vectors and matrices, not for emphasis.
- Operators defined via `\DeclareMathOperator` are kept in upright Roman, not italic.

## Examples

Conflict detected:

```
Section 3: Let D denote the dataset of N samples.
Section 5: Let D denote the diffusion coefficient.
```

Resolution:

```
Section 3: Let \mathcal{D} denote the dataset of N samples.
Section 5: Let D_{\text{diff}} denote the diffusion coefficient.

Nomenclature (after abstract):
| Symbol | Definition | Unit |
|--------|------------|------|
| \mathcal{D} | Dataset of N samples | — |
| D_{\text{diff}} | Diffusion coefficient | m^2/s |
```

Font convention fix:

```
Before: Let X be the feature space, V be the vertices, and N the neighbors.
After:  Let \mathcal{X} be the feature space, \mathcal{V} the vertices,
        and \mathcal{N} the neighbors.
```

## References

- AMS Author Handbook on mathematical notation.
- Goodfellow, Bengio, Courville, *Deep Learning* (Appendix on notation).
- ISO 80000-2 mathematical signs and symbols standard.
- The LaTeX `amsmath` user guide for environment and symbol conventions.
- Notation in *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman).
