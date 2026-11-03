---
name: zero-fabrication-guard
description: Verify every citation, DOI, URL, dataset name, author name, paper title, and numerical claim in a manuscript against authoritative external sources before submission. Use when checking factual integrity, hunting fabricated references, or auditing numerical claims for accuracy.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [verification, citations, fabrication, doi]
related: [style-integrity/claim-source-tracer, academic-research/literature-review-synthesizer, style-integrity/cross-reference-validator, academic-research/peer-review-simulator]
prerequisites: []
outputs: [markdown, json]
difficulty: advanced
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Zero Fabrication Guard

## When To Use

- User asks to "fact-check", "verify references", or "audit claims" in a manuscript.
- A draft contains citations, DOIs, URLs, dataset names, or numerical statistics whose accuracy is uncertain.
- Author is unsure whether AI-generated text introduced fabricated sources.
- Pre-submission integrity review is required.

## Workflow

1. Extract every factual artifact from the manuscript: author names, paper titles, journal names, years, DOIs, URLs,
   dataset names, and every numerical claim.
2. For each DOI, query `https://api.crossref.org/works/{DOI}` and confirm the returned title, authors, and journal match
   the manuscript's citation.
3. For each citation, search Google Scholar (or Semantic Scholar API at
   `https://api.semanticscholar.org/graph/v1/paper/search`) using title and first author. Confirm a matching record
   exists.
4. For each URL, perform an HTTP HEAD request and confirm a 2xx/3xx response. Record redirects.
5. For each dataset name, cross-check against the canonical registry (e.g., `https://registry.identifiers.org/` or the
   dataset's official landing page).
6. For each numerical claim ("accuracy of 94.2%"), locate the originating source and confirm the number, the metric, and
   the experimental setting match.
7. Apply the silent-omission protocol for any claim that cannot be verified: silently omit the claim from the body (do
   NOT emit `[DECLARATION: ...]` text), and append a "Planning Note" at the end of the deliverable listing what was
   omitted and what verification data is still needed.
8. Use only real, verifiable sources. Never invent a DOI, URL, or author to "fill in" a gap.
9. Produce a verification report: verified items, mismatched items, and silently-omitted items.

## Inputs

- Manuscript text with inline citations and bibliography.
- Optional `.bib` file for cross-checking.
- Access to a browser or `curl`/`httpx` for live checks.

## Outputs

- Verification table: claim, source type, source URL, match status.
- Revised manuscript with unverifiable claims silently omitted.
- Planning Note appended at the end listing omitted items and required verifications.

## Key Rules

- Every DOI, URL, citation, dataset name, author, and numerical claim must be verified against a real external source.
- Unverifiable claims are silently omitted from the body — no `[DECLARATION: ...]` markers.
- A "Planning Note" at the end lists what was omitted and what the user must provide.
- Use only real, verifiable sources. Never fabricate a reference to close a gap.
- Record the API or URL queried for each verification so the audit is reproducible.
- Author names are checked in display order against the publisher's official record.
- Numerical claims must match on metric, value, unit, and experimental setting.

## Examples

Before (body):

```
Recent work shows an accuracy of 97.4% on ImageNet [Smith et al. 2024,
doi:10.1000/fake123].
```

After (body):

```
Recent work reports strong accuracy on ImageNet [verified reference].
```

Planning Note (appended):

```
Planning Note:
- Omitted claim: "accuracy of 97.4%" — DOI 10.1000/fake123 returned 404
  from Crossref. Provide a corrected DOI or the original paper's Table 3
  values for verification.
```

Verification table (excerpt):

```
| Claim                  | Source Type | Source URL                                      | Match |
|------------------------|-------------|--------------------------------------------------|-------|
| accuracy 97.4%         | DOI         | https://api.crossref.org/works/10.1000/fake123   | 404   |
| ImageNet dataset       | Registry    | https://registry.identifiers.org/registry/miriam | Yes   |
| Smith et al. 2024      | Search      | https://api.semanticscholar.org/...              | No    |
```
