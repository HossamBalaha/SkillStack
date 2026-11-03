---
name: ai-text-detector
description: Detect AI-generated text by scanning for a structured catalogue of tells across lexical, structural, thematic, tonal, statistical, and citation categories. Use when you need to assess whether a passage was likely written by an LLM, audit a document for machine-written sections, or triage submissions for human review.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [ai-detection, tells, perplexity, burstiness]
related: [ai-text/ai-tell-catalogue, ai-text/severity-classifier, ai-text/perplexity-burstiness-scorer, ai-text/citation-hallucination-detector]
prerequisites: []
outputs: [markdown, json]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# AI Text Detector

## When To Use

- A user asks "is this AI-written?" or wants a likelihood score for a passage.
- You need to audit a long document (essay, report, blog post) and flag suspect paragraphs.
- A reviewer wants reproducible evidence rather than a gut judgement.
- You are triaging drafts, comments, or submissions before deeper verification.
- You want to feed clean inputs into a humanization or rewrite workflow.

## Workflow

1. Read the full passage once end-to-end without judging.
2. Split the text into analysis windows (paragraph or ~300-word blocks).
3. For each window, scan the six tell categories in order: lexical, structural, thematic, tonal, statistical, citation.
4. Cross-reference every match against the `ai-tell-catalogue` to confirm it is a known pattern.
5. Assign each match a severity level (S1-S4) using `severity-classifier`.
6. Record the evidence: tell name, location (quote + offset), category, severity.
7. Apply the cumulative-evidence rule R1: a single S1 or S2 match is never enough on its own. Require at least two
   overlapping patterns from different categories before flagging a block.
8. Where statistics are involved, optionally call `perplexity-burstiness-scorer` to add numeric support.
9. Verify any suspicious citations with `citation-hallucination-detector`. Hallucinated DOIs count as S4 regardless of
   other evidence.
10. Produce a verdict per window: `Likely Human`, `Mixed`, `Likely AI`, or `Near-Certain AI`.
11. Emit a summary table with counts by category and severity.

## Inputs

- The text under review (plain text preferred; HTML/Markdown acceptable if structural tells matter).
- Optional: claimed author or source, so verdict can be contextualized.
- Optional: target voice profile, if you want to check deviation from an author's baseline.

## Outputs

- A verdict per window plus an overall document verdict.
- An evidence table: `Location | Tell | Category | Severity | Note`.
- Category coverage summary showing which of the six categories were triggered.
- A short justification paragraph citing the strongest overlapping patterns.

## Key Rules

- R1 (cumulative evidence): never issue an AI verdict on a single indicator. Require overlap from at least two
  categories.
- Treat S4 signals (hallucinated citations, phantom DOIs) as near-confirmation; they override R1.
- Quote exact spans. Do not paraphrase evidence — reviewers need to verify.
- Distinguish "common in both" (S1) from "rare in human writing" (S3) before weighting.
- Never present a detector verdict as proof. Use language like "consistent with AI authorship patterns".
- If the author's voice profile is known, voice overrides generic tells (see `voice-profile-matcher`).
- Report what you did NOT find as well; absence of lexical tells with strong statistical tells is still informative.

## Examples

**Input passage:**

```
The 2023 study by Chen et al. delves into the pivotal role of federated learning
in the broader landscape of edge computing. It underscores how seamless
integration can mark a turning point, leaving an indelible mark on the field.
DOI: 10.1109/FAKE.2023.99999.
```

**Detector output (excerpt):**

```
Window 1 — Verdict: Near-Certain AI

| Location                       | Tell                  | Category  | Sev |
|--------------------------------|-----------------------|-----------|-----|
| "delves into the pivotal role" | Lexical: delve        | lexical   | S2  |
| "pivotal role"                 | Lexical: pivotal      | lexical   | S2  |
| "broader landscape"            | Inflation             | thematic  | S2  |
| "seamless integration"         | Lexical: seamless     | lexical   | S2  |
| "mark a turning point"         | Inflation             | thematic  | S2  |
| "leaving an indelible mark"    | Inflation             | thematic  | S2  |
| DOI 10.1109/FAKE.2023.99999    | Phantom citation     | citation  | S4  |

R1 satisfied: lexical + thematic overlap. S4 citation triggers near-confirmation.
Action: treat as near-certain AI; route to humanizer and citation verifier.
```

**Before/After (human-style rewrite):**

```
Before: This section delves into the pivotal role of caching.
After:  Caching matters here because every repeated query hits the database twice.
```
