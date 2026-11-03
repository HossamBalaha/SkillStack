---
name: tense-consistency-fixer
description: Fixes tense drift in academic prose by enforcing PAST for Methods and Results, PRESENT for established facts and the Discussion, and PRESENT PERFECT for prior work leading to the current study. Use when a draft shifts tense mid-paragraph or when a reviewer has flagged inconsistent verb tense.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [tense, grammar, methods, results, discussion]
related: [writing-citation/english-academic-editor, writing-citation/hedging-language-balancer]
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
last_reviewed: 2026-11-02
verified_against: []
---

# Tense Consistency Fixer

## When To Use

- A reviewer comment says "tense is inconsistent" without specifics.
- A Methods paragraph starts in past tense and drifts to present.
- A Results paragraph uses present tense for findings ("the model achieves 92%") rather than past ("the model achieved
  92%").
- A Discussion paragraph uses past tense for established facts that should be present.

## Workflow

1. Identify the section type (Methods, Results, Discussion, Introduction, Literature Review) since tense rules are
   section-relative.
2. Apply the canonical tense map:
    - Methods: PAST (what was done).
    - Results: PAST (what was found).
    - Discussion: PRESENT for interpretation, PRESENT PERFECT for prior work, PAST for the study's own findings being
      re-stated.
    - Introduction / Lit Review: PRESENT PERFECT for prior work, PRESENT for established facts.
3. Walk paragraph-by-paragraph; tag each verb with its current tense and target tense.
4. Where a tense shift exists within a paragraph, identify whether it is justified (e.g., a Methods sentence that
   legitimately references a present-tense general fact) or a drift.
5. Rewrite drifted verbs to the target tense; preserve meaning, voice, and any citations.
6. Re-read each paragraph to confirm tense is uniform except for justified shifts.
7. Emit a per-paragraph tense audit and the corrected prose.

## Inputs

- The manuscript draft (Markdown, LaTeX, or plain text).
- Section labels (so the tense map can be applied per section).
- Optional list of approved tense shifts (e.g., a Methods paragraph that cites a present-tense general fact).

## Outputs

- `tense_corrected.md` — the revised manuscript with tense unified.
- `tense_audit.csv` — paragraph, verb, original tense, target tense, action (kept / rewritten).
- `justified_shifts.md` — list of tense shifts that were preserved with rationale.

## Key Rules

- Methods and Results use PAST tense — no exceptions except for citing a general present-tense fact.
- Established facts and statements about the paper itself use PRESENT tense.
- Prior work leading up to the current study uses PRESENT PERFECT ("have shown," "has been reported").
- A tense shift within a paragraph is allowed only when the meaning demands it (e.g., contrasting a past experimental
  action with a present general truth).
- Do not change voice (active/passive) while fixing tense — keep voice stable to isolate the change.
- Citations, numbers, and proper nouns must not be altered.

## Examples

```text
Before (Methods, drifting):
"We trained the model for 50 epochs. The optimizer is Adam with a
learning rate of 1e-3. We evaluate the model on the test set. The
results show that accuracy improves steadily."

After (Methods, past-tense unified):
"We trained the model for 50 epochs. The optimizer was Adam with a
learning rate of 1e-3. We evaluated the model on the test set. The
results showed that accuracy improved steadily."

Justified shift preserved:
"We evaluated the model on the test set, which is a standard
benchmark in the field."
(past for the action; present for the general fact that the test set is
standard — preserved.)
```

```text
Discussion fix:
Before: "Our model achieved 92% accuracy. This shows that attention
mechanisms help in noisy settings. Prior work showed similar gains."

After:  "Our model achieved 92% accuracy. This shows that attention
mechanisms help in noisy settings. Prior work has shown similar gains."
(Discussion: past for the study's own result; present for the
interpretation; present perfect for prior work.)
```
