# Maestro Routing Test Cases

50 sample prompts and their expected routes. Use these to verify routing regressions.

| #  | User Prompt                                                           | Theme               | Skill                          |
|----|-----------------------------------------------------------------------|---------------------|--------------------------------|
| 1  | "Propose 3 research ideas for a medical imaging journal"              | academic-research   | research-ideation-planner      |
| 2  | "Scaffold a research repo with src/, configs, and manual"             | academic-research   | research-repo-builder          |
| 3  | "Draft the methods section of my paper in LaTeX"                      | academic-research   | journal-manuscript-writer      |
| 4  | "Find gaps in prior work on federated learning"                       | academic-research   | related-work-surveyor          |
| 5  | "Plan a 3-aim grant for an NIH R01 submission"                        | academic-research   | grant-proposal-writer          |
| 6  | "Outline chapter 4 of my PhD thesis"                                  | academic-research   | thesis-chapter-planner         |
| 7  | "Enforce 2-space indent and CamelCase in my Python repo"              | style-integrity     | coding-conventions-enforcer    |
| 8  | "Check my LaTeX for missing % ====== % separators"                    | style-integrity     | latex-style-guard              |
| 9  | "Verify every DOI in my bibliography is real"                         | style-integrity     | zero-fabrication-guard         |
| 10 | "Flag banned filler words like 'very' and 'really'"                   | style-integrity     | banned-vocabulary-filter       |
| 11 | "Catch passive voice in my paper's abstract"                          | style-integrity     | passive-voice-detector         |
| 12 | "Make sure I write 3.14 not 3.141592 in tables"                       | style-integrity     | numerical-value-formatter      |
| 13 | "Run a multi-seed training loop with .to(device) on every nn.Module"  | ml-engineering      | reproducible-experiment-runner |
| 14 | "Bayesian hyperparameter search with Optuna TPE"                      | ml-engineering      | hyperparameter-tuner           |
| 15 | "Generate SHAP summary and dependence plots for my classifier"        | ml-engineering      | model-explainer                |
| 16 | "Scaffold a PyTorch Lightning module with train and val steps"        | ml-engineering      | pytorch-lightning-scaffold     |
| 17 | "Find a good learning-rate range before training my transformer"      | ml-engineering      | learning-rate-finder           |
| 18 | "Run 5-fold cross-validation with stratification and report mean±std" | ml-engineering      | cross-validation-engine        |
| 19 | "Build an ETL with idempotent transforms and audit trail"             | data-engineering    | etl-pipeline-builder           |
| 20 | "Validate my CSV against a pandera schema"                            | data-engineering    | data-quality-validator         |
| 21 | "One-hot encode categoricals for my XGBoost model"                    | data-engineering    | categorical-encoder            |
| 22 | "Track which rows came from which source file"                        | data-engineering    | data-lineage-tracker           |
| 23 | "Detect distribution drift between train and prod data"               | data-engineering    | data-drift-monitor             |
| 24 | "Generate a dataset card in Model Card format"                        | data-engineering    | dataset-card-generator         |
| 25 | "Make a journal-ready 300 DPI matplotlib figure"                      | visualization       | publication-figure-maker       |
| 26 | "Draw a TikZ pipeline diagram with solid grouping lines"              | visualization       | tikz-framework-diagrammer      |
| 27 | "Pick a colorblind-safe palette for 7-class ROC curves"               | visualization       | color-palette-selector         |
| 28 | "Compose a 2x3 multi-panel figure for my ablation study"              | visualization       | multi-panel-figure-composer    |
| 29 | "Plot ROC and PR curves for my binary classifier"                     | visualization       | roc-pr-curve-plotter           |
| 30 | "Design a scientific poster for my conference talk"                   | visualization       | scientific-poster-designer     |
| 31 | "Convert my .bib to IEEE citation style"                              | writing-citation    | citation-style-converter       |
| 32 | "Check that every bibitem is \\cite'd at least once"                  | writing-citation    | bibtex-citation-manager        |
| 33 | "Verify a list of DOIs resolves to the right papers"                  | writing-citation    | doi-verifier                   |
| 34 | "Smooth transitions between paragraphs in my intro"                   | writing-citation    | paragraph-transition-smoother  |
| 35 | "Build an annotated bibliography of 30 papers"                        | writing-citation    | annotated-bibliography-builder |
| 36 | "Detect if this essay is AI-generated"                                | ai-text             | ai-text-detector               |
| 37 | "Humanize this AI text but keep all facts intact"                     | ai-text             | ai-text-humanizer              |
| 38 | "Score perplexity and burstiness of this text"                        | ai-text             | perplexity-burstiness-scorer   |
| 39 | "Find AI tells like 'delve' and 'tapestry' in my draft"               | ai-text             | ai-tell-catalogue              |
| 40 | "Check if this text carries a SynthID watermark"                      | ai-text             | ai-watermark-detector          |
| 41 | "Check if this LLM response contains hallucinated facts"              | ai-output-judgement | hallucination-detector         |
| 42 | "Verify the factual claims in this AI-generated paragraph"            | ai-output-judgement | factuality-checker             |
| 43 | "Check if my RAG output is grounded in the retrieved docs"            | ai-output-judgement | groundedness-verifier          |
| 44 | "Audit my LLM outputs for gender and race bias"                       | ai-output-judgement | bias-auditor                   |
| 45 | "Build an LLM eval harness with MMLU and GSM8K"                       | ai-output-judgement | evaluation-harness-builder     |
| 46 | "Bundle my repo into a zip excluding results/ and .git/"              | project-tooling     | project-zip-packager           |
| 47 | "Write a Dockerfile for reproducible research"                        | project-tooling     | docker-research-container      |
| 48 | "Generate a README.md for my Python package"                          | project-tooling     | readme-generator               |
| 49 | "Generate release notes from my git log"                              | project-tooling     | release-notes-generator        |
| 50 | "Create a pyproject.toml for my scientific Python package"            | project-tooling     | pyproject-toml-builder         |

