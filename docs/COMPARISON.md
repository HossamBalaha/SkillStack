# SkillStack vs. Other Skill & Eval Frameworks

> How SkillStack differs from Anthropic Agent Skills, SkillDB, OpenAI Evals, good-readme, and ClawHub Skills.
>
> 168 skills · 9 themes · 1 maestro orchestrator · MIT License · by Hossam Magdy Balaha

---

## At a glance

SkillStack is a **composable, self-routing skill library** for LLM agents. Its distinguishing features are: (1) a
maestro orchestrator that classifies any task into one of 9 independent themes, (2) themes that are non-numbered so any
can be dropped or renamed without breaking routing, (3) skills written from scratch in the author's own words rather
than aggregated from third parties, and (4) coverage spanning academic publishing, ML, data engineering, visualization,
writing, AI-text, AI-output judgement, and project tooling in one stack.

The alternatives below each solve a different — usually narrower — problem.

---

## Comparison table

| Dimension                            | **SkillStack**                                                                                  | Anthropic Agent Skills                           | SkillDB                                          | OpenAI Evals                                 | good-readme                       | ClawHub Skills                       |
|--------------------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------|----------------------------------------------|-----------------------------------|--------------------------------------|
| **Scope**                            | Cross-domain agent skill library (research, ML, data, AI safety, writing, tooling)              | General-purpose agent skills bundled with Claude | A registry/index of community skills             | LLM evaluation framework only                | Single-purpose: generate a README | A marketplace of installable skills  |
| **Skill count**                      | 168 skills across 9 themes                                                                      | A small curated set (~10–20)                     | Hundreds (community-submitted, variable quality) | N/A (eval tasks, not skills)                 | 1                                 | Dozens, growing                      |
| **Format**                           | Plain `SKILL.md` Markdown + YAML frontmatter + optional `references/`                           | Markdown with metadata                           | Varies (often Markdown + manifest)               | Python/YAML eval definitions                 | A single prompt/template          | Markdown + install manifests         |
| **Self-routing maestro**             | Yes — `maestro/SKILL.md` classifies and routes every task                                       | No — agent picks                                 | No — user browses/searches                       | No — user writes eval configs                | No                                | No                                   |
| **MIT license**                      | Yes (whole stack)                                                                               | Varies per skill                                 | Varies per entry                                 | MIT (the eval framework)                     | MIT                               | Varies per skill                     |
| **Original vs. aggregated content**  | **Original** — written from scratch in the author's own words; no verbatim third-party content  | Original (Anthropic-authored)                    | **Aggregated** — community submissions           | Original (OpenAI-authored) + public datasets | Original                          | **Aggregated** — community-submitted |
| **Supports MCP**                     | Not natively (protocol-agnostic Markdown)                                                       | Yes (MCP-native)                                 | Varies                                           | N/A                                          | N/A                               | Yes (MCP-oriented)                   |
| **Multi-theme routing**              | Yes — 9 independent, drop-any themes routed by folder name                                      | No (flat set)                                    | No (flat registry)                               | No (single framework)                        | No (single tool)                  | No (flat marketplace)                |
| **Mandatory body sections**          | Yes — When To Use, Workflow, Inputs, Outputs, Key Rules, Examples, References (linter-enforced) | No enforced template                             | No enforced template                             | Eval-task schema only                        | N/A                               | No enforced template                 |
| **Single author / consistent voice** | Yes — Hossam Magdy Balaha, one style throughout                                                 | Yes (Anthropic)                                  | No (many contributors)                           | Yes (OpenAI)                                 | Yes                               | No (many contributors)               |
| **Offline-capable**                  | Yes (Markdown only; API-dependent skills flag it in `cost_warning`)                             | Varies                                           | Varies                                           | No (needs model + datasets)                  | Yes                               | Varies                               |
| **Drop-any-theme portability**       | Yes — remove a theme folder, routing still works                                                | No                                               | No                                               | No                                           | No                                | No                                   |

---

## Strengths and limits

### SkillStack strengths

- **Self-routing** — the maestro removes the "which skill do I load?" guesswork; the agent reads one file and gets a
  concrete route.
- **Drop-any-theme** — non-numbered folders mean deleting a theme never breaks routing for the others.
- **Consistency** — one author, one template, one linter, one voice across all 168 skills.
- **Cross-domain** — research, ML, data, AI safety, writing, and tooling in a single stack, so chains span themes
  without switching libraries.
- **Original content** — written from scratch; no license or attribution tangle from aggregated third-party skills.
- **Protocol-agnostic** — works with Claude, GPT, Llama, Cursor, or any agent that reads Markdown.

### SkillStack limits

- **No MCP server** — if your agent requires MCP-native tools, you must wrap a skill yourself.
- **No central registry / lockfile** — versioning is by Git ref; there is no `skillstack install` or `skillstack.lock`.
- **No runtime executor** — skills are instructions, not code; the agent must execute them, so quality depends on the
  model.
