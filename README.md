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

### 🎓 [`academic-research/`](academic-research/README.md) — Research Planning & Writing

> Plan studies, draft manuscripts, write theses, design grants, review papers, prepare talks.

| #  | Skill                                                                                               | One-Line Description                                                                           | Link                                                           |
|----|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| 1  | [`research-ideation-planner`](academic-research/research-ideation-planner/SKILL.md)                 | Propose 3+ novel research ideas aligned to a target venue, then build an end-to-end blueprint. | `academic-research/research-ideation-planner/SKILL.md`         |
| 2  | [`research-repo-builder`](academic-research/research-repo-builder/SKILL.md)                         | Scaffold a complete modular research repository (src/, configs, manual, datasets.md).          | `academic-research/research-repo-builder/SKILL.md`             |
| 3  | [`journal-manuscript-writer`](academic-research/journal-manuscript-writer/SKILL.md)                 | Draft publication-ready journal sections in LaTeX with strict style rules.                     | `academic-research/journal-manuscript-writer/SKILL.md`         |
| 4  | [`academic-book-author`](academic-research/academic-book-author/SKILL.md)                           | Draft academic book chapters with pedagogical structure and code walkthroughs.                 | `academic-research/academic-book-author/SKILL.md`              |
| 5  | [`grant-proposal-writer`](academic-research/grant-proposal-writer/SKILL.md)                         | Draft competitive grant proposals (specific aims, significance, approach, budget).             | `academic-research/grant-proposal-writer/SKILL.md`             |
| 6  | [`literature-review-synthesizer`](academic-research/literature-review-synthesizer/SKILL.md)         | Build systematic reviews with PICO/SPIDER framing and PRISMA flow.                             | `academic-research/literature-review-synthesizer/SKILL.md`     |
| 7  | [`peer-review-simulator`](academic-research/peer-review-simulator/SKILL.md)                         | Generate peer-review reports and author rebuttal letters.                                      | `academic-research/peer-review-simulator/SKILL.md`             |
| 8  | [`conference-talk-prep`](academic-research/conference-talk-prep/SKILL.md)                           | Draft conference talks with slide outline, notes, and Q&A prep.                                | `academic-research/conference-talk-prep/SKILL.md`              |
| 9  | [`thesis-chapter-planner`](academic-research/thesis-chapter-planner/SKILL.md)                       | Plan thesis/dissertation chapters with cross-chapter non-redundancy.                           | `academic-research/thesis-chapter-planner/SKILL.md`            |
| 10 | [`research-question-formulator`](academic-research/research-question-formulator/SKILL.md)           | Formulate FINER/PICO research questions and hypotheses.                                        | `academic-research/research-question-formulator/SKILL.md`      |
| 11 | [`hypothesis-designer`](academic-research/hypothesis-designer/SKILL.md)                             | Design testable hypotheses with null/alternative and effect-size framing.                      | `academic-research/hypothesis-designer/SKILL.md`               |
| 12 | [`experimental-design-planner`](academic-research/experimental-design-planner/SKILL.md)             | Plan experimental designs (RCT, factorial, crossover) with sample-size calculation.            | `academic-research/experimental-design-planner/SKILL.md`       |
| 13 | [`scope-and-aims-writer`](academic-research/scope-and-aims-writer/SKILL.md)                         | Draft scope, aims, and contribution statements.                                                | `academic-research/scope-and-aims-writer/SKILL.md`             |
| 14 | [`related-work-surveyor`](academic-research/related-work-surveyor/SKILL.md)                         | Survey related work and build thematic comparison tables.                                      | `academic-research/related-work-surveyor/SKILL.md`             |
| 15 | [`citation-network-mapper`](academic-research/citation-network-mapper/SKILL.md)                     | Map citation networks and identify influential/bridge papers.                                  | `academic-research/citation-network-mapper/SKILL.md`           |
| 16 | [`research-portfolio-tracker`](academic-research/research-portfolio-tracker/SKILL.md)               | Track research outputs, deadlines, and submission status.                                      | `academic-research/research-portfolio-tracker/SKILL.md`        |
| 17 | [`open-science-advocate`](academic-research/open-science-advocate/SKILL.md)                         | Apply open-science practices (open data, open code, preprints, OSF).                           | `academic-research/open-science-advocate/SKILL.md`             |
| 18 | [`pre-registration-drafter`](academic-research/pre-registration-drafter/SKILL.md)                   | Draft pre-registration documents (AsPredicted, OSF, Registered Report).                        | `academic-research/pre-registration-drafter/SKILL.md`          |
| 19 | [`reproducibility-checklist-author`](academic-research/reproducibility-checklist-author/SKILL.md)   | Author a reproducibility checklist for a submitted manuscript.                                 | `academic-research/reproducibility-checklist-author/SKILL.md`  |
| 20 | [`supplementary-materials-organizer`](academic-research/supplementary-materials-organizer/SKILL.md) | Organize supplementary materials (appendices, code, data, figures).                            | `academic-research/supplementary-materials-organizer/SKILL.md` |

### 🛡️ [`style-integrity/`](style-integrity/README.md) — LaTeX, Prose & Coding Conventions

> Enforce strict style rules, verify citations, audit notation, execute multi-step tasks with discipline.

