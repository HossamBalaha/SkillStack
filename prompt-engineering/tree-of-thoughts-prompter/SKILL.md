---
name: tree-of-thoughts-prompter
description: 'Build Tree-of-Thoughts (ToT) prompts that turn reasoning into a search problem: generate multiple candidate "thoughts" per step, evaluate each state, and explore via BFS or DFS until a solution is found. Use when CoT is insufficient for tasks requiring planning, backtracking, or comparison of partial solutions — e.g., 24-game, creative writing, crosswords, or multi-step puzzles where a wrong early commitment sinks the whole chain.'
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [tree-of-thoughts, search, planning, reasoning, llm]
related: [prompt-engineering/chain-of-thought-prompter, prompt-engineering/react-agent-prompter, prompt-engineering/system-prompt-architect]
prerequisites: []
outputs: [markdown, json, python]
difficulty: advanced
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Tree-of-Thoughts Prompter

## When To Use

- The task rewards exploring alternatives and backtracking (24-game, Sudoku-style puzzles, creative writing with
  constraints).
- A linear CoT chain commits too early and cannot recover from a wrong mid-step.
- You have a budget for many more LLM calls than CoT — ToT makes 10-100x more calls per question.
- Trigger keywords: tree-of-thoughts, ToT, search over reasoning, state evaluation, BFS, DFS, thought branching.
- You can define a state evaluator that scores partial solutions.

## Workflow

1. Define the thought decomposition: how many thoughts per node, the depth of the tree, and the branching factor.
2. Author three prompt templates:
   (a) **Thought generator** — given the current state, propose K next thoughts. (b) **State evaluator** — given a
   state, score it as "sure / maybe / impossible" or a numeric value 1-10. (c) **Answer extractor** — when a leaf state
   passes the goal check, format the final answer.
3. Pick the search strategy: BFS (keep top-B states per depth) or DFS with backtracking on dead states.
4. Set the stopping conditions: goal state reached, max depth reached, or all branches evaluated as "impossible".
5. Implement the harness: a queue/stack of states, each with its reasoning history and evaluation score.
6. Add memoization on state hashes so identical partial states are not re-expanded.
7. Log every generated thought, its score, and whether it survived pruning — the trace is the asset.
8. Evaluate on a task with known gold answers (24-game, Creative Writing from the ToT paper) and report success rate,
   nodes expanded, and LLM calls per task.

## Inputs

- Task prompt and a goal-check predicate.
- Parameters: branching factor K, beam width B, max depth D, search strategy (BFS/DFS).
- Three prompt templates: thought generator, state evaluator, answer extractor.
- Eval set with gold answers.

## Outputs

- `thought_generator.txt` — the template for proposing K next thoughts from a state.
- `state_evaluator.txt` — the template for scoring a state.
- `search_harness.py` — the BFS/DFS loop with memoization.
- `search_tree.json` — full expansion: nodes, scores, parents, pruned flag, leaf flag.
- `eval_report.md` — success rate, avg nodes expanded, avg LLM calls, latency.

## Key Rules

- The state evaluator is the bottleneck — a noisy evaluator dooms the search even with perfect thought generation.
- Always cap depth and branching factor; unbounded ToT diverges into expensive dead branches.
- Memoize on state hashes to avoid re-expanding identical subtrees.
- Compare ToT against CoT baseline at matched LLM-call budget — ToT that uses 50x the calls to beat CoT by 5 points is
  rarely worth it in production.
- Log the full search tree; without it, ToT failures are unexplainable.
- Prefer BFS for shallow trees (depth ≤ 4) and DFS with backtracking for deeper ones.

## Examples

```text
24-game with ToT (state = expression so far, target = 24):

State: "4 7 8 8"
Thought generator outputs (K=3):
  T1: "(8 / (8 - (7 - 4)))"   # state evaluator: sure (resolves to 24)
  T2: "(7 - 4) * 8"           # state evaluator: impossible (only uses 3 of 4 numbers)
  T3: "(4 + 7) + (8 - 8)"     # state evaluator: maybe (resolves to 11, wrong target)
BFS keeps T1, drops T2, defers T3.
Answer extractor emits: 8 / (8 - (7 - 4)) = 24.
```

```python
def RunTreeOfThoughts(RootState, GenerateThoughts, EvaluateState, BeamWidth, MaxDepth):
  # Maintain the open frontier as a list of states.
  Frontier = [RootState]
  # Loop until the frontier is empty or the depth budget is exhausted.
  for Depth in range(MaxDepth):
    # Expand every state in the frontier by generating K thoughts.
    Candidates = []
    # Generate thoughts for each frontier state.
    for State in Frontier:
      # Ask the model for K candidate next thoughts.
      Thoughts = GenerateThoughts(State)
      # Score each thought with the state evaluator.
      for Thought in Thoughts:
        # Append the scored thought to the candidate pool.
        Candidates.append((Thought, EvaluateState(Thought)))
    # Sort candidates by descending evaluator score.
    Candidates.sort(key=lambda Pair: Pair[1], reverse=True)
    # Keep the top BeamWidth candidates as the next frontier.
    Frontier = [Candidate[0] for Candidate in Candidates[:BeamWidth]]
    # Check whether any frontier state passes the goal check.
    for State in Frontier:
      # Return immediately when the goal is reached.
      if (IsGoal(State)):
        # Return the goal state and stop the search.
        return State
  # Raise when no goal state was found within the budget.
  raise RuntimeError("No solution found within depth budget.")
```

## References

- Yao, S. et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models."
  https://arxiv.org/abs/2305.10601
- Long, J. (2023). "Large Language Model Guided Tree-of-Thought." https://arxiv.org/abs/2305.08291
- 24-game dataset (ToT paper): https://github.com/princeton-nlp/tree-of-thought-llm
