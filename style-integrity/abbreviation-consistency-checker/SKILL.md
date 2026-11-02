---
name: abbreviation-consistency-checker
description: Verify every abbreviation in a manuscript is defined exactly once at first appearance, used consistently thereafter, and aggregated in a final abbreviations table when the count exceeds ten. Use when reviewing acronym usage, catching duplicate definitions, or preparing a manuscript for an abbreviations appendix.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [abbreviations, acronyms, consistency, manuscript, glossary]
related: [style-integrity/notation-consistency-checker, style-integrity/latex-style-guard, style-integrity/cross-reference-validator]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 830
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Abbreviation Consistency Checker

## When To Use

- A manuscript mixes defined and undefined abbreviations.
- An abbreviation is re-expanded in later sections ("Convolutional Neural Network (CNN)" appears twice).
- The number of distinct abbreviations exceeds ten and a list is warranted.
- A reviewer has flagged inconsistent acronym usage.

## Workflow

1. Scan the manuscript for every parenthetical definition matching the pattern `<Full Term> (<UPPERCASE>)` (e.g.,
   "Convolutional Neural Network (CNN)").
2. Build a map: `abbreviation → first-definition-site` (section, line, full term).
3. Flag any abbreviation defined more than once. Keep the first occurrence; rewrite later occurrences to use the bare
   abbreviation.
4. Scan for every use of each abbreviation outside its definition site. Flag any abbreviation used before it is defined.
5. Flag abbreviations defined but never used afterwards — either use them or remove the definition.
6. If the distinct abbreviation count exceeds ten, generate an "Abbreviations" table at the end of the manuscript
   listing each abbreviation and its full form.
7. Apply fixes: delete redundant definitions, move first-use definitions earlier when needed, expand lone abbreviations.
8. Re-scan to confirm one-definition-per-abbreviation.
9. Produce a change report: line, original, action taken.

## Inputs

- Manuscript source text (LaTeX, Markdown, or plain text).
- Optional project-specific glossary of permitted abbreviations.

## Outputs

- Revised manuscript with one definition per abbreviation at first appearance.
- An "Abbreviations" table appended at the end if count > 10.
- A change report listing redundant definitions removed and reordering actions.

## Key Rules

- Every abbreviation is defined exactly once, at its first appearance in the body (including abstract if the
  abbreviation also appears there).
- The full term precedes the abbreviation in parentheses: "Convolutional Neural Network (CNN)".
- The abbreviation is used consistently after definition; the full term is not re-expanded.
- An abbreviation must not be used before it is defined.
- If distinct abbreviations exceed ten, an "Abbreviations" table is appended at the end.

## Examples

Before:

```
We use a Convolutional Neural Network (CNN) for feature extraction.
The Convolutional Neural Network (CNN) is trained on ImageNet.
Results show that GAN outperforms baselines. We use a Generative
Adversarial Network (GAN) for synthesis.
```

After:

```
We use a Convolutional Neural Network (CNN) for feature extraction.
The CNN is trained on ImageNet.
We use a Generative Adversarial Network (GAN) for synthesis; results
show that the GAN outperforms baselines.
```

Abbreviations table (appended):

```
## Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| CNN | Convolutional Neural Network |
| GAN | Generative Adversarial Network |
```

Change report:

```
Line 2:  Removed redundant definition of "Convolutional Neural Network (CNN)".
Line 3:  Moved first-use definition of "Generative Adversarial Network (GAN)"
         earlier; reordered sentence so definition precedes use.
```

## References

- AMA Manual of Style on acronyms and abbreviations.
- IEEE Editorial Style Manual, section on abbreviations.
- The `glossaries` LaTeX package for managing acronyms programmatically.
