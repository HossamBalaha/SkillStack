# SkillStack — Data Privacy Guide

> What every SkillStack skill sends, where it sends it, why, and the residual
> privacy risk. Use this table to decide which skills are safe to run on
> sensitive data and which require a sanitized copy first.
>
> 168 skills · 9 themes · MIT License · by Hossam Magdy Balaha.

---

## How To Read This Table

Each row maps a SkillStack skill to four facts:

- **Skill** — the `<theme>/<skill-name>` identifier.
- **Data Sent** — what bytes the skill actually transmits off-host (or to a
  local model server / library). Empty when the skill operates purely
  in-process on local files.
- **Destination** — where those bytes go. Local means the bytes never leave
  the machine the skill runs on. Remote means a third-party service receives
  them.
- **Purpose** — the operational reason the bytes are sent.
- **Privacy Risk** — one of `None`, `Low`, `Medium`, `High`, `Critical`,
  with a short justification.

**Rule of thumb:** any skill marked `Medium` or higher should be fed **anonymized or synthetic data** when run against
production corpora. Use
`data-engineering/data-anonymizer` first.

---

## Theme — `ai-output-judgement`

| Skill                        | Data Sent                                             | Destination                              | Purpose                                                 | Privacy Risk                                                |
|------------------------------|-------------------------------------------------------|------------------------------------------|---------------------------------------------------------|-------------------------------------------------------------|
| `factuality-checker`         | Atomic claims extracted from the LLM output           | Web search APIs (Bing / Google CSE)      | Verify each claim against the open web                  | Medium — claims may paraphrase sensitive content            |
| `hallucination-detector`     | Named entities + citation strings from the LLM output | Wikidata, Crossref, PyPI, GitHub APIs    | Resolve every entity/citation; flag the fabricated ones | Medium — entity list may leak subject matter                |
| `groundedness-verifier`      | LLM output + retrieved-doc snippets                   | Local embedding model (default)          | Compute NLI / entailment scores locally                 | Low — defaults to in-process; remote embeddings opt-in only |
| `faithfulness-scorer`        | Source docs + summary                                 | Local NLI model                          | Score summary faithfulness locally                      | Low — local only                                            |
| `reference-accuracy-checker` | Citation strings from AI-generated references         | Crossref, arXiv, Semantic Scholar        | Verify every reference resolves to a real paper         | Medium — citation list may leak research intent             |
| `pii-leak-detector`          | Text of the LLM output                                | spaCy NER model (local)                  | Detect PII entities locally; never transmits the text   | None — runs entirely in-process via spaCy                   |
| `bias-auditor`               | Generated responses + demographic labels              | Local classifier                         | Measure demographic skew in outputs                     | Low — local only                                            |
| `safety-classifier`          | Text of the LLM output                                | Local safety model                       | Predict unsafe-content category                         | Low — local only                                            |
| `relevance-scorer`           | Query + candidate doc                                 | Local cross-encoder                      | Score relevance locally                                 | Low — local only                                            |
| `consistency-checker`        | Multiple sampled responses                            | Local NLI model                          | Detect contradictions across samples                    | Low — local only                                            |
| `coherence-fluency-scorer`   | Text of the LLM output                                | Local LM scoring                         | Score coherence and fluency locally                     | Low — local only                                            |
| `numeric-accuracy-verifier`  | Numeric claims                                        | Local sympy + Crossref (opt-in)          | Verify arithmetic; resolve cited stats                  | Low — Crossref call is opt-in                               |
| `alignment-evaluator`        | Prompt + response pairs                               | Local rubric model                       | Score alignment locally                                 | Low — local only                                            |
| `llm-as-judge-evaluator`     | Prompts + responses                                   | Configured judge LLM (remote by default) | Use a stronger LLM as a judge                           | High — prompts and responses leave the host                 |
| `response-quality-scorer`    | Text of the LLM output                                | Local scoring rubric                     | Score quality locally                                   | Low — local only                                            |
| `code-output-validator`      | AI-generated Python source                            | Local subprocess (10s timeout)           | Execute the code in a sandboxed subprocess              | Medium — code may read local files; run in a venv           |
| `prompt-injection-detector`  | Retrieved web page text                               | Local classifier                         | Detect injection attempts in retrieved content          | Low — local only                                            |
| `evaluation-harness-builder` | Eval datasets (e.g., MMLU, GSM8K)                     | Local model server                       | Drive the model under test                              | Low — runs against your own model server                    |

