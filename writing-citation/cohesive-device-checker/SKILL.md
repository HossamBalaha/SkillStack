---
name: cohesive-device-checker
description: Checks cohesive devices in academic prose — reference (this/that/these/those/it), conjunction (however, therefore, moreover), lexical (repetition, synonyms, superordinates), and ellipsis — to ensure cohesion without overusing any single device. Use when a reviewer flags "unclear referents" or when demonstratives pile up without clear antecedents.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [cohesion, reference, conjunction, lexical, ellipsis]
related: [writing-citation/english-academic-editor, writing-citation/paragraph-transition-smoother]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: en
---

# Cohesive Device Checker

## When To Use

- A reviewer says "the antecedent of 'this' is unclear."
- A draft begins three consecutive paragraphs with "However" or "Moreover."
- The prose repeats the same noun so often it feels mechanical (under-use of lexical cohesion).
- A non-native author's draft over-relies on demonstrative pronouns ("This shows...") with no clear referent.

## Workflow

1. Tokenize the draft into paragraphs and sentences.
2. Inventory each cohesive device:
    - Reference: this, that, these, those, it, they, such, the former, the latter.
    - Conjunction: however, therefore, moreover, consequently, nevertheless, in contrast, in addition.
    - Lexical: repetition of the same noun, synonyms, superordinates (e.g., "model" → "architecture" → "system").
    - Ellipsis: omitted words recoverable from context (e.g., "the first model trained faster than the second [did]").
3. For each reference device, locate its antecedent within the same paragraph (or the immediately preceding one); flag
   any device whose antecedent is missing, ambiguous, or far away.
4. For each conjunction, check that it appears at most once per paragraph and that the logical relationship matches the
   surrounding sentences.
5. For lexical cohesion, check that key terms recur enough to anchor the topic but not so often that the prose feels
   repetitive (rule of thumb: 2-4 occurrences per term per paragraph).
6. For ellipsis, confirm the omitted material is unambiguously recoverable; if not, restore it.
7. Flag overuse: any device used more than twice per paragraph is a candidate for variation.
8. Emit a per-paragraph device inventory plus suggested fixes.

## Inputs

- The draft section (Markdown or LaTeX).
- Optional style guide (e.g., journal preference for "However" as sentence-initial vs. mid-sentence).
- Optional list of approved technical terms whose repetition is acceptable.

## Outputs

- `cohesion_report.md` — per-paragraph inventory of devices with status (OK / OVERUSED / AMBIGUOUS).
- `ambiguity_flags.md` — list of demonstratives or pronouns whose antecedent is missing or far away, with suggested fix.
- `device_balance.csv` — counts per device per paragraph, with overuse thresholds.

## Key Rules

- Every demonstrative (this/that/these/those) must have an unambiguous antecedent within the same or preceding sentence.
- The same conjunction should not appear more than once per paragraph.
- Lexical repetition of a key term is healthy (anchors topic); repetition of a generic word ("thing," "aspect") is a
  defect.
- Ellipsis is acceptable only when the omitted material is unambiguously recoverable.
- A device whose antecedent is more than one sentence away must be replaced with the full noun phrase.
- Overuse of "this" as a sentence opener ("This shows... This means...") is a defect to be varied.

## Examples

```text
Before (ambiguous demonstrative):
"We trained two models, A and B, on the same dataset. Model A converged
in 50 epochs while model B required 200. This suggests that the
attention mechanism stabilizes training."

After (anchored antecedent):
"We trained two models, A and B, on the same dataset. Model A converged
in 50 epochs while model B required 200. This divergence in convergence
speed suggests that the attention mechanism stabilizes training."

Fix: added "divergence in convergence speed" to anchor "this."
```

```text
Device inventory (paragraph 3 of Results):
  Reference:
    "this" (×3) — antecedents: sentences 1, 3, 5 — last one AMBIGUOUS (5)
    "it"   (×1) — antecedent: "the optimizer" (sentence 2) — OK
  Conjunction:
    "however" (×2) — OVERUSED (max 1 per paragraph) — vary the second
  Lexical:
    "model" (×6) — over-repetition — vary with "architecture," "system"
  Ellipsis:
    "the first model trained faster than the second" — OK (recoverable)

Suggested fix: replace one "however" with a conceptual contrast; vary
two occurrences of "model" with "architecture" and "system."
```

## References

- Halliday, M. A. K., & Hasan, R. (1976). *Cohesion in English*. Longman — the foundational reference for cohesive
  devices.
- Hoey, M. (1991). *Patterns of Lexis in Text*. Oxford University Press.
- Purdue OWL on
  cohesion: https://owl.purdue.edu/owl/general_writing/mechanics/transitions_and_transitional_devices/index.html.
