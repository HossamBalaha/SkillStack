---
name: maestro
description: Top-level orchestrator for the SkillStack 168-skill composable toolkit. When a task arrives, classify it into one of 9 themes (academic-research, style-integrity, ml-engineering, data-engineering, visualization, writing-citation, ai-text, ai-output-judgement, project-tooling) and point the agent at the correct skill folder and skill name. Themes are non-numbered so any can be dropped, swapped, or renamed without renumbering — removing a theme never breaks routing for the others. Use this FIRST whenever the agent needs to find a skill, before loading any individual skill.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  role: orchestrator
  skill_count: 168
  theme_count: 9
  repo_name: SkillStack
---

# Maestro — Skill Orchestrator

## Purpose

This skill is the front door to a 168-skill composable library organized into 9 independent theme folders. Themes are independent modules — drop, swap, or rename any of them and the rest of the stack still works. When you receive a task, do NOT guess which skill to load. Instead:

1. Read the task description.
2. Match it to **one** of the 9 themes below.
3. Inside that theme folder, find the skill whose name and description best fit.
4. Load that skill's `SKILL.md` and follow it.

## Repo Layout

```
skillstack/
├── maestro/SKILL.md                          ← YOU ARE HERE
├── README.md                                 ← Master index (all 168 skills)
├── academic-research/    (20 skills)         ← research planning & writing
├── style-integrity/      (18 skills)         ← LaTeX, prose, coding conventions
├── ml-engineering/        (22 skills)         ← PyTorch, training, validation
├── data-engineering/      (18 skills)         ← ETL, schemas, lineage
├── visualization/         (18 skills)         ← figures, TikZ, posters
├── writing-citation/      (18 skills)         ← BibTeX, editing, paraphrasing
├── ai-text/               (15 skills)         ← detect & humanize AI text
├── ai-output-judgement/   (18 skills)         ← judge & verify AI outputs
└── project-tooling/       (20 skills)         ← packaging, Docker, CI/CD
```

Each theme subfolder contains one folder per skill, and each skill folder has a `SKILL.md` (some also have a `references/` subfolder with deeper rules).

## Theme Routing Table

| Theme Folder | Use When The Task Involves... | # Skills |
|---|---|---|
| `academic-research/` | planning a study, drafting a manuscript, writing a thesis, designing a grant, reviewing a paper, preparing a talk | 20 |
| `style-integrity/` | enforcing LaTeX/prose/coding style rules, zero-fabrication checks, notation consistency, executing any multi-step task with discipline | 18 |
| `ml-engineering/` | building, training, tuning, explaining, or validating ML models in PyTorch/Lightning/HuggingFace | 22 |
| `data-engineering/` | ETL, data quality, schema enforcement, feature stores, dataset cards, converters | 18 |
| `visualization/` | publication figures, TikZ diagrams, posters, tables, dashboards, plots | 18 |
| `writing-citation/` | BibTeX, citations, abstracts, IMRaD, methodology, English editing, paraphrasing | 18 |
| `ai-text/` | detecting AI-generated text, humanizing AI text, perplexity/burstiness, watermark detection | 15 |
| `ai-output-judgement/` | judging AI outputs for factuality, hallucination, bias, safety, groundedness, faithfulness, alignment, code correctness, building eval harnesses | 18 |
| `project-tooling/` | packaging, Docker, CI/CD, pytest, docs, READMEs, pyproject.toml, Makefiles | 20 |

## How To Route

### Step 1 — Classify the task

Read the user's request and pick exactly ONE primary theme. If a task spans two themes (e.g., "write a paper and generate its figures"), route to the **primary** theme first, then chain to the second.

### Step 2 — Pick the skill

Inside the theme folder, scan skill names. Each `SKILL.md` opens with a YAML `description` field stating when to use it. Match the task to the closest description.

### Step 3 — Load and follow

Open the chosen `SKILL.md`, read it in full, and follow its workflow. If it references a `references/` subfile, read that too before acting.

### Step 4 — Chain if needed

If the task naturally chains (e.g., `research-ideation-planner` → `research-repo-builder` → `modular-ml-architect`), finish the first skill's output before loading the next.

## Common Routing Examples

