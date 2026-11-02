---
name: evaluation-harness-builder
description: Build standardized evaluation harnesses for LLMs in the style of EleutherAI lm-evaluation-harness, OpenAI Evals, and Stanford HELM. Define the task suite, configure the model endpoint, run with few-shot prompting, compute metrics, and aggregate results into a leaderboard JSON. Use when benchmarking a new model or comparing variants on standard suites.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [eval-harness, benchmark, mmlu, helm]
related: [ai-output-judgement/llm-as-judge-evaluator, ai-output-judgement/response-quality-scorer]
prerequisites: []
outputs: [python, json, bash]
difficulty: advanced
estimated_tokens: 2000
cost_warning: Runs benchmarks against model APIs — usage costs apply.
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Evaluation Harness Builder

## When To Use

- A new model variant must be benchmarked on standard suites (MMLU, GSM8K, HumanEval, TruthfulQA, etc.).
- Trigger keywords: "eval harness", "lm-evaluation-harness", "HELM", "OpenAI Evals", "MMLU", "pass@k", "leaderboard".
- Comparing two model checkpoints or two prompt templates on the same tasks reproducibly.
- A research paper requires a leaderboard-style results table.

## Workflow

1. Define the task suite. Default recommended set: MMLU (57-subject knowledge), GSM8K (grade-school math), HumanEval
   (code pass@1, pass@10), TruthfulQA (honesty), HellaSwag (commonsense), ARC-Challenge (science QA), WinoGrande
   (coreference), BBH (reasoning). For domain-specific evals, add PubMedQA, LegalBench, FinanceBench.
2. Configure the model endpoint:
    - Local HF model: load via `transformers` or `vLLM`, fix seed and temperature per task (T=0 for deterministic tasks,
      T=0.7 + n≥20 for pass@k).
    - API model (OpenAI, Anthropic, Together): set the API key, retry with exponential backoff, cache responses.
3. Define metrics per task: accuracy (multiple-choice), exact-match (QA), pass@k (code), BLEU/ROUGE (generation),
   FActScore (factuality). Use standard formulas.
4. Apply few-shot prompting consistently (default: 5-shot for MMLU, 0-shot for GSM8K with chain-of-thought, 0-shot for
   HumanEval). Lock the few-shot examples in version control.
5. Run the harness with deterministic seeds; record per-example outputs, prompts, and raw model responses to disk.
6. Compute metrics, with confidence intervals via bootstrap. Run a second seed to detect instability.
7. Aggregate into a leaderboard JSON: `{model, task, metric, value, ci, n_shot, seed, timestamp}`. Emit a markdown
   leaderboard table sorted by overall rank.

## Inputs

- The model under test (HF checkpoint path or API endpoint; required).
- The task suite (named standard suite or custom YAML/JSON; required).
- Optional: few-shot configuration, generation parameters (T, top_p, max_tokens, n_samples), seed.
- Optional: a reference model for pairwise comparison.

## Outputs

- `leaderboard.json` — per-task metrics with CIs, seeds, and timestamps.
- `leaderboard.md` — markdown table sorted by overall rank, with per-task columns.
- `raw_outputs.jsonl` — per-example prompt, response, parsed answer, correctness (for auditability).
- `config.yaml` — frozen config of the run (model, suite, few-shot, seed, date) for reproducibility.

## Key Rules

- Lock the few-shot examples, prompts, and seeds in version control; reproducibility is non-negotiable.
- Use the canonical metric formula per task (e.g., HumanEval pass@k uses the unbiased estimator from Chen et al. 2021).
- Report confidence intervals; do not crown a winner if CIs overlap.
- Cache API responses to disk so reruns are cheap and audit trails exist.
- Run a second seed to detect instability — single-seed results are not reliable.
- Disclose which tasks were excluded (e.g., contamination concerns) and why.
- Local and API models must use the same prompts and few-shot counts; mixing formats invalidates comparisons.

## Examples

```text
Config (config.yaml):
  model: meta-llama/Llama-3-8B-Instruct
  suite: [mmlu, gsm8k, humaneval, truthfulqa, hellaswag]
  few_shot: {mmlu: 5, gsm8k: 0, humaneval: 0, truthfulqa: 0, hellaswag: 0}
  seed: 42
  temperature: {humaneval: 0.7, default: 0.0}
  n_samples: {humaneval: 20, default: 1}

Leaderboard (excerpt):
  | Model              | MMLU  | GSM8K | HumanEval pass@1 | TruthfulQA | HellaSwag |
  | Llama-3-8B-Instruct| 66.7  | 79.6  | 72.1             | 57.5       | 78.6      |
  | Mistral-7B-Instruct| 60.1  | 52.2  | 40.3             | 42.2       | 73.3      |
CIs via 1000-iter bootstrap, seed 42 and 43.
```

```text
Raw output record (raw_outputs.jsonl):
  {"task": "mmlu_anatomy", "prompt": "...", "response": "A", "parsed": "A",
   "gold": "A", "correct": true, "seed": 42, "timestamp": "2025-01-15T10:23:01Z"}
```

## References

- EleutherAI lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness
- Stanford HELM (Holistic Evaluation of Language Models): https://crfm.stanford.edu/helm — paper: Liang et al.
  (2022) https://arxiv.org/abs/2211.09110
- OpenAI Evals: https://github.com/openai/evals
- Hendrycks, D. et al. (2021). "Measuring Massive Multitask Language Understanding." (MMLU)
  ICLR. https://arxiv.org/abs/2009.03300
- Cobbe, K. et al. (2021). "Training Verifiers to Solve Math Word Problems." (GSM8K) https://arxiv.org/abs/2110.14168
- Chen, M. et al. (2021). (HumanEval, pass@k) https://arxiv.org/abs/2107.03374
- Lin, S. et al. (2022). (TruthfulQA) https://arxiv.org/abs/2109.07958
- Companion skills: `response-quality-scorer`, `llm-as-judge-evaluator`, `code-output-validator`, `alignment-evaluator`.
