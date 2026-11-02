---
name: factuality-checker-lite
description: Verify factual claims in AI outputs by atomizing the text, retrieving evidence from trusted sources (Wikipedia API, Crossref, web search), and labeling each claim SUPPORTED, REFUTED, or UNVERIFIABLE. Use when an LLM response, summary, or long-form answer makes factual assertions that must be checked before release.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement

lite: true
full_version: factuality-checker/SKILL.md
language: en
---

# Factuality Checker (Lite)

> Condensed version. Load `factuality-checker/SKILL.md` for the full workflow.

Verifies factual claims in AI outputs by atomizing text, retrieving evidence from trusted sources, and labeling each
claim SUPPORTED / REFUTED / UNVERIFIABLE with a FActScore.

## Top 3 Workflow Steps

1. Normalize the AI output (strip markdown cruft, segment into sentences, keep a span map); atomize each sentence into
   atomic claims — one verifiable proposition each, no pronouns, no compound clauses.
2. For each atomic claim, retrieve evidence in order: Wikipedia REST API → Wikidata → Crossref → vetted web search API;
   quote the retrieved passage and record its URL.
3. Decide per claim with a verifier pass (NLI model `microsoft/deberta-v3-large-mnli` + LLM judge with one-sentence
   rationale); label `SUPPORTED` / `REFUTED` / `UNVERIFIABLE`; compute FActScore = SUPPORTED / total; emit a claim-level
   table plus a global summary report.

## Top 3 Key Rules

1. **Never label a claim SUPPORTED without a retrieved evidence URL** — "model knows it" is NOT verification; only
   retrieved, citable sources count as evidence.
2. **`REFUTED` requires direct contradiction** by retrieved evidence — absence of evidence is `UNVERIFIABLE`, never
   `REFUTED`; require corroboration from a second independent source for sensitive claims.
3. **Atomic claims must not contain pronouns** — resolve references to entities before retrieval; **split compound
   sentences** (sentences joined by "and" usually hide two facts); **do not write new facts during atomization** — only
   restate what the output already says.
