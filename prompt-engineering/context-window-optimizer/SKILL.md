---
name: context-window-optimizer
description: Optimize prompts to fit a model's context window under a token budget — prioritize chunks, summarize before detail, and apply a sliding window over long documents so the most relevant evidence stays in context. Use when prompts blow the token limit, when retrieval returns more chunks than fit, or when latency and cost scale with context length.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [context-window, token-budget, chunking, summarization, llm]
related: [prompt-engineering/rag-prompt-designer, prompt-engineering/prompt-testing-harness, prompt-engineering/few-shot-template-builder]
prerequisites: []
outputs: [python, json, markdown]
difficulty: intermediate
estimated_tokens: 1400
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Context Window Optimizer

## When To Use

- The prompt exceeds the model's context window and the API rejects it.
- Retrieved chunks total more tokens than the budget leaves after reserving room for the instruction and the answer.
- Latency or cost is dominated by context length and you must trim without losing signal.
- Trigger keywords: context window, token budget, chunk prioritization, sliding window, map-reduce summarization, long
  context.
- You need to switch strategies (full context vs. summarize-then-detail) per input.

## Workflow

1. Measure the token budget: `Budget = ModelContextLimit - InstructionTokens - ReserveForAnswer`.
2. Count tokens for every chunk using the model's tokenizer (or a close approximation like `tiktoken`).
3. Pick a strategy:
   (a) **Truncate** — drop chunks past the budget; cheapest, lossiest. (b) **Prioritize** — rank chunks by relevance
   score and keep the top-K within budget. (c) **Summarize-then-detail** — summarize each chunk to a short digest, fit
   all digests, then expand only the top-ranked chunk. (d) **Sliding window** — process the document in windows,
   answering per window and merging at the end.
4. For multi-turn chat, evict old turns first and keep the most recent N turns; never evict the system prompt.
5. Re-count tokens after applying the strategy; assert the rendered prompt is under budget.
6. Log the per-chunk decision (kept, summarized, dropped) so the optimization is auditable.
7. Re-run on the eval set and compare accuracy, latency, and cost against the unoptimized baseline.

## Inputs

- The model's context limit and tokenizer.
- The instruction text and the reserve-for-answer budget (e.g., 1024 tokens).
- The candidate chunks with token counts and relevance scores.
- The strategy choice and its parameters (top-K, summary length, window size).

## Outputs

- `budget.json` — the computed budget with each component's token count.
- `optimized_prompt.txt` — the rendered prompt that fits the budget.
- `chunk_decisions.jsonl` — per chunk: kept, summarized, or dropped with reason.
- `optimization_report.md` — accuracy, latency, cost vs. baseline.

## Key Rules

- Always reserve tokens for the answer — a prompt that fills the context leaves no room for output.
- Use the model's own tokenizer to count tokens; character counts are wrong by 20-40%.
- Never evict the system prompt; evict old user turns first in multi-turn chat.
- Summarize-then-detail is more accurate than truncate but adds latency and cost — pick per use case.
- Re-count tokens after every optimization step; chaining optimizations can still blow the budget.
- Log chunk decisions — without them, accuracy regressions are unexplainable.

## Examples

```text
Budget breakdown (model: 16k tokens):
  Instruction:            800
  System prompt:          300
  Reserve for answer:   1,024
  Available for context: 13,876
Retrieved chunks (7 chunks, 21,000 tokens total):
  Strategy: prioritize by relevance score, keep top-K within 13,876 tokens.
  Decision: keep chunks 1, 3, 4, 6 (15,200 -> 13,500 after trimming); summarize chunks 2, 5, 7.
```

```python
def OptimizeContext(Instruction, Chunks, ModelLimit, ReserveForAnswer):
  # Compute the token budget available for context.
  InstructionTokens = CountTokens(Instruction)
  Budget = ModelLimit - InstructionTokens - ReserveForAnswer
  # Sort chunks by descending relevance score.
  Ranked = sorted(Chunks, key=lambda Chunk: Chunk["Relevance"], reverse=True)
  # Keep chunks until the budget is exhausted.
  Kept = []
  Used = 0
  for Chunk in Ranked:
    # Stop when adding this chunk would exceed the budget.
    if (Used + Chunk["Tokens"] > Budget):
      break
    # Add the chunk to the kept list and tally its tokens.
    Kept.append(Chunk)
    Used += Chunk["Tokens"]
  # Concatenate the kept chunks into a single context block.
  ContextBlock = "\n\n".join(Chunk["Text"] for Chunk in Kept)
  # Return the rendered prompt and the budget audit.
  return Instruction + "\n\n" + ContextBlock, {"Budget": Budget, "Used": Used, "KeptCount": len(Kept)}
```
