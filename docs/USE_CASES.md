# SkillStack — Use Cases

> 15 user stories with concrete personas, real goals, and the skill chains
> that get each persona to their finished artifact. Each chain is a
> left-to-right ordering — finish one skill's declared `Outputs` before
> loading the next.
>
> 168 skills · 9 themes · 1 maestro orchestrator · MIT License · by Hossam
> Magdy Balaha.

---

## How To Read These Stories

- **Persona** — a fictional but representative user with a name, role, and
  concrete goal.
- **Goal** — the artifact they want to ship (a paper, a model, a dashboard,
  a report).
- **Chain** — the ordered list of `theme/skill-name` pairs the maestro
  would route through, with one line of reasoning per link.
- **Outcome** — what the persona ends up with when the chain completes.

Always load `maestro/SKILL.md` first. The maestro decides the chain; this
document is a worked-example reference, not a routing oracle.

---

## 1. Aisha — PhD student writing her first paper (8-skill chain)

**Persona.** Aisha is a 2nd-year PhD student in medical imaging. She has
training data on disk and a working prototype model, but has never written
a journal paper before. Her goal: ship a methods section, results, and
figures good enough for a workshop submission.

**Goal.** A reproducible, well-cited workshop paper with figures.

**Chain.**

1. `academic-research/research-question-formulator` — sharpen her vague
   "I want to detect tumors" into a FINER-framed question with PICO
   population/intervention/comparator/outcome.
2. `academic-research/hypothesis-designer` — convert the question into H0
   and H1 with effect-size framing and the statistical test that will
   evaluate each.
3. `style-integrity/coding-conventions-enforcer` — before she writes any
   training code, load the repo's strict style so every snippet in the
   paper is consistent.
4. `ml-engineering/reproducible-experiment-runner` — set up seeds, device
   resolution, dual logging, and the 4-split experiment folder so the
   paper's results section is reproducible.
5. `ml-engineering/statistical-validation-rigor` — bootstrap CIs, paired
   t-test/Wilcoxon/McNemar, AUC branching for the reported metrics.
6. `visualization/publication-figure-maker` — journal-ready 300 DPI
   matplotlib figures with colorblind-safe palettes.
7. `visualization/figure-caption-writer` — self-contained captions that
   survive the two-column squeeze.
8. `academic-research/journal-manuscript-writer` — draft the methods +
   results in LaTeX with `\section`/`\subsection` only, IEEE numbered
   citations, and the mandatory back-matter.

**Outcome.** A `paper/` folder with `main.tex`, `figures/*.pdf`,
`references.bib`, and a methods section a reviewer can reproduce.

---

## 2. Mateo — ML engineer shipping a fine-tuned model (6-skill chain)

**Persona.** Mateo is an ML engineer at a health-tech startup. His team
has labelled clinical text and wants to fine-tune a transformer for
entity extraction, then ship it behind an API.

**Goal.** A fine-tuned, validated, explainable model served behind a
FastAPI inference endpoint.

**Chain.**

1. `ml-engineering/data-leakage-guard` — enforce train/val/test isolation;
   fit preprocessing on train only.
2. `ml-engineering/train-val-test-splitter` — stratified split at the
   patient level (not the note level) to avoid leakage.
3. `ml-engineering/transformer-finetuner` — fine-tune a Hugging Face
   transformer with Trainer / PEFT, log to W&B, push to a private HF repo.
4. `ml-engineering/hyperparameter-tuner` — Optuna Bayesian search with
   TPE + MedianPruner; persist `OptunaTrials.csv` and `BestParams.json`.
5. `ml-engineering/model-explainer` — SHAP summary + dependence plots for
   the entity-extraction head.
6. `ml-engineering/inference-pipeline-builder` — FastAPI endpoint with
   pre/post-processing and a `/health` probe.

**Outcome.** A `model/` folder with the checkpoint, an `api/` folder with
the FastAPI app, and a `trials.csv` showing the search history.

---

## 3. Dr. Park — reviewer peer-reviewing a manuscript (4-skill chain)

**Persona.** Dr. Park is a tenured professor reviewing a submission for *IEEE TMI*. She wants to write a structured,
fair, actionable review.

**Goal.** A peer-review report with specific, verifiable critiques.

**Chain.**

1. `writing-citation/doi-verifier` — verify every cited DOI resolves to
   the right paper (catch fabricated citations early).
2. `style-integrity/zero-fabrication-guard` — verify every claim/quote/
   URL is real; silent-omit anything missing.
3. `academic-research/peer-review-simulator` — generate a structured
   peer-review report (summary, strengths, weaknesses, minor points,
   recommendation).