| User Says | Theme | Skill |
|---|---|---|
| "Propose 3 research ideas for a medical imaging journal" | academic-research | research-ideation-planner |
| "Scaffold a research repo with src/, configs, manual" | academic-research | research-repo-builder |
| "Draft the methods section in LaTeX" | academic-research | journal-manuscript-writer |
| "Enforce 2-space indent, CamelCase, period-ended comments in my Python" | style-integrity | coding-conventions-enforcer |
| "Check my LaTeX for missing % ====== % separators" | style-integrity | latex-style-guard |
| "Verify every DOI in my bibliography is real" | style-integrity | zero-fabrication-guard |
| "Run a multi-seed training loop with .to(device) on every nn.Module" | ml-engineering | reproducible-experiment-runner |
| "Bayesian hyperparameter search with Optuna TPE" | ml-engineering | hyperparameter-tuner |
| "Generate SHAP summary + dependence plots" | ml-engineering | model-explainer |
| "Build an ETL with idempotent transforms and audit trail" | data-engineering | etl-pipeline-builder |
| "Validate my CSV against a pandera schema" | data-engineering | data-quality-validator |
| "Make a journal-ready 300 DPI matplotlib figure" | visualization | publication-figure-maker |
| "Draw a TikZ pipeline diagram with solid grouping lines" | visualization | tikz-framework-diagrammer |
| "Convert my .bib to IEEE citation style" | writing-citation | citation-style-converter |
| "Check that every bibitem is \cite'd at least once" | writing-citation | bibtex-citation-manager |
| "Detect if this essay is AI-generated" | ai-text | ai-text-detector |
| "Humanize this AI text but keep all facts" | ai-text | ai-text-humanizer |
| "Check if this LLM response contains hallucinated facts" | ai-output-judgement | hallucination-detector |
| "Verify the factual claims in this AI-generated paragraph" | ai-output-judgement | factuality-checker |
| "Check if my RAG output is grounded in the retrieved docs" | ai-output-judgement | groundedness-verifier |
| "Audit my LLM outputs for gender/race bias" | ai-output-judgement | bias-auditor |
| "Build an LLM eval harness with MMLU + GSM8K" | ai-output-judgement | evaluation-harness-builder |
| "Use LLM-as-judge to score these chatbot responses" | ai-output-judgement | llm-as-judge-evaluator |
| "Detect prompt injection in this retrieved web page" | ai-output-judgement | prompt-injection-detector |
| "Validate that this AI-generated Python code runs and passes tests" | ai-output-judgement | code-output-validator |
| "Bundle my repo into a zip excluding results/ and .git/" | project-tooling | project-zip-packager |
| "Write a Dockerfile for reproducible research" | project-tooling | docker-research-container |
| "Generate a README.md for my Python package" | project-tooling | readme-generator |

## Multi-Theme Routing

When a task spans 2+ themes, return an **ordered skill chain** instead of routing to just one skill. Identify the primary artifact the user wants (the file/output they ultimately need), route to that skill first, then chain prerequisite and follow-up skills.

| Task Pattern | Chain |
|---|---|
| "Write a paper and generate its figures" | `academic-research/journal-manuscript-writer` → `visualization/publication-figure-maker` → `visualization/figure-caption-writer` |
| "Tune my model and explain it" | `ml-engineering/hyperparameter-tuner` → `ml-engineering/model-explainer` |
| "Build a RAG pipeline and check for hallucinations" | `data-engineering/etl-pipeline-builder` → `ml-engineering/inference-pipeline-builder` → `ai-output-judgement/groundedness-verifier` → `ai-output-judgement/hallucination-detector` |
| "Audit my code style and lint" | `style-integrity/coding-conventions-enforcer` → `project-tooling/pre-commit-hook-builder` |

When the primary artifact is ambiguous, ask the user ONE clarifying question (max 3 options) before routing.

## Confidence Scoring

When multiple skills seem to match, score them and present the top 3:

- **High (≥0.8)**: Skill name + description directly matches task keywords. Route immediately.
- **Medium (0.4-0.8)**: Skill covers part of the task. Present top 3 and ask user to confirm.
- **Low (<0.4)**: No good match. Tell user, suggest closest skills, ask for clarification.

Scoring heuristic: count keyword overlaps between the task and each skill's `description` + `tags` frontmatter fields, normalized by total keywords.

## Fallback Chain

If the first-loaded skill's output is incomplete (e.g., it references a missing file, raises an unhandled error, or the user reports the output is wrong):

