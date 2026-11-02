---
name: academic-prose-polisher
description: Rewrite informal or AI-flavored prose into formal academic register suitable for peer-reviewed venues. Use when editing manuscript body text, removing banned vocabulary, eliminating em-dashes, suppressing bullet points in main prose, and stripping meta-commentary.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [prose, academic-register, editing, revision, formal]
related: [style-integrity/banned-vocabulary-filter, style-integrity/em-dash-eliminator, style-integrity/meta-commentary-stripper, style-integrity/passive-voice-detector]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
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

# Academic Prose Polisher

## When To Use

- User asks to "polish", "tighten", or "academicize" prose in a manuscript or draft.
- Draft contains banned vocabulary (delve, tapestry, underscore, pivotal, leverage, crucial, testament, multifaceted,
  navigating, realm, novel, rigorous).
- Prose uses em-dashes as parenthetical separators.
- Body paragraphs contain bullet points that should be prose.
- Phrases like "In this section we will show…" or "It is worth noting" appear.

## Workflow

1. Read the full manuscript section to understand scope and argument.
2. Run the banned-vocabulary scan: flag every instance of *delve, tapestry, underscore, pivotal, leverage, crucial,
   testament, multifaceted, navigating, realm, novel, rigorous, paramount, "It is worth noting", "In conclusion", "plays
   a vital role"*.
3. Replace each banned term with a precise concrete synonym (e.g., `delve` → `examine`; `leverage` → `use`; `crucial` →
   `important`; `novel` → `new`; `rigorous` → `thorough`; `multifaceted` → `complex`).
4. Remove every em-dash (`—`). Restructure using commas, parentheses, or en-dashes with no surrounding spaces for
   numerical ranges.
5. Convert bullet lists in the main body into flowing prose. Permit bullets only in explicitly pedagogical sections
   (e.g., "Summary of Contributions").
6. Strip meta-commentary: delete "In this section we will show…", "We now turn to…", "It is worth noting that…", "As we
   will discuss in Section~\ref{…}".
7. Define every abbreviation at first appearance: "Convolutional Neural Network (CNN)". Use the abbreviation thereafter;
   do not redefine in later sections.
8. Re-read the revised text to confirm tone, flow, and density match a top-tier journal.
9. Produce a change log listing each substitution and its justification.

## Inputs

- Source manuscript text (LaTeX, Markdown, or plain text).
- Target venue if known (affects acceptable passive/active ratio).
- Existing abbreviation list if one exists.

## Outputs

- Polished text file with all rules applied.
- Change log: original → replacement, with line references.

## Key Rules

- Banned vocabulary is forbidden. Replace, do not delete.
- Em-dashes (`—`) are forbidden in body prose. Use commas or parentheses.
- Bullet points are forbidden in main prose; permitted only in pedagogical sections.
- Meta-commentary about the paper's own structure is forbidden.
- Every abbreviation is defined exactly once at first appearance.
- Sentences remain concise and dense; no rhetorical throat-clearing.
- Conclusions are signaled by content, not by the phrase "In conclusion".
- Emphasis is conveyed by precision, not by intensifiers (paramount, pivotal, crucial).

## Examples

Before:

```
In this section, we will delve into the multifaceted realm of representation
learning—which plays a vital role in modern ML—and leverage crucial insights
from prior work. It is worth noting that novel architectures often yield
rigorous gains.
```

After:

```
Representation learning is central to modern machine learning and builds on
prior empirical results. New architectures often yield measurable gains.
```

Before (em-dash and bullet point):

```
Our model has three strengths—it is fast, accurate, and small:
- Trains in 2 hours on a single GPU.
- Reaches 94% top-1 accuracy.
- Has 4M parameters.
```

After (prose, no em-dash):

```
Our model trains in 2 hours on a single GPU, reaches 94% top-1 accuracy,
and contains 4M parameters.
```

## References

- William Zinsser, *On Writing Well* (for density and clarity).
- The Economist Style Guide (concise prose conventions).
- ACS/IEEE author guidelines on register and abbreviations.