4. `ai-output-judgement/factuality-checker` — atomic-claim verification
   on any sentences the reviewer suspects are wrong.

**Outcome.** A `review.md` with verifiable critiques, ready to paste into
the journal's review form.

---

## 4. Sara — RAG engineer verifying her system is grounded (6-skill chain)

**Persona.** Sara is building a RAG system for a legal firm. She wants to
ship only if the outputs are grounded in the retrieved docs and free of
hallucinations.

**Goal.** A RAG pipeline with a per-query grounding + hallucination score.

**Chain.**

1. `data-engineering/etl-pipeline-builder` — idempotent ETL with
   extract-validate-transform-load and audit trail for the document
   corpus.
2. `ml-engineering/inference-pipeline-builder` — FastAPI endpoint for the
   retriever + generator.
3. `ai-output-judgement/groundedness-verifier` — NLI / entailment check
   between the generated answer and the retrieved snippets.
4. `ai-output-judgement/hallucination-detector` — extract named entities
   from the answer; verify each against Wikidata / Crossref / the corpus.
5. `ai-output-judgement/prompt-injection-detector` — scan every retrieved
   page for injection attempts before trusting it.
6. `ai-output-judgement/evaluation-harness-builder` — build an eval
   harness with a legal-domain QA set for regression testing.

**Outcome.** A `pipeline/` folder, a `reports/` folder with per-query
grounding + hallucination scores, and an eval harness.

---

## 5. Tom — solo founder auditing his chatbot for bias (5-skill chain)

**Persona.** Tom is a solo founder shipping a customer-support chatbot.
Before launch, he wants to audit it for demographic bias and unsafe
outputs.

**Goal.** A bias + safety audit report he can show investors.

**Chain.**

1. `ai-output-judgement/bias-auditor` — measure demographic skew across
   name-variants in the prompts.
2. `ai-output-judgement/safety-classifier` — predict unsafe-content
   category on a stress-test set.
3. `ai-output-judgement/alignment-evaluator` — score alignment against a
   rubric of helpful + harmless + honest.
4. `ai-output-judgement/llm-as-judge-evaluator` — use a stronger LLM as
   a judge for the cases the local classifier is unsure about.
5. `project-tooling/release-notes-generator` — generate a public release
   note documenting the audit findings and mitigations.

**Outcome.** An `audit/` folder with bias + safety + alignment reports,
plus a release note.

---

## 6. Yuki — postdoc preparing a grant proposal (6-skill chain)

**Persona.** Yuki is a postdoc applying for an NSF CAREER grant. She has
preliminary data and needs a structured proposal narrative.

**Goal.** A complete NSF CAREER proposal narrative.

**Chain.**

1. `academic-research/research-ideation-planner` — propose 3 research
   ideas aligned to NSF's review criteria.
2. `academic-research/scope-and-aims-writer` — draft scope, aims, and
   contribution statements.
3. `academic-research/experimental-design-planner` — plan the experimental
   design with sample-size calculation via power analysis.
4. `academic-research/pre-registration-drafter` — draft an AsPredicted
   pre-registration for the proposed work.
5. `academic-research/grant-proposal-writer` — draft Specific Aims (1
   page), Background, Innovation, Approach, Budget Justification.
6. `style-integrity/latex-style-guard` — enforce LaTeX typography on the
   final narrative.

**Outcome.** A `proposal/` folder with `specific-aims.tex`,
`background-and-innovation.tex`, `approach.tex`, `budget-justification.tex`.

---

## 7. Liam — DevOps engineer containerizing a research repo (5-skill chain)

**Persona.** Liam is a DevOps engineer asked to make a research repo
reproducible by containerizing it.

**Goal.** A Docker image + Makefile + CI workflow that reproduces the
paper's results from a clean checkout.

**Chain.**

1. `project-tooling/requirements-pinner` — pin every dependency to a
   reproducible lockfile.
2. `project-tooling/docker-research-container` — write a Dockerfile for
   reproducible research (multi-stage, cache mounts, non-root user).
3. `project-tooling/makefile-generator` — generate a Makefile with the
   standard targets (`lint`, `test`, `build`, `run`, `clean`).
4. `project-tooling/github-actions-research-ci` — generate a GitHub
   Actions workflow that runs lint + test + build on every push.
5. `project-tooling/project-zip-packager` — bundle the repo into a zip
   excluding `results/`, `.git/`, and `__pycache__/`.

**Outcome.** A `Dockerfile`, `Makefile`, `.github/workflows/ci.yml`, and
a reproducible zip artifact.

