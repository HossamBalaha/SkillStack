---
name: staging-tell-remover
description: Remove staging tells that signal importance instead of adding a fact — "Not X but Y" constructions, one-line closers, sayings that sound deep, staged run-ups, and arguing with no one. Use when `ai-text-detector` flags staging-category tells, or when a draft gestures at significance rather than stating it.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [humanization, staging, rewriting, ai-text]
related: [ai-text/ai-text-humanizer, ai-text/ai-text-detector, ai-text/inflation-stripper, ai-text/ai-tell-catalog]
prerequisites: [ai-text/ai-tell-catalog]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 2100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Staging Tell Remover

## When To Use

- `ai-text-detector` flagged staging-category tells (catalog #1-#5).
- A draft repeatedly tells the reader how important something is rather than what it is.
- A passage opens with "Let's dive in" or "Here's what you need to know" before the actual content.
- A sentence argues against a position nobody took ("A tempting approach would be… but").
- A document ends paragraphs with deep-sounding aphorisms that add no information.

## Workflow

1. Identify staging tells using the catalog (#1 Not X but Y; #2 one-line closers; #3 sayings that sound deep; #4
   staged run-ups; #5 arguing with no one).
2. For each match, locate the underlying factual claim.
3. Apply the canonical fix:
    - **Not X but Y**: collapse to a single direct statement. "It's not merely a report, it's a manifesto" → "The report
      also functions as a manifesto."
    - **One-line closers**: delete the sentence. The prior sentence already makes the point.
    - **Sayings that sound deep**: replace the aphorism with a concrete claim. "Symmetry is the language of trust" →
      "Symmetric layouts feel more predictable to readers."
    - **Staged run-ups**: delete. "Let's dive in.", "Here's what you need to know." Cut them; the content follows.
    - **Arguing with no one**: state the actual choice. "A tempting approach would be to cache everything, but we chose
      lazy loading" → "We chose lazy loading because writes are infrequent."
4. If the underlying fact cannot be verified, invoke `grace-degradation-protocol`: omit or insert `[Verify Source]`.
5. Re-read for cohesion. Staging removal often leaves a paragraph feeling abrupt; add a single concrete sentence where
   needed.
6. Voice override: if the author's profile shows a genuine habit of aphorism, keep one or two but cut the rest.
7. Emit the rewritten text plus a staging log: `Span removed | Tell type | Replacement`.

## Inputs

- The text containing staging tells.
- Optional: source material to verify underlying facts.
- Optional: voice profile (aphorism-prone authors keep some).

## Outputs

- The rewritten text.
- A staging log: `Span | Tell type (#) | Replacement`.
- A note on which tells were voice-kept (if a profile was applied).

## Key Rules

- Staging signals importance; rewrite to add facts instead.
- One-line closers are deleted, not paraphrased.
- Staged run-ups are deleted unconditionally.
- "Not X but Y" collapses to a single direct statement, never to a new two-clause construction.
- "Arguing with no one" becomes a positive statement of the actual choice.
- Do not invent facts to replace staging; if no fact exists, omit or mark `[Verify Source]`.
- Sayings that sound deep are replaced with concrete claims — never with another aphorism.

## Examples

**Not X but Y:**

```
Before: It's not merely a song — it's a statement about belonging.
After:  The song makes a clear statement about belonging.
```

**One-line closer:**

```
Before: The cache hit rate doubled overnight. And that, ultimately, is the real win.
After:  The cache hit rate doubled overnight.

[Staging log]
- "And that, ultimately, is the real win." | one-line closer (#2) | deleted
```

**Saying that sounds deep:**

```
Before: Symmetry is the language of trust.
After:  Symmetric layouts feel more predictable to readers.
```

**Staged run-up:**

```
Before: Let's dive in. The API exposes three endpoints.
After:  The API exposes three endpoints.
```

**Arguing with no one:**

```
Before: A tempting approach would be to cache everything, but we chose lazy loading.
After:  We chose lazy loading because writes are infrequent and cache invalidation
        was becoming the dominant cost.
```

**Mixed (multiple staging tells):**

```
Before: Let's dive in. It's not merely a refactor, it's a re-architecture. The new
shape handles 3× the load. Symmetry is the language of trust. And that is the real win.

After:  The refactor re-architected the ingestion path; the new shape handles 3× the
        load. Symmetric module boundaries made the layout easier to reason about.

[Staging log]
- "Let's dive in."                                            | run-up (#4)    | deleted
- "It's not merely a refactor, it's a re-architecture."      | Not X but Y (#1) | collapsed to "The refactor re-architected the ingestion path"
- "Symmetry is the language of trust."                       | deep saying (#3) | replaced with concrete claim
- "And that is the real win."                                | closer (#2)     | deleted
```
