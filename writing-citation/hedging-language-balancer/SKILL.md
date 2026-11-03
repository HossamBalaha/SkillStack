---
name: hedging-language-balancer
description: Balances hedging (cautious language) to match evidence strength, deploying modal verbs, epistemic adverbs, and tentative reporting verbs where claims outrun the data, and removing excess hedging where claims are well-supported. Use when a draft overclaims or underclaims, or when a reviewer has asked for calibrated language.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [hedging, modals, epistemic, calibrated, claims]
related: [writing-citation/english-academic-editor, writing-citation/tense-consistency-fixer]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Hedging Language Balancer

## When To Use

- A reviewer says your claims are "too strong" or "too cautious."
- The Results section uses "demonstrates" or "proves" for findings that are correlational.
- The Discussion over-hedges a well-powered, replicated result.
- A non-native English author has sprinkled "maybe" or "perhaps" throughout, weakening legitimate claims.

## Workflow

1. Walk the manuscript section by section; tag each claim with its evidence strength (LOW: correlational or
   single-study; MEDIUM: replicated or controlled; HIGH: meta-analytic or causal mechanism).
2. Inventory the hedging devices already present: modal verbs (may, might, could, can), epistemic adverbs (arguably,
   potentially, possibly, likely), tentative reporting verbs (suggest, indicate, appear to, seem to), and probability
   adverbs (probably, likely).
3. Calibrate: LOW-evidence claims require at least one hedging device; HIGH-evidence claims require none (or only a
   softener like "broadly").
4. Remove redundant hedging ("may possibly suggest" → "suggests").
5. Replace informal hedges ("maybe," "kind of") with formal equivalents ("may," "arguably").
6. Strengthen under-hedged LOW-evidence claims by inserting an appropriate modal or reporting verb.
7. Re-read the balanced passage; the resulting claims should be defensible but not timid.
8. Emit a calibration log: claim → evidence strength → hedging added / removed.

## Inputs

- The draft section (Markdown or LaTeX).
- Optional evidence annotations per claim (LOW / MEDIUM / HIGH).
- Optional list of journal-specific stance preferences (e.g., Nature prefers minimal hedging in abstracts).

## Outputs

- `balanced_section.md` — the revised prose with calibrated hedging.
- `hedging_calibration.csv` — claim, evidence strength, original hedge, action taken.
- `overhedging_report.md` — list of redundant hedges that were collapsed.

## Key Rules

- Hedging strength must match evidence strength — never the reverse.
- A single hedging device is sufficient per claim; stacking ("may possibly indicate") is forbidden.
- HIGH-evidence claims (replicated, meta-analytic, or causal-mechanism) require no hedging.
- LOW-evidence claims (correlational, single-study, anecdotal) require at least one hedge.
- Replace informal hedges with formal equivalents.
- Never introduce a hedge that contradicts the data (e.g., hedging a measured p < 0.001 result with "may suggest").
- Reporting verbs ("suggest," "indicate," "demonstrate") carry implicit hedge strength — choose deliberately.

## Examples

```text
Before (overclaim, LOW evidence):
"Our results prove that attention mechanisms cause better accuracy."

After (calibrated):
"Our results suggest that attention mechanisms may contribute to
higher accuracy, though a causal mechanism has not been established."
```

```text
Before (overhedging, HIGH evidence):
"It may possibly seem to suggest, arguably, that the intervention
could perhaps reduce mortality."

After (calibrated, removed redundant hedges):
"The intervention reduced mortality (HR 0.71, 95% CI 0.62-0.81,
p < 0.001) in a meta-analysis of 14 RCTs."

Calibration log:
  claim: "intervention reduces mortality"
  evidence strength: HIGH (meta-analysis of 14 RCTs)
  original hedge: "may possibly seem to suggest, arguably, ... could perhaps"
  action: removed all hedges; rendered with effect size and CI
```

## Common Pitfalls

- Stacking hedges ("may possibly seem to suggest") — one device per claim is enough.
- Removing hedges from LOW-evidence claims because the author "wants to sound confident."
- Adding hedges to HIGH-evidence claims (meta-analyses, causal mechanisms) — this weakens defensible results.
- Using informal hedges ("maybe," "kind of") in formal academic prose.
- Treating all reporting verbs as interchangeable — "demonstrates," "indicates," and "suggests" carry different hedge
  strength.
