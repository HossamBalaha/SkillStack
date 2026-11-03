---
name: chain-of-thought-prompter
description: Design chain-of-thought (CoT) prompts that elicit step-by-step reasoning from large language models. Use when accuracy on multi-step arithmetic, commonsense, symbolic, or logical tasks drops under direct prompting, or when you need zero-shot CoT ("Let's think step by step"), few-shot CoT with worked examples, or self-consistency sampling over multiple reasoning paths.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [chain-of-thought, reasoning, few-shot, self-consistency, llm]
related: [prompt-engineering/tree-of-thoughts-prompter, prompt-engineering/few-shot-template-builder, prompt-engineering/system-prompt-architect]
prerequisites: []
outputs: [markdown, json, python]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Chain-of-Thought Prompter

## When To Use

- The task requires multi-step reasoning (arithmetic, commonsense, symbolic manipulation, logic puzzles).
- A direct prompt produces low accuracy and the model answers in one shot without showing work.
- You want to compare zero-shot CoT, few-shot CoT, and self-consistency variants on the same task.
- Trigger keywords: chain-of-thought, CoT, self-consistency, reasoning trace, step-by-step, "let's think".
- You need to audit the reasoning trace, not just the final answer.

## Workflow

1. Classify the task: arithmetic (GSM8K-style), commonsense (CommonsenseQA-style), or symbolic (last-letter
   concatenation).
2. Decide between zero-shot CoT (append "Let's think step by step.") and few-shot CoT (provide 2-8 worked exemplars with
   human-written reasoning traces).
3. For few-shot CoT, hand-author each exemplar: question, full reasoning trace ending in "The answer is X.", and the
   final answer on its own line.
4. Pick an answer-extraction pattern (e.g., `The answer is \boxed{X}`) so the final token is machine-parseable.
5. If the task tolerates extra latency, run self-consistency: sample N=5-40 chains at temperature 0.5-0.7, then
   marginalize the final answers by majority vote.
6. Run a baseline (direct prompt with no reasoning) on the same eval set so you can report the lift CoT provides.
7. Inspect the reasoning traces on failure cases — a wrong final answer with a clean trace reveals a knowledge gap,
   while a broken trace reveals a prompting issue.
8. Tune the number and order of exemplars; recent work shows exemplar order and label balance shift accuracy.
9. Document the final prompt, the sampling configuration, and the measured accuracy lift in a single JSON manifest.

## Inputs

- Task definition and 5-20 seed questions with gold answers.
- (Optional) Worked exemplars written by a domain expert.
- Eval set with ground-truth answers (e.g., GSM8K, StrategyQA).
- Sampling budget: max tokens per chain, number of samples N for self-consistency.

## Outputs

- `prompt_zero_shot.txt` — base instruction plus the "Let's think step by step." suffix.
- `prompt_few_shot.txt` — instruction plus K exemplars with reasoning traces.
- `exemplars.json` — list of `{Question, Trace, Answer}` objects, one per exemplar.
- `eval_results.jsonl` — per-question: chain(s), extracted answer, gold, correct flag.
- `summary.json` — accuracy of direct, zero-shot CoT, few-shot CoT, and self-consistency variants.

## Key Rules

- Every exemplar trace must end with an explicit answer statement parseable by regex.
- Never edit a single exemplar to fix one test case — exemplars are shared across the whole eval set.
- For self-consistency, keep temperature ≥ 0.5 so samples actually differ; at temperature 0 it collapses to one chain.
- Report accuracy with a direct-prompt baseline; a CoT lift below 2 points means CoT is not the right tool.
- Exemplars must use the same answer-extraction pattern as the test cases.
- Keep traces concise — long traces blow the context budget without raising accuracy past a saturation point.

## Examples

```text
Few-shot CoT exemplar:

Q: A cafeteria had 23 apples. They used 8 for lunch and bought 5 more. How many do they have?
A: They started with 23 apples. They used 8, so 23 - 8 = 15 remain.
   They bought 5 more, so 15 + 5 = 20. The answer is 20.
```

```python
def BuildSelfConsistencySampler(PromptTemplate, Question, SampleCount, Temperature):
  # Store the sampled chains in a list for downstream voting.
  Chains = []
  # Sample SampleCount reasoning chains at the requested temperature.
  for Index in range(SampleCount):
    # Generate one chain by calling the model with the prompt template.
    Chain = CallModel(PromptTemplate, Question, Temperature)
    # Append the chain to the list.
    Chains.append(Chain)
  # Extract the final answer from each chain using the shared pattern.
  Answers = [ExtractAnswer(Chain) for Chain in Chains]
  # Return the most frequent answer as the consensus.
  return MostCommon(Answers)
```
