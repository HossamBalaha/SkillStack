---
name: severity-classifier
description: Classify detected AI tells into four severity levels (S1 weak, S2 moderate, S3 strong, S4 critical) using specificity and how rarely the pattern occurs in human writing. Use when an `ai-text-detector` run produces raw matches and you need to weight them before issuing a verdict.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [severity, classification, tells, ai-detection]
related: [ai-text/ai-text-detector, ai-text/ai-tell-catalogue]
prerequisites: [ai-text/ai-tell-catalogue]
outputs: [markdown, json]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Severity Classifier

## When To Use

- The detector has produced a list of tell matches and you need to rank them.
- A reviewer wants to know which matches to act on first.
- You are deciding whether to escalate a block to humanizer or merely note it.
- A compliance audit requires a reproducible severity scale across reviewers.
- You need to override a default catalogue severity based on local context.

## Workflow

1. Receive the raw match list from `ai-text-detector` (tell name, location, default severity from the catalogue).
2. For each match, evaluate two axes: (a) specificity — how distinctive is the pattern; (b) human-occurrence rate — how
   often real humans produce it.
3. Map to a level:
    - **S1 Weak**: common in both human and AI writing; low specificity. Note but do not weight heavily.
    - **S2 Moderate**: more common in AI but possible in human writing. Combine with other indicators.
    - **S3 Strong**: rare in human writing, highly characteristic of LLM output. Flag for review or rewrite.
    - **S4 Critical**: almost exclusively found in AI-generated text. Treat as near-confirmation; rewrite or delete.
4. Apply mandatory overrides:
    - Hallucinated DOI, phantom citation, fabricated quote, invented name → S4 regardless of context.
    - Repeated identical opening across 4+ sentences → upgrade by one level.
    - Voice-profile match (target author genuinely uses the pattern) → downgrade by one level, minimum S2.
5. Aggregate: count tells by severity. Apply R1 (cumulative evidence):
    - One S1 alone → no verdict.
    - One S2 alone → no verdict; require a second indicator from a different category.
    - One S3 alone → flag as `Mixed`, request review.
    - Any S4 → near-confirmation regardless of R1.
6. Emit a severity table and the aggregate verdict logic used.

## Inputs

- Raw match list with tell name, location, default severity, category.
- Optional: voice profile of claimed author (to allow downgrades).
- Optional: citation verification results from `citation-hallucination-detector`.

## Outputs

- A severity table: `Tell | Location | Default | Final | Reason`.
- Aggregate counts: `S1=n, S2=n, S3=n, S4=n`.
- The verdict logic chain showing which rule (R1, voice override, S4 override) produced the final label.
- A recommended action: `Note`, `Review`, `Rewrite`, `Delete and re-author`.

## Key Rules

- S4 is reserved for near-certain AI signals. Hallucinated citations are always S4.
- Voice profile overrides can downgrade at most one level and never below S2.
- A single S1 never produces a verdict. Ever.
- Severity is contextual. "Delve" in a fantasy novel is S1; "delve" in a corporate memo is S2.
- When in doubt between two levels, choose the lower. Bias toward fewer false positives.
- Document the override logic so the verdict is reproducible.

## Examples

**Input match list:**

```
1. "delves into"                  | lexical    | default S2
2. "pivotal role"                 | lexical    | default S2
3. "broader landscape"            | thematic   | default S2
4. "leaves an indelible mark"     | thematic   | default S2
5. DOI 10.1109/FAKE.2023.99999    | citation   | default S4
6. Uniform 17-word sentences       | statistical| default S3
```

**Severity table:**

```
| # | Tell                  | Default | Final | Reason                         |
|---|-----------------------|---------|-------|--------------------------------|
| 1 | "delves into"         | S2      | S2    | corporate context, no override |
| 2 | "pivotal role"        | S2      | S2    | corporate context              |
| 3 | "broader landscape"   | S2      | S2    | —                              |
| 4 | "leaves an indelible" | S2      | S2    | —                              |
| 5 | Phantom DOI           | S4      | S4    | mandatory S4 override          |
| 6 | Uniform sentence len  | S3      | S3    | confirmed by scorer            |

Aggregate: S1=0 S2=4 S3=1 S4=1
Verdict: Near-Certain AI (S4 overrides R1)
Action: Delete and re-author; route citation to verifier.
```

**Before/after (with voice profile override):**

```
Before classification: "em-dash as connector" → default S2
Voice profile: target author uses em-dashes in 12% of sentences (baseline 1%).
After classification: S1 (downgraded one level, voice override).
Reason: pattern matches the author's genuine habit, not an AI tell here.
```