| #  | Skill                                                                                           | One-Line Description                                                                                                            | Link                                                        |
|----|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| 1  | [`latex-style-guard`](style-integrity/latex-style-guard/SKILL.md)                               | Enforce LaTeX typography: blank lines around floats, `% ====== %` separators, LaTeX quotes.                                     | `style-integrity/latex-style-guard/SKILL.md`                |
| 2  | [`academic-prose-polisher`](style-integrity/academic-prose-polisher/SKILL.md)                   | Enforce formal prose: banned-vocabulary filter, no em-dashes, no meta-commentary.                                               | `style-integrity/academic-prose-polisher/SKILL.md`          |
| 3  | [`zero-fabrication-guard`](style-integrity/zero-fabrication-guard/SKILL.md)                     | Verify every citation, DOI, URL, dataset name via web search; silent-omit if missing.                                           | `style-integrity/zero-fabrication-guard/SKILL.md`           |
| 4  | [`execution-protocol`](style-integrity/execution-protocol/SKILL.md)                             | 10-stage meta-discipline: Comprehend → Clarify → Define Success → ... → Deliver.                                                | `style-integrity/execution-protocol/SKILL.md`               |
| 5  | [`notation-consistency-checker`](style-integrity/notation-consistency-checker/SKILL.md)         | Audit one-to-one symbol mapping; mandate Nomenclature table if >15 symbols.                                                     | `style-integrity/notation-consistency-checker/SKILL.md`     |
| 6  | [`coding-conventions-enforcer`](style-integrity/coding-conventions-enforcer/SKILL.md)           | Enforce camelCase variables, CamelCase functions/classes/files/dict-keys, parens in `if`, period-ended comments, double quotes. | `style-integrity/coding-conventions-enforcer/SKILL.md`      |
| 7  | [`banned-vocabulary-filter`](style-integrity/banned-vocabulary-filter/SKILL.md)                 | Strip banned LLM-flavored words (delve, tapestry, leverage, paramount, etc.).                                                   | `style-integrity/banned-vocabulary-filter/SKILL.md`         |
| 8  | [`claim-source-tracer`](style-integrity/claim-source-tracer/SKILL.md)                           | Map every factual claim in a manuscript to its source binder/page/quote.                                                        | `style-integrity/claim-source-tracer/SKILL.md`              |
| 9  | [`silent-omission-protocol`](style-integrity/silent-omission-protocol/SKILL.md)                 | Remove jarring `[DECLARATION: ...]` text; relocate to external omission log.                                                    | `style-integrity/silent-omission-protocol/SKILL.md`         |
| 10 | [`planning-note-logger`](style-integrity/planning-note-logger/SKILL.md)                         | Append a "Planning Note" listing data still needed for the task.                                                                | `style-integrity/planning-note-logger/SKILL.md`             |
| 11 | [`cross-reference-validator`](style-integrity/cross-reference-validator/SKILL.md)               | Verify every `\ref{}` and `\label{}` resolves and every float is referenced.                                                    | `style-integrity/cross-reference-validator/SKILL.md`        |
| 12 | [`abbreviation-consistency-checker`](style-integrity/abbreviation-consistency-checker/SKILL.md) | Define abbreviations once at first use; enforce consistency thereafter.                                                         | `style-integrity/abbreviation-consistency-checker/SKILL.md` |
| 13 | [`numerical-value-formatter`](style-integrity/numerical-value-formatter/SKILL.md)               | Wrap standalone numbers in `\ineq{}` and apply PIP/en-dash replacements.                                                        | `style-integrity/numerical-value-formatter/SKILL.md`        |
| 14 | [`math-symbol-auditor`](style-integrity/math-symbol-auditor/SKILL.md)                           | Audit math symbols: no reuse, consistent notation, defined in nomenclature.                                                     | `style-integrity/math-symbol-auditor/SKILL.md`              |
| 15 | [`passive-voice-detector`](style-integrity/passive-voice-detector/SKILL.md)                     | Detect passive voice and suggest active alternatives.                                                                           | `style-integrity/passive-voice-detector/SKILL.md`           |
| 16 | [`em-dash-eliminator`](style-integrity/em-dash-eliminator/SKILL.md)                             | Replace em-dashes with standard punctuation or en-dashes.                                                                       | `style-integrity/em-dash-eliminator/SKILL.md`               |
| 17 | [`meta-commentary-stripper`](style-integrity/meta-commentary-stripper/SKILL.md)                 | Remove "In this section we will show" / "The reader will learn" patterns.                                                       | `style-integrity/meta-commentary-stripper/SKILL.md`         |
| 18 | [`voice-matching-guard`](style-integrity/voice-matching-guard/SKILL.md)                         | Match author voice sample if provided; override generic rules.                                                                  | `style-integrity/voice-matching-guard/SKILL.md`             |

### ⚙️ [`ml-engineering/`](ml-engineering/README.md) — PyTorch, Training & Validation

> Build, train, tune, explain, and validate ML models in PyTorch/Lightning/HuggingFace.

