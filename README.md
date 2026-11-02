<div align="center">

# 🧱 SkillStack

### A composable skill library with a maestro orchestrator that routes any task to the correct skill.

[![Skills](https://img.shields.io/badge/Skills-168-blue)]()
[![Themes](https://img.shields.io/badge/Themes-9-green)]()
[![Maestro](https://img.shields.io/badge/Maestro-Orchestrator-orange)]()
[![Status](https://img.shields.io/badge/Status-Active-success)]()
[![Version](https://img.shields.io/badge/Version-1.0-blue)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-Lightning-ee4c2c?logo=pytorch&logoColor=white)](https://lightning.ai)
[![LaTeX](https://img.shields.io/badge/LaTeX-publication--ready-008080?logo=latex&logoColor=white)](https://www.latex-project.org)
[![Optuna](https://img.shields.io/badge/Optuna-Bayesian-black?logo=optuna)](https://optuna.org)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-9b59b6)](https://shap.readthedocs.io)
[![pytest](https://img.shields.io/badge/pytest-scientific-0a9ed4?logo=pytest&logoColor=white)](https://docs.pytest.org)
[![Docker](https://img.shields.io/badge/Docker-reproducible-2496ed?logo=docker&logoColor=white)](https://www.docker.com)
[![BibTeX](https://img.shields.io/badge/BibTeX-managed-lightgrey)](https://www.bibtex.org)
[![CLI](https://img.shields.io/badge/CLI-Skill.py-blueviolet)](scripts/Skill.py)
[![MCP](https://img.shields.io/badge/MCP-server-teal)](mcp-server/)

**`academic-research`** · **`style-integrity`** · **`ml-engineering`** · **`data-engineering`** · **`visualization`** ·*
*`writing-citation`** · **`ai-text`** · **`ai-output-judgement`** · **`project-tooling`**

*Themes are independent modules — drop, swap, or rename any of them and the rest of the stack still works.*

</div>

---

## 📖 Overview

SkillStack is a composable library of 168 skills, organized into 9 independent theme folders. Each skill lives in its
own folder and is described by a `SKILL.md` file the agent loads on demand. A maestro orchestrator at the root
classifies any incoming task and routes it to the correct theme and skill.

The stack is **domain-agnostic by design**. Themes are independent modules: drop, swap, or rename any of them and the
rest of the stack still works. The maestro routes by folder name, not by ordinal, so removing a theme never breaks
routing for the others. Add your own themes, fork the ones you want, or trim the stack down to a single theme — the
maestro, the conventions, and the routing pattern all keep working.

Each skill ships with a concrete workflow (When To Use → Workflow → Inputs → Outputs → Key Rules → Examples →
References) and is written from scratch in the author's own words based on publicly documented best practices. No
third-party skill content is reproduced verbatim.

## 🚀 Start Here

Load **`maestro/SKILL.md`** first. It classifies any incoming task into a theme and points at the correct skill. Do not
guess — route through the maestro.

```bash
# Load maestro, then the routed skill
maestro/SKILL.md → <theme>/<skill-name>/SKILL.md
```

## 📁 Repo Layout

```
skillstack/
├── README.md ← this file
├── LICENSE, .gitignore, NOTICE ← governance
├── CONTRIBUTING.md, CODE_OF_CONDUCT.md
├── requirements-scripts.txt, .pre-commit-config.yaml
├── skills.yaml ← auto-generated manifest (167 themed + 1 maestro)
├── maestro/ ← orchestrator (load first)
│ ├── SKILL.md, SKILL.ar.md, SKILL.zh.md
│ └── test-cases.md ← 50 routing regression tests
├── academic-research/   (20 skills + README.md)
├── style-integrity/      (18 skills + README.md)
├── ml-engineering/        (22 skills + README.md)
├── data-engineering/      (18 skills + README.md)
├── visualization/         (18 skills + README.md)
├── writing-citation/      (18 skills + README.md)
├── ai-text/               (15 skills + README.md)
├── ai-output-judgement/   (18 skills + README.md)
├── project-tooling/       (20 skills + README.md)
├── scripts/ ← 11 CamelCase Python utility scripts
├── docs/ ← QUICKSTART, COOKBOOK, FAQ, etc.
│ └── assets/ ← logo.svg, og-image.svg, etc.
├── mcp-server/ ← MCP server wrapper
└── export/anthropic/ ← Anthropic-format export (generated)

```

Each skill folder contains a `SKILL.md` with YAML frontmatter (`name`, `description`, `metadata`) plus a workflow body.
Some skills also have a `references/` subfolder with deeper rule files.

> **Themes are non-numbered on purpose.** You can drop or rename any theme folder without renumbering the others — the
> maestro routes by folder name, not by ordinal.

## 🏷️ Skill Naming Convention

- Folders use lowercase-kebab-case (e.g., `hyperparameter-tuner`).
- Inside the folder: one `SKILL.md`.
- Optional `references/` subfolder for auxiliary rule files referenced by the main skill.

## 📚 Master Index — All 168 Skills

### 🎓 `academic-research/` — Research Planning & Writing

> Plan studies, draft manuscripts, write theses, design grants, review papers, prepare talks.

| #  | Skill                               | One-Line Description                                                                           |
|----|-------------------------------------|------------------------------------------------------------------------------------------------|
| 1  | `research-ideation-planner`         | Propose 3+ novel research ideas aligned to a target venue, then build an end-to-end blueprint. |
| 2  | `research-repo-builder`             | Scaffold a complete modular research repository (src/, configs, manual, datasets.md).          |
| 3  | `journal-manuscript-writer`         | Draft publication-ready journal sections in LaTeX with strict style rules.                     |
| 4  | `academic-book-author`              | Draft academic book chapters with pedagogical structure and code walkthroughs.                 |
| 5  | `grant-proposal-writer`             | Draft competitive grant proposals (specific aims, significance, approach, budget).             |
| 6  | `literature-review-synthesizer`     | Build systematic reviews with PICO/SPIDER framing and PRISMA flow.                             |
| 7  | `peer-review-simulator`             | Generate peer-review reports and author rebuttal letters.                                      |
| 8  | `conference-talk-prep`              | Draft conference talks with slide outline, notes, and Q&A prep.                                |
| 9  | `thesis-chapter-planner`            | Plan thesis/dissertation chapters with cross-chapter non-redundancy.                           |
| 10 | `research-question-formulator`      | Formulate FINER/PICO research questions and hypotheses.                                        |
| 11 | `hypothesis-designer`               | Design testable hypotheses with null/alternative and effect-size framing.                      |
| 12 | `experimental-design-planner`       | Plan experimental designs (RCT, factorial, crossover) with sample-size calculation.            |
| 13 | `scope-and-aims-writer`             | Draft scope, aims, and contribution statements.                                                |
| 14 | `related-work-surveyor`             | Survey related work and build thematic comparison tables.                                      |
| 15 | `citation-network-mapper`           | Map citation networks and identify influential/bridge papers.                                  |
| 16 | `research-portfolio-tracker`        | Track research outputs, deadlines, and submission status.                                      |
| 17 | `open-science-advocate`             | Apply open-science practices (open data, open code, preprints, OSF).                           |
| 18 | `pre-registration-drafter`          | Draft pre-registration documents (AsPredicted, OSF, Registered Report).                        |
| 19 | `reproducibility-checklist-author`  | Author a reproducibility checklist for a submitted manuscript.                                 |
| 20 | `supplementary-materials-organizer` | Organize supplementary materials (appendices, code, data, figures).                            |

### 🛡️ `style-integrity/` — LaTeX, Prose & Coding Conventions

> Enforce strict style rules, verify citations, audit notation, execute multi-step tasks with discipline.

| #  | Skill                              | One-Line Description                                                                                                            |
|----|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| 1  | `latex-style-guard`                | Enforce LaTeX typography: blank lines around floats, `% ====== %` separators, LaTeX quotes.                                     |
| 2  | `academic-prose-polisher`          | Enforce formal prose: banned-vocabulary filter, no em-dashes, no meta-commentary.                                               |
| 3  | `zero-fabrication-guard`           | Verify every citation, DOI, URL, dataset name via web search; silent-omit if missing.                                           |
| 4  | `execution-protocol`               | 10-stage meta-discipline: Comprehend → Clarify → Define Success → ... → Deliver.                                                |
| 5  | `notation-consistency-checker`     | Audit one-to-one symbol mapping; mandate Nomenclature table if >15 symbols.                                                     |
| 6  | `coding-conventions-enforcer`      | Enforce camelCase variables, CamelCase functions/classes/files/dict-keys, parens in `if`, period-ended comments, double quotes. |
| 7  | `banned-vocabulary-filter`         | Strip banned LLM-flavored words (delve, tapestry, leverage, paramount, etc.).                                                   |
| 8  | `claim-source-tracer`              | Map every factual claim in a manuscript to its source binder/page/quote.                                                        |
| 9  | `silent-omission-protocol`         | Remove jarring `[DECLARATION: ...]` text; relocate to external omission log.                                                    |
| 10 | `planning-note-logger`             | Append a "Planning Note" listing data still needed for the task.                                                                |
| 11 | `cross-reference-validator`        | Verify every `\ref{}` and `\label{}` resolves and every float is referenced.                                                    |
| 12 | `abbreviation-consistency-checker` | Define abbreviations once at first use; enforce consistency thereafter.                                                         |
| 13 | `numerical-value-formatter`        | Wrap standalone numbers in `\ineq{}` and apply PIP/en-dash replacements.                                                        |
| 14 | `math-symbol-auditor`              | Audit math symbols: no reuse, consistent notation, defined in nomenclature.                                                     |
| 15 | `passive-voice-detector`           | Detect passive voice and suggest active alternatives.                                                                           |
| 16 | `em-dash-eliminator`               | Replace em-dashes with standard punctuation or en-dashes.                                                                       |
| 17 | `meta-commentary-stripper`         | Remove "In this section we will show" / "The reader will learn" patterns.                                                       |
| 18 | `voice-matching-guard`             | Match author voice sample if provided; override generic rules.                                                                  |

### ⚙️ `ml-engineering/` — PyTorch, Training & Validation

> Build, train, tune, explain, and validate ML models in PyTorch/Lightning/HuggingFace.

| #  | Skill                            | One-Line Description                                                                     |
|----|----------------------------------|------------------------------------------------------------------------------------------|
| 1  | `modular-ml-architect`           | Enforce modular Python conventions: 2-space indent, CamelCase, period-ended comments.    |
| 2  | `reproducible-experiment-runner` | Setup reproducible experiments: device resolution, seeds, dual logging, 4-split folders. |
| 3  | `data-leakage-guard`             | Enforce train/val/test isolation; fit preprocessing on train only.                       |
| 4  | `statistical-validation-rigour`  | Bootstrap CIs, paired t-test/Wilcoxon/McNemar, AUC branching.                            |
| 5  | `hyperparameter-tuner`           | Optuna Bayesian optimization (TPE, median pruner, multi-fidelity).                       |
| 6  | `model-explainer`                | SHAP/LIME/Integrated-Gradients explanations and plots.                                   |
| 7  | `pytorch-lightning-scaffold`     | Scaffold LightningModule, DataModule, Callbacks, Loggers.                                |
| 8  | `transformer-finetuner`          | Fine-tune Hugging Face transformers with Trainer/PEFT.                                   |
| 9  | `dataset-adapter-builder`        | Defensive dataset adapters with actionable FileNotFoundError.                            |
| 10 | `seed-and-device-resolver`       | Resolve `torch.device` once and `.to(device)` on every nn.Module.                        |
| 11 | `experiment-folder-organizer`    | Single timestamped experiment folder; 4 split subfolders (Train/Val/Test/Aggregated).    |
| 12 | `train-val-test-splitter`        | Stratified splitting at highest hierarchical level.                                      |
| 13 | `early-stopping-configurator`    | Configure early stopping with patience, mode, delta.                                     |
| 14 | `learning-rate-finder`           | Run LR range test (Smith 2015) and plot loss-vs-LR.                                      |
| 15 | `mixed-precision-trainer`        | AMP autocast + GradScaler for fp16/bf16 training.                                        |
| 16 | `distributed-training-setup`     | DDP setup with `torchrun`, `find_unused_parameters`, world-size.                         |
| 17 | `model-checkpoint-manager`       | Save/load checkpoints with epoch, val-metric, optimizer state.                           |
| 18 | `inference-pipeline-builder`     | Build FastAPI inference endpoint with pre/post-processing.                               |
| 19 | `baseline-model-zoo`             | Implement baseline models (LR, RF, XGBoost, MLP) for comparison.                         |
| 20 | `ablation-study-runner`          | Run ablations by removing/altering components systematically.                            |
| 21 | `cross-validation-engine`        | k-fold, stratified, grouped, and time-series cross-validation.                           |
| 22 | `metrics-computation-suite`      | Accuracy, F1, AUC, MCC, Cohen's kappa, calibration error.                                |

### 🔬 `data-engineering/` — ETL, Schemas & Lineage

> Build robust data pipelines, enforce schemas, anonymize PII, track lineage.

| #  | Skill                         | One-Line Description                                                     |
|----|-------------------------------|--------------------------------------------------------------------------|
| 1  | `etl-pipeline-builder`        | Idempotent ETL with extract-validate-transform-load and audit trail.     |
| 2  | `feature-store-recipe`        | Feature engineering with point-in-time correctness and freshness checks. |
| 3  | `data-quality-validator`      | Validate with pandera/great-expectations; null/duplicate/outlier checks. |
| 4  | `csv-json-converter`          | Convert between CSV/JSON/Parquet/Arrow with type preservation.           |
| 5  | `dataset-card-generator`      | Generate dataset cards: provenance, license, composition, intended use.  |
| 6  | `data-schema-enforcer`        | Enforce schema with pydantic models or pandera DataFrameSchemas.         |
| 7  | `incremental-loader`          | Load incrementally with stateful checkpoints and idempotent re-runs.     |
| 8  | `data-anonymizer`             | Anonymize PII: hashing, k-anonymity, generalization, suppression.        |
| 9  | `time-series-resampler`       | Resample time series with forward/backward fill and alignment.           |
| 10 | `missing-data-imputer`        | Impute missing data: mean/median/KNN/iterative/MICE.                     |
| 11 | `outlier-detector`            | Detect outliers: IQR, z-score, isolation forest, DBSCAN.                 |
| 12 | `data-drift-monitor`          | Monitor data drift: PSI, KS test, Wasserstein distance.                  |
| 13 | `feature-engineering-toolkit` | Build features: polynomial, binning, target encoding, interactions.      |
| 14 | `categorical-encoder`         | Encode categoricals: one-hot, ordinal, target, hash, embedding.          |
| 15 | `text-preprocessor`           | Preprocess text: tokenize, lowercase, lemmatize, stopword removal.       |
| 16 | `image-dataset-loader`        | Load image datasets with augmentation, batching, and prefetch.           |
| 17 | `tabular-data-sampler`        | Sample tabular data: random, stratified, weighted, reservoir.            |
| 18 | `data-lineage-tracker`        | Track data lineage: source → transform → sink with provenance graph.     |

### 📊 `visualization/` — Figures, TikZ & Posters

> Generate publication-ready figures, TikZ diagrams, A0 posters, results tables, dashboards.

| #  | Skill                         | One-Line Description                                                    |
|----|-------------------------------|-------------------------------------------------------------------------|
| 1  | `publication-figure-maker`    | Journal-ready matplotlib figures with correct sizes and vector formats. |
| 2  | `academic-plotting-pipeline`  | Two-track: image-gen diagrams + matplotlib data figures.                |
| 3  | `tikz-framework-diagrammer`   | TikZ pipeline diagrams: concise nodes, solid groups, resizebox.         |
| 4  | `scientific-poster-designer`  | A0 posters (841×1189mm), IMRAD layout, 1m readability.                  |
| 5  | `results-table-formatter`     | booktabs tables with multi-row headers and 95% CI columns.              |
| 6  | `infographic-summarizer`      | Single-page infographics with visual hierarchy.                         |
| 7  | `confusion-matrix-plotter`    | Plot confusion matrix with normalized + raw counts.                     |
| 8  | `roc-pr-curve-plotter`        | ROC and PR curves with AUC and baseline references.                     |
| 9  | `training-curve-visualizer`   | Plot train/val loss and accuracy over epochs.                           |
| 10 | `attention-map-visualizer`    | Visualize transformer attention weights as heatmaps.                    |
| 11 | `embedding-projector`         | Project high-dim embeddings via PCA/t-SNE/UMAP.                         |
| 12 | `dashboard-builder`           | Build interactive dashboards (Streamlit, Dash, Gradio).                 |
| 13 | `interactive-plot-builder`    | Interactive plots with Plotly/Bokeh/Holoviews.                          |
| 14 | `color-palette-selector`      | Select colorblind-friendly palettes (viridis, cividis, colorbrewer).    |
| 15 | `figure-caption-writer`       | Write detailed captions: what / how / why.                              |
| 16 | `multi-panel-figure-composer` | Compose multi-panel figures with subplots and shared axes.              |
| 17 | `surface-plotter`             | 3D surface plots with proper view angles and colorbars.                 |
| 18 | `network-graph-visualizer`    | Visualize network graphs with layout algorithms.                        |

### 📝 `writing-citation/` — BibTeX, Editing & Paraphrasing

> Manage citations, draft abstracts, edit non-native English, paraphrase safely.

| #  | Skill                            | One-Line Description                                                   |
|----|----------------------------------|------------------------------------------------------------------------|
| 1  | `bibtex-citation-manager`        | Manage BibTeX: citekeys, dedup, field validation, every bibitem cited. |
| 2  | `structured-abstract-writer`     | Draft structured abstracts (Background/Methods/Results/Conclusion).    |
| 3  | `imrad-thesis-writer`            | Draft full IMRaD theses with non-redundant cross-references.           |
| 4  | `research-methodology-designer`  | Design methodologies: study design, sampling, sample size, ethics.     |
| 5  | `english-academic-editor`        | Edit non-native English: articles, tense, hedging, register.           |
| 6  | `plagiarism-paraphraser`         | Rewrite to avoid plagiarism while preserving meaning.                  |
| 7  | `zotero-better-bibtex-bridge`    | Bridge Zotero BetterBibTeX exports to LaTeX workflows.                 |
| 8  | `citation-style-converter`       | Convert between IEEE, APA, Chicago, Vancouver, MLA.                    |
| 9  | `doi-verifier`                   | Verify DOIs resolve to the claimed paper via crossref.org.             |
| 10 | `reference-list-formatter`       | Format reference lists in any citation style.                          |
| 11 | `annotated-bibliography-builder` | Build annotated bibliographies with summary and assessment.            |
| 12 | `literature-matrix-builder`      | Build a literature matrix (paper × dimension) for synthesis.           |
| 13 | `outline-to-prose-expander`      | Expand a bullet outline into flowing academic prose.                   |
| 14 | `paragraph-transition-smoother`  | Smooth paragraph transitions with logical connectors.                  |
| 15 | `tense-consistency-fixer`        | Fix tense: past for methods/results, present for discussion.           |
| 16 | `hedging-language-balancer`      | Balance hedging (modal verbs, adverbs) to match evidence strength.     |
| 17 | `cohesive-device-checker`        | Check cohesive devices: reference, conjunction, lexical.               |
| 18 | `reading-level-adjuster`         | Adjust reading level to target grade (Flesch-Kincaid).                 |

### 🤖 `ai-text/` — Detect & Humanize AI Text

> Detect AI-generated text, restore natural voice, verify citations, detect watermarks.

| #  | Skill                             | One-Line Description                                          |
|----|-----------------------------------|---------------------------------------------------------------|
| 1  | `ai-text-detector`                | Detect AI text using 6-category tells with S1-S4 severity.    |
| 2  | `ai-text-humanizer`               | Rewrite AI text to restore natural voice, preserving facts.   |
| 3  | `perplexity-burstiness-scorer`    | Compute perplexity and burstiness statistics for a text.      |
| 4  | `ai-tell-catalogue`               | Reference catalogue of 26 AI tells organized by category.     |
| 5  | `severity-classifier`             | Classify detected tells into S1/S2/S3/S4 severity.            |
| 6  | `voice-profile-matcher`           | Match a target author voice profile (vocabulary, rhythm).     |
| 7  | `chatbot-residue-cleaner`         | Remove "I hope this helps", "Great question!" residue.        |
| 8  | `inflation-stripper`              | Remove inflated significance ("pivotal moment", "testament"). |
| 9  | `staging-tell-remover`            | Remove staging tells ("Not X but Y", one-line closers).       |
| 10 | `rhythm-by-rule-fixer`            | Fix forced triads, repeated openings, dashes-as-connectors.   |
| 11 | `formatting-by-rule-cleaner`      | Clean decorative bold, title-case headings, curly quotes.     |
| 12 | `citation-hallucination-detector` | Detect fake DOIs, phantom citations, fake outlets.            |
| 13 | `grace-degradation-protocol`      | When a fact can't be verified, omit or `[Verify Source]`.     |
| 14 | `ai-watermark-detector`           | Detect LLM watermarks (Kirchenbauer et al. 2023).             |
| 15 | `multi-engine-verification`       | Cross-reference outputs across GPTZero, Originality.ai, etc.  |

### 🔍 `ai-output-judgement/` — Judge & Verify AI Outputs

> Evaluate AI outputs for factuality, hallucination, bias, safety, groundedness, faithfulness, and correctness. Build
> evaluation harnesses.

| #  | Skill                        | One-Line Description                                                                   |
|----|------------------------------|----------------------------------------------------------------------------------------|
| 1  | `factuality-checker`         | Verify factual claims in AI outputs against trusted sources (FActScore, SAFE).         |
| 2  | `hallucination-detector`     | Detect hallucinated content: fabricated entities, fake citations, invented statistics. |
| 3  | `llm-as-judge-evaluator`     | Implement LLM-as-judge with rubrics, bias mitigation, inter-judge agreement.           |
| 4  | `response-quality-scorer`    | Score responses on helpfulness, completeness, relevance, clarity, depth (1-5).         |
| 5  | `bias-auditor`               | Audit outputs for demographic/cognitive bias via counterfactual prompts.               |
| 6  | `safety-classifier`          | Classify outputs for violence, hate, sexual, self-harm, illegal content.               |
| 7  | `groundedness-verifier`      | Verify RAG outputs are grounded in retrieved context via NLI models.                   |
| 8  | `consistency-checker`        | Check consistency across temperature, paraphrased inputs, multiple samples.            |
| 9  | `faithfulness-scorer`        | Score summarization/QA faithfulness to source (NLI, QAGS, SummaC).                     |
| 10 | `relevance-scorer`           | Score relevance to query via semantic similarity and intent matching.                  |
| 11 | `coherence-fluency-scorer`   | Score coherence, fluency, grammaticality via perplexity and LanguageTool.              |
| 12 | `pii-leak-detector`          | Detect PII leakage (emails, phones, SSNs, names) via Presidio + spaCy NER.             |
| 13 | `prompt-injection-detector`  | Detect direct and indirect prompt injection attacks.                                   |
| 14 | `alignment-evaluator`        | Evaluate alignment with HHH framework (Helpful, Honest, Harmless).                     |
| 15 | `reference-accuracy-checker` | Verify AI-generated references resolve to real papers (Crossref, Semantic Scholar).    |
| 16 | `numeric-accuracy-verifier`  | Verify numeric computations, statistics, dates, quantities in outputs.                 |
| 17 | `code-output-validator`      | Validate AI-generated code: syntax, execution, tests, spec match, security.            |
| 18 | `evaluation-harness-builder` | Build eval harnesses (lm-eval-harness, HELM, OpenAI Evals style).                      |

### 🧰 `project-tooling/` — Packaging, Docker & CI/CD

> Bundle, containerize, automate, test, document, and release research projects.

| #  | Skill                         | One-Line Description                                                      |
|----|-------------------------------|---------------------------------------------------------------------------|
| 1  | `project-zip-packager`        | Bundle repo into zip excluding `*.zip`, `Datasets/`, `results/`, `.git/`. |
| 2  | `requirements-pinner`         | Generate unversioned Requirements.txt or pinned requirements.lock.        |
| 3  | `pyproject-toml-builder`      | Build pyproject.toml with Poetry/PDM/setuptools config.                   |
| 4  | `docker-research-container`   | Build Dockerfile for reproducible research (non-root, multi-stage).       |
| 5  | `github-actions-research-ci`  | Build GitHub Actions: install → lint → test → docs → docker push.         |
| 6  | `pytest-scientific-suite`     | Write pytest tests with fixtures, parametrize, deterministic seeds.       |
| 7  | `sphinx-docs-builder`         | Build Sphinx/MkDocs docs with autodoc and tutorials.                      |
| 8  | `readme-generator`            | Generate README.md with hook, what/why, quick-start, real examples.       |
| 9  | `jupyter-to-script-converter` | Convert .ipynb to clean .py with functions and `__main__`.                |
| 10 | `gitignore-builder`           | Generate .gitignore for Python/Node/R/Data/IDE-specific patterns.         |
| 11 | `license-selector`            | Select MIT/Apache-2.0/GPL-3.0/AGPL/BSD based on use case.                 |
| 12 | `changelog-writer`            | Write Keep-a-Changelog format entries with semver bumps.                  |
| 13 | `contribution-guide-builder`  | Build CONTRIBUTING.md with workflow, style, PR template.                  |
| 14 | `code-of-conduct-generator`   | Generate Contributor Covenant Code of Conduct.                            |
| 15 | `issue-template-builder`      | Build bug/feature/question issue templates with YAML frontmatter.         |
| 16 | `pr-template-builder`         | Build PR template with checklist, summary, testing, breaking changes.     |
| 17 | `environment-yaml-builder`    | Build environment.yml (conda) or Pipfile for reproducible envs.           |
| 18 | `makefile-generator`          | Generate Makefile with install/test/lint/docs/run/format targets.         |
| 19 | `pre-commit-hook-builder`     | Build .pre-commit-config.yaml with ruff, black, mypy, end-of-file.        |
| 20 | `release-notes-generator`     | Generate release notes from git log since last tag.                       |

## 🔗 Common Skill Chains

Skills rarely run in isolation. These chains reflect real research workflows — load the first skill, finish its output,
then load the next.

### 🎓 Research Lifecycle Chains

| Chain                                                                                                                                  | Why                                          |
|----------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| `scope-and-aims-writer` → `research-question-formulator` → `hypothesis-designer` → `experimental-design-planner`                       | Scope → question → hypothesis → study design |
| `research-ideation-planner` → `research-repo-builder` → `modular-ml-architect` → `reproducible-experiment-runner`                      | Idea → repo → code style → experiments       |
| `literature-review-synthesizer` → `literature-matrix-builder` → `related-work-surveyor` → `citation-network-mapper`                    | Survey → matrix → gap → influential papers   |
| `grant-proposal-writer` → `research-methodology-designer` → `pre-registration-drafter` → `reproducibility-checklist-author`            | Grant → methods → pre-reg → repro            |
| `thesis-chapter-planner` → `imrad-thesis-writer` → `tense-consistency-fixer` → `hedging-language-balancer` → `cohesive-device-checker` | Plan → draft → tense → hedge → cohesion      |
| `conference-talk-prep` → `scientific-poster-designer` → `supplementary-materials-organizer` → `reproducibility-checklist-author`       | Talk → poster → supplement → repro           |

### 🛡️ Style & Integrity Chains

| Chain                                                                                                                                                         | Why                                              |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| `coding-conventions-enforcer` → `latex-style-guard` → `academic-prose-polisher` → `banned-vocabulary-filter`                                                  | Code + prose style enforcement before submission |
| `bibtex-citation-manager` → `doi-verifier` → `citation-style-converter` → `reference-list-formatter` → `cross-reference-validator` → `zero-fabrication-guard` | Full citation integrity pass                     |
| `claim-source-tracer` → `zero-fabrication-guard` → `silent-omission-protocol` → `planning-note-logger`                                                        | Verify claims → omit silently → log gaps         |
| `notation-consistency-checker` → `math-symbol-auditor` → `numerical-value-formatter` → `abbreviation-consistency-checker`                                     | Math notation audit                              |
| `passive-voice-detector` → `em-dash-eliminator` → `meta-commentary-stripper` → `voice-matching-guard`                                                         | Prose cleanup preserving author voice            |

### ⚙️ ML Engineering Chains

| Chain                                                                                                                                               | Why                                       |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| `train-val-test-splitter` → `data-leakage-guard` → `seed-and-device-resolver` → `experiment-folder-organizer`                                       | Split → isolate → seed → folder           |
| `dataset-adapter-builder` → `image-dataset-loader` → `data-leakage-guard` → `modular-ml-architect`                                                  | Adapter → loader → isolation → code style |
| `pytorch-lightning-scaffold` → `mixed-precision-trainer` → `early-stopping-configurator` → `model-checkpoint-manager`                               | Lightning → AMP → early stop → checkpoint |
| `hyperparameter-tuner` → `early-stopping-configurator` → `model-checkpoint-manager` → `metrics-computation-suite` → `statistical-validation-rigour` | Tune → stop → save → metrics → stats      |
| `transformer-finetuner` → `model-explainer` → `ablation-study-runner` → `cross-validation-engine`                                                   | Train → explain → ablate → CV             |
| `baseline-model-zoo` → `metrics-computation-suite` → `statistical-validation-rigour` → `ablation-study-runner`                                      | Baselines → metrics → stats → ablations   |
| `inference-pipeline-builder` → `model-checkpoint-manager` → `metrics-computation-suite`                                                             | Deploy → load → evaluate                  |

### 🔬 Data Engineering Chains

| Chain                                                                                                                      | Why                                          |
|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| `etl-pipeline-builder` → `data-quality-validator` → `data-schema-enforcer` → `data-lineage-tracker`                        | ETL → validate → enforce → lineage           |
| `feature-engineering-toolkit` → `categorical-encoder` → `missing-data-imputer` → `outlier-detector` → `data-drift-monitor` | Features → encode → impute → outlier → drift |
| `csv-json-converter` → `data-schema-enforcer` → `data-anonymizer` → `dataset-card-generator`                               | Convert → schema → anonymize → card          |
| `incremental-loader` → `time-series-resampler` → `missing-data-imputer` → `data-drift-monitor`                             | Incremental → resample → impute → drift      |
| `text-preprocessor` → `feature-engineering-toolkit` → `categorical-encoder` → `tabular-data-sampler`                       | Text → features → encode → sample            |

### 📊 Visualization Chains

| Chain                                                                                                                | Why                                   |
|----------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| `publication-figure-maker` → `figure-caption-writer` → `results-table-formatter`                                     | Figure + caption + table bundle       |
| `academic-plotting-pipeline` → `tikz-framework-diagrammer` → `multi-panel-figure-composer` → `figure-caption-writer` | Pipeline → diagram → panels → caption |
| `confusion-matrix-plotter` → `roc-pr-curve-plotter` → `training-curve-visualizer` → `embedding-projector`            | Classification evaluation suite       |
| `attention-map-visualizer` → `embedding-projector` → `model-explainer` (ml-engineering)                              | XAI visual bundle                     |
| `color-palette-selector` → `publication-figure-maker` → `multi-panel-figure-composer` → `figure-caption-writer`      | Color → figures → panels → caption    |
| `scientific-poster-designer` → `publication-figure-maker` → `results-table-formatter` → `figure-caption-writer`      | A0 poster bundle                      |
| `dashboard-builder` → `interactive-plot-builder` → `network-graph-visualizer`                                        | Interactive dashboard bundle          |

### 📝 Writing & Citation Chains

| Chain                                                                                                                                               | Why                                           |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| `outline-to-prose-expander` → `paragraph-transition-smoother` → `tense-consistency-fixer` → `hedging-language-balancer` → `cohesive-device-checker` | Outline → flow → tense → hedge → cohesion     |
| `structured-abstract-writer` → `imrad-thesis-writer` → `tense-consistency-fixer` → `english-academic-editor` → `reading-level-adjuster`             | Abstract → IMRaD → tense → edit → readability |
| `zotero-better-bibtex-bridge` → `bibtex-citation-manager` → `doi-verifier` → `citation-style-converter` → `reference-list-formatter`                | Zotero → BibTeX → verify → convert → format   |
| `literature-review-synthesizer` → `annotated-bibliography-builder` → `literature-matrix-builder` → `related-work-surveyor`                          | Review → annotations → matrix → gap           |
| `plagiarism-paraphraser` → `english-academic-editor` → `tense-consistency-fixer` → `cohesive-device-checker`                                        | Paraphrase → edit → tense → cohesion          |

### 🤖 AI-Text Chains

| Chain                                                                                                                                                   | Why                                                            |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| `ai-text-detector` → `severity-classifier` → `ai-tell-catalogue` → `ai-text-humanizer` → `grace-degradation-protocol` → `multi-engine-verification`     | Detect → classify → catalogue → humanize → degrade → re-verify |
| `ai-text-detector` → `citation-hallucination-detector` → `ai-watermark-detector` → `perplexity-burstiness-scorer` → `multi-engine-verification`         | Multi-signal detection suite                                   |
| `ai-text-humanizer` → `chatbot-residue-cleaner` → `inflation-stripper` → `staging-tell-remover` → `rhythm-by-rule-fixer` → `formatting-by-rule-cleaner` | Humanizer sub-skills in sequence                               |
| `voice-profile-matcher` → `ai-text-humanizer` → `multi-engine-verification`                                                                             | Match voice → humanize → verify                                |

### 🔍 AI-Output Judgement Chains

| Chain                                                                                                                       | Why                                                         |
|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| `factuality-checker` → `hallucination-detector` → `reference-accuracy-checker` → `numeric-accuracy-verifier`                | Full factuality audit of an LLM response                    |
| `groundedness-verifier` → `faithfulness-scorer` → `relevance-scorer` → `coherence-fluency-scorer`                           | RAG output quality suite                                    |
| `llm-as-judge-evaluator` → `response-quality-scorer` → `consistency-checker` → `alignment-evaluator`                        | Judge + score + consistency + alignment                     |
| `bias-auditor` → `safety-classifier` → `pii-leak-detector` → `prompt-injection-detector`                                    | Safety & responsibility audit                               |
| `code-output-validator` → `numeric-accuracy-verifier` → `factuality-checker`                                                | Validate AI-generated code + its claims                     |
| `evaluation-harness-builder` → `llm-as-judge-evaluator` → `response-quality-scorer` → `consistency-checker`                 | Build harness + run judge + score + check                   |
| `hallucination-detector` → `factuality-checker` → `reference-accuracy-checker` → `zero-fabrication-guard` (style-integrity) | Hallucination → factuality → references → fabrication guard |
| `prompt-injection-detector` → `safety-classifier` → `pii-leak-detector` → `bias-auditor`                                    | Adversarial input + output safety sweep                     |

### 🧰 Project Tooling Chains

| Chain                                                                                                                                     | Why                                             |
|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| `pyproject-toml-builder` → `requirements-pinner` → `environment-yaml-builder` → `docker-research-container`                               | Project setup → deps → env → container          |
| `gitignore-builder` → `license-selector` → `readme-generator` → `contribution-guide-builder` → `code-of-conduct-generator`                | Repo bootstrapping bundle                       |
| `github-actions-research-ci` → `pytest-scientific-suite` → `pre-commit-hook-builder` → `makefile-generator`                               | CI → tests → hooks → Makefile                   |
| `issue-template-builder` → `pr-template-builder` → `contribution-guide-builder` → `changelog-writer` → `release-notes-generator`          | Issue → PR → contributing → changelog → release |
| `jupyter-to-script-converter` → `coding-conventions-enforcer` → `modular-ml-architect` → `pyproject-toml-builder` → `sphinx-docs-builder` | Notebook → script → style → package → docs      |
| `project-zip-packager` → `release-notes-generator` → `changelog-writer`                                                                   | Final release bundle                            |

### 🌐 Cross-Theme Mega-Chains

| Chain                                                                                                                                                                                                                                                                                                                       | Why                                                                                                                         |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `research-ideation-planner` → `research-repo-builder` → `coding-conventions-enforcer` → `reproducible-experiment-runner` → `statistical-validation-rigour` → `journal-manuscript-writer` → `latex-style-guard` → `bibtex-citation-manager` → `zero-fabrication-guard` → `publication-figure-maker` → `project-zip-packager` | Idea → repo → code → experiments → stats → manuscript → LaTeX → BibTeX → verify → figures → ZIP                             |
| `peer-review-simulator` → `claim-source-tracer` → `zero-fabrication-guard` → `cross-reference-validator` → `bibtex-citation-manager` → `doi-verifier`                                                                                                                                                                       | Review → trace → verify → cross-ref → BibTeX → DOI                                                                          |
| `etl-pipeline-builder` → `data-quality-validator` → `feature-engineering-toolkit` → `train-val-test-splitter` → `data-leakage-guard` → `hyperparameter-tuner` → `model-explainer` → `ablation-study-runner` → `metrics-computation-suite` → `statistical-validation-rigour`                                                 | Full ML pipeline from raw data to validated metrics                                                                         |
| `inference-pipeline-builder` → `response-quality-scorer` → `groundedness-verifier` → `factuality-checker` → `hallucination-detector` → `safety-classifier` → `pii-leak-detector` → `bias-auditor` → `alignment-evaluator`                                                                                                   | Deploy LLM → judge output quality → verify grounding → check facts → catch hallucinations → safety → PII → bias → alignment |
| `evaluation-harness-builder` → `llm-as-judge-evaluator` → `response-quality-scorer` → `consistency-checker` → `factuality-checker` → `reference-accuracy-checker` → `numeric-accuracy-verifier` → `code-output-validator`                                                                                                   | Build eval suite → judge → score → consistency → factuality → references → numerics → code                                  |

## 💻 The Coding-Conventions Skill (Special Note)

This repo enforces a strict, non-standard Python style. When writing Python anywhere in this repo, load
`style-integrity/coding-conventions-enforcer/SKILL.md` first:

1. **Variables** use `camelCase` (e.g., `dataSourceUrl`).
2. **Functions, classes, file names, dict keys** use `CamelCase` (e.g., `ProcessData`, `DataProcessor`,
   `VisualizationUtils.py`, `"ValidationStatus"`).
3. **`if` conditions** wrapped in parentheses: `if (condition):`.
4. **Comments** above each statement, ending with a period: `# Initialize the counter.`.
5. **Strings** use double quotes `""` (except in docstrings).

Framework-mandated lowercase (`forward`, `backward`, `training_step`, `validation_step`, `configure_optimizers`,
`setUp`, `tearDown`) is exempt.

## 🧭 How To Use Any Skill

1. Read `maestro/SKILL.md` to route.
2. Open the chosen skill's `SKILL.md`.
3. Read the YAML frontmatter (especially `description`, `tags`, `related`, `prerequisites`) to confirm fit.
4. Read the body in full.
5. If the body references `references/foo.md`, read that file too.
6. Follow the workflow.
7. If Python code is involved, also load `coding-conventions-enforcer`.
8. If a `LITE.md` exists in the same folder and your context is tight, load that instead.
9. If a `SKILL.ar.md` or `SKILL.zh.md` exists and you need Arabic or Chinese, load that instead.

## 🛠️ Repo Tooling

### Root Governance Files

| File                       | Purpose                                                           |
|----------------------------|-------------------------------------------------------------------|
| `LICENSE`                  | MIT License (2026, Hossam Magdy Balaha)                           |
| `.gitignore`               | Python + Data + IDE patterns                                      |
| `NOTICE`                   | Defensive attribution (original work, paraphrased best practices) |
| `CONTRIBUTING.md`          | How to report bugs, suggest changes, author new skills            |
| `CODE_OF_CONDUCT.md`       | Contributor Covenant v2.1                                         |
| `.pre-commit-config.yaml`  | Auto-run linter + ruff on every commit                            |
| `requirements-scripts.txt` | Pinned deps for the `scripts/` utilities                          |

### Python Utility Scripts (`scripts/`)

All scripts follow the repo's strict coding conventions. Install deps: `pip install -r requirements-scripts.txt`.

| Script                | Purpose                                                      | CLI                                                            |
|-----------------------|--------------------------------------------------------------|----------------------------------------------------------------|
| `GenerateManifest.py` | Walk all skills, write `skills.yaml` manifest                | `python scripts/GenerateManifest.py [--check]`                 |
| `LintSkills.py`       | Validate every SKILL.md (frontmatter, sections, line count)  | `python scripts/LintSkills.py [skill-path]`                    |
| `CheckLinks.py`       | HEAD-request every URL in every skill's References           | `python scripts/CheckLinks.py [--timeout 5]`                   |
| `VerifyCitations.py`  | Verify arXiv IDs and DOIs cited in skills                    | `python scripts/VerifyCitations.py`                            |
| `CoverageReport.py`   | Generate `docs/coverage.md` (per-skill stats)                | `python scripts/CoverageReport.py`                             |
| `Skill.py`            | Skill CLI: list, search, show, validate, graph, tags, health | `python scripts/Skill.py <command>`                            |
| `Audit.py`            | Log skill invocations to `.audit-log.jsonl`                  | `python scripts/Audit.py log <skill> [--input f] [--output f]` |
| `CacheSkill.py`       | Concatenate SKILL.md + references/ into one context blob     | `python scripts/CacheSkill.py <skill-name> [--all]`            |
| `SkillHealth.py`      | Generate `docs/health.html` dashboard                        | `python scripts/SkillHealth.py`                                |
| `GraphvizChains.py`   | Generate `docs/skill-graph.svg` dependency graph             | `python scripts/GraphvizChains.py`                             |
| `ExportAnthropic.py`  | Export to Anthropic Agent Skills format                      | `python scripts/ExportAnthropic.py [--out export/anthropic]`   |

### Skill CLI Quick Examples

```bash
python scripts/Skill.py list                    # list all skills grouped by theme
python scripts/Skill.py search "latex"          # full-text search across name/description/tags
python scripts/Skill.py show hyperparameter-tuner # print a skill's full SKILL.md
python scripts/Skill.py validate latex-style-guard  # lint one skill
python scripts/Skill.py graph                   # print skill dependency graph
python scripts/Skill.py tags                    # print tag cloud
python scripts/Skill.py health                  # print coverage summary
```

### Generated Artifacts (auto-regenerated by CI)

| Path                   | Source                                                                    |
|------------------------|---------------------------------------------------------------------------|
| `skills.yaml`          | `generate_manifest.py` — machine-readable manifest of all 168+ skills     |
| `docs/coverage.md`     | `coverage_report.py` — per-skill line count, has-examples, has-references |
| `docs/health.html`     | `skill_health.py` — visual dashboard                                      |
| `docs/skill-graph.svg` | `graphviz_chains.py` — skill dependency graph                             |
| `export/anthropic/`    | `export_anthropic.py` — Anthropic-format export                           |

## 📚 Documentation (`docs/`)

| File                      | Purpose                                                                   |
|---------------------------|---------------------------------------------------------------------------|
| `docs/QUICKSTART.md`      | 5-minute quickstart (load maestro → route → ship)                         |
| `docs/COOKBOOK.md`        | 20 concrete scenarios → ordered skill chains                              |
| `docs/FAQ.md`             | 28 Q&A pairs (adding themes, disabling skills, MCP, etc.)                 |
| `docs/COMPARISON.md`      | How SkillStack differs from Anthropic skills, SkillDB, OpenAI Evals, etc. |
| `docs/AUTHORING_GUIDE.md` | Canonical template + rules for writing a new skill                        |
| `docs/coverage.md`        | Auto-generated per-skill coverage report                                  |
| `docs/health.html`        | Auto-generated skill health dashboard                                     |
| `docs/skill-graph.svg`    | Auto-generated skill dependency graph                                     |

### Per-Theme READMEs

Each theme folder has its own `README.md` mini-index (skill table with difficulty, tags, related):

`academic-research/README.md` · `style-integrity/README.md` · `ml-engineering/README.md` ·`data-engineering/README.md` ·
`visualization/README.md` · `writing-citation/README.md` · `ai-text/README.md` ·`ai-output-judgement/README.md` ·
`project-tooling/README.md`

## 🔌 Integrations

### MCP Server (`mcp-server/`)

Expose all 168 skills via the Model Context Protocol so any MCP client (Claude Desktop, Cursor, etc.) can load them on
demand.

```bash
cd mcp-server
npm install
npm start  # boots stdio MCP server
```

Register with Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "skillstack": {
      "command": "node",
      "args": [
        "/absolute/path/to/skills/mcp-server/index.js"
      ]
    }
  }
}
```

The server exposes 4 tools: `list_skills`, `search_skills(query)`, `get_skill(theme, skill_name)`,
`route_task(task_description)`. See `mcp-server/README.md` for Cursor config and test prompts.

### Anthropic Agent Skills Export

```bash
python scripts/ExportAnthropic.py --out export/anthropic
```

Exports every skill to Anthropic's format (single `.md` per skill with `name` + `description` frontmatter) under
`export/anthropic/<theme>/<skill-name>.md`.

## 🎨 Branding Assets (`docs/assets/`)

| File                           | Purpose                                               |
|--------------------------------|-------------------------------------------------------|
| `docs/assets/logo.svg`         | SkillStack logo (200×60, stacked-rectangles "S" mark) |
| `docs/assets/og-image.svg`     | 1200×630 social preview image                         |
| `docs/assets/skill-cloud.html` | Interactive tag-cloud page (reads `skills.yaml`)      |
| `docs/assets/demo.txt`         | ASCII-art demo of maestro routing 3 sample tasks      |

## 🪶 Lite Versions & Translations

### Lite Versions (for tight context windows)

5 high-traffic skills ship a condensed ~30-line `LITE.md` variant alongside the full `SKILL.md`:

- `style-integrity/coding-conventions-enforcer/LITE.md`
- `style-integrity/latex-style-guard/LITE.md`
- `academic-research/journal-manuscript-writer/LITE.md`
- `ml-engineering/reproducible-experiment-runner/LITE.md`
- `ai-output-judgement/factuality-checker/LITE.md`

Each `LITE.md` has frontmatter with `lite: true` and `full_version: <skill-name>/SKILL.md` — load it for the gist, load
the full version when you need the complete workflow.

### Arabic Translations (10 skills)

`SKILL.ar.md` files for the 10 most central skills (maestro, coding-conventions-enforcer, latex-style-guard,
zero-fabrication-guard, journal-manuscript-writer, research-repo-builder, reproducible-experiment-runner,
hyperparameter-tuner, ai-text-humanizer, factuality-checker). Each has `language: ar` in frontmatter. Section headers
translated; code blocks, paths, and URLs preserved unchanged.

### Chinese Translations (5 skills)

`SKILL.zh.md` files for the 5 most central skills (maestro, coding-conventions-enforcer, latex-style-guard,
reproducible-experiment-runner, factuality-checker). Each has `language: zh` in frontmatter.

## 🧪 Maestro Test Suite

`maestro/test-cases.md` — 50 sample user prompts with their expected routes, covering all 9 themes (≥5 cases each). Use
as a regression check when modifying the maestro's routing logic.

## 🧭 Enhanced Maestro Features

The maestro now supports 4 advanced routing features (see `maestro/SKILL.md`):

| Feature                     | When It Triggers                                                             |
|-----------------------------|------------------------------------------------------------------------------|
| **Multi-Theme Routing**     | Task spans 2+ themes → returns an ordered skill chain                        |
| **Confidence Scoring**      | Multiple skills match → scores top 3 (High ≥0.8 / Medium 0.4-0.8 / Low <0.4) |
| **Fallback Chain**          | First skill's output incomplete → loads next-best match from top 3           |
| **Skill Conflict Resolver** | Two skills seem to apply → 10-row decision tree picks the right one          |

## 📚 Sources & References

These skills consolidate publicly documented best practices from real, verifiable sources. No third-party skill content
is reproduced verbatim — every rule is paraphrased in the author's own words.

### ML & Deep Learning Frameworks

- [Optuna](https://optuna.org) — Bayesian hyperparameter optimization (Akiba et al. 2019, KDD)
- [OptunaHub](https://hub.optuna.com/) — Community algorithms (Ozaki et al. 2026, JMLR)
- [SHAP](https://shap.readthedocs.io) — Model explainability (Lundberg & Lee 2017, NeurIPS; Lundberg et al. 2020, Nature
  Machine Intelligence)
- [Captum](https://captum.ai) — PyTorch model interpretability (Integrated Gradients)
- [PyTorch Lightning](https://lightning.ai) — Lightweight PyTorch wrapper
- [HuggingFace Transformers](https://huggingface.co/docs/transformers) — Pretrained model hub
- [PyTorch](https://pytorch.org) — Distributed training (DDP), AMP, checkpoints
- [torch_lr_finder](https://github.com/davidtvs/pytorch-lr-finder) — LR range test (Smith 2015, arXiv:1506.01186)
- [scikit-learn](https://scikit-learn.org) — Metrics, CV, splitting
- [FastAPI](https://fastapi.tiangolo.com) — Inference API serving

### Experiment Tracking & MLOps

- [MLflow](https://mlflow.org) — Experiment tracking, model registry
- [Weights & Biases](https://wandb.ai) — Experiment tracking, visualizations
- [Hydra](https://hydra.cc) — Config composition (Composable Research)

### Data Engineering

- [pandera](https://pandera.readthedocs.io) — DataFrame schema validation
- [Great Expectations](https://greatexpectations.io) — Data quality testing
- [pydantic](https://docs.pydantic.dev) — Schema enforcement via type hints
- [Feast](https://feast.dev) · [Hopsworks](https://www.hopsworks.ai) · [Tecton](https://www.tecton.ai) — Feature stores
- [Apache Airflow](https://airflow.apache.org) · [Prefect](https://www.prefect.io) · [Dagster](https://dagster.io) · [dbt](https://www.getdbt.com) —
  Orchestration
- [OpenLineage](https://openlineage.io) · [Apache Atlas](https://atlas.apache.org) · [Amundsen](https://www.amundsen.io) —
  Data lineage
- [evidently AI](https://www.evidentlyai.com) · [alibi-detect](https://docs.seldon.io/projects/alibi-detect) — Drift
  detection
- [pyarrow](https://arrow.apache.org/docs/python) — Columnar data (Parquet/Arrow)

### Visualization

- [SciencePlots](https://github.com/garrettj403/SciencePlots) — Matplotlib styles for academic publishing
- [Matplotlib](https://matplotlib.org) · [seaborn](https://seaborn.pydata.org) — Static figures
- [Plotly](https://plotly.com/python) · [Bokeh](https://bokeh.org) · [Holoviews](https://holoviews.org) · [Datashader](https://datashader.org) —
  Interactive plots
- [Streamlit](https://streamlit.io) · [Dash](https://dash.plotly.com) · [Gradio](https://gradio.app) — Dashboards
- [Wong's colorblind palette](https://www.nature.com/articles/nmeth.1618) — Wong 2011, Nature Methods
- [ColorBrewer](https://colorbrewer2.org) — Cartographic color schemes
- [networkx](https://networkx.org) · [pyvis](https://pyvis.readthedocs.io) — Network graphs
- [bertviz](https://github.com/jessevig/bertviz) — Transformer attention visualization

### Writing & Citation

- [Zotero BetterBibTeX](https://retorquere.github.io/zotero-better-bibtex) — BibTeX export for Zotero
- [Crossref REST API](https://www.crossref.org/education/researchers/how-to-use-our-apis/) — DOI verification
- [Semantic Scholar API](https://www.semanticscholar.org/product/api) — Citation networks
- [Connected Papers](https://www.connectedpapers.com) · [Inciteful](https://inciteful.xyz) — Citation graph exploration
- [biblatex](https://ctan.org/pkg/biblatex) — LaTeX bibliography packages (ieee, apa, chicago, vancouver styles)
- [Flesch-Kincaid](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests) · [Gunning Fog](https://en.wikipedia.org/wiki/Gunning_fog_index) · [SMOG](https://en.wikipedia.org/wiki/SMOG) —
  Readability metrics
- Halliday & Hasan, *Cohesion in English* (1976) — Cohesive devices theory
- [CASRAI Hedging Guide](https://casrai.org/guides/hedging-in-academic-writing) — Hedging in academic writing

### AI Text Detection & Watermarking

- [Kirchenbauer et al. 2023](https://arxiv.org/abs/2301.10226) — LLM watermarks
- [Weber-Wulff et al. 2023](https://www.sciencedirect.com/science/article/pii/S2666389923001947) — Testing AI detection
  tools (*Patterns* 4(7))
- [Liang et al. 2023](https://arxiv.org/abs/2304.02819) — GPT detector bias against non-native English writers
- [DetectRL Benchmark](https://arxiv.org/abs/2310.13547) — Adversarial robustness of detectors
- [GPTZero](https://gptzero.me) · [Originality.ai](https://originality.ai) · [Turnitin AI Detection](https://www.turnitin.com/solutions/ai-writing) —
  Commercial detectors

### AI Output Judgement & Evaluation

- [FActScore](https://github.com/shmsw25/FActScore) — Min et al. 2023, EMNLP — fine-grained factuality
- [SAFE](https://github.com/google-deepmind/long-form-factuality) — Google DeepMind 2024 — Search Augmented Factuality
  Evaluator
- [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — Standardized LLM eval
  framework
- [HELM](https://crfm.stanford.edu/helm) — Stanford Holistic Evaluation of Language Models (Liang et al. 2022)
- [OpenAI Evals](https://github.com/openai/evals) — OpenAI eval framework
- [RewardBench](https://github.com/allenai/reward-bench) — Lambert et al. 2024 — reward model evaluation
- [MT-Bench / LLM-as-Judge](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge) — Zheng et al. 2023,
  NeurIPS
- [TruthfulQA](https://github.com/sylinrl/TruthfulQA) — Lin et al. 2022 — hallucination benchmark
- [HumanEval](https://github.com/openai/human-eval) — Chen et al. 2021 — code generation eval
- [SWE-bench](https://github.com/princeton-nlp/SWE-bench) — Jimenez et al. 2024 — real-world software engineering eval
- [JailbreakBench](https://jailbreakbench.github.io) — Chao et al. 2024 — adversarial robustness
- [AdvBench](https://github.com/llm-attacks/llm-attacks) — Zou et al. 2023 — adversarial suffixes
- [Microsoft Presidio](https://microsoft.github.io/presidio/) — PII detection and anonymization
- [spaCy NER](https://spacy.io/usage/linguistic-features#named-entities) — Named entity recognition for PII
- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation) · [Google Perspective API](https://perspectiveapi.com) · [Meta Llama Guard](https://github.com/meta-llama/llama-guard) —
  Safety classifiers
- [Detoxify](https://github.com/unitaryai/detoxify) — Open-source toxicity classifier
- [Sentence-Transformers](https://www.sbert.net) · [MTEB](https://github.com/embeddings-benchmark/mteb) — Embedding
  similarity (relevance, consistency)
- [SummaC](https://github.com/tingofurro/summac) — Laban et al. 2022 — summarization consistency
- [LanguageTool](https://languagetool.org) — Grammar checking for fluency scoring
- [bandit](https://github.com/PyCQA/bandit) · [semgrep](https://semgrep.dev) — Code security scanning
- [Greshake et al. 2023](https://arxiv.org/abs/2302.12173) — Indirect prompt injection
- [Askell et al. 2021](https://arxiv.org/abs/2112.00861) — HHH alignment framework
- [Ji et al. 2023](https://arxiv.org/abs/2202.03629) — Survey of Hallucination (ACM Computing Surveys)
- [Gekhman et al. 2024](https://arxiv.org/abs/2405.05904) — Fine-tuning and hallucination
- [Kryscinski et al. 2020](https://arxiv.org/abs/2010.07100) — Factual consistency of summarization (EMNLP)
- [Bolukbasi et al. 2016](https://arxiv.org/abs/1607.06520) — Word embeddings and gender bias
- [StereoSet](https://github.com/meganlp/StereoSet) — Nadeem et al. 2021 — stereotyping benchmark

### Project Tooling

- [Docker for reproducible research](https://dl.acm.org/doi/10.1145/2723872.2723882) — Boettiger 2015
- [AEA Data Editor Docker Guide](https://aeadataeditor.github.io/posts/2021-11-16-docker) — Docker in economics
- [GitHub Actions](https://docs.github.com/actions) — CI/CD automation
- [pytest](https://docs.pytest.org) — Testing framework
- [Sphinx](https://www.sphinx-doc.org) · [MkDocs Material](https://squidfunk.github.io/mkdocs-material) · [mkdocstrings](https://mkdocstrings.github.io) —
  Documentation
- [Poetry](https://python-poetry.org) · [PDM](https://pdm-project.org) · [pip-tools](https://pip-tools.readthedocs.io) —
  Dependency management
- [pyproject.toml spec](https://packaging.python.org/en/latest/guides/writing-pyproject-toml) — PyPA standard
- [Keep a Changelog](https://keepachangelog.com) — Changelog format
- [Semantic Versioning](https://semver.org) — Version numbering
- [Contributor Covenant](https://www.contributor-covenant.org) — Code of Conduct
- [choosealicense.com](https://choosealicense.com) — License selector
- [pre-commit](https://pre-commit.com) — Pre-commit hooks
- [ruff](https://docs.astral.sh/ruff) · [black](https://black.readthedocs.io) · [mypy](https://mypy.readthedocs.io) —
  Linting/formatting/type-checking

### Research Methodology & Open Science

- [PRISMA 2020](https://www.prisma-statement.org) — Systematic review reporting guideline
- [CASP](https://casp-uk.net) · [AMSTAR-2](https://amstar.ca) · [ROBIS](https://www.robis-tool.info) — Quality appraisal
  tools
- [CONSORT](https://www.consort-statement.org) — RCT reporting guideline
- [COPE](https://publicationethics.org) — Committee on Publication Ethics
- [Open Science Framework (OSF)](https://osf.io) · [AsPredicted](https://aspredicted.org) — Pre-registration
- [Zenodo](https://zenodo.org) · [Figshare](https://figshare.com) · [Dryad](https://datadryad.org) — Data archiving with
  DOI
- [arXiv](https://arxiv.org) · [bioRxiv](https://www.biorxiv.org) · [medRxiv](https://www.medrxiv.org) — Preprint
  servers
- [G*Power](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower) — Sample
  size / power analysis
- [Ioannidis et al.](https://elsevier.digitalcommonsdata.com/datasets/btchxktawy) — Top 2% scientists (
  Stanford/Elsevier)
- [Code review checklist for reproducibility](https://ecoevorxiv.org/repository/view/9055) — Stone-Vlasak et al. 2025
- [Mitchell et al. 2019](https://arxiv.org/abs/1810.03677) — Model Cards (Google) — adapted for dataset cards

### ML/AI Foundational Papers (cited in skills)

- Akiba et al. 2019 — Optuna (KDD)
- Lundberg & Lee 2017 — SHAP (NeurIPS)
- Lundberg et al. 2020 — TreeSHAP (Nature Machine Intelligence)
- Smith 2015 — Cyclical Learning Rates (arXiv:1506.01186)
- Kirchenbauer et al. 2023 — LLM Watermarks (arXiv:2301.10226)
- Weber-Wulff et al. 2023 — Detector reliability testing (*Patterns*)
- Liang et al. 2023 — Detector bias (arXiv:2304.02819)
- Mitchell et al. 2019 — Model Cards (arXiv:1810.03677)
- Boettiger 2015 — Docker for reproducible research (ACM)
- Wong 2011 — Colorblind palette (Nature Methods)

## 📜 License

These skills are written from scratch in the author's own words based on publicly documented best practices. No
third-party skill content is reproduced verbatim. Use under your own project's license.

## 🏷️ GitHub Topics

```
academic-research · machine-learning · reproducible-science · latex ·
pytorch · pytorch-lightning · huggingface · optuna · shap · explainable-ai ·
mlops · data-engineering · etl · data-quality · feature-store · data-lineage ·
visualization · matplotlib · seaborn · tikz · scientific-figures ·
bibtex · citation-management · academic-writing · paraphrasing ·
ai-text-detection · ai-text-humanization · llm-watermark ·
ai-output-judgement · factuality · hallucination-detection · llm-as-judge ·
ai-safety · ai-alignment · bias-audit · prompt-injection · rag-groundedness ·
evaluation-harness · llm-evaluation ·
project-tooling · docker · github-actions · pytest · sphinx ·
agent-skills · skill-repository · maestro-orchestrator
```

## 🔗 Quick Links

| Resource                   | Link                                                                                               |
|----------------------------|----------------------------------------------------------------------------------------------------|
| 🎯 Maestro (load first)    | `maestro/SKILL.md`                                                                                 |
| 📖 This README             | `README.md`                                                                                        |
| 🚀 Quickstart              | `docs/QUICKSTART.md`                                                                               |
| 🍳 Cookbook (20 scenarios) | `docs/COOKBOOK.md`                                                                                 |
| ❓ FAQ                      | `docs/FAQ.md`                                                                                      |
| 📝 Authoring Guide         | `docs/AUTHORING_GUIDE.md`                                                                          |
| 🆚 Comparison              | `docs/COMPARISON.md`                                                                               |
| 📊 Coverage Report         | `docs/coverage.md`                                                                                 |
| 🩺 Health Dashboard        | `docs/health.html`                                                                                 |
| 🕸️ Skill Graph            | `docs/skill-graph.svg`                                                                             |
| 🏷️ Tag Cloud              | `docs/assets/skill-cloud.html`                                                                     |
| 🎨 Logo                    | `docs/assets/logo.svg`                                                                             |
| 🖼️ Social Preview         | `docs/assets/og-image.svg`                                                                         |
| 🧪 Maestro Test Cases      | `maestro/test-cases.md`                                                                            |
| 🔌 MCP Server              | `mcp-server/`                                                                                      |
| 🛠️ Skill CLI              | `python scripts/Skill.py --help`                                                                   |
| 📋 Manifest                | `skills.yaml`                                                                                      |
| 🎓 Academic Research       | `academic-research/README.md`                                                                      |
| 🛡️ Style & Integrity      | `style-integrity/README.md`                                                                        |
| ⚙️ ML Engineering          | `ml-engineering/README.md`                                                                         |
| 🔬 Data Engineering        | `data-engineering/README.md`                                                                       |
| 📊 Visualization           | `visualization/README.md`                                                                          |
| 📝 Writing & Citation      | `writing-citation/README.md`                                                                       |
| 🤖 AI Text                 | `ai-text/README.md`                                                                                |
| 🔍 AI Output Judgement     | `ai-output-judgement/README.md`                                                                    |
| 🧰 Project Tooling         | `project-tooling/README.md`                                                                        |
| 👤 Author CV               | [hossambalaha.github.io](https://hossambalaha.github.io/)                                          |
| 📦 HMB-Helpers Package     | [github.com/HossamBalaha/HMB-Helpers-Package](https://github.com/HossamBalaha/HMB-Helpers-Package) |

## 👤 About the Author

<div align="center">

**Hossam Magdy Balaha** · *Ph.D. Candidate & Graduate Teaching Assistant*

[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--5940--0341-a6ce39?logo=orcid)](https://orcid.org/)
[![Google Scholar](https://img.shields.io/badge/Scholar-H--Index%2029-4285F4?logo=googlescholar&logoColor=white)](https://scholar.google.com/)
[![GitHub](https://img.shields.io/badge/GitHub-hossambalaha-181717?logo=github&logoColor=white)](https://github.com/HossamBalaha)
[![YouTube](https://img.shields.io/badge/YouTube-Courses-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/)
[![CV](https://img.shields.io/badge/CV-Website-000000?logo=aboutdotme&logoColor=white)](https://hossambalaha.github.io/)

</div>

**Affiliation:** Ph.D. Candidate and Graduate Teaching Assistant (GTA) at the Bioengineering Department, J.B. Speed
School of Engineering, University of Louisville, USA. Assistant Lecturer at the Computer Engineering and Control Systems
Department, Faculty of Engineering, Mansoura University, Egypt.

**Research focus:** Medical Image Analysis, Deep Learning, Computer Vision, Radiomics, Explainable AI (XAI), and System
Development — applied to oncology (breast, bladder, prostate, Wilms' tumor) and neurodegenerative disorders (
Parkinson's, AMD).

**Selected recognitions:**

- 🏆 Top 2% Scientists Globally (Stanford/Elsevier, 2025 & 2026)
- 🏆 Top-1000 Scholar (2026 Edition), best world rank Top 0.47% in AI in Cancer Detection
- 🏆 UofL Student Champion (2025-2026)
- 🏆 Outstanding Graduate/Professional Student Award (2025, 2026)
- 🏆 Best Student Paper Award, ICPR 2024 (Track 6)
- 🏆 Graduate Student Inventorship Award (2025) — for the US patent on AI-based cervical vertebral maturation assessment
- 📚 Author of *The AI Starter Kit: From Data to Models with Python* (Amazon KDP, 2025)
- 📦 Creator of the [HMB-Helpers Package](https://github.com/HossamBalaha/HMB-Helpers-Package) (PyPI: `hmb-helpers`) — a
  utility library that inspired several skills in this stack, especially `modular-ml-architect` and
  `coding-conventions-enforcer`
- 📝 50+ peer-reviewed publications in Nature Scientific Reports, IEEE Access, Engineering Applications of Artificial
  Intelligence, Bioengineering, Cancers, Soft Computing, etc.
- 👨‍🏫 Teaches BE 544 (AI Techniques in Digital Histopathology) and BE 645 (AI and Radiomics) at UofL, with all materials
  open-sourced on GitHub and YouTube
- ✉️ Contact: hmbala01@louisville.edu · hossam.m.balaha@mans.edu.eg

## ⚠️ Disclaimers

Read this section in full before loading any skill. By using this repository you accept every clause below.

### 1. Use At Your Own Risk

These skills are provided "as is" without warranty of any kind, express or implied. By loading and applying any skill in
this repository, you assume full responsibility for any and all consequences — including but not limited to:

- 📁 **Files**: Modifications, overwrites, deletions, or corruption of your files, directories, repositories, datasets,
  or system configurations.
- 📝 **Content**: Changes to your manuscripts, code, configurations, citations, generated text, or any other content the
  agent edits on your behalf.
- 🔬 **Results**: Incorrect, fabricated, or misleading outputs produced by automated application of these skills (e.g., a
  metric computed wrong, a citation hallucinated, a figure mislabeled).
- 🧾 **Citations**: Unverified or hallucinated references that may slip past the `zero-fabrication-guard` if the agent
  skips verification steps.
- 🤖 **AI outputs**: Unjudged LLM responses, model predictions, or RAG outputs that pass through without the
  `ai-output-judgement` skills catching a hallucination, bias, or safety issue.
- 💸 **Costs**: API charges, compute bills, or storage costs incurred when skills call external services (LLM APIs,
  Docker registries, cloud compute).

**Always review the agent's changes before committing, publishing, or submitting.** Always keep backups (version
control, snapshots, `git stash`) before running skills against irreplaceable work. The author and contributors of this
stack accept **no liability** for any damage, loss, professional consequences, or financial costs arising from the use
or misuse of these skills.

If a skill produces an unexpected result, **halt**, revert from your backup, and inspect the skill's `SKILL.md` to
understand the intended workflow before retrying. When in doubt, run skills on a throwaway copy first.

### 2. Originality & Similarity To Other Works

Some skills in this repository may **resemble** other public skill collections, prompt templates, style guides, or
best-practice documents in topic, structure, or naming. This is expected: the underlying practices (e.g., "verify DOIs
via Crossref", "use Optuna TPE for Bayesian optimization", "enforce LaTeX float placement") are well-established and
documented in many places. **SkillStack does not claim these practices as its own invention.**

However, every `SKILL.md` in this repository was **written from scratch by the author with the assistance of AI tools (
large language models) and external web searches**. No third-party skill content, prompt text, or documentation was
copied verbatim. Where a skill references a real tool, paper, or framework (e.g., Optuna, SHAP, PyTorch Lightning,
FActScore), that reference is cited by name and URL for the user's convenience; the cited work belongs to its respective
owners.

If you believe any content in this repository infringes your copyright, please open an issue with the specific file path
and the alleged source, and it will be reviewed and addressed promptly.

### 3. AI-Assisted Authorship

This repository was authored with the assistance of AI tools (large language models) and external web searches. The
author directed the AI, reviewed every generated file, and accepted the final content. Despite this review:

- AI may have **hallucinated** facts, URLs, paper titles, or API signatures in skill bodies. Always verify claims
  against primary sources before relying on them.
- AI may have **phrased** things in ways that resemble existing copyrighted text without the author's intent. If you
  spot such a case, open an issue.
- The author is **not a lawyer**; nothing in this repository constitutes legal advice. For copyright, licensing, or
  compliance questions, consult a qualified attorney.

### 4. No Ethical, Academic, Or Professional Guarantee

SkillStack provides tools; it does **not** guarantee:

- 🎓 **Academic integrity**: Using `ai-text-humanizer` to disguise AI-generated text in a graded assignment,
  peer-reviewed manuscript, or grant submission may violate your institution's academic integrity policy. The author
  does not endorse or facilitate academic dishonesty.
- 📜 **Compliance**: Using `data-anonymizer` does not guarantee GDPR, HIPAA, or CCPA compliance. Compliance requires a
  holistic review by a qualified data protection officer or legal counsel.
- 🤖 **AI safety**: Using `ai-output-judgement` skills does not guarantee that an LLM deployment is safe, unbiased, or
  aligned. These skills are aids, not substitutes for a rigorous safety review.
- 🏥 **Clinical, legal, or financial safety**: No skill in this repository provides medical, legal, or financial advice.
  Outputs from these skills must not be used to make clinical, legal, or financial decisions without independent expert
  review.
- 🔬 **Scientific validity**: Using `statistical-validation-rigour` or `reproducible-experiment-runner` does not
  guarantee your study is methodologically sound or its conclusions are correct. These skills enforce procedural
  discipline, not scientific truth.

### 5. No Commercial Warranty & No Endorsement

- SkillStack is **not affiliated with, endorsed by, or sponsored by** any of the tools, papers, or organizations it
  references (Optuna, SHAP, HuggingFace, PyTorch Lightning, Anthropic, OpenAI, Google, Meta, Stanford, etc.). All
  trademarks belong to their respective owners.
- This repository is **free software under the MIT License**. There is **no paid support, no SLA, no warranty of
  merchantability, and no fitness for a particular purpose**. Use it commercially at your own risk.
- The author receives **no revenue** from this repository and has **no commercial relationship** with the cited tools
  unless explicitly stated in a skill's `cost_warning` field.
- If you use SkillStack in a commercial product, you assume all liability for outcomes, including regulatory,
  contractual, and financial consequences.

### 6. Citation & Attribution Expectations

- **Citing SkillStack**: If SkillStack (or any of its skills) materially assisted your research, you are encouraged (but
  not required) to acknowledge it in your manuscript's Acknowledgments section. Suggested wording: *"The authors used
  SkillStack (https://github.com/<user>/skillstack), an open-source skill library by H. M. Balaha, to assist
  with <specific task>."*
- **Citing the underlying tools**: When a skill helped you use a specific tool (e.g., Optuna, SHAP), you must still cite
  that tool's canonical paper per its own citation policy. SkillStack's `References` sections list these canonical
  citations for your convenience.
- **No fabrication**: The `zero-fabrication-guard` and `ai-output-judgement` skills exist to catch hallucinated
  citations, but they are not infallible. You remain responsible for the accuracy of every citation in your published
  work.

### 7. Responsible Use & Misuse

These skills are designed for **legitimate research, education, and engineering work**. The author does not condone
using SkillStack to:

- 🚫 Evade plagiarism detection or AI-text detection for academic dishonesty.
- 🚫 Fabricate data, citations, or results in any publication, grant, or report.
- 🚫 Anonymize data in a way that misleads regulators or violates data subjects' rights.
- 🚫 Generate or distribute malware, disinformation, or harmful content.
- 🚫 Bypass institutional review boards (IRBs), ethical review, or informed consent requirements.
- 🚫 Infringe copyrights, trademarks, or trade secrets.

If you are unsure whether a use case is appropriate, **consult your institution's ethics board, legal counsel, or
compliance officer before proceeding.** When in doubt, do not use the skill.

### 8. Third-Party Service Risks

Several skills call external services (LLM APIs, Crossref, arXiv, HuggingFace Hub, Docker registries, etc.). When you
run such a skill:

- Your data may be **transmitted to third parties**. Review the service's privacy policy and terms of service before
  sending sensitive, confidential, or personal data.
- API keys and credentials may incur **costs**. Check `cost_warning` fields in skill frontmatter and monitor your
  billing dashboards.
- Network-dependent skills may **fail** if a service is down, rate-limits, or changes its API. Always handle failures
  gracefully.
- The author has **no control** over third-party services and accepts no liability for their behavior, outages, data
  handling, or pricing changes.

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