---

## Theme — `ml-engineering`

| Skill                            | Data Sent                          | Destination                    | Purpose                                          | Privacy Risk                                      |
|----------------------------------|------------------------------------|--------------------------------|--------------------------------------------------|---------------------------------------------------|
| `transformer-finetuner`          | Training dataset + HF_TOKEN        | HuggingFace Hub (push)         | Push checkpoints/datasets to the Hub for sharing | High — dataset leaves the host if push is enabled |
| `inference-pipeline-builder`     | Inference queries                  | Model server (local or remote) | Serve the model under test                       | Medium — depends on where the model server lives  |
| `model-explainer`                | Trained model + background dataset | Local SHAP / LIME / IG         | Generate explanations locally                    | Low — local only                                  |
| `hyperparameter-tuner`           | Validation metrics                 | Local Optuna study             | Drive Bayesian optimization                      | None — metrics never leave the host               |
| `reproducible-experiment-runner` | Training logs                      | Local file system              | Persist logs under timestamped experiment folder | None — local only                                 |
| `cross-validation-engine`        | Fold metrics                       | Local                          | Aggregate CV statistics                          | None — local only                                 |
| `metrics-computation-suite`      | Predictions + labels               | Local                          | Compute accuracy / F1 / AUC / MCC                | None — local only                                 |
| `baseline-model-zoo`             | Training data                      | Local sklearn / xgboost        | Train baseline models locally                    | None — local only                                 |
| `model-checkpoint-manager`       | Model state dicts                  | Local disk                     | Save / load checkpoints                          | None — local only                                 |
| `distributed-training-setup`     | Gradients across ranks             | Local NCCL / Gloo              | Multi-GPU training                               | None — stays inside the cluster                   |

> Remaining `ml-engineering` skills (`modular-ml-architect`, `seed-and-device-resolver`,
> `experiment-folder-organizer`, `train-val-test-splitter`, `early-stopping-configurator`,
> `learning-rate-finder`, `mixed-precision-trainer`, `data-leakage-guard`,
> `statistical-validation-rigour`, `pytorch-lightning-scaffold`, `dataset-adapter-builder`,
> `ablation-study-runner`) all operate locally on the user's files and model objects.
> Privacy risk: **None**.

---

## Theme — `data-engineering`

| Skill                    | Data Sent                 | Destination         | Purpose                         | Privacy Risk      |
|--------------------------|---------------------------|---------------------|---------------------------------|-------------------|
| `data-anonymizer`        | PII fields                | Local hash / k-anon | Strip or generalize PII locally | None — local only |
| `dataset-card-generator` | Dataset metadata          | Local               | Generate a Model-Card-style doc | None — local only |
| `data-lineage-tracker`   | Row → source-file mapping | Local               | Track provenance                | None — local only |
| `etl-pipeline-builder`   | Row payloads              | Local               | Transform + load                | None — local only |
| `feature-store-recipe`   | Feature vectors           | Local feature store | Serve point-in-time features    | None — local only |

> Remaining `data-engineering` skills (`data-quality-validator`, `csv-json-converter`,
> `data-schema-enforcer`, `incremental-loader`, `time-series-resampler`,
> `missing-data-imputer`, `outlier-detector`, `data-drift-monitor`,
> `categorical-encoder`, `feature-engineering-toolkit`, `image-dataset-loader`,
> `text-preprocessor`, `tabular-data-sampler`) operate locally. Privacy risk: **None**.

