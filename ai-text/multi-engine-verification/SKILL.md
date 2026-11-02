---
name: multi-engine-verification
description: Run text through two or more external AI-detection engines (GPTZero, Originality.ai, Turnitin AI detection, OpenAI's retired classifier — note OpenAI retired theirs in 2023) and cross-reference their verdicts. Use when a single detector's verdict is insufficient, when stakes require triangulation, or when compliance demands multiple independent checks.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ai-text
tags: [ai-detection, multi-engine, triangulation, verification]
related: [ai-text/ai-text-detector, ai-text/perplexity-burstiness-scorer, ai-text/ai-watermark-detector]
prerequisites: [ai-text/ai-text-detector]
outputs: [markdown, json]
difficulty: intermediate
estimated_tokens: 2000
cost_warning: Calls paid AI-detection APIs (GPTZero, Originality.ai) — budget accordingly.
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
---

# Multi-Engine Verification

## When To Use
- A single detector's verdict is not sufficient because the stakes are high (academic integrity, publication, legal).
- A reviewer demands triangulation across independent systems.
- `ai-text-detector` returned `Mixed` and you need a tiebreaker.
- You want to characterize disagreement between detectors as a signal in itself.
- Compliance requires more than one independent check before a finding.

## Workflow
1. Confirm the candidate engines are available and their terms permit the use case. Note: OpenAI retired its classifier in July 2023; do not cite it as an active detector.
2. Select at least two engines from: GPTZero, Originality.ai, Turnitin AI detection, Copyleaks, Winston AI, Sapling, or similar current offerings. Prefer engines with independent methodologies.
3. Run the same text through each engine. Use identical input (same character count, same formatting) so results are comparable.
4. Capture each engine's verdict and score (percentage, label, confidence) with timestamp.
5. Record each engine's documented methodology if disclosed (perplexity-based, transformer-based, hybrid).
6. Compare verdicts:
   - All engines agree → high-confidence result, but still combine with manual tell analysis.
   - Majority agree → medium-confidence; note the dissenting engine and its methodology.
   - Engines disagree substantially → low-confidence; treat as `Inconclusive` and route to manual review.
7. Apply R1 (cumulative evidence): do not rely on any single detector. Weber-Wulff et al. (2023) documented non-trivial error rates, including false positives on non-native English writing.
8. Combine engine output with `ai-text-detector` manual tell analysis and `perplexity-burstiness-scorer` numeric scores. A finding stands when at least two independent signal classes agree.
9. Emit a comparison table and a combined verdict with confidence level.
10. Log engine versions and timestamps so the verdict is reproducible.

## Inputs
- The text to verify.
- Credentials or API access for at least two detection engines.
- Optional: a known-human baseline by the same author for false-positive calibration.

## Outputs
- A comparison table: `Engine | Verdict | Score | Confidence | Methodology | Timestamp`.
- An agreement summary: `unanimous`, `majority`, `split`.
- A combined verdict: `Likely Human`, `Mixed`, `Likely AI`, `Near-Certain AI`, or `Inconclusive`.
- A confidence level: `High`, `Medium`, `Low`.
- A reconciliation note: how the engine output was combined with manual tell analysis and statistical scores.

## Key Rules
- R1: do not rely on a single detector. Always require at least two engines for a publishable finding.
- OpenAI's classifier was retired in July 2023. Do not cite it as active.
- Disagreement between engines is itself a signal. Report it; do not average it away.
- Be alert to known false-positive biases: non-native English writing, formulaic genres (legal, technical specs), and short samples.
- Engine verdicts are model-relative. An 80% score from one engine is not equivalent to 80% from another.
- Combine with manual tell analysis (`ai-text-detector`) and statistical scores (`perplexity-burstiness-scorer`). A finding stands on overlapping independent signal classes, not on a single engine's number.
- Log engine versions and timestamps. Detector models change; reproducibility requires provenance.
- Treat commercial-detector output as evidence, not proof. Always state confidence level and known limitations.

## Examples

**Comparison table (agreement):**
```
| Engine          | Verdict        | Score | Methodology      | Timestamp        |
|-----------------|----------------|-------|------------------|------------------|
| GPTZero         | AI-generated   | 94%   | perplexity/burst | 2025-01-12 14:02 |
| Originality.ai  | AI-generated   | 91%   | transformer      | 2025-01-12 14:03 |
| Turnitin AI     | AI-generated   | 88%   | proprietary      | 2025-01-12 14:05 |

Agreement: unanimous.
Combined verdict: Likely AI (High confidence).
Reconciliation: all three engines agree; `ai-text-detector` flagged S3-S4 lexical
and citation tells; `perplexity-burstiness-scorer` z-scores in the bottom decile.
```

**Disagreement (inconclusive):**
```
| Engine          | Verdict        | Score | Methodology      |
|-----------------|----------------|-------|------------------|
| GPTZero         | Human          | 12%   | perplexity/burst |
| Originality.ai  | AI-generated   | 79%   | transformer      |
| Turnitin AI     | Human          | 18%   | proprietary      |

Agreement: split.
Combined verdict: Inconclusive (Low confidence).
Reconciliation: 1 of 3 engines flags AI. Manual tell analysis flagged S1-S2
lexical tells only; no S3-S4. Author profile (non-native English writer) is a
known false-positive factor. Recommend manual review; do not publish a finding.
```

**Note on OpenAI classifier:**
```
The OpenAI classifier was retired in July 2023 due to low accuracy. Do not
treat it as an active engine. If a prior report cited it, re-run with a
current engine before relying on the finding.
```

## References
- Weber-Wulff, S., et al. (2023). "Testing of detection signals for AI-generated text." *Patterns* 4(7). Documents high error rates and false-positive bias against non-native English writing — basis for R1 and the caution on single-detector reliance.
- OpenAI (2023). "AI Text Classifier — no longer available." https://help.openai.com/en/articles/5727991 — confirms retirement.
- GPTZero: https://gptzero.me — methodology includes perplexity and burstiness.
- Originality.ai: https://originality.ai — transformer-based detection.
- Turnitin AI detection: https://www.turnitin.com/solutions/ai-writing — proprietary, used in academic contexts.
- Companion skills: `ai-text-detector`, `perplexity-burstiness-scorer`, `severity-classifier`, `voice-profile-matcher`.
