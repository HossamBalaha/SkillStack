# SkillStack — Skill-Level Changelog

> Per-skill changelog, separate from any repo-wide changelog. Every released
> skill is listed by theme. New skills, modified skills, and deprecated
> skills get their own version entries.
>
> Companion to [`docs/ROADMAP.md`](ROADMAP.md).
>
> Author: Hossam Magdy Balaha · MIT License · 168 skills across 9 themes
> (167 themed + 1 maestro) shipped in v1.0.0.

---

## How To Read This Changelog

- **Released** blocks list every skill shipped at that version.
- **Added** entries mark brand-new skills.
- **Modified** entries list the skills whose `SKILL.md` workflow, inputs,
  outputs, or permissions changed.
- **Deprecated** entries warn about skills scheduled for removal (none
  yet).
- Skill counts always include the maestro: 168 = 167 themed + 1 maestro.

---

## v1.0.0 — 2026-11-02 — Initial public release 🟢

**Total:** 168 skills (167 themed + 1 maestro) across 9 themes.

### Maestro (1 skill)

- `maestro/SKILL.md` — top-level orchestrator; 9-theme routing table,
  conflict resolver, fallback chain, confidence-scoring heuristic. Trilingual (`SKILL.md`, `SKILL.ar.md`,
  `SKILL.zh.md`). Ships with
  `maestro/test-cases.md` (50 routing regression tests).

### `academic-research/` — 20 skills

> Research planning & writing.

- `academic-book-author`
- `citation-network-mapper`
- `conference-talk-prep`
- `experimental-design-planner`
- `grant-proposal-writer`
- `hypothesis-designer`
- `journal-manuscript-writer`
- `literature-review-synthesizer`
- `open-science-advocate`
- `peer-review-simulator`
- `pre-registration-drafter`
- `related-work-surveyor`
- `reproducibility-checklist-author`
- `research-ideation-planner`
- `research-portfolio-tracker`
- `research-question-formulator`
- `research-repo-builder`
- `scope-and-aims-writer`
- `supplementary-materials-organizer`
- `thesis-chapter-planner`

### `style-integrity/` — 18 skills

> LaTeX, prose, and coding conventions.

- `abbreviation-consistency-checker`
- `academic-prose-polisher`
- `banned-vocabulary-filter`
- `claim-source-tracer`
- `coding-conventions-enforcer`
- `cross-reference-validator`
- `em-dash-eliminator`
- `execution-protocol`
- `latex-style-guard`
- `math-symbol-auditor`
- `meta-commentary-stripper`
- `notation-consistency-checker`
- `numerical-value-formatter`
- `passive-voice-detector`
- `planning-note-logger`
- `silent-omission-protocol`
- `voice-matching-guard`
- `zero-fabrication-guard`

### `ml-engineering/` — 22 skills

> PyTorch, training, validation.

- `ablation-study-runner`
- `baseline-model-zoo`
- `cross-validation-engine`
- `data-leakage-guard`
- `dataset-adapter-builder`
- `distributed-training-setup`
- `early-stopping-configurator`
- `experiment-folder-organizer`
- `hyperparameter-tuner`
- `inference-pipeline-builder`
- `learning-rate-finder`
- `metrics-computation-suite`
- `mixed-precision-trainer`
- `model-checkpoint-manager`
- `model-explainer`
- `modular-ml-architect`
- `pytorch-lightning-scaffold`
- `reproducible-experiment-runner`
- `seed-and-device-resolver`
- `statistical-validation-rigor`
- `train-val-test-splitter`
- `transformer-finetuner`

### `data-engineering/` — 18 skills

> ETL, schemas, lineage.

- `categorical-encoder`
- `csv-json-converter`
- `data-anonymizer`
- `data-drift-monitor`
- `data-lineage-tracker`
- `data-quality-validator`
- `data-schema-enforcer`
- `dataset-card-generator`
- `etl-pipeline-builder`
- `feature-engineering-toolkit`
- `feature-store-recipe`
- `image-dataset-loader`
- `incremental-loader`
- `missing-data-imputer`
- `outlier-detector`
- `tabular-data-sampler`
- `text-preprocessor`
- `time-series-resampler`

### `visualization/` — 18 skills

> Figures, TikZ, posters, dashboards.

