---
name: reference-accuracy-checker
description: Verify that references and citations produced by an AI model resolve to real sources — DOI via Crossref, title via Google Scholar / Semantic Scholar, author names match, venue exists. Use specifically for AI-generated reference lists (higher hallucination risk than human-typed .bib files). Differs from `writing-citation/doi-verifier` which targets human-authored bibliographies.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [references, citations, doi, hallucination]
related: [ai-output-judgement/hallucination-detector, ai-output-judgement/factuality-checker, ai-text/citation-hallucination-detector]
prerequisites: []
outputs: [markdown, json]
difficulty: intermediate
estimated_tokens: 1800
cost_warning: Crossref and Semantic Scholar API calls — mostly free but rate-limited.
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Reference Accuracy Checker

## When To Use

- An LLM generated a bibliography or inline citations and every entry must be verified before submission.
- Trigger keywords: "AI-generated references", "fake citation", "phantom DOI", "Crossref check", "Semantic Scholar",
  "verify bibliography".
- A draft includes citations that look real but the model could have fabricated DOIs, journals, or author lists.
- A reviewer requires proof that every AI-assisted reference resolves to a real work.

## Workflow

1. Parse citations from the output: inline `(Author, Year)` markers, numbered `[1]` references, and full bibliography
   entries. Normalize each into a record with fields: `title`, `authors`, `year`, `venue`, `DOI` (if present).
2. For each DOI, query `https://api.crossref.org/works/{DOI} with a polite `User-Agent` mailto. Classify:
    - 200 + matching metadata → `VERIFIED`.
    - 200 + mismatched title/author → `MISMATCH` (the DOI is real but points elsewhere — common hallucination).
    - 404 → `UNRESOLVED`.
3. For each title (no DOI), query Semantic Scholar Academic Graph API
   (`https://api.semanticscholar.org/graph/v1/paper/search?query=...`). Take the top result; compare normalized title
   similarity and first-author surname. Threshold: similarity ≥ 0.90 for VERIFIED.
4. Verify the venue exists: Crossref journal list, Ulrichsweb, or the publisher site. Watch for plausible-sounding
   fabricated journals ("Journal of Contemporary Applied Systems Research").
5. Verify the author-year combination: search the author's publication list (Semantic Scholar author API) for a paper
   with the cited title in the cited year.
6. Score per citation: `VERIFIED`, `MISMATCH`, `UNRESOLVED`, `VENUE_NOT_FOUND`, `AUTHOR_MISMATCH`.
7. Emit a verification table and a recommended action: keep, replace DOI with recovered one, or delete (require human
   approval).

## Inputs

- The AI output with citations (required) — text, markdown, or .bib.
- Optional: contact email for Crossref's polite pool.
- Optional: similarity threshold override (default 0.90), Semantic Scholar API key for higher rate limits.
- Optional: known-good citation corpus for cross-checking.

## Outputs

- `reference_verification.jsonl` — one row per citation: title, authors, year, venue, DOI, status, evidence_url, action.
- `reference_report.md` — table, verification rate, hallucination rate, top problematic entries.
- `actions.md` — per-citation recommended actions for human approval.

## Key Rules

- This skill is for AI-generated references specifically — models hallucinate plausible citations at a much higher rate
  than humans mistype them.
- A DOI that resolves to a different paper is a MISMATCH, not a verification; this is the most common AI citation
  failure.
- Plausible-sounding journal names require venue verification — never assume existence from the name alone.
- Never auto-delete a citation; every removal must be human-approved.
- Respect Crossref's polite pool (≤ 5 req/s, include mailto) and Semantic Scholar rate limits.
- A 404 on Crossref means "DOI not found in Crossref" — it may exist in another DOI registrar; flag for human review, do
  not conclude fabrication.

## Examples

```text
AI-generated reference:
  Patel, R., & Nguyen, T. (2022). "Adaptive routing in mesh networks."
  Journal of Network Systems, 14(2), 88-103.

Checks:
  DOI: none provided.  Crossref title search: no match.
  Semantic Scholar title search: no exact match; similar titles exist with different authors.
  Ulrichsweb: "Journal of Network Systems" not listed; ISSN lookup fails.
Status: VENUE_NOT_FOUND + UNRESOLVED.
Action: delete (S4 hallucination). Human review required before deletion.
```

```text
AI-generated reference:
  Vaswani, A. et al. (2017). "Attention is all you need."
  DOI: 10.5555/3295222.3295349.

Crossref: 200, title matches, first author "Vaswani" matches.
Semantic Scholar paper ID: 204e3073870fae3d05bcbc2f6a8e261d9b2e57a6.
Status: VERIFIED.
```

## Common Pitfalls

- Treating a DOI that resolves to a different paper as verified — it is a MISMATCH, the most common AI citation failure.
- Assuming a plausible-sounding journal name is real — always verify the venue in Ulrichsweb or Crossref's journal list.
- Auto-deleting citations that fail verification — every removal must be human-approved; flag, do not delete.
- Concluding fabrication from a Crossref 404 — the DOI may exist in another registrar or be unindexed; flag for review.
- Skipping Semantic Scholar when no DOI is present — title search there often recovers the real paper.
- Comparing titles case-sensitively — Crossref returns title-cased strings; lowercase before similarity scoring.