---

## 8. Priya — data journalist cleaning a CSV and telling a story (6-skill chain)

**Persona.** Priya is a data journalist who just received a messy CSV of
public-health spending by county. She wants to clean it, anonymize it, and
turn it into a story with charts.

**Goal.** A clean dataset + an annotated chart + a 500-word story.

**Chain.**

1. `data-engineering/data-quality-validator` — pandera schema with null/
   duplicate/outlier checks.
2. `data-engineering/data-anonymizer` — hash PII, k-anonymity on
   quasi-identifiers.
3. `data-engineering/missing-data-imputer` — impute missing spending values
   with MICE.
4. `visualization/infographic-summarizer` — turn the cleaned table into a
   one-page infographic.
5. `writing-citation/outline-to-prose-expander` — expand a 5-bullet story
   outline into 500 words of prose.
6. `writing-citation/reading-level-adjuster` — adjust reading level to
   Grade 8 for the general public.

**Outcome.** A `cleaned.csv`, an `infographic.svg`, and a `story.md`.

---

## 9. Dr. Chen — thesis writer polishing her LaTeX (5-skill chain)

**Persona.** Dr. Chen is writing her PhD thesis. She has 4 chapters drafted
in LaTeX and wants to enforce consistency before submission.

**Goal.** A thesis PDF with consistent notation, no banned words, and
verified cross-references.

**Chain.**

1. `style-integrity/latex-style-guard` — enforce blank lines around floats,
   `% ====== %` separators, LaTeX quotes.
2. `style-integrity/notation-consistency-checker` — audit one-to-one
   symbol mapping; mandate a Nomenclature table if >15 symbols.
3. `style-integrity/banned-vocabulary-filter` — strip banned LLM-flavored
   words (delve, tapestry, leverage, etc.).
4. `style-integrity/cross-reference-validator` — verify every `\ref{}` and
   `\label{}` resolves and every float is referenced.
5. `academic-research/thesis-chapter-planner` — plan the remaining
   chapters with cross-chapter non-redundancy.

**Outcome.** A `thesis/` folder with `main.tex` that compiles cleanly and
passes every style guard.

---

## 10. Marcus — ML researcher running a multi-seed ablation (7-skill chain)

**Persona.** Marcus is an ML researcher running a multi-seed ablation study
to compare three attention variants. He wants a leaderboard table + a
significance callout.

**Goal.** A reproducible ablation study with a leaderboard CSV + a
significance callout in the paper.

**Chain.**

1. `ml-engineering/seed-and-device-resolver` — resolve `torch.device`
   once; `.to(device)` on every `nn.Module`.
2. `ml-engineering/reproducible-experiment-runner` — multi-seed training
   loop with dual logging and 4-split folders.
3. `ml-engineering/ablation-study-runner` — run ablations by removing/
   altering each attention variant systematically.
4. `ml-engineering/statistical-validation-rigor` — bootstrap CIs + paired
   t-test/Wilcoxon/McNemar for the significance callout.
5. `visualization/results-table-formatter` — format the leaderboard as a
   LaTeX booktabs table.
6. `visualization/multi-panel-figure-composer` — compose a 2x3 multi-panel
   figure for the ablation curves.
7. `project-tooling/changelog-writer` — write a changelog entry for the
   ablation run.

**Outcome.** An `Aggregated/` folder with the leaderboard CSV, a
`figures/ablation.pdf`, and a `CHANGELOG.md` entry.

---

## 11. Fatima — librarian building an annotated bibliography (5-skill chain)

**Persona.** Fatima is a university librarian asked to compile an annotated
bibliography of 30 papers on a specific topic for a faculty member.

**Goal.** A `bibliography.bib` + an annotated `bibliography.md`.

**Chain.**

1. `academic-research/related-work-surveyor` — survey related work and
   build a thematic comparison table.
2. `academic-research/citation-network-mapper` — map the citation network
   to identify the seminal papers.
3. `writing-citation/doi-verifier` — verify every DOI resolves.
4. `writing-citation/bibtex-citation-manager` — dedup, normalize citekeys,
   enforce `bibitem` ↔ `\cite` consistency.
5. `writing-citation/annotated-bibliography-builder` — build the annotated
   bibliography with one paragraph per paper.

**Outcome.** A `bibliography.bib` with 30 verified entries and a
`bibliography.md` with annotations.

---

## 12. Kevin — AI safety researcher red-teaming an LLM (6-skill chain)

**Persona.** Kevin is an AI safety researcher building a red-team suite for
a chatbot his company is about to ship.

