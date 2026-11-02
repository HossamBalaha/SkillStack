---
name: research-question-formulator
description: Formulate research questions using the FINER criteria (Feasible, Interesting, Novel, Ethical, Relevant) and PICO/SPIDER/PCC frameworks. Generate three to five candidate questions ranked by novelty and feasibility. Use when the user is scoping a new study, preparing a thesis proposal, or pre-registering a study's central question.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [research-question, finer, pico, spider, pcc]
related: [academic-research/hypothesis-designer, academic-research/research-ideation-planner, academic-research/scope-and-aims-writer]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 820
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Research Question Formulator

## When To Use

- The user says "what should my research question be", "help me formulate a question", or "is my question FINER".
- The user is preparing a thesis proposal, grant, or pre-registration.
- The user wants multiple candidate questions ranked before committing.
- Trigger keywords: research question, FINER, PICO, SPIDER, PCC, scoping, hypothesis seeding.

## Workflow

1. Collect the broad domain, available data, and the candidate population.
2. Pick a framework: PICO (clinical/intervention), SPIDER (qualitative/mixed), PCC (scoping).
3. Draft 3-5 candidate questions; each phrased as a single interrogative sentence with a measurable outcome.
4. Score each question on FINER: Feasible (1-5), Interesting (1-5), Novel (1-5), Ethical (1-5), Relevant (1-5).
5. Compute a composite score and rank. Flag any question scoring below 3 on Feasibility or Ethical as needs-rework.
6. For the top-ranked question, produce the explicit PICO/SPIDER/PCC breakdown.
7. Write a one-paragraph justification linking the question to a documented gap.
8. Identify data needs, statistical test family, and ethical considerations.
9. Cross-check novelty against a quick literature scan (PubMed / arXiv / Google Scholar).
10. Output the ranked candidates and a finalized question block ready for a protocol.

## Inputs

- Broad domain and target population.
- Available data sources and compute.
- Constraints: ethics approval timeline, team expertise, funding.
- Optional: prior literature scan or seed question.

## Outputs

- `candidate_questions.md` — 3-5 questions with scores.
- `finer_matrix.csv` — question × FINER dimension scores.
- `framework_breakdown.md` — PICO/SPIDER/PCC elements for the top question.
- `gap_justification.md` — paragraph linking the question to a documented gap.
- `finalized_question.md` — final question statement ready for a protocol.

## Key Rules

- Each question is a single interrogative sentence with a measurable outcome.
- Every question is scored on all five FINER criteria.
- Questions scoring <3 on Feasibility or Ethical must be revised or dropped.
- Framework (PICO/SPIDER/PCC) must match the study design.
- Novelty check uses at least one database; cite the closest prior work.
- Output always ends with a finalized, single-sentence question.

## Examples

```text
Candidate Q1: In adult stroke survivors undergoing rehabilitation, does
robot-assisted gait training (RAGT) plus conventional physiotherapy improve
6-minute walk distance at 12 weeks compared to conventional physiotherapy alone?

FINER scores (Q1): F=4, I=4, N=3, E=5, R=5 → composite 21/25 (rank 1)

PICO breakdown (Q1):
  P: adult stroke survivors
  I: RAGT + conventional physiotherapy
  C: conventional physiotherapy alone
  O: 6-minute walk distance at 12 weeks (continuous, meters)
```

```text
Finalized question:
  Among adults (18-80 years) with first-ever ischemic stroke and baseline
  walking speed <0.8 m/s, does 12 weeks of RAGT added to conventional
  physiotherapy increase 6-minute walk distance by >=30 m compared with
  conventional physiotherapy alone?
```

## References

- FINER criteria (Hulley et al., Designing Clinical Research): https://www.lww.com/Designing-Clinical-Research
- PICO framework (Cochrane): https://training.cochrane.org/handbook/current/chapter-02
- SPIDER framework (Cooke, Smith & Booth 2012): https://doi.org/10.1108/20401621211223494
- PCC for scoping reviews (JBI): https://jbi.global/scoping-review

## Notes

- Keep the finalized question stable; downstream hypothesis design depends on it.
- If the question is changed after hypothesis design, the entire downstream chain must be re-validated.
- Mark secondary candidate questions explicitly so they can become future studies.
