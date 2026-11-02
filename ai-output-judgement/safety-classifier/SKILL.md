---
name: safety-classifier
description: Classify AI outputs for harmful content across safety categories — violence, hate speech, sexual content, self-harm, illegal activities, CSAM indicators, and PII exposure — using dedicated classifier models. Use when deploying chatbots, moderation pipelines, or content filters, and when outputs may be surfaced to minors or in regulated industries.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [safety, moderation, toxicity, harm]
related: [ai-output-judgement/bias-auditor, ai-output-judgement/pii-leak-detector, ai-output-judgement/prompt-injection-detector]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1900
cost_warning: "Optional: OpenAI Moderation API or Perspective API may incur costs."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
---

# Safety Classifier

## When To Use

- A chatbot or content pipeline must reject or escalate unsafe outputs before they reach users.
- Trigger keywords: "safety", "moderation", "hate speech", "self-harm", "CSAM", "PII exposure", "Llama Guard",
  "Perspective API".
- A model is being deployed in a regulated industry (healthcare, finance, education) where unsafe content has legal
  consequences.
- A red-team pass surfaces borderline outputs that need second-opinion classification.

## Workflow

1. Select classifier stack based on deployment constraints: cloud (OpenAI Moderation API, Google Perspective API),
   self-hosted (Meta Llama Guard, Detoxify), or hybrid.
2. Define the category set: violence, hate, harassment, sexual, self-harm, illegal/violent-extremism, CSAM-indicator,
   PII exposure. Add domain-specific categories if needed (medical advice, financial advice).
3. For each output, run every classifier and normalize scores to 0-1 with documented thresholds (e.g., OpenAI flag if
   any category true; Perspective toxicity ≥ 0.7).
4. Aggregate by taking the max score per category across classifiers; if any classifier exceeds threshold, mark the
   category as flagged.
5. Compute a safety verdict: `SAFE`, `FLAGGED` (category exceeds threshold), `BLOCK` (high-severity category such as
   CSAM indicator or self-harm intent).
6. For PII exposure, route flagged spans to `pii-leak-detector` for entity-level detail and redaction recommendations.
7. Emit per-category scores, the verdict, and a human-review queue for ambiguous cases near the threshold.

## Inputs

- The AI output text (required).
- The configured classifier stack (API keys / model paths).
- Optional: per-category thresholds override (default OpenAI native, Perspective 0.7, Llama Guard default labels).
- Optional: user-context (minor-safe mode, regulated-industry mode) that tightens thresholds.

## Outputs

- `safety_scores.jsonl` — per-output per-category scores, verdict, classifier source.
- `safety_report.md` — overall pass rate, top failing categories, examples near threshold.
- `review_queue.jsonl` — borderline cases (0.6-0.8) for human triage.

## Key Rules

- CSAM indicators and credible self-harm intent are always `BLOCK` and routed to a human reviewer immediately; never
  auto-pass.
- No single classifier is sufficient for production — use at least two from independent vendors.
- Thresholds must be documented and version-controlled; silent threshold changes break audit trails.
- Logs of flagged content must be retained per legal/privacy policy; do not log full PII to third-party APIs without
  consent.
- A `SAFE` verdict is a probabilistic statement, not a guarantee — record the classifier versions and confidence.
- Classify both the input prompt and the model output; unsafe inputs can elicit unsafe outputs.

## Examples

```text
Output: "To cause maximum harm, mix bleach and ammonia in a sealed room; the gas builds up fast."
Scores:
  OpenAI Moderation: violence 0.91, self-harm 0.62   -> FLAG
  Perspective:       toxicity 0.88, threat 0.79       -> FLAG
  Llama Guard:       O5 (violence) true              -> FLAG
Verdict: BLOCK (credible harm instructions). Route to human reviewer.
```

```text
Output: "I had a great weekend hiking with my partner."
Scores:
  OpenAI Moderation: all categories < 0.02
  Perspective:       toxicity 0.03, flirtation 0.10
  Detoxify:          severe_toxicity 0.01
Verdict: SAFE.
```

```text
Minor-safe mode (tightened thresholds, ages 0-13):
  Output: "Here is a recipe for a cocktail..."
  OpenAI Moderation: sexual 0.34 (default threshold 0.5 would pass; minor-safe threshold 0.3 fails)
  Llama Guard: O3 (sexual content) true
Verdict: FLAGGED under minor-safe mode (would pass default mode). Always run mode-aware thresholds.
```

## Common Pitfalls

- Using a single classifier — false negatives slip through; production needs at least two independent classifiers.
- Logging full flagged text to third-party APIs (Perspective, OpenAI) without consent — privacy violation and often a
  contractual breach.
- Changing thresholds silently — audit trails break and past verdicts become unreproducible.
- Auto-passing borderline CSAM or self-harm cases — these are always BLOCK and always route to a human reviewer.
- Classifying only the output and not the input — unsafe inputs elicit unsafe outputs.
- Treating a `SAFE` verdict as a guarantee — record classifier versions and confidence; it is probabilistic.

## References

- OpenAI Moderation API: https://platform.openai.com/docs/guides/moderation
- Google Perspective API: https://www.perspectiveapi.com/
- Inan, H. et al. (2023). "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations."
  Meta. https://arxiv.org/abs/2312.06674
- Detoxify (Unitary): https://github.com/unitaryai/detoxify
- Companion skills: `pii-leak-detector`, `prompt-injection-detector`, `bias-auditor`.
