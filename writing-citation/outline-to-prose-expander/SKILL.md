---
name: outline-to-prose-expander
description: Expands a bullet outline into flowing academic prose where each bullet becomes a 3-5 sentence paragraph with topic sentence, evidence, and transition. Use when converting a section outline into a first draft, or when an author hands off bullets and asks for "real paragraphs." Inserts `[CITATION NEEDED]` placeholders rather than fabricating sources.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: writing-citation
tags: [outline, prose, paragraphs, topic-sentence, transition]
related: [writing-citation/imrad-thesis-writer, writing-citation/paragraph-transition-smoother]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Outline to Prose Expander

## When To Use
- You have an approved section outline and need to draft the prose.
- A co-author shared bullet points and asked for paragraphs.
- You are turning presentation slides into a written report.
- A reviewer says "this reads like a list" and wants connected prose.

## Workflow
1. Parse the outline: identify headings (level 1/2/3) and bullet items.
2. For each bullet, draft a topic sentence that states the bullet's main claim.
3. Add 1-2 supporting sentences: elaboration, definition, or evidence.
4. Add a transitional sentence that bridges to the next bullet (conceptual, not formulaic).
5. Where a claim requires support, insert `[CITATION NEEDED]` rather than inventing a reference.
6. Preserve every factual assertion from the bullet — do not add or drop facts.
7. Run a coherence check: each paragraph must have exactly one main idea; split if a paragraph carries two.
8. Verify word count per paragraph is in the 3-5 sentence range (looser for thesis paragraphs).
9. Emit the expanded prose with `[CITATION NEEDED]` markers aggregated into a follow-up task list.

## Inputs
- A bullet outline (Markdown, plain text, or slide bullets).
- The intended section type (Introduction, Methods, Results, Discussion) — affects tense and tone.
- Optional known citations to insert where the agent is confident.

## Outputs
- `expanded_prose.md` — paragraphs in order, one per bullet.
- `citation_tasks.md` — list of `[CITATION NEEDED]` markers with the surrounding claim, for follow-up.
- `outline_diff.md` — mapping of each bullet to its resulting paragraph (audit trail).

## Key Rules
- Never fabricate a citation. If a claim needs support, insert `[CITATION NEEDED]`.
- Every factual assertion in the outline must appear in the prose; none may be dropped.
- Each paragraph must have exactly one main idea.
- Transitions must be conceptual (the last sentence introduces the next paragraph's topic), not formulaic.
- Tense must match the section type: past for Methods/Results, present for established facts, present perfect for prior work.
- Do not pad paragraphs with filler; if a bullet's content genuinely yields only 2 sentences, leave it at 2.

## Examples
```text
Before (outline):
- Federated learning trains models across many devices without moving raw data.
- This protects privacy but introduces heterogeneity challenges.
- Recent work addresses heterogeneity via personalization.

After (prose):
Federated learning trains a shared model across many client devices without
transferring the underlying raw data to a central server [CITATION NEEDED].
This decentralized training pattern protects user privacy by construction,
since only model updates — not the data itself — leave the device. However,
the same property that protects privacy also introduces statistical
heterogeneity: clients differ in their data distributions, local sample
counts, and hardware capabilities, which can slow convergence and degrade
global accuracy. Recent work has begun to address this heterogeneity by
introducing personalization mechanisms that allow each client to maintain a
tailored model while still contributing to a shared global representation
[CITATION NEEDED]. These mechanisms, in turn, raise the question of how
much personalization is appropriate before the global model loses coherence.
```

```text
citation_tasks.md excerpt:
  [CITATION NEEDED] #1 — claim: "Federated learning trains a shared model
      across many client devices without transferring the underlying raw data."
      Suggested search: "McMahan et al. 2017 federated learning."
  [CITATION NEEDED] #2 — claim: "personalization mechanisms that allow
      each client to maintain a tailored model..."
      Suggested search: "Collins et al. 2021 personalization federated."
```

## References
- Williams, J. M., & Colomb, G. G. *The Craft of Argument*. University of Chicago Press.
- Toulmin, S. *The Uses of Argument* (for claim-evidence structure).
- Graff, G., & Birkenstein, C. *They Say / I Say: The Moves That Matter in Academic Writing*. Norton.
