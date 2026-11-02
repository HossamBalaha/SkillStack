---
name: grace-degradation-protocol
description: When a factual claim cannot be verified from the source text, either silently omit the claim or insert a `[Verify Source]` placeholder — never fabricate. Use during humanization or rewriting whenever a citation, name, date, number, or quote cannot be confirmed, so the narrative stays cohesive without inventing evidence.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [humanization, hallucination-prevention, citations, fallback]
related: [ai-text/ai-text-humanizer, ai-text/inflation-stripper, ai-text/citation-hallucination-detector, style-integrity/zero-fabrication-guard]
prerequisites: [ai-text/ai-text-humanizer]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Grace Degradation Protocol

## When To Use

- `ai-text-humanizer` is rewriting text and a cited fact cannot be confirmed against source material.
- `inflation-stripper` removed a significance claim and the underlying fact is missing.
- `citation-hallucination-detector` flagged a citation as hallucinated and a replacement is needed.
- You are tempted to invent a plausible-sounding statistic to fill a gap. Stop and use this protocol instead.
- A rewrite would otherwise leave a coherence hole that breaks the narrative.

## Workflow

1. Identify the unverifiable claim: a citation, name, date, number, quote, or attributed opinion.
2. Attempt verification through the appropriate channel:
    - Citation → `citation-hallucination-detector` (Crossref, Scholar, Ulrichsweb).
    - Number or statistic → original source material, dataset, or report.
    - Quote → the original primary source.
    - Name → public record, organizational page, or attributed source.
3. If verification succeeds, use the verified fact and cite the source.
4. If verification fails, choose between two graceful outcomes:
    - **Silent omission**: if the claim is not load-bearing, delete the sentence or clause. Patch pronoun references and
      transitions so the omission does not leave a visible hole.
    - **`[Verify Source]` placeholder**: if the claim is load-bearing (the argument depends on it), keep the claim's
      structure but replace the unverifiable fact with the literal placeholder `[Verify Source]`. The placeholder
      travels with the document until a human resolves it.
5. Never fabricate. Do not invent a citation, name, date, number, or quote. Do not invent a "plausible" replacement.
6. Maintain cohesive professional narrative in the body. Do not insert meta-commentary like `[DECLARATION: omitted]`,
   `[REWRITTEN]`, `[OMITTED FOR VERIFICATION]` inside the prose. The body reads as finished prose; the log lives
   outside.
7. Append an Omission Log outside the main output. Format:
   `Span omitted/placeholdered | Original claim | Verification attempted | Outcome`.
8. Re-read the body. If a reader cannot tell that anything was omitted (other than the visible `[Verify Source]`
   placeholders, which are intentional), the protocol has succeeded.

## Inputs

- The text under rewrite.
- Any source material available for verification.
- The list of unverifiable claims flagged by other skills.

## Outputs

- The rewritten text with cohesive body and `[Verify Source]` placeholders where load-bearing claims await verification.
- An Omission Log appended separately, listing every omitted or placeholdered span.
- A verification trail: for each entry, what was checked and where.

## Key Rules

- Never fabricate. No invented citations, names, dates, numbers, or quotes.
- Choose silent omission when the claim is not load-bearing; choose `[Verify Source]` when it is.
- The body never contains `[DECLARATION: ...]`-style meta-commentary. Only `[Verify Source]` is permitted in the body,
  and only where a fact is genuinely missing.
- The Omission Log lives outside the main output, not inside the prose.
- Cohesion matters: omissions must not leave dangling pronouns, broken transitions, or factual gaps a reader notices.
- Re-read the body after each omission. If cohesion broke, patch with a single concrete sentence (only if a real fact is
  available) or restructure.
- `[Verify Source]` is a tracking token, not a citation. It must be resolved before publication.

## Examples

**Silent omission (non-load-bearing):**

```
Original (inflation removed, fact unverifiable):
"The framework stands as a testament to a 2019 McKinsey report claiming 73%
adoption across Fortune 500 companies."

Outcome:
"The framework was adopted by a subset of Fortune 500 companies between 2019 and 2022."

[Omission Log]
- Omitted: "73% adoption across Fortune 500 companies"
- Reason: McKinsey report not located in source material; no verifiable source.
- Verification attempted: Crossref, McKinsey.com search, Google Scholar — no match.
- Outcome: silent omission; replaced with non-numeric qualifier.
```

**`[Verify Source]` placeholder (load-bearing):**

```
Original (citation hallucinated):
"Chen et al. (2023) report a 38% latency reduction (DOI 10.1109/FAKE.2023.99999)."

Outcome:
"Chen et al. (2023) report a 38% latency reduction [Verify Source]."

[Omission Log]
- Placeholdered: DOI 10.1109/FAKE.2023.99999
- Reason: DOI does not resolve on Crossref; paper title not found on Scholar.
- Verification attempted: Crossref API (404), Google Scholar (no match).
- Outcome: claim retained with [Verify Source] because the 38% figure is load-bearing
  for the next paragraph; author must supply a real source or remove the claim.
```

**Wrong vs. right (no meta-commentary in body):**

```
WRONG (meta-commentary in body):
"The framework is widely adopted. [DECLARATION: omitted McKinsey stat for
verification] It supports distributed workloads."

RIGHT (clean body, log outside):
"The framework is widely adopted. It supports distributed workloads."

[Omission Log]
- Omitted: "73% adoption across Fortune 500 companies" — verification pending.
```

## References

- Companion skills: `ai-text-humanizer`, `inflation-stripper`, `citation-hallucination-detector`.
- Weber-Wulff, S., et al. (2023). "Testing of detection signals for AI-generated text." *Patterns* 4(7) — hallucinated
  citations as a documented LLM failure mode.
