---
name: numeric-accuracy-verifier
description: Verify numeric computations, statistics, dates, and quantities in AI outputs by parsing values and units, re-computing arithmetic claims, checking dates against known events, and cross-checking quantities against trusted sources. Use when outputs contain numbers that readers will rely on (statistics, financial figures, dates, conversions).
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [numeric, arithmetic, dates, units, verification]
related: [ai-output-judgement/factuality-checker, ai-output-judgement/hallucination-detector, ai-output-judgement/reference-accuracy-checker]
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

# Numeric Accuracy Verifier

## When To Use

- An AI output contains statistics, percentages, financial figures, or dates that will be quoted downstream.
- Trigger keywords: "numeric accuracy", "arithmetic check", "verify statistics", "date check", "unit conversion",
  "REALTIME".
- A reviewer asks "is that number right?" for a figure in a generated report.
- A model is being benchmarked on numeric reasoning (GSM8K-style).

## Workflow

1. Extract numeric claims via regex + spaCy: numbers with units, percentages, currency, dates (ISO and
   natural-language), and quantities ("8 billion", "1.5M cases", "94.2% accuracy").
2. Classify each claim:
    - `arithmetic` — derivable by computation ("15% of 200 is 30").
    - `statistical` — a quantity that must be cross-checked against a trusted source.
    - `date` — must match a known event or document.
    - `conversion` — unit conversion ("100 km/h ≈ 62 mph").
3. For arithmetic claims: parse the operands, re-compute with a deterministic library (Python `decimal` or `fractions`),
   compare. Allow tolerance of 0.5% for floating-point claims.
4. For conversion claims: re-compute using canonical conversion factors; flag if the stated value deviates by more than
   1%.
5. For statistical claims: retrieve a trusted source (Wikipedia, government statistics, peer-reviewed paper) and
   compare; if the trusted source gives a different value, label `REFUTED` with the source value.
6. For date claims: verify against an event knowledge base (Wikidata, Wikipedia infoboxes). Flag obviously impossible
   dates (future events claimed as past, or events before the inventor's birth).
7. Score per claim: `CORRECT`, `INCORRECT` (with the correct value and source), `UNVERIFIABLE` (no trusted source
   available).
8. Emit a per-claim table and an overall numeric accuracy rate.

## Inputs

- The AI output text (required).
- Optional: trusted-source allowlist for statistics (IMF, World Bank, census, peer-reviewed).
- Optional: tolerance overrides (arithmetic 0.5%, conversion 1%).
- Optional: a Wolfram Alpha or sympy backend for symbolic re-computation.

## Outputs

- `numeric_claims.jsonl` — per claim: text, type, value, unit, recomputed_value, status, evidence_url.
- `numeric_report.md` — accuracy rate, top incorrect claims with corrections, unverifiable claims.
- `corrections.md` — proposed text fixes with the corrected value and source.

## Key Rules

- Arithmetic claims must be re-computed, not eyeballed — LLMs frequently produce plausible-looking wrong arithmetic (
  "17% of 460 = 92" is actually 78.2).
- Conversion factors must use canonical sources (NIST, BIPM SI brochure); do not trust the model's stated factor.
- Dates must be checked against a knowledge base — an LLM can confidently misplace an event by a year or a decade.
- Statistical claims without a retrievable source are `UNVERIFIABLE`, not `CORRECT`.
- Tolerances must be documented; silent tolerance changes break audit trails.
- Currency claims must include the date of the rate (exchange rates drift); a number without a date is suspect.

## Examples

```text
Output: "15% of 460 is 92."
Type: arithmetic.  Recomputed: 0.15 * 460 = 69.0.  Stated 92.
Status: INCORRECT.  Correction: "15% of 460 is 69."
```

```text
Output: "The world population reached 8 billion in November 2022."
Type: date + statistical.
Date check: Wikidata Q... confirms UN projected 8 billion on 15 Nov 2022.
Source value: 8,000,000,000 (UN World Population Prospects).
Status: CORRECT. Evidence: https://www.un.org/en/desa/world-population-reach-8-billion-15-november-2022
```

```text
Output: "The speed of light is about 3 × 10^8 m/s, which is roughly 186,000 miles per second."
Type: conversion.
Recomputed: 299,792,458 m/s → 186,282.4 mi/s.
Stated 186,000. Deviation 0.15% < 1% tolerance.
Status: CORRECT (rounded).
```

## Common Pitfalls

- Eyeballing arithmetic — LLMs frequently produce plausible-looking wrong arithmetic (e.g., "17% of 460 = 92" is
  actually 78.2); always recompute deterministically.
- Accepting currency conversions without a date — exchange rates drift; a number without a date is suspect.
- Changing tolerances without recording — audit trails break; document tolerance per claim type.
- Accepting statistical claims without a retrievable source — label UNVERIFIABLE, not CORRECT.
- Using the model's stated conversion factor — always use canonical sources (NIST, BIPM SI brochure).
- Trusting dates that "sound right" — verify against a knowledge base; an LLM can confidently misplace an event by a
  decade.

## References

- Gupta, A. et al. (2024). "REALTIME: A Benchmark for Reasoning About Numeric and Temporal
  Information." https://arxiv.org/abs/2402.18949
- Cobbe, K. et al. (2021). "Training Verifiers to Solve Math Word Problems." (GSM8K) https://arxiv.org/abs/2110.14168
- NIST Reference on Constants, Units, and Uncertainty: https://physics.nist.gov/cuu/Units/
- Companion skills: `factuality-checker`, `hallucination-detector`, `reference-accuracy-checker`.