**Goal.** A red-team report with adversarial prompts, jailbreak attempts,
and severity classifications.

**Chain.**

1. `ai-output-judgement/prompt-injection-detector` — scan his test prompts
   to ensure they classify as injection.
2. `ai-text/severity-classifier` — classify the model's responses by harm
   severity.
3. `ai-output-judgement/safety-classifier` — predict the unsafe-content
   category.
4. `ai-output-judgement/hallucination-detector` — extract entities; verify
   each.
5. `ai-output-judgement/evaluation-harness-builder` — build an eval harness
   that runs the red-team suite on every model revision.
6. `project-tooling/release-notes-generator` — write a release note
   summarizing the red-team findings.

**Outcome.** A `redteam/` folder with prompts, responses, severity
classifications, and a release note.

---

## 13. Elena — biology PhD student anonymizing patient data (4-skill chain)

**Persona.** Elena has a clinical CSV with PII she needs to anonymize
before sharing with collaborators.

**Goal.** An anonymized CSV + a dataset card documenting the anonymization.

**Chain.**

1. `data-engineering/data-quality-validator` — validate the CSV against a
   pandera schema.
2. `data-engineering/data-anonymizer` — hash PII, k-anonymity on
   quasi-identifiers, suppress low-count cells.
3. `ai-output-judgement/pii-leak-detector` — sanity-check the anonymized
   output for residual PII.
4. `data-engineering/dataset-card-generator` — generate a dataset card
   documenting provenance, license, composition, intended use.

**Outcome.** An `anonymized.csv`, a `pii-leak-report.jsonl`, and a
`dataset-card.md`.

---

## 14. Daniel — DevRel engineer preparing a conference talk (5-skill chain)

**Persona.** Daniel is a DevRel engineer preparing a 20-minute conference
talk on SkillStack itself. He wants a slide plan, a demo notebook, and a
Q&A prep doc.

**Goal.** A slide outline + a runnable demo notebook + a Q&A prep doc.

**Chain.**

1. `academic-research/conference-talk-prep` — draft the slide-by-slide
   outline with speaker notes, transitions, time-boxing, and Q&A prep.
2. `project-tooling/jupyter-to-script-converter` — convert the demo
   notebook to a script so it can run in CI.
3. `visualization/scientific-poster-designer` — design a one-page poster
   to leave at the venue.
4. `project-tooling/readme-generator` — generate a README for the demo
   repo that attendees will clone.
5. `writing-citation/structured-abstract-writer` — write a structured
   abstract for the conference proceedings.

**Outcome.** A `slides/` folder, a `demo.ipynb`, a `poster.pdf`, a
`README.md`, and an `abstract.md`.

---

## 15. Zara — ML engineer building an eval harness (6-skill chain)

**Persona.** Zara is an ML engineer asked to benchmark her team's fine-tuned
LLM against MMLU and GSM8K with LLM-as-judge scoring.

**Goal.** A reproducible eval harness + a leaderboard table.

**Chain.**

1. `ai-output-judgement/evaluation-harness-builder` — build the harness
   with MMLU + GSM8K datasets.
2. `ml-engineering/metrics-computation-suite` — compute accuracy / F1 /
   AUC / MCC / calibration error.
3. `ai-output-judgement/llm-as-judge-evaluator` — use a stronger LLM as a
   judge for the open-ended responses.
4. `ml-engineering/statistical-validation-rigor` — bootstrap CIs on the
   leaderboard scores.
5. `visualization/results-table-formatter` — format the leaderboard as a
   LaTeX booktabs table.
6. `project-tooling/pytest-scientific-suite` — generate a pytest suite so
   the eval harness runs in CI.

**Outcome.** An `eval/` folder with the harness, a `leaderboard.csv`, a
`leaderbook.tex` table, and a `tests/` folder for CI.

---

## Cross-Cutting Patterns

Across all 15 stories, three patterns repeat:

1. **Load the maestro first.** Every story opens with `maestro/SKILL.md`.
2. **Style before code.** When a story involves writing code or LaTeX,
   `style-integrity/coding-conventions-enforcer` (for Python) or
   `style-integrity/latex-style-guard` (for LaTeX) loads early.
3. **Validate before ship.** When a story ends with shipping an artifact,
   the last 1–2 links are validators (`zero-fabrication-guard`,
   `statistical-validation-rigor`, `pii-leak-detector`,
   `prompt-injection-detector`).

---

## Want Your Story Here?

Open a GitHub Discussion under "Show & Tell" with your persona, goal, and
chain. The maintainer will work with you to land it in the next release of
this document.