- `academic-plotting-pipeline`
- `attention-map-visualizer`
- `color-palette-selector`
- `confusion-matrix-plotter`
- `dashboard-builder`
- `embedding-projector`
- `figure-caption-writer`
- `infographic-summarizer`
- `interactive-plot-builder`
- `multi-panel-figure-composer`
- `network-graph-visualizer`
- `publication-figure-maker`
- `results-table-formatter`
- `roc-pr-curve-plotter`
- `scientific-poster-designer`
- `surface-plotter`
- `tikz-framework-diagrammer`
- `training-curve-visualizer`

### `writing-citation/` — 18 skills

> BibTeX, citations, abstracts, IMRaD, English editing, paraphrasing.

- `annotated-bibliography-builder`
- `bibtex-citation-manager`
- `citation-style-converter`
- `cohesive-device-checker`
- `doi-verifier`
- `english-academic-editor`
- `hedging-language-balancer`
- `imrad-thesis-writer`
- `literature-matrix-builder`
- `outline-to-prose-expander`
- `paragraph-transition-smoother`
- `plagiarism-paraphraser`
- `reading-level-adjuster`
- `reference-list-formatter`
- `research-methodology-designer`
- `structured-abstract-writer`
- `tense-consistency-fixer`
- `zotero-better-bibtex-bridge`

### `ai-text/` — 15 skills

> Detect & humanize AI text; perplexity, burstiness, watermark detection.

- `ai-tell-catalog`
- `ai-text-detector`
- `ai-text-humanizer`
- `ai-watermark-detector`
- `chatbot-residue-cleaner`
- `citation-hallucination-detector`
- `formatting-by-rule-cleaner`
- `grace-degradation-protocol`
- `inflation-stripper`
- `multi-engine-verification`
- `perplexity-burstiness-scorer`
- `rhythm-by-rule-fixer`
- `severity-classifier`
- `staging-tell-remover`
- `voice-profile-matcher`

### `ai-output-judgement/` — 18 skills

> Judge & verify AI outputs for factuality, hallucination, bias, safety,
> groundedness, faithfulness, alignment, code correctness.

- `alignment-evaluator`
- `bias-auditor`
- `code-output-validator`
- `coherence-fluency-scorer`
- `consistency-checker`
- `evaluation-harness-builder`
- `factuality-checker`
- `faithfulness-scorer`
- `groundedness-verifier`
- `hallucination-detector`
- `llm-as-judge-evaluator`
- `numeric-accuracy-verifier`
- `pii-leak-detector`
- `prompt-injection-detector`
- `reference-accuracy-checker`
- `relevance-scorer`
- `response-quality-scorer`
- `safety-classifier`

### `project-tooling/` — 20 skills

> Packaging, Docker, CI/CD, pytest, docs, READMEs, pyproject.toml,
> Makefiles.

- `changelog-writer`
- `code-of-conduct-generator`
- `contribution-guide-builder`
- `docker-research-container`
- `environment-yaml-builder`
- `github-actions-research-ci`
- `gitignore-builder`
- `issue-template-builder`
- `jupyter-to-script-converter`
- `license-selector`
- `makefile-generator`
- `pr-template-builder`
- `pre-commit-hook-builder`
- `project-zip-packager`
- `pyproject-toml-builder`
- `pytest-scientific-suite`
- `readme-generator`
- `release-notes-generator`
- `requirements-pinner`
- `sphinx-docs-builder`

---

## v1.1 — Planned 🟡 (target: Q1 2027)

**Scope:** 5 new themes, ~54 new skills. Theme count goes from 9 → 14.
Total skill count goes from 168 → ~222.

### Added — New themes

#### `prompt-engineering/` (planned ~12 skills)

- `prompt-template-author`
- `few-shot-scaffolder`
- `chain-of-thought-guard`
- `system-prompt-auditor`
- `prompt-injection-hardener`
- `prompt-regression-tester`
- `prompt-version-differ`
- `prompt-token-budget-estimator`
- `prompt-eval-suite-builder`
- `prompt-rewrite-optimizer`
- `prompt-coverage-mapper`
- `prompt-anti-leakage-guard`

#### `ethics-compliance/` (planned ~10 skills)

- `irb-protocol-drafter`
- `gdpr-data-subject-request-handler`
- `ccpa-opt-out-workflow`
- `ai-act-risk-classifier`
- `model-card-author`
- `impact-assessment-drafter`
- `consent-form-builder`
- `data-retention-policy-author`
- `vendor-dpa-checker`
- `ethics-review-board-prep`

#### `devops/` (planned ~12 skills)

