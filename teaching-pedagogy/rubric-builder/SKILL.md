---
name: rubric-builder
description: Build analytic and holistic rubrics with criteria, performance levels, descriptors, and point allocation. Use when the user asks to create grading rubrics, score essays or projects, or design consistent scoring guides.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [rubric, analytic, holistic, grading, descriptors]
related: [teaching-pedagogy/assessment-designer, teaching-pedagogy/formative-feedback-writer, teaching-pedagogy/exam-question-author]
prerequisites: []
outputs: [markdown, csv]
difficulty: intermediate
estimated_tokens: 1400
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Rubric Builder

## When To Use

- The user asks for "a rubric for this assignment" or "grading criteria".
- An essay, project, or portfolio needs consistent scoring across graders.
- A course wants to publish grading expectations at assignment release, not at grading time.
- Multiple graders need to be calibrated before scoring a batch.
- Trigger keywords: rubric, analytic, holistic, criteria, performance level, descriptor, calibration.

## Workflow

1. Decide rubric type: analytic (separate score per criterion) or holistic (single overall score). Use analytic when
   feedback per criterion matters; holistic when speed matters.
2. List 3-7 criteria derived from the assignment's objectives — never more than 7 because the grader loses focus.
3. Define 3-5 performance levels with descriptive labels (e.g., Beginning, Developing, Proficient, Exemplary).
4. Write descriptors for each cell (criterion × level) that describe observable behavior in the work, not the learner.
5. Assign point values that sum to the assignment total; ensure intervals reflect real quality gaps, not arbitrary
   fractions.
6. Add a comments column per criterion for personalized feedback that goes beyond the descriptor.
7. Pilot the rubric on a sample submission at each level and revise ambiguous descriptors.
8. Calibrate with a co-grader: independently score the same three samples, then reconcile.
9. Publish the rubric to students when the assignment is released, not when grades are returned.
10. Track inter-rater reliability (Cohen's kappa) across the first batch; aim for kappa ≥ 0.6.
11. Retire descriptors that no submission ever fits (non-functioning descriptors) and revise them.

## Inputs

- Assignment description and the objectives it assesses.
- Sample submissions at different quality levels (anchor papers).
- Grading scale (points or letter) and assignment weight.
- Number of graders and whether calibration is required.

## Outputs

- `rubric_analytic.csv` — criteria × levels × points matrix.
- `rubric_holistic.md` — single-scale narrative rubric with anchor descriptions.
- `descriptors.md` — observable behavior per cell, written in present tense.
- `calibration_samples.md` — anchored submissions at each level, with rationale.
- `calibration_log.md` — grader × sample × score, plus the kappa computed.

## Key Rules

- Descriptors describe the work, not the student; never write "the student is lazy" or "the student is smart".
- Criteria count between 3 and 7; more dilutes focus and slows grading.
- Performance levels between 3 and 5; fewer than 3 collapses gradations, more than 5 overloads the grader.
- Point intervals must reflect meaningful quality differences, not arbitrary fractions like 3.7 vs 3.8.
- The rubric must be shared with students at assignment release, not at grading time.
- A non-functioning descriptor (one that no submission ever fits) must be revised, not left in.
- Inter-rater agreement should be checked on the first batch; revise descriptors if kappa < 0.6.

## Examples

```text
Criterion: Use of evidence
4 Proficient (4 pts): Cites 3+ credible sources, integrated into
  the argument, correctly formatted in APA.
3 Developing (3 pts): Cites 2 sources, mostly well integrated,
  minor formatting errors.
2 Emerging (2 pts): Cites 1 source, poorly integrated or
  misformatted.
1 Beginning (1 pt): No credible sources cited.
```

```text
Holistic rubric (essay, 1-6 scale):
6 — Exceptional: clear thesis, well-structured argument, 3+
   credible sources, no mechanical errors that impede reading.
4 — Competent: thesis present, argument mostly coherent, 2
   sources, minor mechanical errors.
2 — Novice: thesis unclear, argument underdeveloped, 0-1
   sources, frequent mechanical errors.
```

```text
Calibration sample:
Anchor paper A (level 3 — Developing):
"The author cites Smith (2019) and Jones (2020), but the
Jones citation appears in the bibliography without a
corresponding in-text reference. APA format has minor errors
in the volume number."

Independent scores from three graders: 3, 3, 4.
Reconciled: 3 (revised the third grader on the integration rule).
Cohen's kappa after calibration: 0.72 (acceptable).
```