| #  | Skill                                                                                      | One-Line Description                                                                     | Link                                                     |
|----|--------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 1  | [`modular-ml-architect`](ml-engineering/modular-ml-architect/SKILL.md)                     | Enforce modular Python conventions: 2-space indent, CamelCase, period-ended comments.    | `ml-engineering/modular-ml-architect/SKILL.md`           |
| 2  | [`reproducible-experiment-runner`](ml-engineering/reproducible-experiment-runner/SKILL.md) | Setup reproducible experiments: device resolution, seeds, dual logging, 4-split folders. | `ml-engineering/reproducible-experiment-runner/SKILL.md` |
| 3  | [`data-leakage-guard`](ml-engineering/data-leakage-guard/SKILL.md)                         | Enforce train/val/test isolation; fit preprocessing on train only.                       | `ml-engineering/data-leakage-guard/SKILL.md`             |
| 4  | [`statistical-validation-rigour`](ml-engineering/statistical-validation-rigour/SKILL.md)   | Bootstrap CIs, paired t-test/Wilcoxon/McNemar, AUC branching.                            | `ml-engineering/statistical-validation-rigour/SKILL.md`  |
| 5  | [`hyperparameter-tuner`](ml-engineering/hyperparameter-tuner/SKILL.md)                     | Optuna Bayesian optimization (TPE, median pruner, multi-fidelity).                       | `ml-engineering/hyperparameter-tuner/SKILL.md`           |
| 6  | [`model-explainer`](ml-engineering/model-explainer/SKILL.md)                               | SHAP/LIME/Integrated-Gradients explanations and plots.                                   | `ml-engineering/model-explainer/SKILL.md`                |
| 7  | [`pytorch-lightning-scaffold`](ml-engineering/pytorch-lightning-scaffold/SKILL.md)         | Scaffold LightningModule, DataModule, Callbacks, Loggers.                                | `ml-engineering/pytorch-lightning-scaffold/SKILL.md`     |
| 8  | [`transformer-finetuner`](ml-engineering/transformer-finetuner/SKILL.md)                   | Fine-tune Hugging Face transformers with Trainer/PEFT.                                   | `ml-engineering/transformer-finetuner/SKILL.md`          |
| 9  | [`dataset-adapter-builder`](ml-engineering/dataset-adapter-builder/SKILL.md)               | Defensive dataset adapters with actionable FileNotFoundError.                            | `ml-engineering/dataset-adapter-builder/SKILL.md`        |
| 10 | [`seed-and-device-resolver`](ml-engineering/seed-and-device-resolver/SKILL.md)             | Resolve `torch.device` once and `.to(device)` on every nn.Module.                        | `ml-engineering/seed-and-device-resolver/SKILL.md`       |
| 11 | [`experiment-folder-organizer`](ml-engineering/experiment-folder-organizer/SKILL.md)       | Single timestamped experiment folder; 4 split subfolders (Train/Val/Test/Aggregated).    | `ml-engineering/experiment-folder-organizer/SKILL.md`    |
| 12 | [`train-val-test-splitter`](ml-engineering/train-val-test-splitter/SKILL.md)               | Stratified splitting at highest hierarchical level.                                      | `ml-engineering/train-val-test-splitter/SKILL.md`        |
| 13 | [`early-stopping-configurator`](ml-engineering/early-stopping-configurator/SKILL.md)       | Configure early stopping with patience, mode, delta.                                     | `ml-engineering/early-stopping-configurator/SKILL.md`    |
| 14 | [`learning-rate-finder`](ml-engineering/learning-rate-finder/SKILL.md)                     | Run LR range test (Smith 2015) and plot loss-vs-LR.                                      | `ml-engineering/learning-rate-finder/SKILL.md`           |
| 15 | [`mixed-precision-trainer`](ml-engineering/mixed-precision-trainer/SKILL.md)               | AMP autocast + GradScaler for fp16/bf16 training.                                        | `ml-engineering/mixed-precision-trainer/SKILL.md`        |
| 16 | [`distributed-training-setup`](ml-engineering/distributed-training-setup/SKILL.md)         | DDP setup with `torchrun`, `find_unused_parameters`, world-size.                         | `ml-engineering/distributed-training-setup/SKILL.md`     |
| 17 | [`model-checkpoint-manager`](ml-engineering/model-checkpoint-manager/SKILL.md)             | Save/load checkpoints with epoch, val-metric, optimizer state.                           | `ml-engineering/model-checkpoint-manager/SKILL.md`       |
| 18 | [`inference-pipeline-builder`](ml-engineering/inference-pipeline-builder/SKILL.md)         | Build FastAPI inference endpoint with pre/post-processing.                               | `ml-engineering/inference-pipeline-builder/SKILL.md`     |
| 19 | [`baseline-model-zoo`](ml-engineering/baseline-model-zoo/SKILL.md)                         | Implement baseline models (LR, RF, XGBoost, MLP) for comparison.                         | `ml-engineering/baseline-model-zoo/SKILL.md`             |
| 20 | [`ablation-study-runner`](ml-engineering/ablation-study-runner/SKILL.md)                   | Run ablations by removing/altering components systematically.                            | `ml-engineering/ablation-study-runner/SKILL.md`          |
| 21 | [`cross-validation-engine`](ml-engineering/cross-validation-engine/SKILL.md)               | k-fold, stratified, grouped, and time-series cross-validation.                           | `ml-engineering/cross-validation-engine/SKILL.md`        |
| 22 | [`metrics-computation-suite`](ml-engineering/metrics-computation-suite/SKILL.md)           | Accuracy, F1, AUC, MCC, Cohen's kappa, calibration error.                                | `ml-engineering/metrics-computation-suite/SKILL.md`      |

### 🔬 [`data-engineering/`](data-engineering/README.md) — ETL, Schemas & Lineage

> Build robust data pipelines, enforce schemas, anonymize PII, track lineage.

| #  | Skill                                                                                  | One-Line Description                                                     | Link                                                    |
|----|----------------------------------------------------------------------------------------|--------------------------------------------------------------------------|---------------------------------------------------------|
| 1  | [`etl-pipeline-builder`](data-engineering/etl-pipeline-builder/SKILL.md)               | Idempotent ETL with extract-validate-transform-load and audit trail.     | `data-engineering/etl-pipeline-builder/SKILL.md`        |
| 2  | [`feature-store-recipe`](data-engineering/feature-store-recipe/SKILL.md)               | Feature engineering with point-in-time correctness and freshness checks. | `data-engineering/feature-store-recipe/SKILL.md`        |
| 3  | [`data-quality-validator`](data-engineering/data-quality-validator/SKILL.md)           | Validate with pandera/great-expectations; null/duplicate/outlier checks. | `data-engineering/data-quality-validator/SKILL.md`      |
| 4  | [`csv-json-converter`](data-engineering/csv-json-converter/SKILL.md)                   | Convert between CSV/JSON/Parquet/Arrow with type preservation.           | `data-engineering/csv-json-converter/SKILL.md`          |
| 5  | [`dataset-card-generator`](data-engineering/dataset-card-generator/SKILL.md)           | Generate dataset cards: provenance, license, composition, intended use.  | `data-engineering/dataset-card-generator/SKILL.md`      |
| 6  | [`data-schema-enforcer`](data-engineering/data-schema-enforcer/SKILL.md)               | Enforce schema with pydantic models or pandera DataFrameSchemas.         | `data-engineering/data-schema-enforcer/SKILL.md`        |
| 7  | [`incremental-loader`](data-engineering/incremental-loader/SKILL.md)                   | Load incrementally with stateful checkpoints and idempotent re-runs.     | `data-engineering/incremental-loader/SKILL.md`          |
| 8  | [`data-anonymizer`](data-engineering/data-anonymizer/SKILL.md)                         | Anonymize PII: hashing, k-anonymity, generalization, suppression.        | `data-engineering/data-anonymizer/SKILL.md`             |
| 9  | [`time-series-resampler`](data-engineering/time-series-resampler/SKILL.md)             | Resample time series with forward/backward fill and alignment.           | `data-engineering/time-series-resampler/SKILL.md`       |
| 10 | [`missing-data-imputer`](data-engineering/missing-data-imputer/SKILL.md)               | Impute missing data: mean/median/KNN/iterative/MICE.                     | `data-engineering/missing-data-imputer/SKILL.md`        |
| 11 | [`outlier-detector`](data-engineering/outlier-detector/SKILL.md)                       | Detect outliers: IQR, z-score, isolation forest, DBSCAN.                 | `data-engineering/outlier-detector/SKILL.md`            |
| 12 | [`data-drift-monitor`](data-engineering/data-drift-monitor/SKILL.md)                   | Monitor data drift: PSI, KS test, Wasserstein distance.                  | `data-engineering/data-drift-monitor/SKILL.md`          |
| 13 | [`feature-engineering-toolkit`](data-engineering/feature-engineering-toolkit/SKILL.md) | Build features: polynomial, binning, target encoding, interactions.      | `data-engineering/feature-engineering-toolkit/SKILL.md` |
| 14 | [`categorical-encoder`](data-engineering/categorical-encoder/SKILL.md)                 | Encode categoricals: one-hot, ordinal, target, hash, embedding.          | `data-engineering/categorical-encoder/SKILL.md`         |
| 15 | [`text-preprocessor`](data-engineering/text-preprocessor/SKILL.md)                     | Preprocess text: tokenize, lowercase, lemmatize, stopword removal.       | `data-engineering/text-preprocessor/SKILL.md`           |
| 16 | [`image-dataset-loader`](data-engineering/image-dataset-loader/SKILL.md)               | Load image datasets with augmentation, batching, and prefetch.           | `data-engineering/image-dataset-loader/SKILL.md`        |
| 17 | [`tabular-data-sampler`](data-engineering/tabular-data-sampler/SKILL.md)               | Sample tabular data: random, stratified, weighted, reservoir.            | `data-engineering/tabular-data-sampler/SKILL.md`        |
| 18 | [`data-lineage-tracker`](data-engineering/data-lineage-tracker/SKILL.md)               | Track data lineage: source → transform → sink with provenance graph.     | `data-engineering/data-lineage-tracker/SKILL.md`        |