---

## Theme — `writing-citation`

| Skill                            | Data Sent                 | Destination              | Purpose                            | Privacy Risk                      |
|----------------------------------|---------------------------|--------------------------|------------------------------------|-----------------------------------|
| `doi-verifier`                   | DOI strings               | Crossref API             | Resolve every DOI to a real record | Low — DOIs are public identifiers |
| `bibtex-citation-manager`        | `.bib` entries            | Local                    | Dedup, normalize, enforce citekeys | None — local only                 |
| `citation-style-converter`       | `.bib` entries            | Local                    | Convert IEEE ↔ APA ↔ Chicago       | None — local only                 |
| `annotated-bibliography-builder` | Citation list             | Local                    | Build an annotated bibliography    | None — local only                 |
| `zotero-better-bibtex-bridge`    | Zotero library (local DB) | Local Zotero SQLite      | Sync citekeys with Zotero          | None — local only                 |
| `reference-list-formatter`       | Reference list            | Local                    | Format reference list              | None — local only                 |
| `plagiarism-paraphraser`         | Source + draft            | Configured LLM (remote)  | Detect near-duplicate passages     | High — text leaves the host       |
| `english-academic-editor`        | Draft text                | Configured LLM (remote)  | Polish academic English            | High — text leaves the host       |
| `reading-level-adjuster`         | Draft text                | Local readability scorer | Adjust reading level               | None — local only                 |

> Remaining `writing-citation` skills (`cohesive-device-checker`,
> `hedging-language-balancer`, `tense-consistency-fixer`,
> `paragraph-transition-smoother`, `structured-abstract-writer`,
> `research-methodology-designer`, `literature-matrix-builder`,
> `imrad-thesis-writer`, `outline-to-prose-expander`) operate locally unless
> the user wires them to a remote LLM. Privacy risk: **None** by default.

---

## Theme — `ai-text`

| Skill                             | Data Sent            | Destination                       | Purpose                             | Privacy Risk                           |
|-----------------------------------|----------------------|-----------------------------------|-------------------------------------|----------------------------------------|
| `ai-text-detector`                | Text                 | Local classifier                  | Predict AI-generated probability    | None — local only                      |
| `ai-text-humanizer`               | Text                 | Configured LLM (remote)           | Rewrite to sound human              | High — text leaves the host            |
| `perplexity-burstiness-scorer`    | Text                 | Local GPT-2 scoring               | Compute perplexity + burstiness     | None — local only                      |
| `ai-watermark-detector`           | Text                 | Local watermark decoder           | Detect SynthID / OpenAI watermark   | None — local only                      |
| `ai-tell-catalogue`               | Text                 | Local lexicon                     | Flag AI-flavored words              | None — local only                      |
| `chatbot-residue-cleaner`         | Text                 | Local regex + lexicon             | Strip chatbot residues              | None — local only                      |
| `formatting-by-rule-cleaner`      | Text                 | Local regex                       | Apply formatting rules              | None — local only                      |
| `rhythm-by-rule-fixer`            | Text                 | Local syllable counter            | Fix sentence rhythm                 | None — local only                      |
| `staging-tell-remover`            | Text                 | Local lexicon                     | Strip staging language              | None — local only                      |
| `voice-profile-matcher`           | Voice sample + draft | Local embedding model             | Match author voice                  | None — local only                      |
| `inflation-stripper`              | Text                 | Local rules                       | Strip inflation language            | None — local only                      |
| `severity-classifier`             | Text                 | Local classifier                  | Classify harm severity              | None — local only                      |
| `multi-engine-verification`       | Claim                | Multiple engines (remote)         | Cross-check claim across engines    | Medium — claim leaves the host         |
| `grace-degradation-protocol`      | LLM output           | Local rules                       | Degrade gracefully when uncertain   | None — local only                      |
| `citation-hallucination-detector` | Citation strings     | Crossref, arXiv, Semantic Scholar | Verify every AI-cited paper is real | Medium — citation list may leak intent |

