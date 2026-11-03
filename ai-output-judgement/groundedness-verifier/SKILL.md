---
name: groundedness-verifier
description: Verify that RAG (Retrieval-Augmented Generation) outputs are grounded in the retrieved context — every claim must be entailed by or derivable from the provided source documents. Use when a RAG pipeline produces answers that may rely on parametric memory instead of retrieved passages.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [groundedness, rag, entailment, hallucination]
related: [ai-output-judgement/faithfulness-scorer, ai-output-judgement/hallucination-detector, ai-output-judgement/factuality-checker]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Groundedness Verifier

## When To Use

- A RAG system answers questions and reviewers need to confirm the answer came from the sources, not the model's
  training data.
- Trigger keywords: "groundedness", "RAG evaluation", "entailment", "source-grounded", "faithfulness to context",
  "context-only answer".
- A retrieval step fetches documents and the LLM must cite or stick to them; hallucination beyond context is a risk.
- An enterprise search assistant must produce traceable, citation-backed answers.

## Workflow

1. Collect the (query, retrieved context chunks, generated answer) triple. Keep chunk IDs for provenance.
2. Atomize the answer into self-contained claims (one verifiable proposition each), following the same decomposition as
   `factuality-checker`.
3. For each claim, retrieve the most relevant context chunk via sentence-level embedding similarity
   (sentence-transformers `all-MiniLM-L6-v2` or stronger).
4. Run an NLI entailment check between (chunk, claim) using `roberta-large-mnli` or `microsoft/deberta-v3-large-mnli`.
   Keep the entailment probability.
5. Classify each claim:
    - `GROUNDED` — at least one chunk entails it (entailment prob ≥ 0.7).
    - `PARTIALLY_GROUNDED` — chunk supports part but not the whole claim (split and re-classify).
    - `UNGROUNDED` — no chunk entails it; the claim relies on parametric memory or is fabricated.
6. Optionally run an LLM judge prompt: "Given the context and the claim, output JSON
   `{label, evidence_chunk_id, rationale}`. Refuse to use outside knowledge."
7. Compute groundedness ratio = GROUNDED / total. Emit a per-claim table with the supporting chunk ID and a final
   verdict for the answer.

## Inputs

- The generated answer (required).
- The retrieved context chunks with stable IDs (required).
- Optional: the user query (improves atom resolution).
- Optional: NLI threshold override (default 0.7) and chunk similarity top-k (default 3).

## Outputs

- `groundedness.jsonl` — per claim: text, label, supporting_chunk_id, entailment_prob, rationale.
- `groundedness_report.md` — ratio table, UNGROUNDED claim list, and a verdict for the whole answer.
- `evidence_map.md` — claim → chunk mapping for citation rendering.

## Key Rules

- A claim is grounded only if entailed by retrieved context — not by what the model "knows".
- PARTIALLY_GROUNDED must be split into atomic sub-claims and re-judged; do not silently accept.
- The verifier must never consult the open web; that is the job of `factuality-checker`.
- Record the supporting chunk ID for every GROUNDED claim to enable downstream citation.
- When the model generates an answer with no retrieved context (empty retrieval), every claim is UNGROUNDED by
  construction.
- Distinguish grounding (answer is in context) from faithfulness (answer is faithful to a source) — overlap is high but
  the framing differs.

## Examples

```text
Query:   "What is the capital of Australia?"
Context: [C1] "Canberra is the capital of Australia, located between Sydney and Melbourne."
Answer:  "The capital of Australia is Canberra, a planned city built in 1913."

Claims:
  C1: The capital of Australia is Canberra.                  -> GROUNDED by chunk C1 (p=0.97)
  C2: Canberra is a planned city built in 1913.              -> UNGROUNDED (no chunk says this)

Groundedness ratio: 1/2 = 0.50. Verdict: PARTIALLY_GROUNDED.
Recommendation: retrieve more chunks about Canberra's history before re-answering.
```

```text
Answer: "The drug was approved by the FDA in 2018 based on a Phase 3 trial enrolling 1,200 patients."
Claims:
  C1: FDA approved the drug in 2018.        -> GROUNDED (chunk A)
  C2: Approval was based on a Phase 3 trial -> GROUNDED (chunk B)
  C3: The trial enrolled 1,200 patients.    -> UNGROUNDED (no chunk mentions enrollment size)
Verdict: PARTIALLY_GROUNDED. Flag C3 for human review or re-retrieval.
```

## Common Pitfalls

- Consulting the open web during verification — only retrieved context counts; that is the job of `factuality-checker`.
- Silently accepting PARTIALLY_GROUNDED claims — split them into atomic sub-claims and re-judge each.
- Forgetting to record the supporting chunk ID — downstream citation rendering breaks.
- Setting the NLI threshold too low (e.g., 0.5) — false groundedness slips through; 0.7 is a safer default.
- Treating empty retrieval as grounded — by construction, every claim is UNGROUNDED when no context was retrieved.
- Confusing grounding (answer is in context) with faithfulness (answer is faithful to a source) — overlap is high,
  framing differs.