### 📊 [`visualization/`](visualization/README.md) — Figures, TikZ & Posters

> Generate publication-ready figures, TikZ diagrams, A0 posters, results tables, dashboards.

| #  | Skill                                                                               | One-Line Description                                                    | Link                                                 |
|----|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------|------------------------------------------------------|
| 1  | [`publication-figure-maker`](visualization/publication-figure-maker/SKILL.md)       | Journal-ready matplotlib figures with correct sizes and vector formats. | `visualization/publication-figure-maker/SKILL.md`    |
| 2  | [`academic-plotting-pipeline`](visualization/academic-plotting-pipeline/SKILL.md)   | Two-track: image-gen diagrams + matplotlib data figures.                | `visualization/academic-plotting-pipeline/SKILL.md`  |
| 3  | [`tikz-framework-diagrammer`](visualization/tikz-framework-diagrammer/SKILL.md)     | TikZ pipeline diagrams: concise nodes, solid groups, resizebox.         | `visualization/tikz-framework-diagrammer/SKILL.md`   |
| 4  | [`scientific-poster-designer`](visualization/scientific-poster-designer/SKILL.md)   | A0 posters (841×1189mm), IMRAD layout, 1m readability.                  | `visualization/scientific-poster-designer/SKILL.md`  |
| 5  | [`results-table-formatter`](visualization/results-table-formatter/SKILL.md)         | booktabs tables with multi-row headers and 95% CI columns.              | `visualization/results-table-formatter/SKILL.md`     |
| 6  | [`infographic-summarizer`](visualization/infographic-summarizer/SKILL.md)           | Single-page infographics with visual hierarchy.                         | `visualization/infographic-summarizer/SKILL.md`      |
| 7  | [`confusion-matrix-plotter`](visualization/confusion-matrix-plotter/SKILL.md)       | Plot confusion matrix with normalized + raw counts.                     | `visualization/confusion-matrix-plotter/SKILL.md`    |
| 8  | [`roc-pr-curve-plotter`](visualization/roc-pr-curve-plotter/SKILL.md)               | ROC and PR curves with AUC and baseline references.                     | `visualization/roc-pr-curve-plotter/SKILL.md`        |
| 9  | [`training-curve-visualizer`](visualization/training-curve-visualizer/SKILL.md)     | Plot train/val loss and accuracy over epochs.                           | `visualization/training-curve-visualizer/SKILL.md`   |
| 10 | [`attention-map-visualizer`](visualization/attention-map-visualizer/SKILL.md)       | Visualize transformer attention weights as heatmaps.                    | `visualization/attention-map-visualizer/SKILL.md`    |
| 11 | [`embedding-projector`](visualization/embedding-projector/SKILL.md)                 | Project high-dim embeddings via PCA/t-SNE/UMAP.                         | `visualization/embedding-projector/SKILL.md`         |
| 12 | [`dashboard-builder`](visualization/dashboard-builder/SKILL.md)                     | Build interactive dashboards (Streamlit, Dash, Gradio).                 | `visualization/dashboard-builder/SKILL.md`           |
| 13 | [`interactive-plot-builder`](visualization/interactive-plot-builder/SKILL.md)       | Interactive plots with Plotly/Bokeh/Holoviews.                          | `visualization/interactive-plot-builder/SKILL.md`    |
| 14 | [`color-palette-selector`](visualization/color-palette-selector/SKILL.md)           | Select colorblind-friendly palettes (viridis, cividis, colorbrewer).    | `visualization/color-palette-selector/SKILL.md`      |
| 15 | [`figure-caption-writer`](visualization/figure-caption-writer/SKILL.md)             | Write detailed captions: what / how / why.                              | `visualization/figure-caption-writer/SKILL.md`       |
| 16 | [`multi-panel-figure-composer`](visualization/multi-panel-figure-composer/SKILL.md) | Compose multi-panel figures with subplots and shared axes.              | `visualization/multi-panel-figure-composer/SKILL.md` |
| 17 | [`surface-plotter`](visualization/surface-plotter/SKILL.md)                         | 3D surface plots with proper view angles and colorbars.                 | `visualization/surface-plotter/SKILL.md`             |
| 18 | [`network-graph-visualizer`](visualization/network-graph-visualizer/SKILL.md)       | Visualize network graphs with layout algorithms.                        | `visualization/network-graph-visualizer/SKILL.md`    |

### 📝 [`writing-citation/`](writing-citation/README.md) — BibTeX, Editing & Paraphrasing

> Manage citations, draft abstracts, edit non-native English, paraphrase safely.

