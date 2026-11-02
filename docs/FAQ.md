# SkillStack — Frequently Asked Questions

> 168 skills · 9 themes · 1 maestro orchestrator · MIT License · by Hossam Magdy Balaha

---

### Q1. How do I add a new theme?

Create a new lowercase-kebab-case folder at the repo root (e.g., `bioinformatics/`), add at least one skill subfolder with a `SKILL.md`, then add a row to the routing table in `maestro/SKILL.md` and a section in `README.md`. Themes are non-numbered, so you never renumber the others — the maestro routes by folder name, not by ordinal. Bump the `theme_count` field in the maestro's YAML frontmatter and the badge count in `README.md`.

### Q2. Can I use just one skill without the maestro?

Yes. The maestro is a convenience router, not a runtime. You can open any `SKILL.md` directly (e.g., `ml-engineering/hyperparameter-tuner/SKILL.md`) and follow it. The maestro exists to remove the guesswork of *which* skill to load; once you know, you can skip it.

### Q3. How do I disable `coding-conventions-enforcer`?

The conventions skill (`style-integrity/coding-conventions-enforcer`) is only invoked when the maestro's special note triggers, or when you explicitly ask for a style pass. The five rules (camelCase variables, CamelCase functions/classes/files/dict-keys, parenthesized `if`, period-ended comments, double-quoted strings, 2-space indent) apply only to code the skill actually rewrites — they do not run as a background hook.

To disable it:

- **Per-task:** simply do not load the skill. Other skills do not enforce these rules on your behalf.
- **Per-repo:** remove the "Coding-Conventions Skill" note block from `maestro/SKILL.md` so the maestro no longer recommends loading it.
- **Globally:** delete the `style-integrity/coding-conventions-enforcer/` folder and update the theme's skill count in `README.md` and `maestro/SKILL.md`.

Framework-mandated lowercase methods (`forward`, `training_step`, `configure_optimizers`, `setUp`, `tearDown`) are always exempt, so removing the enforcer does not break PyTorch Lightning or unittest code.

### Q4. What's the difference between `ai-text` and `ai-output-judgement`?

`ai-text` (15 skills) judges whether a **piece of prose** was written by an AI and rewrites it to sound human — detectors, humanizers, perplexity/burstiness scorers, watermark detectors, tell catalogues. `ai-output-judgement` (18 skills) judges whether an **LLM response** is correct, grounded, safe, unbiased, and consistent — hallucination detectors, factuality checkers, bias auditors, eval harnesses, LLM-as-judge. Rule of thumb: if the input is a *document*, use `ai-text`; if the input is a *model response*, use `ai-output-judgement`.

### Q5. Does SkillStack work with Claude Code, Cursor, and OpenAI agents?

Yes. Skills are plain Markdown files; any agent that can read a file and follow instructions can use them. Claude Code: place the `skills/` folder in your project and point the agent at `maestro/SKILL.md`. Cursor: add the folder to your workspace and reference skills in `.cursorrules` or a rules file. OpenAI agents / custom GPTs: paste the relevant `SKILL.md` into the system prompt or a knowledge-base file. No SDK, no API, no protocol binding is required.

### Q6. How do I contribute a new skill?

Read `docs/AUTHORING_GUIDE.md`, copy the canonical template, fill in the YAML frontmatter and all mandatory body sections (When To Use, Workflow, Inputs, Outputs, Key Rules, Examples, References), place it at `<theme>/<skill-name>/SKILL.md`, run the linter, and open a pull request. Skills must be written from scratch in your own words — no verbatim reproduction of third-party skill content.

### Q7. Why is the Python style non-standard (camelCase + CamelCase)?

The repo enforces a deliberate, strict style: `camelCase` for variables, `CamelCase` for functions/classes/filenames/dict-keys, parenthesized `if` conditions, period-ended comments above every statement, double-quoted strings, 2-space indentation. It is non-PEP-8 by design — it makes the author's codebases visually distinct and forces explicit, commented, parenthesized code. Framework-mandated lowercase methods (`forward`, `training_step`, `configure_optimizers`, `setUp`) are exempt.

### Q8. How do I cite SkillStack in a paper?

Cite the repository and author:

> Hossam Magdy Balaha. *SkillStack: A composable library of 168 skills across 9 themes for LLM agents.* 2026. MIT License. https://github.com/HossamBalaha (SkillStack repository).

If you used a specific skill chain, also cite the foundational papers listed in the `References` section of that skill's `SKILL.md` (e.g., Akiba et al. 2019 for Optuna, Lundberg & Lee 2017 for SHAP).

### Q9. Is there a CLI?

Not a bundled one. Skills are Markdown that an LLM follows, not executables, so there is no `skillstack run ...` command and no daemon.

What does ship:

- **`skill-creator/scripts/quick_validate.py`** — validates a `SKILL.md` against the schema (frontmatter, sections, links).
- **`skill-creator/scripts/package_skill.py`** — bundles a skill folder into a distributable archive.
- **`skill-creator/scripts/run_eval.py`** — runs the skill-creator's evaluation loop on a skill.
- **Skills that *generate* CLI tooling:** `project-tooling/makefile-generator`, `project-tooling/github-actions-research-ci`, `project-tooling/pyproject-toml-builder` produce Makefiles, CI workflows, and packaging configs you then invoke with standard tools (`make`, `pytest`, `pip`).

If you want a `skillstack` shell command, wrap `maestro/SKILL.md` in a tiny script that prints the file path for your agent to read.

### Q10. How do I cache skills for offline use?

Clone or copy the entire `skills/` folder to a local path. Every `SKILL.md` and `references/` file is plain Markdown with no runtime fetch, so the skills themselves are fully offline.

The only online dependency is when a skill *calls an external API*:

- **`ai-output-judgement/hallucination-detector`** calls Crossref, Wikidata, PyPI, GitHub.
- **`writing-citation/doi-verifier`** calls `https://api.crossref.org/works/{DOI}`.
- **`style-integrity/zero-fabrication-guard`** verifies URLs resolve.

For those, either (a) pre-cache the API responses as local JSON files and point the skill at them, or (b) skip the verification step and accept unverified output, clearly flagged with a `[Unverified — offline]` marker so it is not mistaken for a confirmed result.

### Q11. What if a skill's URL is broken?

Open an issue. Each skill lists its source URLs in the `References` section. If a URL rots, replace it with a Wayback Machine archive link or an equivalent authoritative source, and submit a PR. Do **not** leave a dead link or silently drop a reference — the `zero-fabrication-guard` skill treats unverifiable citations as fabrication.

### Q12. Can I use SkillStack commercially?

Yes. The entire stack is MIT-licensed: commercial use, modification, distribution, sublicensing, and private use are all permitted. The only requirement is to retain the copyright notice and license text in copies or substantial portions of the software.

Important caveats:

- The MIT license covers the **skills themselves** (the Markdown). It does not cover the third-party tools skills reference (PyTorch, Optuna, SHAP, Docker, etc.) — each of those has its own license you must comply with separately.
- The `Disclaimer` in `README.md` applies: skills are provided "as is" without warranty, and you assume all responsibility for outputs the agent produces on your behalf, including API charges, fabricated citations, or modified files.
- If you ship SkillStack inside a commercial product, attribute the author (Hossam Magdy Balaha) and link to the upstream repository.

### Q13. How do I pin specific skill versions?

Each skill's YAML frontmatter carries `metadata.version` (currently `"1.0"`), but there is no central registry and no `skillstack.lock` file — versioning is by Git ref.

To pin:

1. **Vendor the folder:** copy the `skills/` tree into your repo at a known commit SHA and commit it. Record the SHA in a `SKILLSTACK_VERSION` file.
2. **Git submodule:** add the SkillStack repo as a submodule pinned to a tag.
3. **Fork:** fork at a specific tag and pull updates deliberately.

Bump a skill's `metadata.version` only on material changes to `Workflow` or `Key Rules`; cosmetic edits need not bump it.

### Q14. What's the token cost of loading all 168 skills?

Do not load all 168 at once. The maestro loads only itself plus the one routed skill. A typical `SKILL.md` is 80–180 lines (roughly 1,500–4,000 tokens). Loading the maestro (~140 lines) plus one skill (~120 lines) is ~5,000 tokens. Loading the entire `skills/` tree would be on the order of 500K–700K tokens, which is wasteful and unnecessary — route instead.

### Q15. How do I run the linter?

Run the validator in `skill-creator/scripts/quick_validate.py`:

```bash
python skills/skill-creator/scripts/quick_validate.py <theme>/<skill-name>/SKILL.md
```

It checks YAML frontmatter presence, mandatory body sections, fenced code blocks, and that every URL in `References` resolves with HTTP 200. The `style-integrity/coding-conventions-enforcer` skill is a separate lint pass for Python files, not Markdown.

### Q16. How do I translate skills to another language?

Copy the `skills/` tree, translate the body prose, and keep the YAML `language` field updated (default `en`). Do not translate code, skill folder names, theme folder names, or citation DOIs — those are load-bearing identifiers the maestro matches on. Keep the `Examples` code blocks untranslated. Submit translations as a separate `skills-es/`, `skills-fr/`, etc. tree, not in-place.

### Q17. What LLMs is SkillStack tested with?

