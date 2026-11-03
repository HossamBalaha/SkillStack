---
name: factuality-checker
description: Verify factual claims in AI outputs by atomizing the text, retrieving evidence from trusted sources (Wikipedia API, Crossref, web search), and labeling each claim SUPPORTED, REFUTED, or UNVERIFIABLE. Use when an LLM response, summary, or long-form answer makes factual assertions that must be checked before release.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [factuality, llm, verification, factscore]
related: [ai-output-judgement/hallucination-detector, ai-output-judgement/reference-accuracy-checker, ai-output-judgement/numeric-accuracy-verifier, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [markdown, json]
difficulty: advanced
estimated_tokens: 2200
cost_warning: "Optional: web search API calls may incur costs."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Factuality Checker

## When To Use

- A long-form LLM answer, briefing, or article summary makes factual assertions that will be published or cited.
- A reviewer demands claim-level evidence rather than a single "looks plausible" judgment.
- Trigger keywords: "fact-check", "verify claims", "is this true", "supported by sources", "atomic claims", "FActScore".
- A RAG answer blends retrieved facts with model-internal knowledge and you need to separate the two.

## Workflow

1. Normalize the AI output: strip markdown cruft, segment into sentences, keep a span map for later highlighting.
2. Atomize: split each sentence into atomic claims (one verifiable proposition each). Use a prompt template such as
   "Decompose the following text into self-contained factual claims. One fact per line. No compound clauses."
3. For each atomic claim, retrieve evidence. Default order: (a) Wikipedia REST API (`https://en.wikipedia.org/w/api.php`
   action=query), (b) Wikidata for entity facts, (c) Crossref for citations, (d) a general web search via a vetted
   search API. Quote the retrieved passage and record its URL.
4. Decide per claim with a verifier pass: compare claim vs. evidence using an NLI model
   (`microsoft/deberta-v3-large-mnli`) plus an LLM judge prompt that returns a label and a one-sentence rationale.
5. Label each claim: `SUPPORTED` (evidence entails it), `REFUTED` (evidence contradicts it), or `UNVERIFIABLE` (no
   decisive evidence found in top-k results).
6. Compute a factuality score = (#SUPPORTED) / (#SUPPORTED + #REFUTED + #UNVERIFIABLE) and a strict FActScore =
   SUPPORTED / total.
7. Emit a claim-level table with span, label, evidence URL, and rationale, plus a global summary.

## Inputs

- The AI output text (required).
- Optional: trusted-source allowlist (e.g., PubMed, Statista, government domains).
- Optional: golden claims or seed corpus to short-circuit retrieval.
- Optional: k for top-k evidence and the NLI entailment threshold (default 0.7).

## Outputs

- `claims.jsonl` — one row per atomic claim: `id`, `text`, `span`, `label`, `evidence_url`, `rationale`.
- `factuality_report.md` — table plus FActScore, percentage unsupported, and top problematic claims.
- Highlighted HTML/markdown of the output with SUPPORTED (green), REFUTED (red), UNVERIFIABLE (yellow) spans.

## Key Rules

- Never label a claim SUPPORTED without a retrieved evidence URL; "model knows it" is not verification.
- A claim is REFUTED only when retrieved evidence directly contradicts it — absence of evidence is UNVERIFIABLE, not
  REFUTED.
- Atomic claims must not contain pronouns; resolve references to entities before retrieval.
- Cite retrieval provenance for every label so a human can audit the trail.
- When a single sentence carries two facts, split it; do not label compound statements.
- Do not write new facts during atomization — only restate what the output says.

## Examples

```text
AI output: "Marie Curie won the Nobel Prize in Physics in 1903 and again in Chemistry in 1911.
She was the first person to win two Nobel Prizes."

Atomized claims:
  C1: Marie Curie won the Nobel Prize in Physics in 1903.
  C2: Marie Curie won the Nobel Prize in Chemistry in 1911.
  C3: Marie Curie was the first person to win two Nobel Prizes.

Verdicts:
  C1 SUPPORTED — https://en.wikipedia.org/wiki/Marie_Curie (NLI entailment 0.96)
  C2 SUPPORTED — https://www.nobelprize.org/prizes/chemistry/1911/marie-curie/
  C3 SUPPORTED — Nobel Prize official biography confirms she was first.

FActScore: 1.00 (3/3 supported)
```

```text
AI output: "The Eiffel Tower was completed in 1889 for the World's Fair in London."
C1: The Eiffel Tower was completed in 1889.            -> SUPPORTED
C2: The Eiffel Tower was built for a World's Fair.      -> SUPPORTED (1889 Exposition Universelle)
C3: That World's Fair was held in London.               -> REFUTED (it was in Paris)
FActScore: 0.67; the London claim is refuted by evidence.
```

## Common Pitfalls

- Treating "no evidence found" as REFUTED — it should be UNVERIFIABLE; absence of evidence is not contradiction.
- Using the model's own parametric knowledge as evidence — only retrieved, citable sources count.
- Failing to atomize compound claims — sentences joined by "and" usually hide two independent facts.
- Trusting a single retrieved source for sensitive claims — require corroboration from a second independent source.
- Letting the verifier LLM write new facts during atomization — only restate what the output already says.
