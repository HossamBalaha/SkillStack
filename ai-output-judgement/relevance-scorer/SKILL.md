---
name: relevance-scorer
description: Score how relevant an AI output is to the user query by combining semantic similarity, query-term coverage, and intent classification. Use when outputs drift off-topic, over-hedge, or fail to actually answer what was asked.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [relevance, evaluation, query-coverage, intent]
related: [ai-output-judgement/response-quality-scorer, ai-output-judgement/coherence-fluency-scorer, ai-output-judgement/consistency-checker]
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
---

# Relevance Scorer

## When To Use
- A chatbot occasionally produces fluent but off-topic replies that erode user trust.
- Trigger keywords: "relevance", "off-topic", "query coverage", "intent match", "answer the question".
- An evaluation set needs a relevance dimension alongside helpfulness and correctness.
- Outputs suffer from evasive hedging that technically stays on-topic but evades the actual question.

## Workflow
1. Classify the user intent: `informational`, `transactional`, `navigational`, `how-to`, `opinion`, or `troubleshooting`. Use a small classifier (rule-based + LLM judge).
2. Compute semantic similarity between the query and the output via sentence embeddings (`all-mpnet-base-v2` or `bge-large-en`); use cosine similarity normalized to [0, 1].
3. Compute query-term coverage: extract key terms from the query (nouns, proper nouns, verbs), check how many appear (or are addressed) in the output. Coverage = matched / total.
4. Detect hedging evasion: flag responses where the output apologizes, deflects, or gives disclaimers without substantive content (e.g., "As an AI…" templates, "It depends…" with no follow-through).
5. Detect tangents: identify output sentences whose semantic similarity to the query is below 0.3 — these are off-topic tangents.
6. Compute a weighted relevance score: 0.5 * semantic_sim + 0.3 * coverage + 0.2 * intent_match. Subtract 0.1 if hedging evasion is detected (floor at 0).
7. Emit per-response scores, per-sentence tangent flags, and a recommendation (on-topic, trim tangents, refactor for evasion).

## Inputs
- The (query, response) pair (required).
- Optional: intent classifier override, embedding model override, tangent threshold (default 0.3).
- Optional: a query-keyterm extractor (spaCy `en_core_web_sm` or a custom noun-phrase extractor).

## Outputs
- `relevance.jsonl` — per response: intent, semantic_sim, coverage, intent_match, hedge_flag, tangent_count, score.
- `relevance_report.md` — overall means, worst-offender responses, common evasion patterns.
- `tangents.md` — flagged off-topic sentences with their similarity scores.

## Key Rules
- A high fluency score does not imply relevance — fluent non-answers are common and must be penalized.
- Hedging evasion is detected when the output has disclaimers but low coverage of query key terms.
- Intent must be inferred from the query, never from the output (otherwise the model dictates its own rubric).
- Coverage is on key terms, not raw tokens — stopword overlap must not inflate the score.
- A single high-similarity sentence is not enough; the whole response must address the query.

## Examples

```text
Query:    "How do I reset my password?"
Response: "Passwords are important for security. Many people forget theirs.
           To reset yours, go to Settings → Account → Reset Password and follow the prompts."
Intent:       how-to
Semantic sim: 0.71
Coverage:     4/5 key terms ("reset", "password", "settings", "account", "prompts")
Hedge flag:   false
Tangents:     sentence 1 (sim 0.18 to query) — flagged.
Score: 0.5*0.71 + 0.3*0.80 + 0.2*1.00 = 0.875. Recommendation: trim the tangent.
```

```text
Query:    "Is X safe during pregnancy?"
Response: "As an AI, I cannot give medical advice. You should consult a qualified healthcare
           professional for personalized guidance regarding your situation."
Intent:       informational
Semantic sim: 0.42
Coverage:     1/4 key terms
Hedge flag:   true (template disclaimer + no substantive content)
Score: 0.5*0.42 + 0.3*0.25 + 0.2*1.00 - 0.10 = 0.36.
Verdict: EVASIVE. Recommend routing to a vetted medical source.
```

## Common Pitfalls
- Inferring intent from the response rather than the query — the model then dictates its own rubric.
- Letting stopword overlap inflate coverage — extract key terms (nouns, proper nouns, verbs), not raw tokens.
- One high-similarity sentence masking off-topic tangents — check every sentence, not just the average.
- Mistaking hedging evasion for safe behavior — disclaimers without substance lower the score.
- Confusing fluency with relevance — a fluent non-answer is still a non-answer.
- Penalizing justified clarifying questions as "low relevance" — they may be the correct response.

## References
- Muennighoff, N. et al. (2023). "MTEB: Massive Text Embedding Benchmark." EACL. https://arxiv.org/abs/2210.07316
- Reimers, N. & Gurevych, I. (2019). "Sentence-BERT." EMNLP. https://arxiv.org/abs/1908.10084
- Broder, A. (2002). "A Taxonomy of Web Search." SIGIR Forum. https://dl.acm.org/doi/10.1145/582415.582468
- Companion skills: `response-quality-scorer`, `llm-as-judge-evaluator`, `coherence-fluency-scorer`.
