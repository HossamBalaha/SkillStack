---
name: grant-proposal-writer
description: Draft competitive grant proposals with Specific Aims (1 page), Background and Significance, Innovation, Approach (preliminary data, methodology, pitfalls, alternatives), Budget Justification, and Biosketch narrative. Use when the user is applying to NIH R01, NSF CAREER, ERC Starting Grant, or comparable funding bodies and needs a structured proposal narrative.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [grant, nsf, nih, proposal, specific-aims]
related: [academic-research/scope-and-aims-writer, academic-research/research-ideation-planner, academic-research/journal-manuscript-writer]
prerequisites: []
outputs: [markdown, latex]
difficulty: advanced
estimated_tokens: 830
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Grant Proposal Writer

## When To Use

- The user says "write an R01 specific aims page" or "draft an NSF CAREER proposal".
- The user is preparing an ERC Starting Grant or comparable application.
- The user needs a Budget Justification or Biosketch narrative.
- Trigger keywords: grant, proposal, specific aims, R01, CAREER, ERC, budget justification, biosketch.

## Workflow

1. Identify the funding body, mechanism, and the program announcement (FOA/NSF solicitation number).
2. Pull the official review criteria: e.g., NIH uses Significance, Innovation, Approach, Investigator, Environment; NSF
   uses Intellectual Merit and Broader Impacts; ERC uses Excellence, Impact, Quality, Implementation.
3. Draft the Specific Aims page (1 page max). Lead with a hypothesis-driven title, a 3-4 sentence rationale, 2-4
   numbered aims, and an impact statement.
4. Draft Background and Significance (2-3 pages). Establish the gap, the field's stakes, and how the work shifts the
   paradigm.
5. Draft Innovation (0.5-1 page). Contrast the proposed approach with the state of the art; name what is
   paradigm-shifting.
6. Draft Approach: preliminary data, methodology per aim, potential pitfalls with alternatives, timeline (Gantt), and
   team roles.
7. Compose Budget Justification: personnel effort, equipment, travel, materials, subcontracts, indirect cost rationale.
8. Draft the Biosketch narrative (NIH SciENcv style: Personal Statement, Positions, Contributions to Science, Honors).
9. For NSF CAREER, add an Education/Integration Plan and Broader Impacts section.
10. For ERC, add a Career development plan and Host institution support letter stub.
11. Run a checklist against the FOA's page limits, font size (11-pt Arial or comparable), and margin requirements.
12. Output a single reviewable PDF-ready LaTeX root with one file per section.

## Inputs

- Funding body and mechanism (NIH R01, NSF CAREER, ERC Starting Grant).
- FOA / solicitation number and link.
- Principal Investigator CV and preliminary data summary.
- Co-Investigator list and roles.
- Budget envelope (direct + indirect).
- Project title and central hypothesis.

## Outputs

- `specific_aims.tex` — 1-page Specific Aims.
- `background_significance.tex`, `innovation.tex`, `approach.tex`.
- `budget_justification.tex`, `biosketch.tex`, `career_plan.tex` (NSF/ERC).
- `gantt.tex` — timeline chart.
- `checklist.md` — compliance checklist against the FOA.

## Key Rules

- Specific Aims page is exactly 1 page; do not exceed.
- Every Aim must be hypothesis-driven and tied to a measurable outcome.
- Approach must include "Potential Pitfalls and Alternative Strategies" per aim.
- Budget Justification must justify every line item; lump sums are not acceptable.
- Biosketch Personal Statement must align with the proposal's aims.
- For NSF, Broader Impacts must be substantive, not boilerplate.
- Page limits, fonts, margins from the official FOA must be respected verbatim.

## Examples

```text
Aim 2 (NIH R01 sample):
"Hypothesis: Topology-regularized aggregation reduces inter-site variance in
federated segmentation of brain MRI.
Aim 2: Develop and validate a persistent-homology regularizer for FedBN
aggregation.
Expected outcome: $\geq 4$ Dice-point improvement over FedBN on 4 multi-site
datasets; deliver a public benchmark."
```

```text
Pitfall/alternative block:
"Pitfall: Sites may drop out mid-training, causing aggregator instability.
Alternative: We will implement a weighted aggregation that re-weights by
surviving client count, with a verified fallback to centralized training
on the remaining sites."
```

## References

- NIH R01 grant page: https://grants.nih.gov/grants/funding/r01.htm
- NSF CAREER program: https://www.nsf.gov/funding/opportunities/career-faculty-early-career-development-program
- ERC Starting Grant: https://erc.europa.eu/funding/starting-grants
- NIH Biosketch format (SciENcv): https://grants.nih.gov/grants/forms/biosketch.htm

## Notes

- Always match section lengths to the FOA's explicit page limits; reviewers penalize non-compliant formatting.
- For Early-Career mechanisms (CAREER, ERC Starting), emphasize PI development alongside research aims.
- Track revisions in a change log to satisfy NIH "Resubmission" letter requirements.
