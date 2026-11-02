---
name: faithfulness-scorer
description: Score faithfulness of summarization and QA outputs to their source documents, using entailment-based checks, QAGS-style question generation, and fine-grained factuality decomposition. Use when abstractive summaries or answers must not contradict or go beyond the source.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [faithfulness, summarization, entailment, qa]
related: [ai-output-judgement/groundedness-verifier, ai-output-judgement/factuality-checker, ai-output-judgement/coherence-fluency-scorer]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Faithfulness Scorer

## When To Use
- An abstractive summarization system must be checked for fabricated content (a long-standing failure mode).
- Trigger keywords: "faithfulness", "factual consistency", "summarization eval", "QAGS", "SummaC", "FFE".
- A QA system must answer strictly from a passage and you need a faithfulness score before surfacing the answer.
- A reviewer asks: "Does this summary actually match the article?"

## Workflow
1. Take the (source document, generated summary or answer) pair.
2. Run three complementary methods and aggregate:
   (a) **NLI / SummaC** — split the summary into sentences, check entailment vs. the source with `roberta-large-mnli` or `microsoft/deberta-v3-large-mnli`. Faithful if entailment > contradiction.
   (b) **QAGS** — generate questions from each summary sentence, answer them using the source, and answer them using the summary; if answers disagree, the sentence is unfaithful.
   (c) **FFE (fine-grained)** — atomize the summary into atomic facts and check each against the source (overlap with `groundedness-verifier`).
3. For each summary sentence, label `FAITHFUL`, `UNFAITHFUL`, or `PARTIALLY_FAITHFUL`, and mark the offending spans.
4. Compute a faithfulness score in [0, 1] = (# FAITHFUL atoms) / (# total atoms). For sentence-level, also report mean NLI entailment prob.
5. Cross-validate with an LLM judge prompt: "Given source S and summary sentence T, output JSON `{label, rationale}`. Use only the source."
6. Emit a per-sentence table, the overall score, and a list of unfaithful spans for editor review.

## Inputs
- The source document (required).
- The generated summary or answer (required).
- Optional: NLI model override (default `roberta-large-mnli`), question generator override (an LLM), entailment threshold (default 0.7).
- Optional: a few-shot set of known faithful and unfaithful summaries for calibration.

## Outputs
- `faithfulness.jsonl` — per sentence: text, label, entailment_prob, qags_match, offending_spans.
- `faithfulness_report.md` — overall score, per-method agreement, top unfaithful sentences.
- `unfaithful_spans.md` — flagged spans with proposed rewrites drawn from the source.

## Key Rules
- A sentence contradicted by the source is UNFAITHFUL, regardless of how fluent or plausible it sounds.
- QAGS questions must be answerable from the summary sentence alone; unanswerable questions are discarded, not counted as failures.
- Do not consult the open web — only the source document counts.
- Report per-method agreement (NLI vs. QAGS vs. LLM judge); deep disagreement means borderline cases that need human review.
- Faithfulness is necessary but not sufficient — a summary can be faithful yet uninformative; route completeness to `response-quality-scorer`.

## Examples

```text
Source:    "The Apollo 11 mission landed on the Moon on July 20, 1969. Neil Armstrong was
            the first human to step onto the lunar surface."
Summary:   "Apollo 11 landed on the Moon in 1969. Buzz Aldrin was the first to walk on it."

Sentence-level:
  S1 "Apollo 11 landed on the Moon in 1969."                  -> FAITHFUL (entail 0.98)
  S2 "Buzz Aldrin was the first to walk on the Moon."         -> UNFAITHFUL (contradicts source;
                                                                entail 0.21, contradict 0.74)

QAGS:
  Q: "Who was the first to walk on the Moon?"  Source-A: "Neil Armstrong"  Summary-A: "Buzz Aldrin"  -> mismatch.
Faithfulness score: 1/2 = 0.50.
```

```text
Source:    "Revenue grew 12% YoY to $4.1B; operating margin expanded to 18%."
Summary:   "Revenue grew 12% to $4.1B and operating margin hit a record 25%."
Atoms:
  A1 Revenue grew 12% YoY.          -> FAITHFUL
  A2 Revenue reached $4.1B.          -> FAITHFUL
  A3 Operating margin expanded to 18%-> FAITHFUL
  A4 Margin hit a record 25%.        -> UNFAITHFUL (25% not in source; "record" unverified)
Faithfulness score: 3/4 = 0.75. Flag A4.
```

## Common Pitfalls
- Consulting the open web — only the source document counts; that is the job of `factuality-checker`.
- Counting QAGS questions that are unanswerable from the summary sentence as failures — discard them, do not penalize.
- Reporting a single method's verdict — cross-check NLI, QAGS, and LLM judge; deep disagreement means a borderline case.
- Treating grammatical-but-contradictory sentences as faithful — fluency masks unfaithfulness.
- Confusing faithfulness with completeness — a summary can be perfectly faithful yet omit key points; route completeness to `response-quality-scorer`.
- Atomizing at sentence level only — long sentences often carry multiple facts that need individual checks.

## References
- Kryscinski, W. et al. (2020). "Evaluating the Factual Consistency of Abstractive Text Summarization." EMNLP. https://arxiv.org/abs/1910.12840
- Wang, A. et al. (2020). "Asking and Answering Questions to Evaluate the Factual Consistency of Summaries." (QAGS) NAACL. https://arxiv.org/abs/2004.04228
- Laban, P. et al. (2022). "SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization." TACL. https://arxiv.org/abs/2111.09525
- Companion skills: `groundedness-verifier`, `factuality-checker`, `hallucination-detector`.