| #  | Skill                                                                                        | One-Line Description                                                   | Link                                                       |
|----|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------|
| 1  | [`bibtex-citation-manager`](writing-citation/bibtex-citation-manager/SKILL.md)               | Manage BibTeX: citekeys, dedup, field validation, every bibitem cited. | `writing-citation/bibtex-citation-manager/SKILL.md`        |
| 2  | [`structured-abstract-writer`](writing-citation/structured-abstract-writer/SKILL.md)         | Draft structured abstracts (Background/Methods/Results/Conclusion).    | `writing-citation/structured-abstract-writer/SKILL.md`     |
| 3  | [`imrad-thesis-writer`](writing-citation/imrad-thesis-writer/SKILL.md)                       | Draft full IMRaD theses with non-redundant cross-references.           | `writing-citation/imrad-thesis-writer/SKILL.md`            |
| 4  | [`research-methodology-designer`](writing-citation/research-methodology-designer/SKILL.md)   | Design methodologies: study design, sampling, sample size, ethics.     | `writing-citation/research-methodology-designer/SKILL.md`  |
| 5  | [`english-academic-editor`](writing-citation/english-academic-editor/SKILL.md)               | Edit non-native English: articles, tense, hedging, register.           | `writing-citation/english-academic-editor/SKILL.md`        |
| 6  | [`plagiarism-paraphraser`](writing-citation/plagiarism-paraphraser/SKILL.md)                 | Rewrite to avoid plagiarism while preserving meaning.                  | `writing-citation/plagiarism-paraphraser/SKILL.md`         |
| 7  | [`zotero-better-bibtex-bridge`](writing-citation/zotero-better-bibtex-bridge/SKILL.md)       | Bridge Zotero BetterBibTeX exports to LaTeX workflows.                 | `writing-citation/zotero-better-bibtex-bridge/SKILL.md`    |
| 8  | [`citation-style-converter`](writing-citation/citation-style-converter/SKILL.md)             | Convert between IEEE, APA, Chicago, Vancouver, MLA.                    | `writing-citation/citation-style-converter/SKILL.md`       |
| 9  | [`doi-verifier`](writing-citation/doi-verifier/SKILL.md)                                     | Verify DOIs resolve to the claimed paper via crossref.org.             | `writing-citation/doi-verifier/SKILL.md`                   |
| 10 | [`reference-list-formatter`](writing-citation/reference-list-formatter/SKILL.md)             | Format reference lists in any citation style.                          | `writing-citation/reference-list-formatter/SKILL.md`       |
| 11 | [`annotated-bibliography-builder`](writing-citation/annotated-bibliography-builder/SKILL.md) | Build annotated bibliographies with summary and assessment.            | `writing-citation/annotated-bibliography-builder/SKILL.md` |
| 12 | [`literature-matrix-builder`](writing-citation/literature-matrix-builder/SKILL.md)           | Build a literature matrix (paper × dimension) for synthesis.           | `writing-citation/literature-matrix-builder/SKILL.md`      |
| 13 | [`outline-to-prose-expander`](writing-citation/outline-to-prose-expander/SKILL.md)           | Expand a bullet outline into flowing academic prose.                   | `writing-citation/outline-to-prose-expander/SKILL.md`      |
| 14 | [`paragraph-transition-smoother`](writing-citation/paragraph-transition-smoother/SKILL.md)   | Smooth paragraph transitions with logical connectors.                  | `writing-citation/paragraph-transition-smoother/SKILL.md`  |
| 15 | [`tense-consistency-fixer`](writing-citation/tense-consistency-fixer/SKILL.md)               | Fix tense: past for methods/results, present for discussion.           | `writing-citation/tense-consistency-fixer/SKILL.md`        |
| 16 | [`hedging-language-balancer`](writing-citation/hedging-language-balancer/SKILL.md)           | Balance hedging (modal verbs, adverbs) to match evidence strength.     | `writing-citation/hedging-language-balancer/SKILL.md`      |
| 17 | [`cohesive-device-checker`](writing-citation/cohesive-device-checker/SKILL.md)               | Check cohesive devices: reference, conjunction, lexical.               | `writing-citation/cohesive-device-checker/SKILL.md`        |
| 18 | [`reading-level-adjuster`](writing-citation/reading-level-adjuster/SKILL.md)                 | Adjust reading level to target grade (Flesch-Kincaid).                 | `writing-citation/reading-level-adjuster/SKILL.md`         |

### 🤖 [`ai-text/`](ai-text/README.md) — Detect & Humanize AI Text

> Detect AI-generated text, restore natural voice, verify citations, detect watermarks.

| #  | Skill                                                                                 | One-Line Description                                          | Link                                               |
|----|---------------------------------------------------------------------------------------|---------------------------------------------------------------|----------------------------------------------------|
| 1  | [`ai-text-detector`](ai-text/ai-text-detector/SKILL.md)                               | Detect AI text using 6-category tells with S1-S4 severity.    | `ai-text/ai-text-detector/SKILL.md`                |
| 2  | [`ai-text-humanizer`](ai-text/ai-text-humanizer/SKILL.md)                             | Rewrite AI text to restore natural voice, preserving facts.   | `ai-text/ai-text-humanizer/SKILL.md`               |
| 3  | [`perplexity-burstiness-scorer`](ai-text/perplexity-burstiness-scorer/SKILL.md)       | Compute perplexity and burstiness statistics for a text.      | `ai-text/perplexity-burstiness-scorer/SKILL.md`    |
| 4  | [`ai-tell-catalogue`](ai-text/ai-tell-catalogue/SKILL.md)                             | Reference catalogue of 26 AI tells organized by category.     | `ai-text/ai-tell-catalogue/SKILL.md`               |
| 5  | [`severity-classifier`](ai-text/severity-classifier/SKILL.md)                         | Classify detected tells into S1/S2/S3/S4 severity.            | `ai-text/severity-classifier/SKILL.md`             |
| 6  | [`voice-profile-matcher`](ai-text/voice-profile-matcher/SKILL.md)                     | Match a target author voice profile (vocabulary, rhythm).     | `ai-text/voice-profile-matcher/SKILL.md`           |
| 7  | [`chatbot-residue-cleaner`](ai-text/chatbot-residue-cleaner/SKILL.md)                 | Remove "I hope this helps", "Great question!" residue.        | `ai-text/chatbot-residue-cleaner/SKILL.md`         |
| 8  | [`inflation-stripper`](ai-text/inflation-stripper/SKILL.md)                           | Remove inflated significance ("pivotal moment", "testament"). | `ai-text/inflation-stripper/SKILL.md`              |
| 9  | [`staging-tell-remover`](ai-text/staging-tell-remover/SKILL.md)                       | Remove staging tells ("Not X but Y", one-line closers).       | `ai-text/staging-tell-remover/SKILL.md`            |
| 10 | [`rhythm-by-rule-fixer`](ai-text/rhythm-by-rule-fixer/SKILL.md)                       | Fix forced triads, repeated openings, dashes-as-connectors.   | `ai-text/rhythm-by-rule-fixer/SKILL.md`            |
| 11 | [`formatting-by-rule-cleaner`](ai-text/formatting-by-rule-cleaner/SKILL.md)           | Clean decorative bold, title-case headings, curly quotes.     | `ai-text/formatting-by-rule-cleaner/SKILL.md`      |
| 12 | [`citation-hallucination-detector`](ai-text/citation-hallucination-detector/SKILL.md) | Detect fake DOIs, phantom citations, fake outlets.            | `ai-text/citation-hallucination-detector/SKILL.md` |
| 13 | [`grace-degradation-protocol`](ai-text/grace-degradation-protocol/SKILL.md)           | When a fact can't be verified, omit or `[Verify Source]`.     | `ai-text/grace-degradation-protocol/SKILL.md`      |
| 14 | [`ai-watermark-detector`](ai-text/ai-watermark-detector/SKILL.md)                     | Detect LLM watermarks (Kirchenbauer et al. 2023).             | `ai-text/ai-watermark-detector/SKILL.md`           |
| 15 | [`multi-engine-verification`](ai-text/multi-engine-verification/SKILL.md)             | Cross-reference outputs across GPTZero, Originality.ai, etc.  | `ai-text/multi-engine-verification/SKILL.md`       |