Skills are model-agnostic Markdown. They have been validated against Claude (3.5 / 4), GPT-4 / 4o, and open models (Llama 3, Qwen 2.5). A skill that calls a specific API (e.g., OpenAI Moderation) notes the dependency in its `cost_warning` and `prerequisites` fields. Smaller models may struggle with the longer multi-step workflows; load one skill at a time and verify each `Outputs` artifact before proceeding.

### Q18. Does SkillStack support MCP (Model Context Protocol)?

Not natively. Skills are plain Markdown, not MCP server definitions. You can wrap a skill as an MCP tool by writing a thin server that reads the `SKILL.md` and exposes its `Workflow` steps as tool calls, but SkillStack itself ships no MCP server. The format is deliberately protocol-agnostic so it works with any agent framework.

### Q19. How do I report a bug or a fabricated citation?

Open a GitHub issue with: the skill path, the exact input, the produced output, and the expected output. If the skill fabricated a citation, include the fabricated reference and the verification query that proved it does not exist. Fabricated-citation bugs are treated as severity S4 (highest) — see `ai-output-judgement/hallucination-detector` for the severity scale.

### Q20. Why are themes non-numbered?

So you can drop, swap, or rename any theme without renumbering the others. The maestro routes by folder name, not by ordinal index. If `academic-research` were `theme-01-academic-research`, removing it would force renumbering every other theme and updating every cross-reference. With plain folder names, deletion is a no-op for routing.

### Q21. Can I fork a theme and rename it?

Yes. Rename the folder (e.g., `academic-research` → `research-writing`), update the routing-table row in `maestro/SKILL.md`, and the rest of the stack keeps working. Skill-internal cross-references use skill names (e.g., `journal-manuscript-writer`), not theme-prefixed paths, so they survive a theme rename as long as the skill folder name is unchanged.

### Q22. Is there a Python package I can `pip install`?

No. SkillStack is a Markdown skill library, not a Python distribution. The repo root has no `setup.py` or `pyproject.toml` for the skills themselves — those live inside skills that *generate* packaging (e.g., `project-tooling/pyproject-toml-builder`). To consume SkillStack programmatically, clone the repo and read the Markdown.

### Q23. How do I keep SkillStack updated?

`git pull` the upstream repository. Because skills are stateless Markdown, updates never require migration — the worst case is a skill's `Workflow` changing, in which case re-read it before re-running. Pin a tag or commit SHA in production deployments (see Q13).

### Q24. What's the relationship between SkillStack and the built-in `docx` / `pdf` / `xlsx` / `charts` skills?

Those built-in skills (which ship with some agent runtimes) handle *document-format* production — turning structured content into a `.docx`, `.pdf`, `.xlsx`, or chart. SkillStack's themes handle *domain* work — research, ML, data, AI safety, citations.

The maestro explicitly notes in its "When NOT To Use Maestro" section that tasks already covered by a built-in skill outside the repo should use that built-in skill directly. The two layers compose: a SkillStack chain produces the *content* (a manuscript's `.tex`, a results table, a figure spec) and then hands it to a built-in skill for *formatting* (e.g., the `pdf` skill compiles the `.tex`, the `xlsx` skill writes the results table). Neither layer duplicates the other.

### Q25. How do I chain skills automatically?

You don't — there is no orchestrator that auto-chains. The maestro routes to **one** skill per task. To chain, you (or the agent) finish the first skill's declared `Outputs`, then return to the maestro with the next sub-task and let it route again. The `docs/COOKBOOK.md` file documents 20 ready-made chains as ordered lists; follow them left-to-right manually. If you want automation, write a thin script that reads each skill's `outputs` field and feeds the next skill's `prerequisites`.

### Q26. What happens if two skills seem to apply to my task?

The maestro's conflict-resolution rule (see `maestro/SKILL.md`) says: prefer the **more specific** skill, and prefer the skill whose theme matches the task's **primary output artifact** (the file or deliverable the user ultimately wants). If still ambiguous, ask the user which artifact they want produced. Do not load both skills at once — they may write conflicting files.

### Q27. How do I know which skill produced a given output?

Every skill's `Outputs` section declares the exact file paths it writes (e.g., `Aggregated/OptunaTrials.csv`, `hallucination_report.md`). If you find an unexpected file, check which skill declares that path in its `outputs` frontmatter field. SkillStack does not write a provenance log by default — if you need one, run `style-integrity/claim-source-tracer` to trace claims back to sources, or `data-engineering/data-lineage-tracker` for dataset provenance.

### Q28. Are skills versioned independently of the maestro?

Yes. Each skill's `metadata.version` is independent. The maestro carries its own `metadata.version` and a `skill_count` / `theme_count` pair. You can upgrade a single skill by replacing its `SKILL.md` without touching the maestro, as long as the skill's `name` and `theme` are unchanged (those are the routing keys). Upgrading the maestro itself never invalidates existing skills — it only changes routing-table metadata.

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
