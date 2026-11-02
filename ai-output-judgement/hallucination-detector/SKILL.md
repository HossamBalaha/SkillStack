---
name: hallucination-detector
description: Detect hallucinated content in AI outputs — fabricated entities, fake citations, invented statistics, made-up quotes, and non-existent API methods — by combining token-level confidence, entity verification against Wikidata/Crossref, and cross-source corroboration. Use when an LLM response invents specifics that look plausible but may not exist.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [hallucination, entities, factuality, llm]
related: [ai-output-judgement/factuality-checker, ai-output-judgement/reference-accuracy-checker, ai-output-judgement/groundedness-verifier, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 1900
cost_warning: "Optional: Wikidata and Crossref API calls — mostly free but rate-limited."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Hallucination Detector

## When To Use

- An LLM produced entities (people, organizations, papers, products, APIs) that need existence checks before publishing.
- Trigger keywords: "hallucination", "made up", "fabricated", "phantom citation", "non-existent API", "invented
  statistic".
- A citation-heavy answer must be screened before submission (overlaps with `factuality-checker`, but this skill focuses
  on entity existence rather than atomic truth).
- A code-generation answer references libraries, classes, or methods that may not exist.

## Workflow

1. Extract candidate entities: named entities via spaCy `en_core_web_sm`, plus regex for DOIs, URLs, version strings
   (`v1.2.3`), and API-shaped tokens (`package.Class.method`).
2. For each entity, classify its type: person, organization, paper/journal, DOI, statistic, quote, library, API method,
   law/regulation.
3. Verify existence per type:
    - Person/Org/Place: Wikidata SPARQL search, Wikipedia API.
    - Paper/DOI: Crossref (`https://api.crossref.org/works/{DOI}`) and arXiv API.
    - Library/API: package registry (PyPI JSON API, npm registry, GitHub repo existence via
      `https://api.github.com/repos/{owner}/{repo}`).
    - Statistic: route to `numeric-accuracy-verifier`.
    - Quote: web search for the exact quoted string.
4. If token log-probs are available from the model, flag low-confidence spans (mean log-prob below the 15th percentile
   of the response) as suspicious.
5. Cross-corroborate: require at least two independent sources confirming an entity; one self-cited blog post is not
   corroboration.
6. Assign severity: S1 (cosmetic), S2 (minor inaccuracy), S3 (misleading), S4 (fabricated entity/citation that a reader
   would rely on).
7. Emit flagged spans with offsets, type, evidence, and severity.

## Inputs

- The AI output text (required).
- Optional: token log-probs from the model (improves precision).
- Optional: domain allowlist of known-good entities (skip verification for them).
- Optional: source documents to check whether the entity is supported (route to `groundedness-verifier` if so).

## Outputs

- `hallucinations.jsonl` — one row per flagged span: `text`, `start`, `end`, `type`, `severity`, `evidence`, `action`.
- `hallucination_report.md` — summary counts by severity, top problematic entities, and a clean/flagged diff.
- Severity legend: S1 cosmetic, S2 minor, S3 misleading, S4 fabricated.

## Key Rules

- A fabricated citation or non-existent API is always S4 — readers will act on it.
- Plausible-sounding names are not evidence of existence; require external corroboration.
- A DOI that resolves to a different paper than the one cited is a hallucination, not a typo.
- Do not invent replacement entities during detection — flag only.
- If log-probs are unavailable, fall back to entity-corroboration only; do not silently fail.
- Distinguish hallucination from ungroundedness: this skill checks existence, not whether a claim is in context.

## Examples

```text
AI output: "In Smith et al. (2022) published in the Journal of Computational Phenomena,
the authors introduced the `transformer.aggregate_layers()` method."

Findings:
  - "Journal of Computational Phenomena" — not in Ulrichsweb or Crossref.        S4
  - "Smith et al. (2022)"        — Crossref title search returns no match.         S4
  - "transformer.aggregate_layers()" — PyPI `transformers` has no such method;
    GitHub repo confirms only `model.aggregate()` exists.                         S4
Mean log-prob of the flagged sentence is in the 4th percentile — corroborating signal.
```

```text
AI output: "The Hugging Face `pipeline` class has a `summarize_async()` method since v4.30.0."
Verification:
  - PyPI `transformers` version 4.30.0 exists.
  - `pipeline` class exists, but `summarize_async` is not in the changelog or source tree.
Result: hallucinated method (S4); recommend telling the user to use `pipeline("summarization")`.
```

## Common Pitfalls

- Assuming a plausible-sounding journal or API method exists — always verify against an external registry; plausible
  names are the most common hallucination pattern.
- Treating a Crossref 404 as "fabricated" — it may be a typo or a recently-assigned DOI not yet indexed; flag for human
  review instead.
- Relying on NER alone — structured PII, DOIs, and version strings need regex; spaCy misses them.
- Inventing replacement entities during detection — this skill flags only; corrections are a separate human task.
- Skipping corroboration for entities that appear only in a single self-cited blog — one source is not corroboration.

## References

- Ji, Z. et al. (2023). "Survey of Hallucination in Natural Language Generation." *ACM Computing Surveys* 55
  (12). https://arxiv.org/abs/2202.03629
- Wikidata SPARQL endpoint: https://query.wikidata.org/
- Crossref REST API: https://api.crossref.org/works/{DOI}
- PyPI JSON API: https://pypi.org/pypi/{package}/json — npm registry: https://registry.npmjs.org/{package}
- Companion skills: `factuality-checker`, `reference-accuracy-checker`, `code-output-validator`.
