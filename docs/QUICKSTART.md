# SkillStack — 5-Minute Quickstart

> Drop any theme. Chain any skills. Ship the work.
> 168 skills · 9 themes · 1 maestro orchestrator · MIT License · by Hossam Magdy Balaha

---

## What is SkillStack?

SkillStack is a composable library of 168 skills, organized into 9 independent theme folders, that an LLM agent loads on
demand to execute research, ML, data, writing, and AI-safety tasks. A maestro orchestrator at the root classifies any
incoming task and routes it to the correct theme and skill — you never guess which skill to load.

The themes are non-numbered and self-contained: drop, swap, or rename any of them and the rest of the stack still routes
correctly, because the maestro routes by folder name, not by ordinal.

---

## Load the maestro

Open **`maestro/SKILL.md`** first. It is the front door to the entire stack and the only file the agent must read before
any task. It contains the 9-theme routing table, the conflict-resolution rules, and the special note on the repo's
strict Python style.

```bash
# The single entry point — read this before anything else.
maestro/SKILL.md
```

That is the whole setup. No install, no daemon, no API key. The maestro is plain Markdown the agent reads and follows.

---

## Route a sample task

The maestro classifies each task into exactly one of 9 themes (`academic-research`, `style-integrity`, `ml-engineering`,
`data-engineering`, `visualization`, `writing-citation`, `ai-text`, `ai-output-judgement`, `project-tooling`), then
picks the skill inside that theme whose `description` best fits. Here are three concrete routes:

### Example 1 — Academic publishing

```
"Draft a methods section for my IEEE journal submission"
        │  maestro routes to theme: academic-research
        ▼
academic-research/journal-manuscript-writer
```

Loads `journal-manuscript-writer`, which drafts the section in LaTeX with `\section` / `\subsection` only, IEEE numbered
citations, `% ====================== %` separator comments around floats, and the mandatory back-matter (CRediT,
Funding, IRB, Data Availability, Conflicts, Abbreviations).

### Example 2 — ML engineering

```
"Tune my PyTorch model with Optuna"
        │  maestro routes to theme: ml-engineering
        ▼
ml-engineering/hyperparameter-tuner
```

Loads `hyperparameter-tuner`, which builds an `optuna.study.Study` with the TPE sampler and a `MedianPruner`, persists
`study.trials_dataframe()` to `Aggregated/OptunaTrials.csv`, writes `Aggregated/BestParams.json`, and re-trains the best
checkpoint.

### Example 3 — AI output judgement

```
"Verify this LLM response for hallucinations"
        │  maestro routes to theme: ai-output-judgement
        ▼
ai-output-judgement/hallucination-detector
```

Loads `hallucination-detector`, which extracts named entities, verifies each against Wikidata / Crossref / PyPI /
GitHub, flags fabricated citations and non-existent APIs as severity S4, and writes `hallucinations.jsonl` plus
`hallucination_report.md`.

When a task spans two themes (e.g., draft a paper *and* generate its figures), the maestro routes to the **primary**
theme first, then you chain to the second after the first skill finishes its declared `Outputs`.

---

## Ship the output

Once the routed skill has produced its declared `Outputs` (a `.tex` file, a CSV, a JSON report), commit the artifact to
your repo and move on — the maestro is stateless, so the next task starts fresh from `maestro/SKILL.md` again.

---

## Next steps

- **Browse all 168 skills:** see `README.md` at the repo root.
- **Compose multi-skill pipelines:** see `docs/COOKBOOK.md` for 20 ready-to-run chains.
- **Write your own skill:** see `docs/AUTHORING_GUIDE.md` for the canonical template and linter rules.
- **Compare with other stacks:** see `docs/COMPARISON.md`.
- **Common questions:** see `docs/FAQ.md`.

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
