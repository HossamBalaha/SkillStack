---
name: ai-text-humanizer
description: Rewrite AI-sounding text to restore natural voice and burstiness while preserving every fact, citation, date, name, and number verbatim. Use when a passage reads as machine-generated and needs to read as a human wrote it, or when an `ai-text-detector` verdict triggers a rewrite.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [humanization, rewriting, voice, ai-text]
related: [ai-text/ai-text-detector, ai-text/voice-profile-matcher, ai-text/staging-tell-remover, ai-text/inflation-stripper, ai-text/rhythm-by-rule-fixer, ai-text/formatting-by-rule-cleaner, ai-text/chatbot-residue-cleaner]
prerequisites: []
outputs: [markdown]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# AI Text Humanizer

## When To Use

- An `ai-text-detector` run returned `Likely AI` or `Near-Certain AI`.
- A user says "this sounds like ChatGPT, can you fix it?" or "make this sound human".
- A draft must pass an editor or reviewer who rejects obviously AI-assisted text.
- You are converting chatbot output into publishable prose.
- You want to humanize without inventing or losing any factual content.

## Workflow

1. Run the input through `ai-text-detector` to obtain the evidence table.
2. Group detected tells by category: staging, rhythm-by-rule, inflation, formatting-by-rule, leftovers.
3. For each group, apply the matching specialized skill:
    - staging tells → `staging-tell-remover`
    - inflation tells → `inflation-stripper`
    - rhythm tells → `rhythm-by-rule-fixer`
    - formatting tells → `formatting-by-rule-cleaner`
    - conversational residue → `chatbot-residue-cleaner`
4. Preserve verbatim: every name, date, number, statistic, citation, DOI, URL, and quoted passage.
5. Restore burstiness: vary sentence length, break up uniform rhythm, allow one short sentence then one long.
6. Vary sentence openings so no two consecutive sentences start with the same word or structure.
7. If a target voice profile exists, call `voice-profile-matcher` and let the author's voice override generic rules.
8. For any factual claim that cannot be verified from source material, invoke `grace-degradation-protocol`: silently
   omit or insert `[Verify Source]`. Never fabricate.
9. Re-run `ai-text-detector` on the rewritten output. Aim for `Likely Human` or `Mixed`.
10. If still flagged, iterate once. Do not loop indefinitely — diminishing returns and risk of over-fitting.
11. Produce a diff summary listing each tell removed, the before/after pair, and any omissions logged.

## Inputs

- The AI-sounding text to rewrite (paragraph, section, or full document).
- Optional: original source material so facts can be verified and not invented.
- Optional: target voice profile (writing sample from the desired author).
- Optional: detection evidence from `ai-text-detector` (saves a re-run).

## Outputs

- The rewritten text in plain prose.
- A before/after diff highlighting every change.
- An Omission Log (if `grace-degradation-protocol` was triggered), appended separately from the main output.
- A post-rewrite detection score showing the new verdict.

## Key Rules

- Preserve facts verbatim. Numbers, dates, names, citations, DOIs, and quoted strings must survive the rewrite
  byte-for-byte.
- Never fabricate a citation, name, date, statistic, or quote. If you cannot verify, omit or mark `[Verify Source]`.
- Voice overrides rules. If the target author genuinely uses an em-dash habit, keep it.
- Do not output meta-commentary (`[DECLARATION: ...]`, `[REWRITTEN]`, etc.) inside the prose body.
- Do not loop the rewrite more than twice. A 70% improvement is better than over-engineering.
- Restore natural burstiness: avoid uniform 15-20 word sentences.
- Keep meaning stable. If a reader could not tell which version they read, you have done it right.

## Examples

**Before:**

```
It's worth noting that this approach delves into the pivotal role of caching
in the broader landscape of modern web architecture, ultimately leaving an
indelible mark on performance optimization.
```

**After:**

```
Caching still matters here. Every repeated query hits the database twice, and on
a busy day that doubles the load on a service we already pay for by the minute.
```

**Before (chatbot residue + inflation):**

```
Great question! The 2023 paper by Chen et al. (DOI: 10.1109/FAKE.2023.99999)
stands as a testament to how seamless integration can reshape the field.
Let me know if you'd like me to expand!
```

**After:**

```
Chen et al. (2023, DOI: 10.1109/FAKE.2023.99999) report that integration reduced
latency by 38% in their test cluster.

[Omission Log]
- Original line "stands as a testament to..." was removed: significance claim
  not supported by the cited paper's abstract.
```
