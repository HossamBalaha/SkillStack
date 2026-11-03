---
name: react-agent-prompter
description: Build ReAct (Reasoning + Acting) prompts that interleave Thought, Action, and Observation steps so an LLM can call external tools before answering. Use when a task needs retrieval, calculation, API lookup, or database query that the model cannot do from weights alone — e.g., open-book QA, current-events lookup, multi-hop reasoning, or any agent that must use tools.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [react, agents, tool-use, reasoning, llm]
related: [prompt-engineering/agent-orchestration-prompter, prompt-engineering/rag-prompt-designer, prompt-engineering/chain-of-thought-prompter]
prerequisites: []
outputs: [markdown, json, python]
difficulty: intermediate
estimated_tokens: 1600
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# ReAct Agent Prompter

## When To Use

- The task requires external tools (search, calculator, code interpreter, SQL, REST API) the LLM cannot answer from
  weights alone.
- Direct prompting hallucinates facts, dates, or numerical results that need verification.
- A multi-hop question forces the model to retrieve, then reason over retrieved evidence.
- Trigger keywords: ReAct, agent loop, Thought/Action/Observation, tool use, multi-step reasoning, agent harness.
- You need an auditable trace of every decision and tool call the agent made.

## Workflow

1. Enumerate the tools the agent may call. For each tool, write a name, a one-sentence description, and a JSON argument
   schema.
2. Write the system prompt: define the agent role, list the available tools, and specify the stop conditions (answer
   ready, max steps reached, tool error).
3. Specify the output format the model must emit on each turn: `Thought: ...`, `Action: toolName[argument]`, then wait
   for `Observation: ...` injected by the harness.
4. Provide 2-3 few-shot exemplars showing a complete Thought/Action/Observation loop ending in `Final Answer: ...`.
5. Define the harness contract: parse `Action:`, dispatch to the tool, format the return value as `Observation:`, and
   feed it back into the next prompt.
6. Set a hard step cap (e.g., 8) and a token cap per turn so the loop cannot diverge.
7. Add error handling: if the action is malformed or the tool throws, inject `Observation: ERROR: <message>` and let the
   model recover.
8. Log every turn to a trace file (Thought, Action, Observation, latency, token cost) for post-run debugging.
9. Evaluate on a held-out task set; report task success rate, average steps, and average tool calls per task.

## Inputs

- Tool catalog with name, description, argument schema, and a Python callable per tool.
- Few-shot exemplars of completed Thought/Action/Observation traces.
- Eval tasks with ground-truth final answers (e.g., HotpotQA, ALFWorld).
- Harness parameters: max steps, max tokens per turn, stop strings.

## Outputs

- `system_prompt.txt` — role, tools, format spec, exemplars.
- `tools.json` — tool catalog with schemas and dispatch pointers.
- `harness.py` — the loop that parses actions, calls tools, and feeds observations back.
- `traces.jsonl` — per-task trace of every Thought/Action/Observation, with token cost and latency.
- `eval_report.md` — success rate, avg steps, tool-call frequency, and failure mode clusters.

## Key Rules

- The model must never see tool outputs that were not produced by the harness — fabricated Observations are the #1 ReAct
  failure mode.
- Every Action must be machine-parseable by a fixed regex; free-form actions break the loop.
- Stop on `Final Answer:` or the step cap, whichever comes first — no infinite loops.
- Tool errors must surface as `Observation: ERROR: ...` so the agent can recover rather than hallucinate.
- Keep the tool list small (≤ 10) — large catalogs confuse the model and slow dispatch.
- Log every turn; without traces, debugging agent failures is guesswork.

## Examples

```text
Question: What is the population of the country whose capital is Ottawa?

Thought 1: I need to identify the country whose capital is Ottawa, then look up its population.
Action 1: Search[capital of Canada]
Observation 1: Ottawa is the capital of Canada.
Thought 2: Ottawa is the capital of Canada, so the country is Canada. Now I need Canada's population.
Action 2: Lookup[Canada population 2024]
Observation 2: Canada's 2024 population is approximately 39 million.
Thought 3: I have the answer.
Final Answer: Approximately 39 million.
```

```python
def RunReactLoop(SystemPrompt, Question, Tools, MaxSteps):
  # Build the running transcript that grows every step.
  Transcript = f"Question: {Question}\n"
  # Loop until the step cap is hit or the agent emits a final answer.
  for Step in range(MaxSteps):
    # Ask the model for the next Thought/Action pair.
    Output = CallModel(SystemPrompt, Transcript)
    # Append the model output to the transcript.
    Transcript += Output
    # Check whether the agent signalled completion.
    if (Output.startswith("Final Answer:")):
      # Return the final answer and the full transcript.
      return Output, Transcript
    # Parse the tool name and arguments from the Action line.
    ToolName, Arguments = ParseAction(Output)
    # Execute the requested tool against its arguments.
    Observation = Tools[ToolName](Arguments)
    # Append the observation so the model can reason over it next.
    Transcript += f"Observation: {Observation}\n"
  # Raise when the agent exhausted its step budget without finishing.
  raise RuntimeError("Step budget exhausted before Final Answer.")
```