### 🔍 [`ai-output-judgement/`](ai-output-judgement/README.md) — Judge & Verify AI Outputs

> Evaluate AI outputs for factuality, hallucination, bias, safety, groundedness, faithfulness, and correctness. Build
> evaluation harnesses.

| #  | Skill                                                                                   | One-Line Description                                                                   | Link                                                      |
|----|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------------|
| 1  | [`factuality-checker`](ai-output-judgement/factuality-checker/SKILL.md)                 | Verify factual claims in AI outputs against trusted sources (FActScore, SAFE).         | `ai-output-judgement/factuality-checker/SKILL.md`         |
| 2  | [`hallucination-detector`](ai-output-judgement/hallucination-detector/SKILL.md)         | Detect hallucinated content: fabricated entities, fake citations, invented statistics. | `ai-output-judgement/hallucination-detector/SKILL.md`     |
| 3  | [`llm-as-judge-evaluator`](ai-output-judgement/llm-as-judge-evaluator/SKILL.md)         | Implement LLM-as-judge with rubrics, bias mitigation, inter-judge agreement.           | `ai-output-judgement/llm-as-judge-evaluator/SKILL.md`     |
| 4  | [`response-quality-scorer`](ai-output-judgement/response-quality-scorer/SKILL.md)       | Score responses on helpfulness, completeness, relevance, clarity, depth (1-5).         | `ai-output-judgement/response-quality-scorer/SKILL.md`    |
| 5  | [`bias-auditor`](ai-output-judgement/bias-auditor/SKILL.md)                             | Audit outputs for demographic/cognitive bias via counterfactual prompts.               | `ai-output-judgement/bias-auditor/SKILL.md`               |
| 6  | [`safety-classifier`](ai-output-judgement/safety-classifier/SKILL.md)                   | Classify outputs for violence, hate, sexual, self-harm, illegal content.               | `ai-output-judgement/safety-classifier/SKILL.md`          |
| 7  | [`groundedness-verifier`](ai-output-judgement/groundedness-verifier/SKILL.md)           | Verify RAG outputs are grounded in retrieved context via NLI models.                   | `ai-output-judgement/groundedness-verifier/SKILL.md`      |
| 8  | [`consistency-checker`](ai-output-judgement/consistency-checker/SKILL.md)               | Check consistency across temperature, paraphrased inputs, multiple samples.            | `ai-output-judgement/consistency-checker/SKILL.md`        |
| 9  | [`faithfulness-scorer`](ai-output-judgement/faithfulness-scorer/SKILL.md)               | Score summarization/QA faithfulness to source (NLI, QAGS, SummaC).                     | `ai-output-judgement/faithfulness-scorer/SKILL.md`        |
| 10 | [`relevance-scorer`](ai-output-judgement/relevance-scorer/SKILL.md)                     | Score relevance to query via semantic similarity and intent matching.                  | `ai-output-judgement/relevance-scorer/SKILL.md`           |
| 11 | [`coherence-fluency-scorer`](ai-output-judgement/coherence-fluency-scorer/SKILL.md)     | Score coherence, fluency, grammaticality via perplexity and LanguageTool.              | `ai-output-judgement/coherence-fluency-scorer/SKILL.md`   |
| 12 | [`pii-leak-detector`](ai-output-judgement/pii-leak-detector/SKILL.md)                   | Detect PII leakage (emails, phones, SSNs, names) via Presidio + spaCy NER.             | `ai-output-judgement/pii-leak-detector/SKILL.md`          |
| 13 | [`prompt-injection-detector`](ai-output-judgement/prompt-injection-detector/SKILL.md)   | Detect direct and indirect prompt injection attacks.                                   | `ai-output-judgement/prompt-injection-detector/SKILL.md`  |
| 14 | [`alignment-evaluator`](ai-output-judgement/alignment-evaluator/SKILL.md)               | Evaluate alignment with HHH framework (Helpful, Honest, Harmless).                     | `ai-output-judgement/alignment-evaluator/SKILL.md`        |
| 15 | [`reference-accuracy-checker`](ai-output-judgement/reference-accuracy-checker/SKILL.md) | Verify AI-generated references resolve to real papers (Crossref, Semantic Scholar).    | `ai-output-judgement/reference-accuracy-checker/SKILL.md` |
| 16 | [`numeric-accuracy-verifier`](ai-output-judgement/numeric-accuracy-verifier/SKILL.md)   | Verify numeric computations, statistics, dates, quantities in outputs.                 | `ai-output-judgement/numeric-accuracy-verifier/SKILL.md`  |
| 17 | [`code-output-validator`](ai-output-judgement/code-output-validator/SKILL.md)           | Validate AI-generated code: syntax, execution, tests, spec match, security.            | `ai-output-judgement/code-output-validator/SKILL.md`      |
| 18 | [`evaluation-harness-builder`](ai-output-judgement/evaluation-harness-builder/SKILL.md) | Build eval harnesses (lm-eval-harness, HELM, OpenAI Evals style).                      | `ai-output-judgement/evaluation-harness-builder/SKILL.md` |