## Coverage Summary

| Theme               | Cases  | Skills Covered                                                                                                                                             |
|---------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| academic-research   | 6      | research-ideation-planner, research-repo-builder, journal-manuscript-writer, related-work-surveyor, grant-proposal-writer, thesis-chapter-planner          |
| style-integrity     | 6      | coding-conventions-enforcer, latex-style-guard, zero-fabrication-guard, banned-vocabulary-filter, passive-voice-detector, numerical-value-formatter        |
| ml-engineering      | 6      | reproducible-experiment-runner, hyperparameter-tuner, model-explainer, pytorch-lightning-scaffold, learning-rate-finder, cross-validation-engine           |
| data-engineering    | 6      | etl-pipeline-builder, data-quality-validator, categorical-encoder, data-lineage-tracker, data-drift-monitor, dataset-card-generator                        |
| visualization       | 6      | publication-figure-maker, tikz-framework-diagrammer, color-palette-selector, multi-panel-figure-composer, roc-pr-curve-plotter, scientific-poster-designer |
| writing-citation    | 5      | citation-style-converter, bibtex-citation-manager, doi-verifier, paragraph-transition-smoother, annotated-bibliography-builder                             |
| ai-text             | 5      | ai-text-detector, ai-text-humanizer, perplexity-burstiness-scorer, ai-tell-catalogue, ai-watermark-detector                                                |
| ai-output-judgement | 5      | hallucination-detector, factuality-checker, groundedness-verifier, bias-auditor, evaluation-harness-builder                                                |
| project-tooling     | 5      | project-zip-packager, docker-research-container, readme-generator, release-notes-generator, pyproject-toml-builder                                         |
| **Total**           | **50** | **All 9 themes covered**                                                                                                                                   |

## How To Use

1. Run each prompt through the maestro routing logic.
2. Compare the routed skill to the expected skill column.
3. A mismatch means a routing regression — investigate whether a skill's `description` or `tags` drifted, or whether
   maestro's conflict resolver picked the wrong branch.
4. Add new rows as new skills land; keep the count at or above 50.
