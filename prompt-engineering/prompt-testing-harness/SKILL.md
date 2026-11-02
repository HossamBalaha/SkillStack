---
name: prompt-testing-harness
description: Build a prompt testing harness that defines test cases (input, expected output, evaluator), runs a prompt against multiple LLMs, and scores outputs with metrics like exact match, BLEU, ROUGE, and semantic similarity. Use when you need reproducible prompt regression tests, when you compare prompt variants across models, or when you must ship a prompt change with quantitative evidence it does not regress.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [testing, evaluation, regression, llm, metrics]
related: [prompt-engineering/prompt-versioning-system, prompt-engineering/few-shot-template-builder, ai-output-judgement/llm-as-judge-evaluator]
prerequisites: []
outputs: [python, json, csv, markdown]
difficulty: intermediate
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Prompt Testing Harness

## When To Use

- You changed a prompt and need to prove it does not regress on a held-out test set.
- You need to compare the same prompt across models (GPT-4o, Claude, Gemini, Llama) on the same eval set.
- Your prompt has multiple variants and you must pick one with data, not vibes.
- Trigger keywords: prompt testing, regression, eval harness, BLEU, ROUGE, semantic similarity, promptfoo, PromptBench.
- You need a CI gate so a prompt change cannot merge without passing tests.

## Workflow

1. Define test cases in a CSV/JSONL file: each row has `Input`, `ExpectedOutput`, and `Evaluator` (e.g., `exact_match`,
   `contains`, `bleu`, `semantic`).
2. Write the prompt template once; render it per test case with the case's `Input`.
3. Define the model matrix: list of providers + model ids + temperature + max tokens.
4. Run the harness: for each (test case, model) pair, call the model, capture the raw output, and store it.
5. Run the evaluator per case: compute the metric on (model_output, ExpectedOutput).
6. Aggregate per model and per prompt variant: mean metric, pass rate, latency p50/p95, token cost.
7. Diff against the baseline run: flag any case that regressed beyond a tolerance threshold.
8. Emit a Markdown report with a per-case table, a per-model summary, and a go/no-go recommendation.
9. Wire the harness into CI so pull requests touching the prompt must pass before merge.

## Inputs

- `test_cases.jsonl` with `Input`, `ExpectedOutput`, `Evaluator` per row.
- The prompt template under test.
- The model matrix (provider, model id, temperature, max tokens).
- The baseline run id to diff against.
- (Optional) API keys for each provider, supplied via environment variables.

## Outputs

- `run_<timestamp>/outputs.jsonl` — per case: model, input, expected, actual, metric, latency, tokens.
- `run_<timestamp>/summary.csv` — per model: mean metric, pass rate, p50/p95 latency, total tokens.
- `run_<timestamp>/diff.md` — cases that regressed vs the baseline, with before/after outputs.
- `run_<timestamp>/report.md` — human-readable go/no-go report.
- `ci_gate.txt` — `PASS` or `FAIL` consumed by CI.

## Key Rules

- Test cases are immutable; never edit them to make a prompt pass — file a new case instead.
- Each evaluator must be deterministic; non-deterministic evaluators (LLM-as-judge) need a fixed seed and a fixed judge
  prompt.
- Run each case at least 3 times for non-deterministic models; report mean and variance.
- Pin the model id and the provider SDK version — silent upgrades change behavior.
- A regression on one case blocks the merge even if the mean improves — means hide tail regressions.
- Latency and token cost must be reported alongside accuracy — a 1% accuracy gain at 3x cost is rarely worth it.

## Examples

```text
test_cases.jsonl:
  {"Input": "Capital of France?", "ExpectedOutput": "Paris", "Evaluator": "exact_match"}
  {"Input": "Translate 'hello' to French.", "ExpectedOutput": "bonjour", "Evaluator": "contains"}
  {"Input": "Summarize: ...", "ExpectedOutput": "<reference summary>", "Evaluator": "bleu"}
```

```python
def RunHarness(TestCases, PromptTemplate, ModelMatrix, Evaluators):
  # Collect one result row per (case, model) pair.
  Results = []
  # Iterate over every test case.
  for Case in TestCases:
    # Iterate over every model in the matrix.
    for Model in ModelMatrix:
      # Render the prompt by substituting the case input.
      Prompt = PromptTemplate.replace("{{Input}}", Case["Input"])
      # Call the model and capture the raw output.
      Output = CallModel(Model, Prompt)
      # Look up the evaluator by its name.
      Evaluator = Evaluators[Case["Evaluator"]]
      # Score the output against the expected answer.
      Score = Evaluator(Output, Case["ExpectedOutput"])
      # Append the result row.
      Results.append({"CaseId": Case["Id"], "Model": Model["Id"], "Score": Score, "Output": Output})
  # Return the full result set for aggregation.
  return Results
```

## References

- promptfoo — prompt testing & evaluation: https://www.promptfoo.dev/
- PromptBench — unified framework for prompt evaluation: https://arxiv.org/abs/2312.03964
- LangSmith — LLM application tracing & eval: https://docs.smith.langchain.com/
- SacreBLEU — reproducible BLEU: https://github.com/mjpost/sacrebleu
- Companion skills: `prompt-versioning-system`, `llm-as-judge-evaluator`.