### 🧰 [`project-tooling/`](project-tooling/README.md) — Packaging, Docker & CI/CD

> Bundle, containerize, automate, test, document, and release research projects.

| #  | Skill                                                                                 | One-Line Description                                                      | Link                                                   |
|----|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------|--------------------------------------------------------|
| 1  | [`project-zip-packager`](project-tooling/project-zip-packager/SKILL.md)               | Bundle repo into zip excluding `*.zip`, `Datasets/`, `results/`, `.git/`. | `project-tooling/project-zip-packager/SKILL.md`        |
| 2  | [`requirements-pinner`](project-tooling/requirements-pinner/SKILL.md)                 | Generate unversioned Requirements.txt or pinned requirements.lock.        | `project-tooling/requirements-pinner/SKILL.md`         |
| 3  | [`pyproject-toml-builder`](project-tooling/pyproject-toml-builder/SKILL.md)           | Build pyproject.toml with Poetry/PDM/setuptools config.                   | `project-tooling/pyproject-toml-builder/SKILL.md`      |
| 4  | [`docker-research-container`](project-tooling/docker-research-container/SKILL.md)     | Build Dockerfile for reproducible research (non-root, multi-stage).       | `project-tooling/docker-research-container/SKILL.md`   |
| 5  | [`github-actions-research-ci`](project-tooling/github-actions-research-ci/SKILL.md)   | Build GitHub Actions: install → lint → test → docs → docker push.         | `project-tooling/github-actions-research-ci/SKILL.md`  |
| 6  | [`pytest-scientific-suite`](project-tooling/pytest-scientific-suite/SKILL.md)         | Write pytest tests with fixtures, parametrize, deterministic seeds.       | `project-tooling/pytest-scientific-suite/SKILL.md`     |
| 7  | [`sphinx-docs-builder`](project-tooling/sphinx-docs-builder/SKILL.md)                 | Build Sphinx/MkDocs docs with autodoc and tutorials.                      | `project-tooling/sphinx-docs-builder/SKILL.md`         |
| 8  | [`readme-generator`](project-tooling/readme-generator/SKILL.md)                       | Generate README.md with hook, what/why, quick-start, real examples.       | `project-tooling/readme-generator/SKILL.md`            |
| 9  | [`jupyter-to-script-converter`](project-tooling/jupyter-to-script-converter/SKILL.md) | Convert .ipynb to clean .py with functions and `__main__`.                | `project-tooling/jupyter-to-script-converter/SKILL.md` |
| 10 | [`gitignore-builder`](project-tooling/gitignore-builder/SKILL.md)                     | Generate .gitignore for Python/Node/R/Data/IDE-specific patterns.         | `project-tooling/gitignore-builder/SKILL.md`           |
| 11 | [`license-selector`](project-tooling/license-selector/SKILL.md)                       | Select MIT/Apache-2.0/GPL-3.0/AGPL/BSD based on use case.                 | `project-tooling/license-selector/SKILL.md`            |
| 12 | [`changelog-writer`](project-tooling/changelog-writer/SKILL.md)                       | Write Keep-a-Changelog format entries with semver bumps.                  | `project-tooling/changelog-writer/SKILL.md`            |
| 13 | [`contribution-guide-builder`](project-tooling/contribution-guide-builder/SKILL.md)   | Build CONTRIBUTING.md with workflow, style, PR template.                  | `project-tooling/contribution-guide-builder/SKILL.md`  |
| 14 | [`code-of-conduct-generator`](project-tooling/code-of-conduct-generator/SKILL.md)     | Generate Contributor Covenant Code of Conduct.                            | `project-tooling/code-of-conduct-generator/SKILL.md`   |
| 15 | [`issue-template-builder`](project-tooling/issue-template-builder/SKILL.md)           | Build bug/feature/question issue templates with YAML frontmatter.         | `project-tooling/issue-template-builder/SKILL.md`      |
| 16 | [`pr-template-builder`](project-tooling/pr-template-builder/SKILL.md)                 | Build PR template with checklist, summary, testing, breaking changes.     | `project-tooling/pr-template-builder/SKILL.md`         |
| 17 | [`environment-yaml-builder`](project-tooling/environment-yaml-builder/SKILL.md)       | Build environment.yml (conda) or Pipfile for reproducible envs.           | `project-tooling/environment-yaml-builder/SKILL.md`    |
| 18 | [`makefile-generator`](project-tooling/makefile-generator/SKILL.md)                   | Generate Makefile with install/test/lint/docs/run/format targets.         | `project-tooling/makefile-generator/SKILL.md`          |
| 19 | [`pre-commit-hook-builder`](project-tooling/pre-commit-hook-builder/SKILL.md)         | Build .pre-commit-config.yaml with ruff, black, mypy, end-of-file.        | `project-tooling/pre-commit-hook-builder/SKILL.md`     |
| 20 | [`release-notes-generator`](project-tooling/release-notes-generator/SKILL.md)         | Generate release notes from git log since last tag.                       | `project-tooling/release-notes-generator/SKILL.md`     |

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

### Skill CLI — Many Examples

The `scripts/Skill.py` CLI is the primary interface for terminal-based skill discovery, validation, and inspection.
Below are concrete examples covering every subcommand.

#### `list` — enumerate skills

```bash
# List every skill across every theme (defaults to all 9 SkillStack themes).
python scripts/Skill.py list

# List is theme-aware: skills are grouped under their theme header.
# Sample output (truncated):
#   academic-research (20 skills)
#     research-ideation-planner
#     research-repo-builder
#     journal-manuscript-writer
#     ...
#   style-integrity (18 skills)
#     coding-conventions-enforcer
#     latex-style-guard
#     ...
```

#### `search <query>` — full-text search

