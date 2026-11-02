---
name: consistency-checker
description: Check that an LLM produces semantically consistent outputs across temperature variations, paraphrased inputs, and repeated samples at fixed temperature. Use when outputs must be reliable (medical, legal, factual Q&A) and high variance signals unreliability.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [consistency, self-consistency, reliability, llm]
related: [ai-output-judgement/response-quality-scorer, ai-output-judgement/coherence-fluency-scorer]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1800
cost_warning: Requires LLM API calls for sampling — budget accordingly.
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Consistency Checker

## When To Use
- The same query must yield the same answer regardless of decoding randomness (factual Q&A, classification, structured extraction).
- Trigger keywords: "consistency", "self-consistency", "temperature variation", "paraphrase invariance", "reliability audit", "CoT consistency".
- A reviewer wants a reliability metric, not just a single accuracy number.
- The model is being compared to a predecessor and consistency drift would matter.

## Workflow
1. Run three consistency probes:
   (a) Temperature sweep — same prompt at T = {0.0, 0.3, 0.7, 1.0}, k samples each (default k=3).
   (b) Paraphrase invariance — generate 3-5 paraphrases of the prompt, run at T=0.0, compare outputs.
   (c) Fixed-temperature self-consistency — n samples at T=0.7, measure semantic agreement.
2. For each probe, compute semantic similarity between outputs using sentence embeddings (`all-MiniLM-L6-v2`) and pairwise cosine.
3. For free-form outputs, additionally extract atomic claims and measure claim-set overlap (Jaccard).
4. For multiple-choice / numeric tasks, compute exact-match agreement and a majority-vote answer; report the share of samples matching the majority.
5. Aggregate metrics:
   - Temperature consistency = mean pairwise cosine across the temperature sweep.
   - Paraphrase consistency = mean pairwise cosine across paraphrases.
   - Self-consistency = share of samples matching the majority answer at T=0.7.
6. Flag a prompt as `UNRELIABLE` if any consistency metric falls below 0.80 (cosine) or 0.70 (majority share).
7. Emit a per-prompt consistency report plus the most divergent sample pair for manual inspection.

## Inputs
- A set of prompts to probe (required).
- Model endpoint with controllable temperature and seed (required).
- Optional: paraphrase generator (an LLM or rule-based synonym substitution).
- Optional: thresholds (cosine 0.80, majority share 0.70) and sample counts.

## Outputs
- `consistency.jsonl` — one row per prompt with the three metrics, majority answer, and a pass/fail flag.
- `consistency_report.md` — per-prompt table, overall reliability rate, worst offenders.
- `divergent_pairs.md` — the most divergent output pair per failing prompt for manual inspection.

## Key Rules
- T=0.0 runs must be perfectly reproducible (same seed → same output); if not, the endpoint is not deterministic and the audit is invalid.
- Paraphrases must preserve meaning — validate by having a second LLM judge semantic equivalence before trusting.
- For safety-critical domains, raise thresholds (cosine ≥ 0.90, majority ≥ 0.90).
- Always include the majority answer so downstream pipelines can use it as a stabilized prediction.
- Distinguish semantic consistency (this run says the same thing) from factual correctness (this run says the right thing) — they are not the same.

## Examples

```text
Prompt: "What is the freezing point of water in Celsius?"
Temperature sweep:
  T=0.0 (×3): "0°C" / "0°C" / "0°C"
  T=0.3 (×3): "0°C" / "0 degrees Celsius" / "Water freezes at 0°C"
  T=0.7 (×3): "0°C" / "32°F which is 0°C" / "0°C"
  T=1.0 (×3): "0°C" / "Water freezes at 0 degrees" / "0 degrees Celsius"
Cosine mean: 0.94. Majority answer: "0°C". Verdict: CONSISTENT.
```

```text
Prompt: "Should I take aspirin daily?"
Temperature sweep:
  T=0.0: "Consult your doctor."
  T=0.7: "Daily aspirin can prevent heart attacks in high-risk patients."
  T=1.0: "Some studies suggest benefits; side effects include bleeding."
Cosine mean: 0.41. Majority share: 0.33. Verdict: UNRELIABLE.
Recommendation: deterministic guardrails or refusal template before deployment.
```

## Common Pitfalls
- Treating semantic consistency as correctness — a model can be confidently and consistently wrong; pair with `factuality-checker`.
- Paraphrases that subtly change meaning — invalidate the probe; validate paraphrases with a second LLM judge before use.
- Running on a non-deterministic T=0 endpoint — the audit is invalid if T=0 is not reproducible.
- Reporting a single sample at fixed temperature — too noisy; use n ≥ 5 samples.
- Ignoring the majority answer — it wastes the self-consistency signal that Wang et al. introduced.
- Lowering thresholds to make a model "pass" — keep thresholds documented and fixed across model comparisons.

## References
- Wang, X. et al. (2023). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." ICLR. https://arxiv.org/abs/2203.11171
- Reimers, N. & Gurevych, I. (2019). "Sentence-BERT." EMNLP. https://arxiv.org/abs/1908.10084
- Tamkin, A. et al. (2021). "Task Ambiguity in Humans and Language Models." https://arxiv.org/abs/2212.10681
- Companion skills: `factuality-checker`, `response-quality-scorer`, `llm-as-judge-evaluator`.
