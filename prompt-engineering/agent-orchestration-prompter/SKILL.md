---
name: agent-orchestration-prompter
description: Build multi-agent orchestration prompts that assign roles to agents, define a message-passing protocol, decompose tasks across agents, and aggregate their results. Use when a single agent cannot solve the task end-to-end, when the workflow needs specialized roles (planner, researcher, coder, critic), or when you must coordinate N agents with a stable communication contract.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [multi-agent, orchestration, message-passing, agentic, llm]
related: [prompt-engineering/react-agent-prompter, prompt-engineering/system-prompt-architect, prompt-engineering/chain-of-thought-prompter]
prerequisites: []
outputs: [markdown, json, python]
difficulty: advanced
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

# Agent Orchestration Prompter

## When To Use

- A single agent cannot solve the task end-to-end (planning, retrieval, coding, and critique all need different
  behavior).
- The workflow needs specialized roles (planner, researcher, coder, reviewer).
- You must coordinate N agents with a stable communication contract.
- Trigger keywords: multi-agent, orchestration, role assignment, message passing, task decomposition, AutoGen, CrewAI,
  LangGraph.
- You need an auditable trace of which agent produced which intermediate artifact.

## Workflow

1. Decompose the task into roles: list each role with a one-sentence responsibility, an input contract, and an output
   contract.
2. Define the message-passing protocol: a fixed envelope `{From, To, Type, Payload, TraceId}` that every agent emits and
   every other agent parses.
3. Write one system prompt per role — each prompt states the role, its input/output contract, and the rule to never
   impersonate another role.
4. Pick a topology: pipeline (linear chain), hub-and-spoke (one coordinator fans out to specialists), or graph
   (arbitrary connections declared as edges).
5. Pick a termination condition: a "done" message from the final aggregator, a max round cap, or a goal-check predicate.
6. Implement the orchestrator: route messages per the topology, log every message, and enforce the round cap.
7. Add a result-aggregation step: the final agent (or the orchestrator) merges the sub-results into a single artifact,
   resolving conflicts by a declared rule (latest-wins, majority vote, or human escalation).
8. Log every (From, To, Payload, Round) tuple so the whole run is replayable.
9. Evaluate on a multi-step task set; report task success rate, average rounds, and average messages per task.

## Inputs

- The task description.
- The role roster with responsibilities and input/output contracts.
- The topology (pipeline, hub-and-spoke, or graph) and the termination condition.
- A goal-check predicate (for graph topologies).

## Outputs

- `roles.json` — the role roster with system prompts and contracts.
- `topology.json` — edges (from → to) and the termination condition.
- `orchestrator.py` — the message router with round cap and logging.
- `trace.jsonl` — per message: From, To, Type, Payload, Round, TraceId.
- `final_artifact.md` — the aggregated output from the final agent.
- `eval_report.md` — task success rate, avg rounds, avg messages, conflict-resolution count.

## Key Rules

- Every agent must emit the fixed message envelope; ad-hoc payloads break the router.
- Each agent's system prompt must forbid impersonating another role — role leakage is the #1 multi-agent bug.
- The round cap is mandatory — without it, a coordinator loop can run forever.
- Conflict resolution must be declared up front (latest-wins, majority, human escalation); ambiguous merges break the
  final artifact.
- Log every message with a TraceId — multi-agent failures are unexplainable without the full trace.
- One orchestrator, N specialists — the orchestrator routes, the specialists act; never let a specialist route.

## Examples

```text
Role roster for a research task:
  Planner:    decomposes the task into sub-questions. Input: task. Output: list of sub-questions.
  Researcher: answers one sub-question using search tools. Input: sub-question. Output: evidence-backed answer.
  Critic:     flags unsupported claims. Input: researcher's answer. Output: critique.
  Aggregator: merges sub-answers into the final report. Input: all sub-answers. Output: final report.

Topology: pipeline Planner -> Researcher -> Critic -> Aggregator.
Termination: Aggregator emits "done" or round cap = 5.
```

```python
def RouteMessage(Message, Topology, RoundCap):
  # Reject the message if the round cap is exceeded.
  if (Message["Round"] > RoundCap):
    # Raise to stop a divergent orchestration loop.
    raise RuntimeError("Round cap exceeded before termination.")
  # Look up the recipients for the sender in the topology.
  Recipients = Topology.get(Message["From"], [])
  # If the sender is the aggregator, the run is finished.
  if (Message["From"] == "Aggregator" and Message["Type"] == "done"):
    # Signal completion to the orchestrator.
    return "TERMINATE"
  # Dispatch the message to every recipient agent in order.
  for Recipient in Recipients:
    # Call the recipient agent and capture its reply.
    Reply = CallAgent(Recipient, Message["Payload"])
    # Wrap the reply in a new envelope and continue routing.
    RouteMessage(Reply, Topology, RoundCap)
```

## References

- Wu, Q. et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation."
  https://arxiv.org/abs/2308.08155
- CrewAI framework: https://docs.crewai.com/
- LangGraph — multi-agent orchestration: https://langchain-ai.github.io/langgraph/
- Hong, S. et al. (2023). "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework."
  https://arxiv.org/abs/2308.00352
- Companion skills: `react-agent-prompter`, `system-prompt-architect`, `chain-of-thought-prompter`.
