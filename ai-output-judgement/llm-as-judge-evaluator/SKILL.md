---
name: llm-as-judge-evaluator
description: Run LLM-as-judge evaluation over (input, output) pairs using a rubric prompt template, parse scores, and mitigate known judge biases (position, verbosity, self-enhancement) via order swapping, length normalization, and cross-model judges. Use when you need a scalable automated evaluator for chatbot, summarization, or instruction-following tasks.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [llm-as-judge, evaluation, rubrics, bias]
related: [ai-output-judgement/response-quality-scorer, ai-output-judgement/consistency-checker, ai-output-judgement/evaluation-harness-builder]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 2400
cost_warning: Requires LLM API calls — budget for judge model usage.
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# LLM-as-Judge Evaluator

## When To Use
- You need to score many (prompt, response) pairs at scale where human grading is too costly.
- Trigger keywords: "LLM judge", "auto-eval", "rubric scoring", "MT-Bench", "chatbot arena", "pairwise comparison".
- Comparing two model variants (A/B) on a benchmark and need a reproducible verdict.
- Pre-screening outputs before a smaller human-rating round.

## Workflow
1. Define the rubric. Default dimensions: `correctness`, `clarity`, `completeness`, `instruction-following`, each scored 1-5 with anchor descriptions per integer.
2. Build the judge prompt template: include the user query, the candidate response, the rubric, an instruction to output strictly JSON `{"correctness": int, "clarity": int, "completeness": int, "instruction_following": int, "rationale": str}`.
3. For pairwise comparisons (model A vs. model B), run the judge twice with swapped ordering to control position bias; emit the verdict only if both orders agree, otherwise mark `inconclusive`.
4. Length-normalize the final score (`score / max_score` and adjust by response-token count) to dampen verbosity bias.
5. Use a different judge model family than the model under evaluation to avoid self-enhancement bias.
6. Repeat each judgment with k≥3 samples at temperature 0.3; report mean, std, and majority label.
7. Compute inter-judge agreement: run a second judge model on the same pairs and report Cohen's kappa (or weighted kappa for ordinal scores). Target κ ≥ 0.6 before trusting the setup.
8. Aggregate per dimension, per task, and per model. Emit a leaderboard table plus a JSONL of every raw judgment for auditability.

## Inputs
- A list of `{id, prompt, response}` records (single-response scoring) or `{id, prompt, response_a, response_b}` (pairwise).
- A judge model endpoint (OpenAI, Anthropic, or local HF model) and API key.
- Optional: rubric override file and a few-shot set of graded examples.
- Optional: target agreement threshold (default κ ≥ 0.6).

## Outputs
- `judgments.jsonl` — one row per (pair, judge_run) with raw scores, rationale, and run metadata.
- `leaderboard.md` — mean per dimension, overall, win-rate for pairwise, kappa between judges.
- `bias_report.md` — diagnostics: order-swap disagreement rate, length-score correlation, self-judge inflation rate.

## Key Rules
- Always swap order in pairwise comparisons; treat disagreements as `inconclusive`, not as ties.
- Never use the same model family as both candidate and judge for final scoring (allowed only for sanity checks).
- Force structured JSON output and validate parsing; reject and retry on malformed output up to 2 times.
- Report kappa (or weighted kappa) alongside scores — a single judge without agreement data is untrustworthy.
- Lock the rubric and judge prompt in version control; record model ID and date for reproducibility.
- Length-normalize but never hide raw lengths — surface both so reviewers can detect verbosity bias.

## Examples

```text
Prompt:    "Explain photosynthesis in 2 sentences to a 10-year-old."
Response:  "Plants use sunlight to make food. They take in water and air and turn them into sugar
            and oxygen inside their leaves."
Judge output:
  {"correctness": 5, "clarity": 5, "completeness": 4, "instruction_following": 5,
   "rationale": "Accurate and age-appropriate; misses the word 'chlorophyll' but stays within scope."}
Length-normalized overall: 4.75 / 5.00
```

```text
Pairwise A vs. B, order-swapped:
  Order A-first: judge picks B.  Order B-first: judge picks B.  Verdict: B wins.
  Order A-first: judge picks A.  Order B-first: judge picks B.  Verdict: inconclusive (position bias).
Inter-judge kappa (GPT-4o vs. Claude): 0.71 — above threshold.
```

```text
Self-enhancement bias check:
  Candidate model: GPT-4o-mini   Judge: GPT-4o-mini   mean score: 4.31
  Candidate model: GPT-4o-mini   Judge: Claude-3.5     mean score: 3.92
  Inflation: 0.39 — switch to the cross-family judge before reporting.
```

## Common Pitfalls
- Skipping the order swap in pairwise comparisons — position bias silently inflates the first-position win rate by 10-20 percentage points in many judge models.
- Using the same model family as both candidate and judge — self-enhancement bias over-rates the candidate; switch families for the final score.
- Reporting a single judge run without inter-judge agreement (kappa) — a single verdict carries no reliability signal.
- Allowing free-form judge output — unstructured prose breaks parsing and yields noisy scores; force JSON.
- Forgetting length normalization before declaring a winner — verbose responses routinely out-score concise ones regardless of quality.
- Running the judge at high temperature — judgments become irreproducible; use T ≤ 0.3.

## References
- Zheng, L. et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." NeurIPS. https://arxiv.org/abs/2306.05685
- Dubois, Y. et al. (2024). "Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators." https://arxiv.org/abs/2404.04475
- Cohen, J. (1960). "A Coefficient of Agreement for Nominal Scales." *Educational and Psychological Measurement* 20(1).
- Companion skills: `response-quality-scorer`, `relevance-scorer`, `faithfulness-scorer`.