- **English-first** — skills default to `language: en`; translations must be forked (see FAQ Q16).
- **API-dependent skills need network** — hallucination detectors, DOI verifiers, and zero-fabrication guards call
  external APIs and flag offline mode.

---

## Detailed comparison

### SkillStack vs. Anthropic Agent Skills

Anthropic Agent Skills ship bundled with Claude and are authored by Anthropic. They are MCP-native and high-quality but
small in number and flat — there is no internal router that classifies a task and points at the right skill. SkillStack
is model-agnostic (any agent that reads Markdown), ships 168 skills in 9 themed folders, and adds the maestro so the
agent never guesses which skill to load. SkillStack's themes are also independently droppable, whereas Anthropic's set
is a flat bundle. Where Anthropic optimizes for tight Claude + MCP integration, SkillStack optimizes for breadth,
self-routing, and drop-in portability across any agent.

### SkillStack vs. SkillDB

SkillDB is a community registry: it aggregates many skills of varying quality and license, and the user must browse,
evaluate, and pick. There is no enforced schema, no shared body-section template, and no router — discovery is manual
search. SkillStack is a curated, single-author, MIT-licensed library where every skill follows the same template, the
same frontmatter schema, and the same body-section discipline (When To Use → Workflow → Inputs → Outputs → Key Rules →
Examples → References). SkillStack's maestro also routes automatically. Use SkillDB when you want breadth of community
choice; use SkillStack when you want consistency and zero routing guesswork.

### SkillStack vs. OpenAI Evals

OpenAI Evals is an **evaluation framework** for benchmarking LLMs on standard suites (MMLU, GSM8K, HumanEval,
TruthfulQA). It is not a skill library and does not help an agent *do* work — it helps you *measure* model quality with
runnable Python/YAML task definitions. SkillStack includes an `ai-output-judgement` theme (18 skills) that covers
eval-harness building, hallucination detection, bias auditing, and LLM-as-judge, but those skills are operational
instructions for an agent, not a runnable eval framework. The two are complementary: use OpenAI Evals to benchmark a
model with code, use SkillStack's `evaluation-harness-builder` skill to have an agent *build* a comparable harness, and
use `llm-as-judge-evaluator` to have an agent *score* responses.

### SkillStack vs. good-readme

good-readme is a **single-purpose** tool: it generates a README. SkillStack includes a
`project-tooling/readme-generator` skill that does the same job, plus 19 other project-tooling skills (Docker, CI/CD,
pytest suites, pyproject.toml, changelogs, license selection, contribution guides) and 148 more skills across the other
8 themes. good-readme is a useful but narrow utility; SkillStack is a full cross-domain library that *contains* an
equivalent capability plus 167 others. Reach for good-readme when you need exactly one README; reach for SkillStack when
the README is one artifact in a larger research or ML workflow.

### SkillStack vs. ClawHub Skills

ClawHub Skills is a marketplace of installable, often MCP-oriented skills contributed by the community. Quality,
license, and style vary by author, and there is no shared validator or routing layer. SkillStack is a single-author,
MIT-licensed, convention-enforced library: every skill passes the same `quick_validate.py` linter, follows the same YAML
schema, and is written in the same voice. ClawHub is broad and community-driven (good for finding niche MCP tools);
SkillStack is deep, consistent, and self-routing (good for a coherent cross-domain workflow where every skill chains
predictably).

---

## When to use what

| If you want to...                                                                | Use                    |
|----------------------------------------------------------------------------------|------------------------|
| Have an LLM agent route and execute cross-domain research/ML/data/AI-safety work | **SkillStack**         |
| Get Anthropic-curated skills tightly integrated with Claude + MCP                | Anthropic Agent Skills |
| Browse a wide community registry and pick your own skills                        | SkillDB                |
| Benchmark an LLM on MMLU/GSM8K/HumanEval with a runnable framework               | OpenAI Evals           |
| Generate a single README quickly                                                 | good-readme            |
| Install community MCP skills from a marketplace                                  | ClawHub Skills         |

None of these are mutually exclusive. A common setup: use **SkillStack** as the day-to-day skill library, **OpenAI Evals
** for rigorous model benchmarking, **Anthropic Agent Skills** when working inside Claude Code with MCP, and *
*good-readme** or ClawHub for one-off utilities SkillStack does not cover.

---

## Summary

SkillStack's niche is **self-routing, original, cross-domain, drop-any-theme skill composition for LLM agents**. It is
not an eval framework, not a marketplace, and not a single-purpose generator — it is the only option here that ships a
maestro orchestrator, 9 independently droppable themes, and 168 originally-authored skills under one MIT license.

If your work spans research, ML, data, AI safety, and writing — and you want one consistent, linter-enforced library
that any agent can route through — SkillStack is the fit. If you need a single capability (a README, an eval suite, one
MCP tool), the narrower options above are lighter to adopt.

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
