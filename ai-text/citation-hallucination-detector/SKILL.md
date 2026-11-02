---
name: citation-hallucination-detector
description: Detect hallucinated citations by verifying DOIs via Crossref, paper titles via Google Scholar or publisher sites, author-journal-name matches, and "featured in regional trade publications" claims with no verifiable source. Use when a passage cites papers, DOIs, or journals that may be fabricated, or when `ai-text-detector` flags citation-category tells (always S4).
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [citations, hallucination, doi, verification]
related: [ai-text/ai-text-detector, ai-text/grace-degradation-protocol, ai-output-judgement/reference-accuracy-checker]
prerequisites: []
outputs: [markdown, json]
difficulty: intermediate
estimated_tokens: 1900
cost_warning: "Optional: Crossref and Google Scholar API calls may incur costs."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
---

# Citation Hallucination Detector

## When To Use

- `ai-text-detector` flagged citation-category tells.
- A passage cites DOIs, paper titles, or journals that may be fabricated.
- A claim says "featured in regional trade publications" or "widely cited in industry literature" with no names.
- An academic-looking reference list was produced by an LLM and needs verification before submission.
- A reviewer requires evidence that citations resolve before approving a draft.

## Workflow

1. Extract every citation-shaped claim: DOI strings, paper titles in quotes, author+year pairs, journal names, "featured
   in" / "widely cited" claims.
2. For each DOI, query Crossref (`https://api.crossref.org/works/{DOI}`). If the DOI resolves and returns metadata
   matching the cited title and authors, mark `Verified`. If it 404s or returns mismatched metadata, mark
   `Hallucinated`.
3. For each paper title, search Google Scholar or the publisher site. If no exact or near-exact match exists, mark
   `Likely hallucinated`.
4. For each author+year pair, verify the named author exists in the field and published in that year. If the author is
   plausible but the paper is not found, mark `Author plausible, paper not verified`.
5. For each journal name, verify the journal exists (Ulrichsweb, ISSN portal, publisher site). Watch for
   plausible-but-fake names ("Journal of Applied Computational Studies").
6. For "featured in regional trade publications" or "widely cited in industry" with no names, mark
   `Unverifiable claim — no source named`.
7. Cross-check internal consistency: does the cited DOI's metadata actually list the cited authors and title? A DOI that
   resolves to a different paper is a hallucination.
8. Assign severity: every hallucinated citation is S4 (critical), per `severity-classifier`.
9. Emit a verification table and a recommendation: verify with the author, delete the citation, or replace with a
   verified source.

## Inputs

- The text or reference list containing citations.
- Optional: known-good reference corpus to cross-check against.
- Optional: API access to Crossref (default: public API).

## Outputs

- A verification table: `Citation | Type | Verification method | Result | Severity`.
- A list of unverifiable claims with the phrasing flagged.
- A recommendation per citation: `Verified`, `Replace`, `Delete`, `Ask author for source`.
- A summary: `n citations checked, m verified, k hallucinated, j unverifiable`.

## Key Rules

- Every hallucinated DOI or phantom citation is S4. No exceptions.
- A DOI that resolves to a different paper is hallucinated, even if the DOI itself exists.
- Plausible-sounding journal names ("Journal of Contemporary Applied Systems Research") require verification; do not
  assume existence.
- "Featured in regional trade publications" without named publications is unverifiable; flag, do not silently accept.
- If a citation cannot be verified, do not invent a replacement. Route to `grace-degradation-protocol`.
- Crossref's public API is the canonical DOI resolver. A publisher landing page alone is not enough for journals
  Crossref does not index — note the gap.
- Author plausibility is not verification. A real author's name attached to a non-existent paper is still hallucinated.

## Examples

**Verification table:**

```
| Citation                                              | Type      | Method          | Result                | Sev |
|-------------------------------------------------------|-----------|-----------------|-----------------------|-----|
| Chen et al. (2023), DOI 10.1109/FAKE.2023.99999        | DOI       | Crossref API    | 404 — DOI not found   | S4  |
| "Federated learning at the edge: a comprehensive…"    | title     | Scholar search  | no match              | S4  |
| Journal of Applied Computational Studies              | journal   | Ulrichsweb      | not listed            | S4  |
| Smith, J. (2019), Advances in Neural Processing        | author+yr | author lookup   | author plausible,     | S3  |
|                                                       |           |                 | paper not found       |     |
| "featured in regional trade publications"             | vague     | —               | no source named       | S4  |
| Vaswani et al. (2017), DOI 10.48550/arXiv.1706.03762  | DOI       | Crossref/arXiv  | verified, matches     | OK  |

Summary: 6 citations checked, 1 verified, 4 hallucinated, 1 unverifiable.
Recommendation: delete hallucinated citations; route unverifiable claim to author.
```

**Plausible-but-fake example:**

```
Cited: Patel, R., & Nguyen, T. (2022). "Adaptive routing in mesh networks."
       Journal of Network Systems, 14(2), 88-103.

Detection:
- Crossref: no DOI attached; search by title returns no match.
- Google Scholar: no exact title match; similar titles exist but with different authors.
- Ulrichsweb: "Journal of Network Systems" not listed; ISSN lookup fails.
Result: hallucinated (S4).
Author names plausible (real surnames in the field) but the paper is not real.
```

**Author plausible, paper not:**

```
Cited: LeCun, Y., Bengio, Y., & Hinton, G. (2015). "Deep learning reinvents vision."

Detection:
- Authors are real and well-known.
- Crossref and Scholar: no paper with this exact title by these authors in 2015.
- Closest real paper: LeCun, Bengio, Hinton (2015), "Deep learning", Nature 521.
Result: author plausible, paper title fabricated (S3 → S4 because title mismatch).
```

## References

- Crossref REST API: https://api.crossref.org — canonical DOI resolver.
- Google Scholar: https://scholar.google.com — title and author search.
- Ulrichsweb (serials directory) and the ISSN Portal (portal.issn.org) for journal verification.
- Weber-Wulff, S., et al. (2023). "Testing of detection signals for AI-generated text." *Patterns* 4(7) — documents
  hallucinated citations as a strong AI signal.
- Companion skills: `ai-text-detector`, `severity-classifier`, `grace-degradation-protocol`.
