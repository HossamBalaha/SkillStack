---
name: doi-verifier
description: Verifies that each DOI in a bibliography resolves to the paper claimed by the entry, by querying the Crossref REST API and matching title, first author, and journal. Use when cleaning a `.bib` file before submission, or when a reviewer has flagged suspected fake or mismatched DOIs.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [doi, crossref, verification, citations]
related: [ai-output-judgement/reference-accuracy-checker, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [json, csv, markdown]
difficulty: intermediate
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# DOI Verifier

## When To Use

- A `.bib` file has DOIs that may be stale, mistyped, or fabricated.
- A reviewer flagged a reference whose DOI does not appear to match the cited title.
- You are importing a large bibliography scraped from PDFs and need a sanity check.
- A manuscript has been desk-rejected for "unverifiable references."

## Workflow

1. Parse the `.bib` file; extract every DOI alongside the entry's title, first author, and container
   (journal/booktitle).
2. For each DOI, issue an HTTPS GET to `https://api.crossref.org/works/{DOI} with a polite `User-Agent` including a
   mailto.
3. Classify the response:
    - 404 → DOI does not resolve → suspected fake.
    - 200 → parse returned `title`, first `author`, `container-title`.
4. Compute a match score between the local entry and the Crossref record using normalized title similarity (Jaccard or
   Levenshtein) plus first-author surname match.
5. Mark an entry as VERIFIED if title similarity ≥ 0.90 and first-author surname matches; otherwise MISMATCH.
6. For mismatches, attempt to recover the correct DOI by querying Crossref with the local title and first author.
7. Emit a verification table and propose an action per entry: keep, replace DOI with recovered DOI, or remove.
8. Never silently delete an entry; surface every action for human review.

## Inputs

- The `.bib` file to verify.
- A contact email for Crossref's polite pool (recommended but not mandatory).
- Optional similarity threshold override (default 0.90).

## Outputs

- `doi_verification.md` — table with columns: citekey, DOI, resolved title, first author, similarity, status (VERIFIED /
  MISMATCH / UNRESOLVED), action.
- `recovered_dois.csv` — for each MISMATCH, the candidate DOI recovered via title search.
- `cleaned.bib` — copy of the input with DOIs replaced where recovery succeeded (mismatches left untouched pending
  review).

## Key Rules

- Query rate must respect Crossref's polite-pool guidance (≤ 5 requests/second, include mailto in User-Agent).
- Title comparison must be case-insensitive and whitespace-normalized.
- A DOI that resolves to a different paper is a MISMATCH, not a verification.
- A 404 response means the DOI is unverifiable, not necessarily fabricated — flag for human review.
- Never auto-delete an entry; every change must be human-approved.
- The verification table must preserve the original citekey so the manuscript's `\cite{}` calls remain valid.

## Examples

```text
Verification table excerpt:
| citekey          | DOI                  | resolved title                       | first author | sim   | status    | action          |
|------------------|----------------------|--------------------------------------|--------------|-------|-----------|-----------------|
| Chronis2024Survey  | 10.1109/OJCS.2024.3396344      | A survey of federated learning       | Chronis      | 0.99  | VERIFIED  | keep            |
| Lee2022Sparse    | 10.1109/FAKE.2022.99 | 404 — no record                      | —            | 0.00  | UNRESOLVED | remove          |
| Ng2021Methods    | 10.1109/METH.2021.10 | A different paper entirely           | Patel        | 0.18  | MISMATCH  | recover → 10.1109/TPAMI.2021.3055599 |
```

```text
Recovery example:
  Local entry title: "Sparse attention mechanisms for transformers"
  Local first author: Ng
  Original DOI 10.1109/METH.2021.10 → resolves to unrelated paper (sim 0.18)
  Crossref title query → returned DOI 10.1109/TPAMI.2021.3055599
  Re-verify with recovered DOI → title sim 0.97, author match → VERIFIED
  Proposed action: replace DOI with 10.1109/TPAMI.2021.3055599
```

## Common Pitfalls

- Hitting the Crossref API without a `User-Agent` mailto — you land in the impolite pool and may get throttled or
  blocked.
- Treating a 404 as "fabricated DOI" — it may be a typo or a recently-assigned DOI not yet indexed; flag for human
  review.
- Comparing titles case-sensitively — Crossref returns title-cased strings; lowercase before similarity scoring.
- Auto-deleting mismatched entries — every removal must be human-approved to avoid losing real references.
- Forgetting to re-verify the recovered DOI before accepting it as the replacement.
