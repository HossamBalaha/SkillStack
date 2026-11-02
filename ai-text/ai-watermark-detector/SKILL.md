---
name: ai-watermark-detector
description: Detect statistical watermarks embedded by LLMs using the Kirchenbauer et al. (2023) green-list/red-list scheme — green-list token ratio above baseline, watermark strength parameter δ, and hash-based seeding keyed to the preceding token. Use when you suspect a text was produced by a watermarked model and need to test the watermark signal directly.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [watermark, statistical-detection, green-list, ai-text]
related: [ai-text/perplexity-burstiness-scorer, ai-text/ai-text-detector, ai-text/multi-engine-verification]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# AI Watermark Detector

## When To Use

- You suspect text was produced by a model known to deploy the Kirchenbauer-style watermark.
- A compliance audit requires checking for embedded watermarks before publication.
- You want a signal independent of stylistic tells (`ai-text-detector`) and statistical perplexity
  (`perplexity-burstiness-scorer`).
- You are benchmarking whether a corpus contains watermarked outputs.
- A reviewer asks "is there an actual watermark, or just a vibe?".

## Workflow

1. Confirm the suspected source model uses a green-list/red-list watermark. Many open-weights models do not; most
   production chatbots do not currently publish that they watermark.
2. Reconstruct the watermark parameters if known: the green-list fraction γ (typically ~0.5), the strength δ, the hash
   seeding scheme (keyed on the preceding token or a context window), and the vocabulary split.
3. Tokenize the input with the suspected model's tokenizer.
4. For each token position, compute the hash of the preceding token (or context window) to derive the green-list set for
   that position.
5. Determine whether the actual next token belongs to the green list or the red list.
6. Aggregate: compute the fraction of green-list tokens observed. Compare against the expected baseline γ.
7. Compute a z-score: `z = (observed_green_fraction - γ) / sqrt(γ(1-γ)/N)`. High positive z indicates a watermark.
8. Account for text length: the test is unreliable below ~100 tokens; ≥200 tokens gives a meaningful z-score; ≥500 is
   preferred.
9. Cross-check with the strength parameter δ where recoverable: stronger watermarks (higher δ) produce larger green-list
   bias.
10. Emit a scorecard: observed green fraction, expected baseline, z-score, length, and a watermark-present / absent
    verdict with confidence.
11. If the watermark is absent, do not conclude "human-written" — the text may be from a non-watermarked model. Pair
    with `ai-text-detector` and `multi-engine-verification`.

## Inputs

- The text to test.
- The suspected model's tokenizer and watermark parameters (γ, δ, hash scheme). If unknown, the detector can only report
  green-list ratios for default parameter guesses.
- Optional: a reference distribution of green-list fractions from known-human text for baseline calibration.

## Outputs

- A scorecard: token count, observed green-list fraction, expected baseline γ, z-score, verdict (`Watermark detected` /
  `No watermark detected` / `Inconclusive — text too short`).
- Per-position green/red sequence (optional, for debugging).
- Confidence interval at a chosen significance level (e.g., p < 0.01).
- A caveat paragraph: absence of watermark is not absence of AI authorship.

## Key Rules

- The test is statistical. Below ~100 tokens it is inconclusive; report as such.
- Absence of a watermark does NOT mean human-written. Most production chatbots do not watermark, and a paraphrase or
  rewrite can destroy a watermark even if originally present.
- Presence of a watermark is strong evidence the text came from a watermarked model. Treat as S3-S4 depending on z-score
  and length.
- The detector must reconstruct the same hash seeding the watermark used. A wrong hash scheme produces a null result,
  not a false negative.
- Green-list fraction above baseline alone is weak; combine with the z-score and length before concluding.
- The watermark can survive light editing but is degraded by paraphrase, translation, or aggressive rewriting.
- Never claim detection of a watermark from a model that does not deploy one. State the assumed parameters explicitly.

## Examples

**Scorecard (watermark present):**

```
Text length: 412 tokens
Assumed parameters: γ = 0.5, δ = 2.0, hash seeded on preceding token
Observed green-list fraction: 0.71
Expected baseline γ:        0.50
z-score:                    8.5  (p < 0.0001)
Verdict: Watermark detected — strong.
Caveat: presence indicates a watermarked model. Pair with tell analysis for
full authorship picture.
```

**Scorecard (no watermark):**

```
Text length: 318 tokens
Observed green-list fraction: 0.49
Expected baseline γ:        0.50
z-score:                   -0.36 (p = 0.72)
Verdict: No watermark detected.
Caveat: this does NOT establish human authorship. The text may come from a
non-watermarked model, or a watermark may have been destroyed by paraphrase.
Pair with ai-text-detector and multi-engine-verification.
```

**Inconclusive (too short):**

```
Text length: 47 tokens
Observed green-list fraction: 0.60
z-score: 1.4 — below the 1% significance threshold at this length.
Verdict: Inconclusive — text too short. Need ≥200 tokens for a meaningful test.
```

**After paraphrase:**

```
Original (watermarked, z = 8.5): 412 tokens
Paraphrased (z = 1.1):           389 tokens
Verdict: watermark degraded by paraphrase. Do not conclude human authorship
from the absence of the watermark alone.
```

## References

- Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Interlandi, I., Lee, K., & Goldstein, T. (2023). "A Watermark for
  Large Language Models." arXiv:2301.10226. https://arxiv.org/abs/2301.10226
- Follow-up work on robustness and paraphrase attacks: e.g., Kirchenbauer et al. (2023) §5 on paraphrase robustness.
- Companion skills: `ai-text-detector`, `perplexity-burstiness-scorer`, `multi-engine-verification`.
