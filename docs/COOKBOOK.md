# SkillStack Cookbook — 20 Skill Chains for Real Workflows

> Each recipe is a one-line problem statement followed by an ordered skill chain.
> Load `maestro/SKILL.md` first, then follow the chain left-to-right, finishing each skill's declared `Outputs` before loading the next.
>
> 168 skills · 9 themes · MIT License · by Hossam Magdy Balaha

---

## Table of Contents

1. [Patient CSV → publishable classifier](#1-patient-csv--publishable-classifier) (8 skills)
2. [LLM eval harness for a fine-tuned model](#2-llm-eval-harness-for-a-fine-tuned-model) (6 skills)
3. [Containerize a research repo for reproducibility](#3-containerize-a-research-repo-for-reproducibility) (5 skills)
4. [Detect & humanize AI-sounding prose in a draft](#4-detect--humanize-ai-sounding-prose-in-a-draft) (5 skills)
5. [Audit a chatbot for bias and safety](#5-audit-a-chatbot-for-bias-and-safety) (6 skills)
6. [Journal manuscript from raw results](#6-journal-manuscript-from-raw-results) (8 skills)
7. [Tune & explain a PyTorch model, reproducibly](#7-tune--explain-a-pytorch-model-reproducibly) (7 skills)
8. [Feature store + ETL for streaming tabular data](#8-feature-store--etl-for-streaming-tabular-data) (6 skills)
9. [Verify a RAG system is grounded & safe](#9-verify-a-rag-system-is-grounded--safe) (6 skills)
10. [New research repo with CI/CD and docs](#10-new-research-repo-with-cicd-and-docs) (7 skills)
11. [Detect & strip AI watermarks](#11-detect--strip-ai-watermarks) (5 skills)
12. [Thesis chapters → polished book](#12-thesis-chapters--polished-book) (6 skills)
13. [Multi-seed ablation → leaderboard table](#13-multi-seed-ablation--leaderboard-table) (7 skills)
14. [Dataset card + anonymize a sensitive corpus](#14-dataset-card--anonymize-a-sensitive-corpus) (5 skills)
15. [Pre-register a study + write the methods](#15-pre-register-a-study--write-the-methods) (6 skills)
16. [Dashboard from model eval results](#16-dashboard-from-model-eval-results) (5 skills)
17. [Validate LLM-generated code before shipping](#17-validate-llm-generated-code-before-shipping) (6 skills)
18. [Clean & publish LaTeX with strict guardrails](#18-clean--publish-latex-with-strict-guardrails) (6 skills)
19. [Messy bibliography → verified, styled .bib](#19-messy-bibliography--verified-styled-bib) (6 skills)
20. [Package a research artifact for journal review](#20-package-a-research-artifact-for-journal-review) (6 skills)

---

## 1. Patient CSV → publishable classifier

> A clinical CSV with PII must become a trained, validated, explainable classifier documented well enough for a journal reviewer to reproduce.

Skill chain (8 skills):

1. `data-engineering/data-quality-validator` →
2. `data-engineering/data-anonymizer` →
3. `ml-engineering/train-val-test-splitter` →
4. `data-engineering/feature-engineering-toolkit` →
5. `ml-engineering/modular-ml-architect` →
6. `ml-engineering/cross-validation-engine` →
7. `ml-engineering/model-explainer` →
8. `academic-research/journal-manuscript-writer`

---

## 2. LLM eval harness for a fine-tuned model

> Benchmark a fine-tuned checkpoint on standard suites, judge with LLM-as-judge, and ship a reproducible leaderboard table.

Skill chain (6 skills):

1. `ai-output-judgement/evaluation-harness-builder` →
2. `ai-output-judgement/llm-as-judge-evaluator` →
3. `ai-output-judgement/hallucination-detector` →
4. `ai-output-judgement/bias-auditor` →
5. `visualization/results-table-formatter` →
6. `academic-research/reproducibility-checklist-author`

---

## 3. Containerize a research repo for reproducibility

> Ship a runnable Docker artifact so reviewers can reproduce the paper's results on any host.

Skill chain (5 skills):

1. `academic-research/research-repo-builder` →
2. `project-tooling/requirements-pinner` →
3. `project-tooling/docker-research-container` →
4. `project-tooling/github-actions-research-ci` →
5. `project-tooling/readme-generator`

---

## 4. Detect & humanize AI-sounding prose in a draft

> An essay reads as machine-generated; remove the tells and restore a human voice without losing any fact.

Skill chain (5 skills):

1. `ai-text/ai-text-detector` →
2. `ai-text/ai-tell-catalogue` →
3. `ai-text/staging-tell-remover` →
4. `ai-text/inflation-stripper` →
5. `ai-text/ai-text-humanizer`

---

## 5. Audit a chatbot for bias and safety

> A deployed chatbot must pass demographic-bias, safety, prompt-injection, PII-leak, and overall-quality checks before release.

Skill chain (6 skills):

1. `ai-output-judgement/bias-auditor` →
2. `ai-output-judgement/safety-classifier` →
3. `ai-output-judgement/prompt-injection-detector` →
4. `ai-output-judgement/pii-leak-detector` →
5. `ai-output-judgement/consistency-checker` →
6. `ai-output-judgement/response-quality-scorer`

---

## 6. Journal manuscript from raw results

> Turn a folder of results, figures, and a `.bib` into a submission-ready journal article.

Skill chain (8 skills):

1. `academic-research/literature-review-synthesizer` →
2. `writing-citation/research-methodology-designer` →
3. `writing-citation/structured-abstract-writer` →
4. `academic-research/journal-manuscript-writer` →
5. `visualization/publication-figure-maker` →
6. `writing-citation/bibtex-citation-manager` →
7. `style-integrity/zero-fabrication-guard` →
8. `style-integrity/academic-prose-polisher`

---

## 7. Tune & explain a PyTorch model, reproducibly

> Scaffold, seed, find a learning rate, Bayesian-tune, run reproducibly, ablate, then explain with SHAP.

Skill chain (7 skills):

1. `ml-engineering/pytorch-lightning-scaffold` →
2. `ml-engineering/seed-and-device-resolver` →
3. `ml-engineering/learning-rate-finder` →
4. `ml-engineering/hyperparameter-tuner` →
5. `ml-engineering/reproducible-experiment-runner` →
6. `ml-engineering/ablation-study-runner` →
7. `ml-engineering/model-explainer`

---

## 8. Feature store + ETL for streaming tabular data

> Ingest a streaming tabular source, enforce a schema, clean, engineer features, and publish to a feature store.

Skill chain (6 skills):

1. `data-engineering/etl-pipeline-builder` →
2. `data-engineering/data-schema-enforcer` →
3. `data-engineering/missing-data-imputer` →
4. `data-engineering/outlier-detector` →
5. `data-engineering/feature-engineering-toolkit` →
6. `data-engineering/feature-store-recipe`

---

## 9. Verify a RAG system is grounded & safe

> A retrieval-augmented chatbot's answers must be grounded in retrieved docs, factually correct, free of hallucination, and leak no PII.

Skill chain (6 skills):

1. `ai-output-judgement/groundedness-verifier` →
2. `ai-output-judgement/factuality-checker` →
3. `ai-output-judgement/hallucination-detector` →
4. `ai-output-judgement/reference-accuracy-checker` →
5. `ai-output-judgement/pii-leak-detector` →
6. `ai-output-judgement/faithfulness-scorer`

---

## 10. New research repo with CI/CD and docs

> Bootstrap a research codebase with packaging, pinned deps, ignores, scientific tests, CI, docs, and contribution guide.

Skill chain (7 skills):

1. `project-tooling/pyproject-toml-builder` →
2. `project-tooling/requirements-pinner` →
3. `project-tooling/gitignore-builder` →
4. `project-tooling/pytest-scientific-suite` →
5. `project-tooling/github-actions-research-ci` →
6. `project-tooling/sphinx-docs-builder` →
7. `project-tooling/contribution-guide-builder`

---

## 11. Detect & strip AI watermarks

> Screen model output for watermarking schemes and burstiness anomalies, then clean conversational residue.

Skill chain (5 skills):

1. `ai-text/ai-watermark-detector` →
2. `ai-text/perplexity-burstiness-scorer` →
3. `ai-text/ai-tell-catalogue` →
4. `ai-text/formatting-by-rule-cleaner` →
5. `ai-text/chatbot-residue-cleaner`

---

## 12. Thesis chapters → polished book

> Expand thesis chapters into a coherent academic book with smooth transitions and edited prose.

Skill chain (6 skills):

1. `academic-research/thesis-chapter-planner` →
2. `academic-research/academic-book-author` →
3. `writing-citation/outline-to-prose-expander` →
4. `writing-citation/paragraph-transition-smoother` →
5. `writing-citation/english-academic-editor` →
6. `writing-citation/reference-list-formatter`

---

## 13. Multi-seed ablation → leaderboard table

> Run a multi-seed ablation, statistically validate, compute metrics, and ship a leaderboard figure plus table.

Skill chain (7 skills):

1. `ml-engineering/seed-and-device-resolver` →
2. `ml-engineering/ablation-study-runner` →
3. `ml-engineering/statistical-validation-rigour` →
4. `ml-engineering/metrics-computation-suite` →
5. `visualization/results-table-formatter` →
6. `visualization/training-curve-visualizer` →
7. `academic-research/reproducibility-checklist-author`

---

## 14. Dataset card + anonymize a sensitive corpus

> Anonymize a sensitive dataset, validate it, generate a Model-Card-style dataset card, and track its lineage.

Skill chain (5 skills):

1. `data-engineering/data-anonymizer` →
2. `data-engineering/data-quality-validator` →
3. `data-engineering/dataset-card-generator` →
4. `data-engineering/data-lineage-tracker` →
5. `data-engineering/data-drift-monitor`

---

## 15. Pre-register a study + write the methods

> Move from a research question through hypothesis and experimental design to a pre-registration and methods section.

Skill chain (6 skills):

1. `academic-research/research-question-formulator` →
2. `academic-research/hypothesis-designer` →
3. `academic-research/experimental-design-planner` →
4. `academic-research/pre-registration-drafter` →
5. `writing-citation/research-methodology-designer` →
6. `academic-research/scope-and-aims-writer`

---

## 16. Dashboard from model eval results

> Build a dashboard from ROC/PR curves, confusion matrices, and a multi-panel figure summary.

Skill chain (5 skills):

1. `visualization/roc-pr-curve-plotter` →
2. `visualization/confusion-matrix-plotter` →
3. `visualization/multi-panel-figure-composer` →
4. `visualization/figure-caption-writer` →
5. `visualization/dashboard-builder`

---

## 17. Validate LLM-generated code before shipping

> An LLM produced Python code; verify it runs, is numerically correct, internally consistent, injection-free, safe, and coherent.

Skill chain (6 skills):

1. `ai-output-judgement/code-output-validator` →
2. `ai-output-judgement/numeric-accuracy-verifier` →
3. `ai-output-judgement/consistency-checker` →
4. `ai-output-judgement/prompt-injection-detector` →
5. `ai-output-judgement/safety-classifier` →
6. `ai-output-judgement/coherence-fluency-scorer`

---

## 18. Clean & publish LaTeX with strict guardrails

> Pass a LaTeX draft through the full style-integrity pipeline before journal submission.

Skill chain (6 skills):

1. `style-integrity/latex-style-guard` →
2. `style-integrity/cross-reference-validator` →
3. `style-integrity/notation-consistency-checker` →
4. `style-integrity/abbreviation-consistency-checker` →
5. `style-integrity/em-dash-eliminator` →
6. `style-integrity/math-symbol-auditor`

---

## 19. Messy bibliography → verified, styled .bib

> Convert a messy reference list into a verified, DOI-checked, venue-styled `.bib`.

Skill chain (6 skills):

1. `writing-citation/doi-verifier` →
2. `writing-citation/bibtex-citation-manager` →
3. `writing-citation/citation-style-converter` →
4. `writing-citation/reference-list-formatter` →
5. `writing-citation/zotero-better-bibtex-bridge` →
6. `style-integrity/zero-fabrication-guard`

---

## 20. Package a research artifact for journal review

> Bundle a finished repo into a reproducible, documented, versioned artifact for journal review.

Skill chain (6 skills):

1. `academic-research/reproducibility-checklist-author` →
2. `project-tooling/project-zip-packager` →
3. `project-tooling/docker-research-container` →
4. `project-tooling/readme-generator` →
5. `project-tooling/release-notes-generator` →
6. `project-tooling/changelog-writer`

---

## How to compose your own chain

1. **Identify the primary artifact** the user ultimately wants (a `.tex`, a CSV, a JSON report, a Docker image).
2. **Load `maestro/SKILL.md`** and route to the primary theme.
3. **Pick the first skill** whose `When To Use` matches the starting state of the inputs.
4. **Read each skill's `Outputs`** — those become the inputs to the next skill in the chain.
5. **Prefer the more specific skill** when two seem to apply; the maestro's conflict-resolution rule.
6. **Finish each skill before loading the next** — never overlap, or you risk half-written artifacts.
7. **End the chain on a packaging or review skill** (e.g., `reproducibility-checklist-author`, `zero-fabrication-guard`) so the output is shippable.

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
