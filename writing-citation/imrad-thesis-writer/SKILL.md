---
name: imrad-thesis-writer
description: Drafts full IMRaD theses and dissertations with strict cross-chapter non-redundancy, keeping contributions only in the Introduction, technical detail only in Methods, neutral reporting in Results, and interpretation in Discussion. Use when scaffolding or revising a multi-chapter thesis, dissertation, or long-form research monograph.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [imrad, thesis, dissertation, structure, non-redundancy]
related: [writing-citation/outline-to-prose-expander, writing-citation/structured-abstract-writer]
prerequisites: []
outputs: [markdown, latex]
difficulty: advanced
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# IMRaD Thesis Writer

## When To Use
- You are starting a thesis or dissertation and need a chapter-by-chapter skeleton that respects IMRaD.
- A draft has duplicated content — definitions in Chapter 2 reappear verbatim in Chapter 5.
- The advisor flagged "proposal language" (e.g., "we will investigate") surviving in the Methods chapter.
- The Results chapter drifts into interpretation that belongs in the Discussion.

## Workflow
1. Confirm the institutional template (chapter names, front matter, required sections).
2. Outline the four core chapters: Introduction, Methods, Results, Discussion (plus Lit Review as a separate chapter if required).
3. Assign each piece of content to exactly one chapter using a content-ownership table; mark everything else as "reference back."
4. Draft the Introduction with: problem statement, gap, research questions/hypotheses, and contributions — contributions appear ONLY here.
5. Draft Methods in two voices: the technical "how" (apparatus, algorithms, parameters) and the domain "why" (justification per cited precedent); excise all "we will" / "we plan to" phrasing.
6. Draft Results as neutral reporting — figures, tables, statistics — with no interpretive verbs ("surprisingly," "interestingly") and no comparison to prior literature.
7. Draft Discussion by interpreting findings, comparing to literature, listing limitations and future work; pull numbers from Results via cross-reference ("As shown in Table 4.3...") rather than restating.
8. Run a cross-chapter redundancy check: every definition, table, or argument must appear in exactly one chapter; downstream mentions must use phrases like "As detailed in Section 2.3".
9. Verify tense conventions: past tense for Methods and Results, present for established facts, present/present perfect for Discussion comparisons.

## Inputs
- Source materials: prior proposal, lab notes, paper drafts, references.
- Institutional thesis template (chapter list, style guide).
- Content-ownership table (which chapter "owns" each definition, table, argument).

## Outputs
- `thesis_outline.md` — chapter-by-chapter outline with section-level bullet points.
- `content_ownership.csv` — map of content element → owning chapter → referencing chapters.
- `draft_chapter_N.md` per chapter, with cross-references rendered as placeholders ("See Section 2.3").
- `redundancy_report.md` — flagged duplicate passages with suggested remediation.

## Key Rules
- Contributions belong ONLY in the Introduction; the Discussion may re-state implications but not list new contributions.
- Methods must use past tense and must avoid proposal language ("will," "intend to," "we plan").
- Results must be neutral; interpretation verbs ("surprisingly," "importantly") are forbidden here.
- Any content reused across chapters must be cross-referenced, not re-typed.
- Each figure/table is defined in exactly one chapter; other chapters cite by number.
- Limitations live in the Discussion, not in Methods or Results.

## Examples
```text
Before (redundant, mixed voice):
Chapter 2: "A recurrent neural network (RNN) is a class of neural networks
where connections form a directed cycle, allowing the network to maintain
state across time steps."
Chapter 5: "We use a recurrent neural network (RNN), which is a class of
neural networks where connections form a directed cycle, allowing the
network to maintain state across time steps. Our RNN achieved 92% accuracy."

After (cross-referenced, voice-correct):
Chapter 2: "A recurrent neural network (RNN) is a class of neural networks
in which connections form a directed cycle, allowing the network to maintain
state across time steps."
Chapter 5: "Building on the RNN formalism defined in Section 2.3, the
proposed model achieved 92% accuracy (Table 5.1) on the held-out test set."
```

```text
Methods (correct, past tense, no proposal language):
"We trained each model for 50 epochs using the Adam optimizer (lr = 1e-3)
on a single NVIDIA A100 GPU. Hyperparameters were selected via 5-fold
cross-validation on the training split."

Discussion (correct, interpretation):
"The 92% accuracy exceeded the 84% baseline reported by Lee et al. [12],
likely because the dual-attention mechanism (Section 4.2) reduces sequence-
length sensitivity — a known weakness of vanilla RNNs."
```

## References
- Swales, J. M. (1990). *Genre Analysis: English in Academic and Research Settings*. Cambridge University Press.
- Booth, W. C., Colomb, G. G., & Williams, J. M. *The Craft of Research*. University of Chicago Press.
- Institutional graduate-school thesis formatting guides (consult your institution's dissertation office).
