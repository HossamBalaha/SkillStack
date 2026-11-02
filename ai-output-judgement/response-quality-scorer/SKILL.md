---
name: response-quality-scorer
description: Score LLM responses on multi-dimensional quality — helpfulness, completeness, relevance, clarity, and depth — each on a 1-5 rubric, with a weighted aggregate. Use when ranking chatbot replies, training reward models, or running A/B tests between model variants.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [response-quality, rlhf, reward-model, evaluation]
related: [ai-output-judgement/llm-as-judge-evaluator, ai-output-judgement/relevance-scorer, ai-output-judgement/coherence-fluency-scorer]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 1900
cost_warning: "Optional: LLM-based scoring may incur API costs."
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Response Quality Scorer

## When To Use

- Ranking candidate chatbot replies for production rollout.
- Producing scalar reward signals for RLHF or DPO training.
- Trigger keywords: "response quality", "reward model", "RLHF", "helpfulness", "A/B test models", "chatbot evaluation".
- Building a leaderboard comparing several model variants on a held-out prompt set.

## Workflow

1. Pick a scoring protocol. Default is pointwise (each response scored independently); pairwise (which is better?) is
   supported via `llm-as-judge-evaluator`.
2. Apply the 5-dimension rubric, each 1-5: `helpfulness`, `completeness`, `relevance`, `clarity`, `depth`. Provide
   anchor descriptions per integer (e.g., 5 = "fully addresses intent with depth and no filler").
3. For each (prompt, response) pair, ask the judge LLM to output JSON with the five scores plus a one-sentence rationale
   per dimension.
4. Compute per-dimension means and a weighted aggregate. Default weights: helpfulness 0.30, completeness 0.20, relevance
   0.20, clarity 0.15, depth 0.15.
5. Sanity-check with a reward model when available (e.g., RewardBench-tracked open models) and report agreement as
   Pearson r.
6. Detect verbosity bias: compute correlation between response length and score; if |r| > 0.4, length-normalize or
   switch to length-controlled scoring.
7. Emit per-response scores, per-prompt means, and a final leaderboard with confidence intervals from bootstrap
   resampling.

## Inputs

- A list of `{prompt, response}` records (and optionally `model_id` to group by).
- A judge LLM endpoint (or a local reward model).
- Optional: rubric override, weight override, held-out human-rated set for calibration.
- Optional: few-shot graded examples to anchor the judge.

## Outputs

- `scores.jsonl` — one row per (prompt, response): five dimension scores, rationale, aggregate, response_length.
- `leaderboard.md` — per-model mean per dimension, weighted aggregate, 95% bootstrap CI, sample size.
- `bias_check.md` — length-score correlation, agreement with reference reward model.

## Key Rules

- Always include the rubric anchors in the judge prompt; bare "score 1-5" yields inconsistent grading.
- One response per scoring call to prevent cross-contamination of judgments.
- If length-score correlation exceeds 0.4, switch to length-controlled mode before trusting rankings.
- Report confidence intervals; do not crown a winner if CIs overlap.
- Calibrate against a held-out human-rated set; report Pearson r vs. humans (target r ≥ 0.7).
- Treat models from the same family as the judge with suspicion (self-enhancement bias).

## Examples

```text
Prompt:   "What's the difference between TCP and UDP?"
Response: "TCP is reliable and ordered; UDP is fast but unreliable. TCP is used for web traffic;
           UDP for streaming."
Scores:   helpfulness 5, completeness 4, relevance 5, clarity 5, depth 3.
Aggregate: 0.30*5 + 0.20*4 + 0.20*5 + 0.15*5 + 0.15*3 = 4.50 / 5.00
```

```text
Leaderboard (5-prompt eval, bootstrap CI):
  | Model          | Help | Compl | Rel  | Clar | Depth | Agg   | 95% CI        |
  | gpt-4o-mini    | 4.6  | 4.2   | 4.8  | 4.7  | 3.9   | 4.46  | [4.31, 4.61]  |
  | llama-3-8b     | 4.1  | 3.8   | 4.3  | 4.2  | 3.1   | 3.96  | [3.78, 4.14]  |
Length-score r = 0.18 — no verbosity bias detected.
```

```text
Calibration against human ratings (held-out set, n=200):
  Judge mean:   4.12   Human mean:   3.87
  Pearson r:    0.74   Spearman rho: 0.71
  Above the r ≥ 0.7 threshold — judge is trustworthy for this domain.
  If r drops below 0.6 on the next model variant, re-anchor the rubric.
```

## Common Pitfalls

- Scoring multiple responses in a single judge call — judgments contaminate each other; one response per call.
- Reporting a mean score without confidence intervals — noisy rankings masquerade as real differences.
- Ignoring the length-score correlation — verbosity bias goes undetected and the leaderboard rewards wordiness.
- Using bare "score 1-5" prompts without rubric anchors — grade distributions drift run to run.
- Crowning a winner when bootstrap CIs overlap — that is a tie, not a victory.
- Forgetting to calibrate against held-out human ratings — the judge may be self-consistent yet systematically biased.

## References

- Lambert, N. et al. (2024). "RewardBench: Evaluating Reward Models for Language
  Modeling." https://arxiv.org/abs/2403.13787
- OpenAI Evals framework: https://github.com/openai/evals
- HELM (Holistic Evaluation of Language Models), Stanford CRFM: https://crfm.stanford.edu/helm
- Companion skills: `llm-as-judge-evaluator`, `relevance-scorer`, `coherence-fluency-scorer`.
