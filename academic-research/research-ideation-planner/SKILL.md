---
name: research-ideation-planner
description: Propose three or more novel research ideas aligned to a target venue's scope, then convert the user-selected idea into an end-to-end research blueprint. Use when the user asks to brainstorm research topics, plan a paper from scratch, or scope a project for a specific journal or conference such as IEEE TPAMI, Medical Image Analysis, or Nature Scientific Reports.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [ideation, brainstorm, venue, novelty, research-plan]
related: [academic-research/research-question-formulator, academic-research/scope-and-aims-writer, academic-research/grant-proposal-writer]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 810
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Research Ideation Planner

## When To Use
- The user says "I need a research idea" or "help me brainstorm paper topics".
- The user names a target venue (e.g., IEEE TPAMI, Medical Image Analysis, Nature Scientific Reports) and wants aligned ideas.
- The user has selected one idea and needs a full execution blueprint.
- The user wants a week-by-week timeline, repo skeleton, and manuscript outline in one pass.
- Trigger keywords: ideation, blueprint, project plan, scoping, novel idea, research roadmap.

## Workflow
1. Ask the user for the target venue type, broad domain, and any constraints (deadline, compute, data access).
2. Pull the venue's aims and scope from its official page; extract 3-5 scope keywords.
3. Generate at least three candidate ideas. For each, write a one-paragraph pitch covering problem, novelty hook, and method sketch.
4. Score each idea on novelty (1-5), feasibility (1-5), and venue fit (1-5). Present the scored table.
5. Wait for the user to select one idea (do not auto-proceed).
6. For the selected idea, draft an executive summary (200-300 words) covering motivation, gap, contribution, and expected outcome.
7. Build a week-by-week timeline (typically 12-24 weeks) with milestones: literature, data, implementation, experiments, drafting, revision, submission.
8. Produce a repository directory tree (`src/data`, `src/models`, `src/utils`, `Configs/`, `manual/chapters`, `manual/images`, `manual/scripts`, `Datasets.md`, `Requirements.txt`, `CreateProjectZip.py`, `Main.py`).
9. Outline the mathematical formulation: notation, objective function, constraints, and key assumptions.
10. Generate a modular code generation menu: list each module with its responsibility and inputs/outputs.
11. Draft the manuscript structure with section headings and one-line scope per section.
12. Append mandatory back-matter templates: CRediT, Funding, IRB, Informed Consent, Data Availability, Conflicts, Abbreviations.

## Inputs
- Target venue name or venue type (journal/conference).
- Domain or subfield (e.g., medical image segmentation, federated learning).
- Hard constraints: deadline, available GPUs, dataset access, team size.
- Optional: prior work or seed idea from the user.

## Outputs
- `idea_pitch_table.md` — 3+ scored candidate ideas.
- `executive_summary.md` — selected idea narrative.
- `timeline.md` — week-by-week milestones.
- `repo_tree.txt` — directory tree.
- `math_outline.md` — notation and objective sketch.
- `code_menu.md` — modular code generation list.
- `manuscript_outline.md` — section structure.
- `backmatter_templates.tex` — journal-required sections.

## Key Rules
- Never proceed past ideation without explicit user selection of one idea.
- Every idea must state its novelty hook in one sentence; vague "improves performance" is not acceptable.
- Timeline must include buffer weeks for revision and rebuttal.
- Math outline must distinguish assumptions from derived results.
- Back-matter templates must match the venue's author guide; do not invent sections.
- Cite the venue's official aims and scope URL in the executive summary.

## Examples
```text
Input: "Plan a paper on federated medical imaging for Medical Image Analysis."

Output idea (1 of 3):
  Title: Heterogeneity-Aware Federated Segmentation via Topology-Regularized Aggregation
  Novelty hook: First to combine persistent-homology regularization with FedBN for multi-site MRI.
  Scores: Novelty 5, Feasibility 3, Venue fit 5.
```
```text
Timeline sample:
  Week 1-2:   Literature deep-dive + PRISMA-style gap matrix
  Week 3-4:   Reproduce two baselines
  Week 5-8:   Implementation of proposed aggregator
  Week 9-12:  Experiments on 4-site MRI dataset
  Week 13-15: Ablations and statistical testing
  Week 16-18: Drafting
  Week 19-20: Internal review
  Week 21:    Submission
```

## References
- IEEE TPAMI aims and scope: https://www.computer.org/publications/tpami/about
- Medical Image Analysis author guide: https://www.sciencedirect.com/journal/medical-image-analysis/publish/guide-for-authors
- Nature Scientific Reports submission guide: https://www.nature.com/srep/publish/guidelines
