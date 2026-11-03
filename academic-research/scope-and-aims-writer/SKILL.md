---
name: scope-and-aims-writer
description: Draft scope statements, three to four numbered specific aims, and contribution statements, with contributions reserved for the Introduction only and the Methodology focused on technical "how" and domain "why". Use when the user is preparing a thesis scope page, grant Specific Aims, or paper Introduction contributions block.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [scope, specific-aims, contributions, introduction, thesis]
related: [academic-research/research-ideation-planner, academic-research/grant-proposal-writer, academic-research/thesis-chapter-planner]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Scope and Aims Writer

## When To Use

- The user asks to "write my specific aims", "draft scope statement", or "list contributions".
- The user is preparing a thesis scope page, grant aims page, or paper Introduction.
- The user needs the Methodology section focused on technical how + domain why (not contributions).
- Trigger keywords: scope, specific aims, contributions, methodology framing, novelty claim.

## Workflow

1. Read the finalized research question and hypothesis table.
2. Draft a scope statement (3-5 sentences): what the work covers, what it deliberately excludes, and the boundary.
3. Generate 3-4 numbered Specific Aims; each aim is one sentence, hypothesis-driven, with a measurable outcome.
4. For each Aim, add a one-paragraph rationale linking it to the gap and the prior aim.
5. Draft the Contributions block for the Introduction only; list 3-5 bullets starting with "We propose...", "We
   show...", "We release...".
6. In the Methodology section, frame every subsection as: technical how (mechanism) + domain why (the reason this
   mechanism addresses the gap).
7. Audit the document: any "contribution" language in Methodology is removed or relocated to the Introduction.
8. Validate that each Aim has a matching experiment or analysis in the Methodology.
9. Cross-check that contributions are phrased as outcomes, not as restatements of aims.
10. Output the scope/aims/contributions block ready for LaTeX insertion.

## Inputs

- Finalized research question and hypothesis table.
- Methodology outline (or planned experiments).
- Target venue (journal vs. thesis vs. grant).
- Author preference on number of aims (typically 3-4).

## Outputs

- `scope_statement.md` — 3-5 sentence scope with explicit boundaries.
- `specific_aims.md` — numbered aims with rationale.
- `contributions.md` — Introduction-only contributions bullets.
- `methodology_framing.md` — per-subsection technical-how + domain-why framing.
- `audit_log.md` — list of relocated or removed "contribution" mentions in Methodology.

## Key Rules

- Contributions appear ONLY in the Introduction; Methodology describes mechanism, not contribution.
- Each Aim is one sentence, hypothesis-driven, with a measurable outcome.
- Methodology subsections are framed as "technical how + domain why".
- Contributions are outcome statements ("We show X"), not aim restatements.
- Scope statement must explicitly say what is excluded, not only what is included.
- Every Aim must map to at least one Methodology subsection.

## Examples

```text
Scope statement:
  This work addresses heterogeneity in multi-site brain MRI segmentation
  under federated learning. We focus on structural MRI (T1, T2, FLAIR)
  and exclude functional MRI. We consider non-adversarial aggregation
  methods only; domain-adversarial baselines are referenced as comparators.
```

```text
Aim 1: Characterize inter-site topological shift on the FedBN benchmark.
  Hypothesis: Persistent-homology descriptors differ significantly across
  sites (PERMANOVA p < 0.001). Outcome: per-site topology descriptor table
  + statistical test.
Aim 2: Develop a topology-regularized aggregator (FedTopo).
Aim 3: Validate on 4 multi-site datasets; release code + benchmark.
```

```text
Contributions (Introduction only):
  • We propose FedTopo, the first aggregator that regularizes on
    persistent-homology descriptors across sites.
  • We show that FedTopo reduces inter-site Dice variance by 32%
    compared with FedBN.
  • We release a 4-dataset benchmark and topology-descriptor toolkit
    under an MIT license.
```
