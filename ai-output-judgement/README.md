# 🔍 AI Output Judgement — Judge & Verify AI Outputs

> Judge and verify LLM, RAG, and model-generated outputs for factuality, hallucination, grounding, faithfulness, coherence, safety, bias, PII leakage, prompt injection, and alignment. Includes eval-harness building and LLM-as-judge scoring for end-to-end output quality assurance. Output is always a numeric score plus an evidence trace, never a bare verdict.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-18-blue)]()
[![Theme](https://img.shields.io/badge/Theme-ai-output-judgement-green)]()

</div>

## Theme Overview

This folder contains **18 skills** in the `ai-output-judgement/` theme. Each subfolder holds a `SKILL.md` whose YAML frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| # | Skill | Description | Difficulty | Tags | Related |
|---|---|---|---|---|---|
| 1 | [`alignment-evaluator`](alignment-evaluator/SKILL.md) | Evaluate alignment with human values using the HHH framework (Helpful, Honest, Harmless) on prompts designed to elicit misalignment — deception, sycophancy, reward hacking, power-seeking. | advanced | `alignment`, `hhh-framework`, `sycophancy`, `evaluation` | `ai-output-judgement/bias-auditor`, `ai-output-judgement/safety-classifier`, `ai-output-judgement/response-quality-scorer` |
| 2 | [`bias-auditor`](bias-auditor/SKILL.md) | Audit AI outputs for demographic and cognitive bias by testing counterfactual prompts across protected groups (gender, race, age, religion, disability) and detecting stereotypical associations. | advanced | `bias`, `fairness`, `counterfactual`, `protected-groups` | `ai-output-judgement/safety-classifier`, `ai-output-judgement/pii-leak-detector`, `ai-output-judgement/alignment-evaluator` |
| 3 | [`code-output-validator`](code-output-validator/SKILL.md) | Validate AI-generated code by syntax-checking, executing in a sandbox, running provided unit tests, checking spec compliance, and detecting security issues. | advanced | `code`, `validation`, `sandbox`, `security` | `ai-output-judgement/factuality-checker`, `project-tooling/pytest-scientific-suite` |
| 4 | [`coherence-fluency-scorer`](coherence-fluency-scorer/SKILL.md) | Score coherence (logical flow between sentences), fluency (grammaticality and naturalness), and readability of AI outputs using language-model perplexity, next-sentence prediction, and grammar checking. | intermediate | `coherence`, `fluency`, `readability`, `grammar` | `ai-output-judgement/response-quality-scorer`, `ai-output-judgement/relevance-scorer`, `ai-output-judgement/faithfulness-scorer` |
| 5 | [`consistency-checker`](consistency-checker/SKILL.md) | Check that an LLM produces semantically consistent outputs across temperature variations, paraphrased inputs, and repeated samples at fixed temperature. | intermediate | `consistency`, `self-consistency`, `reliability`, `llm` | `ai-output-judgement/response-quality-scorer`, `ai-output-judgement/coherence-fluency-scorer` |
| 6 | [`evaluation-harness-builder`](evaluation-harness-builder/SKILL.md) | Build standardized evaluation harnesses for LLMs in the style of EleutherAI lm-evaluation-harness, OpenAI Evals, and Stanford HELM. | advanced | `eval-harness`, `benchmark`, `mmlu`, `helm` | `ai-output-judgement/llm-as-judge-evaluator`, `ai-output-judgement/response-quality-scorer` |
| 7 | [`factuality-checker`](factuality-checker/SKILL.md) | Verify factual claims in AI outputs by atomizing the text, retrieving evidence from trusted sources (Wikipedia API, Crossref, web search), and labeling each claim SUPPORTED, REFUTED, or UNVERIFIABLE. | advanced | `factuality`, `llm`, `verification`, `factscore` | `ai-output-judgement/hallucination-detector`, `ai-output-judgement/reference-accuracy-checker`, `ai-output-judgement/numeric-accuracy-verifier`, `style-integrity/zero-fabrication-guard` |
| 8 | [`faithfulness-scorer`](faithfulness-scorer/SKILL.md) | Score faithfulness of summarization and QA outputs to their source documents, using entailment-based checks, QAGS-style question generation, and fine-grained factuality decomposition. | advanced | `faithfulness`, `summarization`, `entailment`, `qa` | `ai-output-judgement/groundedness-verifier`, `ai-output-judgement/factuality-checker`, `ai-output-judgement/coherence-fluency-scorer` |
| 9 | [`groundedness-verifier`](groundedness-verifier/SKILL.md) | Verify that RAG (Retrieval-Augmented Generation) outputs are grounded in the retrieved context — every claim must be entailed by or derivable from the provided source documents. | advanced | `groundedness`, `rag`, `entailment`, `hallucination` | `ai-output-judgement/faithfulness-scorer`, `ai-output-judgement/hallucination-detector`, `ai-output-judgement/factuality-checker` |
| 10 | [`hallucination-detector`](hallucination-detector/SKILL.md) | Detect hallucinated content in AI outputs — fabricated entities, fake citations, invented statistics, made-up quotes, and non-existent API methods — by combining token-level confidence, entity verification against Wikidata/Crossref, and cross-source corroboration. | advanced | `hallucination`, `entities`, `factuality`, `llm` | `ai-output-judgement/factuality-checker`, `ai-output-judgement/reference-accuracy-checker`, `ai-output-judgement/groundedness-verifier`, `style-integrity/zero-fabrication-guard` |
| 11 | [`llm-as-judge-evaluator`](llm-as-judge-evaluator/SKILL.md) | Run LLM-as-judge evaluation over (input, output) pairs using a rubric prompt template, parse scores, and mitigate known judge biases (position, verbosity, self-enhancement) via order swapping, length normalization, and cross-model judges. | advanced | `llm-as-judge`, `evaluation`, `rubrics`, `bias` | `ai-output-judgement/response-quality-scorer`, `ai-output-judgement/consistency-checker`, `ai-output-judgement/evaluation-harness-builder` |
| 12 | [`numeric-accuracy-verifier`](numeric-accuracy-verifier/SKILL.md) | Verify numeric computations, statistics, dates, and quantities in AI outputs by parsing values and units, re-computing arithmetic claims, checking dates against known events, and cross-checking quantities against trusted sources. | intermediate | `numeric`, `arithmetic`, `dates`, `units`, `verification` | `ai-output-judgement/factuality-checker`, `ai-output-judgement/hallucination-detector`, `ai-output-judgement/reference-accuracy-checker` |
| 13 | [`pii-leak-detector`](pii-leak-detector/SKILL.md) | Detect Personally Identifiable Information (PII) leakage in AI outputs — emails, phone numbers, SSNs, credit cards, passport numbers, physical addresses, dates of birth, full names, account numbers — using regex patterns plus NER. | intermediate | `pii`, `gdpr`, `hipaa`, `redaction`, `privacy` | `ai-output-judgement/safety-classifier`, `ai-output-judgement/bias-auditor` |
| 14 | [`prompt-injection-detector`](prompt-injection-detector/SKILL.md) | Detect prompt-injection attacks against LLM systems — both direct injections ("ignore previous instructions", "you are now DAN") and indirect injections embedded in retrieved web pages or documents a RAG pipeline ingests. | intermediate | `prompt-injection`, `jailbreak`, `security`, `llm` | `ai-output-judgement/safety-classifier`, `ai-output-judgement/pii-leak-detector` |
| 15 | [`reference-accuracy-checker`](reference-accuracy-checker/SKILL.md) | Verify that references and citations produced by an AI model resolve to real sources — DOI via Crossref, title via Google Scholar / Semantic Scholar, author names match, venue exists. | intermediate | `references`, `citations`, `doi`, `hallucination` | `ai-output-judgement/hallucination-detector`, `ai-output-judgement/factuality-checker`, `ai-text/citation-hallucination-detector` |
| 16 | [`relevance-scorer`](relevance-scorer/SKILL.md) | Score how relevant an AI output is to the user query by combining semantic similarity, query-term coverage, and intent classification. | intermediate | `relevance`, `evaluation`, `query-coverage`, `intent` | `ai-output-judgement/response-quality-scorer`, `ai-output-judgement/coherence-fluency-scorer`, `ai-output-judgement/consistency-checker` |
| 17 | [`response-quality-scorer`](response-quality-scorer/SKILL.md) | Score LLM responses on multi-dimensional quality — helpfulness, completeness, relevance, clarity, and depth — each on a 1-5 rubric, with a weighted aggregate. | advanced | `response-quality`, `rlhf`, `reward-model`, `evaluation` | `ai-output-judgement/llm-as-judge-evaluator`, `ai-output-judgement/relevance-scorer`, `ai-output-judgement/coherence-fluency-scorer` |
| 18 | [`safety-classifier`](safety-classifier/SKILL.md) | Classify AI outputs for harmful content across safety categories — violence, hate speech, sexual content, self-harm, illegal activities, CSAM indicators, and PII exposure — using dedicated classifier models. | intermediate | `safety`, `moderation`, `toxicity`, `harm` | `ai-output-judgement/bias-auditor`, `ai-output-judgement/pii-leak-detector`, `ai-output-judgement/prompt-injection-detector` |

## Difficulty Breakdown

Across **18** skills in this theme, the difficulty distribution is:

- **Intermediate** — 8 skill(s)
- **Advanced** — 10 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`evaluation` (4), `llm` (4), `hallucination` (3), `bias` (2), `entailment` (2), `factuality` (2), `security` (2), `verification` (2), `alignment` (1), `arithmetic` (1), `benchmark` (1), `citations` (1), `code` (1), `coherence` (1), `consistency` (1), `counterfactual` (1), `dates` (1), `doi` (1), `entities` (1), `eval-harness` (1), `factscore` (1), `fairness` (1), `faithfulness` (1), `fluency` (1), `gdpr` (1), `grammar` (1), `groundedness` (1), `harm` (1), `helm` (1), `hhh-framework` (1), `hipaa` (1), `intent` (1), `jailbreak` (1), `llm-as-judge` (1), `mmlu` (1), `moderation` (1), `numeric` (1), `pii` (1), `privacy` (1), `prompt-injection` (1), `protected-groups` (1), `qa` (1), `query-coverage` (1), `rag` (1), `readability` (1), `redaction` (1), `references` (1), `relevance` (1), `reliability` (1), `response-quality` (1), `reward-model` (1), `rlhf` (1), `rubrics` (1), `safety` (1), `sandbox` (1), `self-consistency` (1), `summarization` (1), `sycophancy` (1), `toxicity` (1), `units` (1), `validation` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the most common sequences observed across the SkillStack repo.

- **`factuality-checker` → `hallucination-detector` → `reference-accuracy-checker` → `numeric-accuracy-verifier`** — Full factuality audit of an LLM response.
- **`groundedness-verifier` → `faithfulness-scorer` → `relevance-scorer` → `coherence-fluency-scorer`** — RAG output quality suite.
- **`llm-as-judge-evaluator` → `response-quality-scorer` → `consistency-checker` → `alignment-evaluator`** — Judge + score + consistency + alignment.
- **`bias-auditor` → `safety-classifier` → `pii-leak-detector` → `prompt-injection-detector`** — Safety & responsibility audit.

## Cross-Theme Connections

Skills in `ai-output-judgement/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../style-integrity/` — 2 related pointer(s)
- `../ai-text/` — 1 related pointer(s)
- `../project-tooling/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../ai-text/README.md`](ai-text/README.md) — humanization triggers re-verification of the rewritten text.
- [`../ml-engineering/README.md`](ml-engineering/README.md) — inference pipelines are audited end-to-end.
- [`../style-integrity/README.md`](style-integrity/README.md) — zero-fabrication guard closes the factuality loop.
- [`../data-engineering/README.md`](data-engineering/README.md) — dataset cards and PII checks share anonymization rules.

## Back to Master

← [Back to SkillStack README](../README.md)
