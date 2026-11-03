# 🧠 Prompt Engineering — Reasoning, Agents, RAG & Safety

> Design chain-of-thought, ReAct, tree-of-thoughts, RAG, multimodal, and multi-agent prompts; architect system prompts
> with safety and refusal framing; enforce structured output; defend against prompt injection; and version, test, and
> roll back prompts like code. Use this theme whenever the deliverable is a prompt (system, few-shot, agent, RAG, or
> multimodal) rather than a research artifact or a figure.

## Theme Overview

This folder contains **15 skills** in the `prompt-engineering/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                   | Description                                                                                                                                                                                                                                                                                       | Difficulty   | Tags                                                                                        | Related                                                                                                                                      |
|----|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`chain-of-thought-prompter`](chain-of-thought-prompter/SKILL.md)       | Design chain-of-thought (CoT) prompts that elicit step-by-step reasoning — zero-shot CoT ("Let's think step by step"), few-shot CoT with worked examples, and self-consistency sampling over multiple reasoning paths.                                                                            | intermediate | `chain-of-thought`, `reasoning`, `few-shot`, `self-consistency`, `llm`                      | `prompt-engineering/tree-of-thoughts-prompter`, `prompt-engineering/few-shot-template-builder`, `prompt-engineering/system-prompt-architect` |
| 2  | [`react-agent-prompter`](react-agent-prompter/SKILL.md)                 | Build ReAct (Reasoning + Acting) prompts interleaving Thought/Action/Observation loops so an LLM can call external tools before answering. Use for open-book QA, current-events lookup, multi-hop reasoning, and any agent that must use tools.                                                   | intermediate | `react`, `agents`, `tool-use`, `reasoning`, `llm`                                           | `prompt-engineering/agent-orchestration-prompter`, `prompt-engineering/rag-prompt-designer`, `prompt-engineering/chain-of-thought-prompter`  |
| 3  | [`rag-prompt-designer`](rag-prompt-designer/SKILL.md)                   | Design retrieval-augmented generation (RAG) prompts that frame retrieved context, enforce inline citations, and trigger an "I don't know" fallback when context is insufficient. Use for chatbots over private documents and any LLM that must ground answers in retrieved evidence.              | intermediate | `rag`, `retrieval`, `citations`, `grounding`, `llm`                                         | `prompt-engineering/react-agent-prompter`, `prompt-engineering/context-window-optimizer`, `ai-output-judgement/faithfulness-scorer`          |
| 4  | [`tree-of-thoughts-prompter`](tree-of-thoughts-prompter/SKILL.md)       | Build Tree-of-Thoughts (ToT) prompts that turn reasoning into a search problem — generate candidate thoughts, evaluate states, and explore via BFS or DFS until a solution is found. Use when CoT commits too early and cannot backtrack.                                                         | advanced     | `tree-of-thoughts`, `search`, `planning`, `reasoning`, `llm`                                | `prompt-engineering/chain-of-thought-prompter`, `prompt-engineering/react-agent-prompter`, `prompt-engineering/system-prompt-architect`      |
| 5  | [`few-shot-template-builder`](few-shot-template-builder/SKILL.md)       | Construct few-shot prompt templates with consistent input/output formatting, deliberate delimiter choices, and principled example-selection strategies (random, diverse, hardest, similarity). Use when reproducibility and exemplar selection matter more than the instruction text.             | beginner     | `few-shot`, `templates`, `exemplars`, `prompt-engineering`, `llm`                           | `prompt-engineering/system-prompt-architect`, `prompt-engineering/prompt-template-library`, `prompt-engineering/prompt-testing-harness`      |
| 6  | [`system-prompt-architect`](system-prompt-architect/SKILL.md)           | Architect system prompts with explicit role definition, capability boundaries, refusal framing, safety guidelines, and a strict output-format specification. Use when shipping a production chatbot, agent, or RAG assistant.                                                                     | intermediate | `system-prompt`, `role-design`, `safety`, `output-format`, `llm`                            | `prompt-engineering/few-shot-template-builder`, `prompt-engineering/prompt-injection-defense`, `prompt-engineering/output-format-enforcer`   |
| 7  | [`prompt-template-library`](prompt-template-library/SKILL.md)           | Curate a reusable library of prompt templates organized by task family (summarization, translation, code generation, classification, extraction, rewriting). Each template ships a name, description, template string, variables, and a worked example.                                           | beginner     | `templates`, `library`, `summarization`, `translation`, `code-generation`, `classification` | `prompt-engineering/few-shot-template-builder`, `prompt-engineering/system-prompt-architect`, `prompt-engineering/prompt-versioning-system`  |
| 8  | [`prompt-testing-harness`](prompt-testing-harness/SKILL.md)             | Build a prompt testing harness that defines test cases (input, expected output, evaluator), runs a prompt against multiple LLMs, and scores outputs with exact match, BLEU, ROUGE, and semantic similarity. Use for reproducible prompt regression tests and CI gates.                            | intermediate | `testing`, `evaluation`, `regression`, `llm`, `metrics`                                     | `prompt-engineering/prompt-versioning-system`, `prompt-engineering/few-shot-template-builder`, `ai-output-judgement/llm-as-judge-evaluator`  |
| 9  | [`prompt-injection-defense`](prompt-injection-defense/SKILL.md)         | Build prompt-injection-resistant prompts using input sanitization, an explicit instruction hierarchy, delimiter fences, and role-locking so untrusted text cannot override the system prompt. Use for any LLM system that mixes untrusted content with privileged instructions.                   | advanced     | `prompt-injection`, `security`, `defense`, `llm`, `safety`                                  | `prompt-engineering/system-prompt-architect`, `prompt-engineering/rag-prompt-designer`, `ai-output-judgement/prompt-injection-detector`      |
| 10 | [`output-format-enforcer`](output-format-enforcer/SKILL.md)             | Enforce structured output from LLMs using JSON schema prompting, function calling, regex-constrained decoding, or Pydantic model prompting so downstream parsers never see malformed output. Use when the model's output feeds another program that needs typed fields.                           | intermediate | `json-schema`, `function-calling`, `structured-output`, `pydantic`, `llm`                   | `prompt-engineering/system-prompt-architect`, `prompt-engineering/few-shot-template-builder`, `prompt-engineering/prompt-testing-harness`    |
| 11 | [`context-window-optimizer`](context-window-optimizer/SKILL.md)         | Optimize prompts to fit a model's context window under a token budget — prioritize chunks, summarize before detail, and apply a sliding window over long documents. Use when prompts blow the token limit, retrieval returns more chunks than fit, or latency and cost scale with context length. | intermediate | `context-window`, `token-budget`, `chunking`, `summarization`, `llm`                        | `prompt-engineering/rag-prompt-designer`, `prompt-engineering/prompt-testing-harness`, `prompt-engineering/few-shot-template-builder`        |
| 12 | [`prompt-versioning-system`](prompt-versioning-system/SKILL.md)         | Version prompts like code with semantic versioning, A/B testing infrastructure, prompt diffing, and rollback support. Use when prompts ship to production, when a prompt change must be reviewable, when you A/B test variants, or when a regression forces a fast rollback.                      | intermediate | `versioning`, `semver`, `ab-testing`, `rollback`, `llm`                                     | `prompt-engineering/prompt-testing-harness`, `prompt-engineering/system-prompt-architect`, `prompt-engineering/prompt-template-library`      |
| 13 | [`constitutional-ai-prompter`](constitutional-ai-prompter/SKILL.md)     | Build Constitutional AI prompts that define a constitution of principles, run a self-critique loop where the model rates its own draft against those principles, and apply revision prompts to fix violations. Use for aligned outputs without massive human-labelling of preferences.            | advanced     | `constitutional-ai`, `alignment`, `self-critique`, `safety`, `llm`                          | `prompt-engineering/system-prompt-architect`, `prompt-engineering/prompt-injection-defense`, `ai-output-judgement/safety-classifier`         |
| 14 | [`multimodal-prompt-designer`](multimodal-prompt-designer/SKILL.md)     | Design multimodal prompts that fuse image and text inputs, interleave modalities, and frame vision-language tasks (VQA, captioning, document understanding, chart reading). Use when an LLM accepts images and the task needs reasoning over both pixels and prose.                               | advanced     | `multimodal`, `vision-language`, `vqa`, `image-text`, `llm`                                 | `prompt-engineering/rag-prompt-designer`, `prompt-engineering/system-prompt-architect`, `prompt-engineering/output-format-enforcer`          |
| 15 | [`agent-orchestration-prompter`](agent-orchestration-prompter/SKILL.md) | Build multi-agent orchestration prompts that assign roles to agents, define a message-passing protocol, decompose tasks across agents, and aggregate their results. Use when a single agent cannot solve the task end-to-end and the workflow needs specialized roles.                            | advanced     | `multi-agent`, `orchestration`, `message-passing`, `agentic`, `llm`                         | `prompt-engineering/react-agent-prompter`, `prompt-engineering/system-prompt-architect`, `prompt-engineering/chain-of-thought-prompter`      |

## Difficulty Breakdown

Across **15** skills in this theme, the difficulty distribution is:

- **Beginner** — 2 skill(s)
- **Intermediate** — 8 skill(s)
- **Advanced** — 5 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`llm` (14), `reasoning` (3), `few-shot` (2), `safety` (2), `summarization` (2), `templates` (2), `ab-testing` (1),
`agents` (1), `agentic` (1), `alignment` (1), `chain-of-thought` (1), `chunking` (1), `citations` (1), `classification`
(1), `code-generation` (1), `constitutional-ai` (1), `context-window` (1), `defense` (1), `evaluation` (1),
`exemplars` (1), `function-calling` (1), `grounding` (1), `image-text` (1), `json-schema` (1), `library` (1),
`message-passing` (1), `metrics` (1), `multi-agent` (1), `multimodal` (1), `orchestration` (1), `output-format` (1),
`planning` (1), `prompt-engineering` (1), `prompt-injection` (1), `pydantic` (1), `rag` (1), `react` (1), `reasoning`
(1), `retrieval` (1), `role-design` (1), `rollback` (1), `search` (1), `self-consistency` (1), `self-critique` (1),
`semver` (1), `structured-output` (1), `system-prompt` (1), `testing` (1), `token-budget` (1), `tool-use` (1),
`translation` (1), `tree-of-thoughts` (1), `versioning` (1), `vision-language` (1), `vqa` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`system-prompt-architect` → `prompt-injection-defense` → `prompt-testing-harness`** — Design the system prompt →
  harden it against injection → regression-test it.
- **`few-shot-template-builder` → `chain-of-thought-prompter` → `tree-of-thoughts-prompter`** — Stable few-shot
  template → linear CoT → search-based ToT (escalating reasoning complexity).
- **`rag-prompt-designer` → `context-window-optimizer` → `output-format-enforcer`** — Frame the RAG prompt → fit it in
  the budget → enforce a structured response.
- **`react-agent-prompter` → `agent-orchestration-prompter` → `constitutional-ai-prompter`** — Single ReAct agent →
  multi-agent orchestration → alignment via self-critique.
- **`prompt-template-library` → `prompt-versioning-system` → `prompt-testing-harness`** — Pick a template → version it
  → gate every version behind an eval run.

## Cross-Theme Connections

Skills in `prompt-engineering/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../ai-output-judgement/` — 4 related pointer(s)

Themes that commonly chain with this one:

- [`../ai-output-judgement/README.md`](ai-output-judgement/README.md) — RAG prompts feed faithfulness scorers, prompt
  injection defense chains with injection detectors, and CAI loops pair with safety classifiers.
- [`../style-integrity/README.md`](style-integrity/README.md) — every Python-emitting prompt skill follows the repo's
  strict coding conventions enforcer.
- [`../ml-engineering/README.md`](ml-engineering/README.md) — agent harnesses and prompt testing rigs produce code that
  lives in ML experiment folders.
- [`../academic-research/README.md`](academic-research/README.md) — CoT, ToT, and RAG prompts underpin research
  demonstrations and ablations in manuscripts.

## Back to Master

← [Back to SkillStack README](../README.md)