```bash
# Search by keyword (matches name, description, and tags).
python scripts/Skill.py search "latex"

# Search for a tool name.
python scripts/Skill.py search "optuna"

# Search for a domain.
python scripts/Skill.py search "hallucination"

# Search for a tag.
python scripts/Skill.py search "citations"

# Multi-word query.
python scripts/Skill.py search "bootstrap confidence interval"
```

#### `show <skill-name>` — print a skill's full SKILL.md

```bash
# Print the full skill body to stdout.
python scripts/Skill.py show hyperparameter-tuner

# Print the maestro itself.
python scripts/Skill.py show maestro

# Pipe into a pager.
python scripts/Skill.py show coding-conventions-enforcer | less

# Save to a file for offline reference.
python scripts/Skill.py show factuality-checker > /tmp/factuality-checker.md
```

#### `validate <skill-name>` — lint one skill

```bash
# Validate a single skill's frontmatter + sections + line count.
python scripts/Skill.py validate latex-style-guard

# Validate a skill you are about to commit.
python scripts/Skill.py validate ai-output-judgement/prompt-injection-detector

# Exit code is non-zero on violations — useful in pre-commit hooks.
python scripts/Skill.py validate my-new-skill || echo "VALIDATION FAILED"
```

#### `graph` — print the skill dependency graph

```bash
# Print a Markdown table of every skill's related + prerequisites.
python scripts/Skill.py graph

# Save the graph for review.
python scripts/Skill.py graph > /tmp/skill-graph.md

# Filter to one theme.
python scripts/Skill.py graph | grep "ml-engineering"
```

#### `tags` — print the tag cloud

```bash
# Print every tag with the number of skills carrying it.
python scripts/Skill.py tags

# Sort by frequency (default).
python scripts/Skill.py tags

# Find the most-tagged skills.
python scripts/Skill.py tags | head -10
```

#### `health` — coverage summary

```bash
# Print the high-level coverage summary (total skills, % with examples, % with references).
python scripts/Skill.py health

# Sample output:
#   Total skills: 168
#   Average lines: 109.5
#   % with examples: 99.4% (167/168)
#   % with references: 99.4% (167/168)
```

### Other Scripts — Many Examples

#### `GenerateManifest.py` — produce `skills.yaml`

```bash
# Generate (or refresh) the manifest at skills.yaml.
python scripts/GenerateManifest.py

# Check freshness: exit non-zero if skills.yaml is stale (used in pre-commit).
python scripts/GenerateManifest.py --check

# Sample output:
#   wrote /home/z/my-project/skills/skills.yaml (167 skills, 9 themes)
```

#### `LintSkills.py` — validate every SKILL.md

```bash
# Lint every skill across every theme.
python scripts/LintSkills.py

# Lint one skill.
python scripts/LintSkills.py academic-research/journal-manuscript-writer/SKILL.md

# Lint one theme.
python scripts/LintSkills.py style-integrity/

# Exit code is non-zero on any violation.
python scripts/LintSkills.py && echo "ALL SKILLS PASS"
```

#### `CheckLinks.py` — verify every URL resolves

```bash
# HEAD-request every URL in every skill's References section.
python scripts/CheckLinks.py

# Use a longer timeout for slow networks.
python scripts/CheckLinks.py --timeout 10

# Sample output:
#   Total URLs: 412
#   OK: 405
#   Broken: 7
#   Broken URLs:
#     https://example.com/dead-link  (404)
#     ...
```

#### `VerifyCitations.py` — verify arXiv IDs and DOIs

```bash
# Verify every arXiv ID and DOI cited in any skill.
python scripts/VerifyCitations.py

# Sample output:
#   arXiv IDs checked: 23
#   DOIs checked: 14
#   Failures: 0
```

#### `CoverageReport.py` — generate `docs/coverage.md`

```bash
# Generate the per-skill coverage report.
python scripts/CoverageReport.py

# Output: docs/coverage.md (Markdown table with line count, has-examples, has-references per skill).
```

#### `SkillHealth.py` — generate `docs/health.html` dashboard

```bash
# Generate the visual HTML dashboard.
python scripts/SkillHealth.py

# Open in a browser.
python scripts/SkillHealth.py && open docs/health.html
```

#### `GraphvizChains.py` — generate `docs/skill-graph.svg`

```bash
# Generate the skill dependency graph as SVG.
python scripts/GraphvizChains.py

# Output: docs/skill-graph.svg (nodes = skills, edges = related/prerequisites).
```

#### `ExportAnthropic.py` — export to Anthropic Agent Skills format

```bash
# Export every skill to export/anthropic/<theme>/<skill-name>.md.
python scripts/ExportAnthropic.py

# Use a custom output directory.
python scripts/ExportAnthropic.py --out /tmp/anthropic-export

# Verify the export.
ls export/anthropic/academic-research/
#   academic-book-author.md
#   citation-network-mapper.md
#   ...
```

#### `Audit.py` — log skill invocations

```bash
# Log that you ran a skill (with input/output files).
python scripts/Audit.py log hyperparameter-tuner --input configs/Config.yaml --output Results/

# Show the last 50 audit entries.
python scripts/Audit.py show

# Print top-10 most-used skills.
python scripts/Audit.py stats
```

#### `CacheSkill.py` — pre-concatenate a skill + its references

```bash
# Concatenate one skill's SKILL.md + references/*.md into a single context blob.
python scripts/CacheSkill.py hyperparameter-tuner

# Output: .cache/hyperparameter-tuner.md (single file ready to load).

# Cache every skill at once.
python scripts/CacheSkill.py --all
```

### Generated Artifacts (auto-regenerated by CI)

| Path                   | Source                                                                   |
|------------------------|--------------------------------------------------------------------------|
| `skills.yaml`          | `GenerateManifest.py` — machine-readable manifest of all 168+ skills     |
| `docs/coverage.md`     | `CoverageReport.py` — per-skill line count, has-examples, has-references |
| `docs/health.html`     | `SkillHealth.py` — visual dashboard                                      |
| `docs/skill-graph.svg` | `GraphvizChains.py` — skill dependency graph                             |
| `export/anthropic/`    | `ExportAnthropic.py` — Anthropic-format export                           |

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

<details>
<summary><strong>📚 Sources & References (click to expand)</strong></summary>


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

</details>

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

<details>
<summary><strong>⚠️ Disclaimers (click to expand)</strong></summary>

> Read this section in full before loading any skill. By using this repository you accept every clause below.


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

</details>

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