1. **Halt** the current skill.
2. **Load the next-best match** from the confidence-scored top 3.
3. If all 3 fail, **ask the user** for clarification or additional input.
4. Never silently retry the same skill with the same inputs more than once.

## Skill Conflict Resolver

When two skills seem to apply, use this decision tree (top 10 most common overlaps):

| Overlap | Resolution |
|---|---|
| `writing-citation/doi-verifier` vs `ai-output-judgement/reference-accuracy-checker` | Use `doi-verifier` for human-typed `.bib` files; use `reference-accuracy-checker` for AI-generated references (higher hallucination risk). |
| `style-integrity/zero-fabrication-guard` vs `ai-output-judgement/factuality-checker` | `zero-fabrication-guard` is for manuscripts (verifies citations/DOIs); `factuality-checker` is for LLM outputs (verifies atomic claims via web search). |
| `style-integrity/coding-conventions-enforcer` vs `ml-engineering/modular-ml-architect` | `coding-conventions-enforcer` is the rule set (the linter); `modular-ml-architect` is the architect (decides folder structure). Load `coding-conventions-enforcer` first, then `modular-ml-architect`. |
| `visualization/publication-figure-maker` vs `visualization/academic-plotting-pipeline` | `publication-figure-maker` is for a single finished figure; `academic-plotting-pipeline` is for choosing chart type from raw data. |
| `ml-engineering/hyperparameter-tuner` vs `ml-engineering/learning-rate-finder` | `learning-rate-finder` is a one-shot LR range test before training; `hyperparameter-tuner` is the full Optuna search. |
| `project-tooling/requirements-pinner` vs `project-tooling/environment-yaml-builder` | `requirements-pinner` for pip-only; `environment-yaml-builder` for conda envs. |
| `ai-text/ai-text-detector` vs `ai-output-judgement/hallucination-detector` | `ai-text-detector` checks if text sounds AI-written; `hallucination-detector` checks if AI output contains fabricated facts. |
| `writing-citation/bibtex-citation-manager` vs `writing-citation/citation-style-converter` | `bibtex-citation-manager` manages the `.bib` file (citekeys, dedup); `citation-style-converter` reformats between IEEE/APA/Chicago. |
| `data-engineering/data-quality-validator` vs `data-engineering/data-schema-enforcer` | `data-schema-enforcer` rejects rows violating schema; `data-quality-validator` runs broader checks (nulls, duplicates, outliers, drift). |
| `project-tooling/sphinx-docs-builder` vs `project-tooling/readme-generator` | `readme-generator` for the repo front door; `sphinx-docs-builder` for full API docs. |

## The Coding-Conventions Skill (Special Note)

The user's repo enforces a strict, non-standard Python style. Whenever you write or edit Python code in this repo, load `style-integrity/coding-conventions-enforcer/SKILL.md` FIRST. The five rules:

1. **Variables** use `camelCase` (e.g., `dataSourceUrl`).
2. **Functions, classes, file names, dict keys** use `CamelCase` (e.g., `ProcessData`, `DataProcessor`, `VisualizationUtils.py`, `"ValidationStatus"`).
3. **`if` statements** always wrap conditions in parentheses: `if (condition):`.
4. **Comments** go above each statement and end with a period: `# Initialize the data source URL.`.
5. **Strings** use double quotes `""` everywhere except inside docstrings.

Framework-mandated lowercase method names (`forward`, `backward`, `training_step`, `validation_step`, `configure_optimizers`, `setUp`, `tearDown`) are exempt.

## Conflict Resolution

If two skills seem to apply:
- Prefer the **more specific** skill.
- Prefer the skill in the theme that matches the task's **primary output** (the file or artifact the user ultimately wants).
- When still unsure, ask the user to confirm which artifact they want produced.

## When NOT To Use Maestro

- Trivial Q&A or single-file reads (just answer directly).
- Tasks already covered by a skill outside this repo (e.g., the built-in `docx`, `pdf`, `xlsx`, `charts` skills).
- Web-only research with no skill invocation needed.

## Updating This File

If you add a new skill to any theme, update that theme's count in the routing table above and in `README.md`. Keep both files in sync.

Themes are non-numbered on purpose — you can drop or rename any theme folder without renumbering the others. The maestro routes by folder name, not by ordinal.
