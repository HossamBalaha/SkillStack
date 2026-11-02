---
name: math-symbol-auditor
description: Audit a math-heavy manuscript for one-to-one symbol-to-concept mapping, immediate textual definition after first equation use, and standard calligraphic-font conventions for sets and spaces. Use when reviewing machine-learning or physics manuscripts, detecting symbol reuse, and mandating a Nomenclature table when distinct symbols exceed fifteen.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [math, symbols, nomenclature, latex, audit]
related: [style-integrity/notation-consistency-checker, style-integrity/latex-style-guard, style-integrity/abbreviation-consistency-checker]
prerequisites: []
outputs: [latex, markdown]
difficulty: advanced
estimated_tokens: 820
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Math Symbol Auditor

## When To Use

- A math-heavy manuscript defines symbols inconsistently or reuses them.
- A reader cannot map a symbol to a concept without hunting through earlier sections.
- Sets, feature spaces, vertices, edges, or neighbors use ad-hoc fonts.
- The number of distinct symbols suggests a Nomenclature table is warranted.

## Workflow

1. Scan every math environment (`equation`, `align`, `gather`, `$...$`, `\[...\]`) for symbols.
2. For each distinct symbol (including subscripts/superscripts variants), record: symbol, first equation, surrounding
   sentence.
3. Confirm the symbol is defined in the prose immediately following its first appearance.
4. Build a `symbol → concept` map. Flag any symbol mapping to more than one concept.
5. Flag any concept that uses more than one symbol.
6. Enforce calligraphic-font conventions:
    - `\mathcal{D}` — datasets
    - `\mathcal{X}` — feature spaces
    - `\mathcal{Y}` — label spaces
    - `\mathcal{V}` — vertex sets
    - `\mathcal{E}` — edge sets
    - `\mathcal{N}` — neighbor sets
7. Enforce blackboard-bold for number domains: `\mathbb{R}`, `\mathbb{Z}`, `\mathbb{N}`, `\mathbb{Q}`.
8. Count distinct symbols. If count > 15, mandate a Nomenclature table listing every symbol, its definition, and its
   unit (or "dimensionless").
9. Rewrite conflicting definitions to enforce a single canonical mapping.
10. Re-scan to confirm zero conflicts.
11. Output the symbol map, conflict report, and the Nomenclature table if required.

## Inputs

- LaTeX manuscript source (`.tex`) including any custom macro definitions.
- Field-specific convention override if applicable.

## Outputs

- A `symbol → concept` map.
- A conflict report listing every violation and its resolution.
- A Nomenclature table (if distinct symbols > 15) for insertion after the abstract.

## Key Rules

- One symbol maps to exactly one concept across the entire manuscript.
- Every symbol is defined in prose immediately following its first equation appearance.
- Calligraphic fonts reserved for sets and spaces (`\mathcal{D}`, `\mathcal{X}`, `\mathcal{Y}`, `\mathcal{V}`,
  `\mathcal{E}`, `\mathcal{N}`).
- Blackboard-bold reserved for number domains (`\mathbb{R}`, `\mathbb{Z}`, `\mathbb{N}`).
- Distinct symbols > 15 mandates a Nomenclature table.
- Physical and clinical quantities include their units in the Nomenclature.

## Examples

Conflict detected:

```
Eq. (1): x \in \mathbb{R}^d denotes an input sample.
Eq. (5): x denotes the iteration counter.
```

Resolution:

```
Eq. (1): x \in \mathbb{R}^d denotes an input sample.
Eq. (5): k denotes the iteration counter.
```

Nomenclature (excerpt, when count > 15):

```
| Symbol | Definition | Unit |
|--------|------------|------|
| \mathcal{D} | Dataset of N samples | — |
| \mathcal{X} | Feature space \subset \mathbb{R}^d | — |
| N | Number of samples | — |
| \eta | Learning rate | — |
| \sigma | Noise standard deviation | — |
```

## References

- AMS Author Handbook on mathematical notation.
- Goodfellow, Bengio, Courville, *Deep Learning*, Appendix on notation.
- ISO 80000-2 mathematical signs and symbols standard.