- `terraform-module-author`
- `pulumi-stack-builder`
- `kubernetes-manifest-author`
- `helm-chart-builder`
- `prometheus-rule-author`
- `opentelemetry-instrumenter`
- `slo-sli-author`
- `on-call-runbook-author`
- `incident-postmortem-author`
- `canary-deploy-builder`
- `blue-green-deploy-builder`
- `observability-dashboard-builder`

#### `teaching-pedagogy/` (planned ~10 skills)

- `lesson-plan-author`
- `bloom-taxonomy-mapper`
- `rubric-author`
- `formative-assessment-designer`
- `course-syllabus-scaffolder`
- `active-learning-activity-author`
- `accessibility-auditor`
- `learning-objective-author`
- `instructor-feedback-rubric`
- `study-guide-author`

#### `data-storytelling/` (planned ~10 skills)

- `narrative-from-data-builder`
- `dataviz-annotation-writer`
- `audience-tailored-deck-builder`
- `infographic-drafter`
- `executive-summary-author`
- `data-journalism-storyline-builder`
- `chart-annotation-writer`
- `dashboard-narrative-builder`
- `presentation-flow-designer`
- `key-takeaway-distiller`

### Modified — Maestro

- `maestro/SKILL.md` — routing table grows to 14 rows; conflict resolver
  gains the new overlaps (`prompt-engineering` vs `ai-text`, `devops` vs
  `project-tooling`, `teaching-pedagogy` vs `academic-research`,
  `data-storytelling` vs `visualization`).
- `maestro/test-cases.md` — grows from 50 → ~80 routing regression tests
  covering the 5 new themes.

### Deprecated — None

No themes or skills are deprecated in v1.1.

---

## v1.2 — Planned 🟡 (target: Q2 2027)

**Scope:** integrations and live-test infrastructure. No new themes.

### Added — Scripts

- `scripts/McpLiveTest.py` — boots `mcp-server/`, routes the 50 maestro
  test prompts through it, asserts the routed skill matches
  `maestro/test-cases.md`.
- `scripts/SkillBrowser.py` v2 — upgraded with theme coverage bars, tag
  cloud, related-skill sidebar, and a "run the Examples" button.

### Added — Cursor integration

- `integrations/cursor/` — a Cursor project rule that loads
  `maestro/SKILL.md`, plus a `SkillStack: Route` command palette entry.

### Modified

- Trilingual coverage extended to every theme's `README.md`
  (Arabic + Chinese translations ship alongside the English versions).

---

## v2.0 — Considering 🔵 (target: Q4 2027)

**Scope:** the multi-surface release.

### Added — Themes

- `pytorch-deep/` (planned ~15 skills) — custom autograd functions, Triton
  kernels, `torch.compile` recipes, FSDP patterns, custom CUDA extensions,
  distributed-checkpoint patterns, profiler-driven optimization.

### Added — Surfaces

- VS Code extension (`integrations/vscode/`).
- GitHub Pages site (`site/`).
- Standalone website (`skillstack.dev`).

### Modified — Governance

- Project transitions from BDFL to a steering committee of 3–5 maintainers (see `docs/GOVERNANCE.md`).

---

## Backlog (no target version)

Themes captured but not yet scheduled (see `docs/ROADMAP.md`):

- `mlops/` — model registry, feature-store ops, drift alerting,
  shadow-deploy patterns. Distinct from `devops` and `ml-engineering`.
- `security/` — threat-modeling skills, SBOM generation, secret scanning,
  dependency-vuln triage. Distinct from `ethics-compliance`.
- `ai-red-team/` — adversarial prompt generation, jailbreak catalogs,
  automated jailbreak discovery, model-extraction attack patterns.

Per-skill versioning (semver in the frontmatter) is on the backlog; it
would land in v2.0 alongside the steering-committee transition.

---

## Change Log Conventions

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
semantics, adapted for a skill library:

- **Added** — new skills, themes, or scripts.
- **Modified** — changes to an existing skill's workflow, inputs,
  outputs, permissions, or tags.
- **Deprecated** — skills or themes scheduled for removal.
- **Removed** — skills or themes actually removed (always paired with a
  prior Deprecated entry and a migration guide in `docs/MIGRATIONS.md`).
- **Fixed** — bug fixes to a skill's `Examples` block that previously
  raised an unhandled exception.
- **Security** — security-relevant fixes (also surfaced in
  `SECURITY.md`).

Dates are `YYYY-MM-DD` and reflect the date the change shipped on `main`,
not the date the PR was opened.