---

## Theme — `academic-research`

| Skill                           | Data Sent              | Destination                                     | Purpose                          | Privacy Risk                                |
|---------------------------------|------------------------|-------------------------------------------------|----------------------------------|---------------------------------------------|
| `citation-network-mapper`       | Seed paper identifier  | Semantic Scholar / Connected Papers / Inciteful | Build citation graph             | Low — paper IDs are public                  |
| `literature-review-synthesizer` | Boolean search strings | PubMed / Semantic Scholar                       | Run systematic searches          | Low — search terms may leak research intent |
| `related-work-surveyor`         | Topic + keywords       | Semantic Scholar                                | Survey related work              | Low — query terms only                      |
| `open-science-advocate`         | Repo URL + dataset DOI | OSF / Zenodo                                    | Advise on open-science practices | None — public artifacts                     |

> Remaining `academic-research` skills (`research-ideation-planner`,
> `research-repo-builder`, `journal-manuscript-writer`, `academic-book-author`,
> `grant-proposal-writer`, `peer-review-simulator`, `conference-talk-prep`,
> `thesis-chapter-planner`, `research-question-formulator`, `hypothesis-designer`,
> `experimental-design-planner`, `scope-and-aims-writer`, `research-portfolio-tracker`,
> `pre-registration-drafter`, `reproducibility-checklist-author`,
> `supplementary-materials-organizer`) operate on local Markdown / LaTeX. Privacy
> risk: **None** by default.

---

## Theme — `style-integrity`, `visualization`, `project-tooling`

All skills in these three themes operate locally:

- `style-integrity/*` — lint rules, prose checks, LaTeX guards, convention
  enforcers, planning-note logger. Privacy risk: **None**.
- `visualization/*` — figure builders, TikZ, posters, dashboards, plot
  utilities. Privacy risk: **None** (charts render from local data).
- `project-tooling/*` — READMEs, Dockerfiles, pyproject.toml, Makefiles,
  CI workflows, zip packager. Privacy risk: **None** (the generated
  `Dockerfile` may pull a base image from Docker Hub at *build* time — that
  is your Docker daemon's standard behaviour, not SkillStack's).

---

## Sensitive-Data Workflow

If your corpus is sensitive (PII, PHI, confidential research data), follow
this chain before invoking any `Medium`-or-higher skill:

```
data-engineering/data-anonymizer
  → data-engineering/data-quality-validator
  → ai-output-judgement/pii-leak-detector   (sanity-check the anonymized output)
  → <any Medium/High skill above>            (run on the anonymized copy)
```

For `High`-risk skills (`llm-as-judge-evaluator`, `plagiarism-paraphraser`,
`english-academic-editor`, `ai-text-humanizer`, `transformer-finetuner`
when pushing to the Hub), prefer one of:

1. Run on a fully synthetic corpus generated from your schema.
2. Point the configured LLM at a self-hosted model server (`vllm`, `text-generation-inference`, `llama.cpp server`).
3. Disable the remote push entirely (`--no-push` flag, where available) and
   keep the artifact local.

---

## Per-Skill Data-Flow Diagrams

For skills with non-trivial flows, the `SKILL.md` itself contains a
"## Data Flow" subsection listing every outbound call. Search the repo:

```bash
rg -l "## Data Flow" --glob '*/SKILL.md'
```

When a skill does **not** have a `## Data Flow` subsection, treat it as **local-only** (no bytes leave the host) unless
this table above says
otherwise.

---

## Update Policy

This table is regenerated by hand on every SkillStack release. If you add a
new skill that makes an outbound call, you **must** update this table in the
same PR. The linter does not yet enforce this; the manual diff review does.

| SkillStack version | Last updated |
|--------------------|--------------|
| 1.0.0              | 2026-11-02   |
