---
name: coherence-fluency-scorer
description: Score coherence (logical flow between sentences), fluency (grammaticality and naturalness), and readability of AI outputs using language-model perplexity, next-sentence prediction, and grammar checking. Use when outputs are technically correct but read awkwardly or jump between ideas.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [coherence, fluency, readability, grammar]
related: [ai-output-judgement/response-quality-scorer, ai-output-judgement/relevance-scorer, ai-output-judgement/faithfulness-scorer]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Coherence Fluency Scorer

## When To Use

- Outputs are factually fine but read awkwardly or jump between unrelated ideas.
- Trigger keywords: "fluency", "coherence", "readability", "perplexity", "grammar", "next-sentence prediction".
- A copy-editing pipeline needs automatic pass/fail before a human editor reviews.
- A model produces long-form answers and you want to flag the incoherent sections.

## Workflow

1. Sentence-segment the output. Compute per-sentence perplexity with a reference LM (GPT-2 or a modern base LM) — high
   perplexity = less fluent.
2. Compute coherence via next-sentence prediction: for each adjacent pair (s_i, s_{i+1}), use a BERT-style NSP model or
   an NLI model to score whether s_{i+1} follows from s_i. Average the scores.
3. Run a grammar checker (LanguageTool or `language_tool_python`) on the full output; count errors by category (grammar,
   style, typography) and severity.
4. Compute readability with Flesch Reading Ease and Flesch-Kincaid grade level. Flag if grade level deviates sharply
   from the target audience.
5. Detect coherence breaks: if a sentence-pair NSP score drops below 0.4, mark the boundary as a coherence break.
6. Score per dimension: fluency = 1 - normalized_perplexity; coherence = mean NSP score; readability = scaled Flesch
   score. Aggregate to a 1-5 scale per dimension.
7. Emit per-sentence scores, flagged awkward spans, and a per-dimension summary with concrete fixes.

## Inputs

- The AI output text (required).
- Optional: target audience (grade level) for readability calibration.
- Optional: reference LM for perplexity (default GPT-2 XL or a modern base model).
- Optional: language (default English; LanguageTool supports 30+ languages).

## Outputs

- `coherence_fluency.jsonl` — per sentence: perplexity, nsp_score, grammar_errors, fluency, coherence.
- `report.md` — per-dimension 1-5 scores, coherence-break boundaries, awkward spans, readability.
- `fixes.md` — suggested edits: rewrite awkward spans, fix grammar, re-order incoherent sentences.

## Key Rules

- Perplexity must be computed with the same LM across all outputs being compared; mixing LMs invalidates the scale.
- A low grammar-error count does not imply fluency — outputs can be grammatical yet awkward.
- Readability must match the audience; a college-grade answer to a primary-school question is a mismatch, not a virtue.
- Coherence breaks between paragraphs matter as much as within paragraphs — check both.
- Flag, do not auto-rewrite; surface the spans and let an editor decide.

## Examples

```text
Output: "Photosynthesis converts light into chemical energy. The Eiffel Tower was built in 1889.
         Plants use this energy to make glucose."

Per-sentence:
  S1 perplexity 22.4, fluency 4/5
  S2 perplexity 18.1, fluency 5/5   -- BUT NSP(S1→S2) = 0.18  -> coherence break
  S3 perplexity 24.0, fluency 3/5   -- NSP(S2→S3) = 0.21      -> coherence break
Grammar errors: 0.  Readability: Flesch 64.2 (plain English).
Scores: fluency 4, coherence 2, readability 4.
Recommendation: delete S2 (off-topic tangent) to restore coherence.
```

```text
Output: "The user should first log in. After logging in they will see their dashboard.
         There account settings is accessable from there."

Per-sentence:
  S1 fluency 5/5
  S2 fluency 4/5 (run-on)
  S3 fluency 2/5 -- "There account settings is accessable" grammar errors:
     "There" → "Their", "is accessable" → "are accessible"
NSP scores all ≥ 0.7 — coherent flow.
Recommendation: fix the grammar errors in S3; coherence is fine.
```

## Common Pitfalls

- Mixing language models for perplexity across runs — the scale is model-specific and comparisons become invalid.
- Equating low grammar-error count with fluency — outputs can be grammatical yet awkward.
- Ignoring the target audience when scoring readability — a college-grade answer to a primary-school question is a
  mismatch, not a virtue.
- Skipping paragraph-boundary coherence checks — breaks between paragraphs matter as much as within paragraphs.
- Auto-rewriting awkward spans — flag for an editor; never silently rewrite.
- Using a small reference LM that flags common modern phrasings as high-perplexity — calibrate the LM to the domain.
