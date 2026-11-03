---
name: assessment-designer
description: Design formative and summative assessments including MCQs with distractor analysis, short-answer rubrics, project rubrics, and peer-review forms. Use when the user asks to build quizzes, write assessment plans, or design peer-review forms.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [assessment, mcq, rubric, formative, summative, peer-review]
related: [teaching-pedagogy/rubric-builder, teaching-pedagogy/learning-objective-writer, teaching-pedagogy/formative-feedback-writer]
prerequisites: []
outputs: [markdown, csv]
difficulty: intermediate
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Assessment Designer

## When To Use

- The user asks to "write a quiz", "design a midterm", or "build a peer-review form".
- A course needs both formative checkpoints and summative measures tied to the same objectives.
- An existing item bank must be audited for distractor quality and Bloom alignment.
- A project-based assessment needs milestones, deliverables, and weighting.
- Trigger keywords: assessment, MCQ, distractor analysis, rubric, peer review, blueprint.

## Workflow

1. List the objectives the assessment must cover and decide formative (low-stakes, feedback) vs summative (high-stakes,
   grade).
2. Choose item types: MCQ for breadth, short answer for recall and explanation, performance for application.
3. Draft MCQs with one correct answer and 3-4 plausible distractors; document why each distractor is plausible.
4. Draft short-answer prompts with a model answer and a 3-level rubric (full / partial / no credit).
5. For project-based assessment, define deliverables, milestones, weighting, and a peer-review stage.
6. Build a peer-review form with 3-5 criteria and a calibration sample so reviewers anchor judgments.
7. Pilot the assessment on a small sample; record item statistics if the prior cohort exists.
8. Run a distractor analysis after first administration: flag items with low discrimination or non-functioning
   distractors.
9. Assemble the assessment blueprint: objective × item × Bloom level × points × time.
10. Document accommodations (extended time, assistive tech) and the time budget per item.
11. Map formative to summative: every summative item should have a formative sibling that rehearsed it.

## Inputs

- Objectives to assess with their Bloom levels.
- Class size, time available, and modality (in-class, take-home, online proctored).
- Prior item bank with statistics, if one exists.
- Grading scale and rubric conventions used in the program.

## Outputs

- `assessment_blueprint.csv` — objective × item × points × Bloom level × time.
- `mcq_bank.md` — items with keyed answer, distractor rationale, and Bloom tag.
- `short_answer_rubric.md` — model answers and 3-level scoring guides.
- `project_rubric.md` — analytic rubric for project-based work.
- `peer_review_form.md` — structured review template with calibration sample.

## Key Rules

- Every assessment item must trace to a stated objective; orphan items are removed.
- MCQ distractors must be plausible to a learner who has not mastered the objective — each one targets a documented
  misconception.
- Avoid "all of the above" and "none of the above" — they inflate scores without measuring mastery.
- Peer review must include a calibration sample so reviewers anchor their judgments.
- Blueprint weights must match the cognitive demand distribution of the objectives.
- Time budget per item must respect the median student's reading speed, not the fastest.
- A summative item should have a formative sibling that rehearsed it earlier in the course.

## Examples

```text
MCQ with distractor analysis:
Q: Which Python construct raises StopIteration?
Correct (keyed): next() on an exhausted iterator.
Distractor A: break inside a for loop — plausible because both
  interrupt iteration, but break exits the loop without raising.
Distractor B: return inside a generator — plausible because both
  end the function, but return with a value raises StopIteration
  carrying that value, which is not what the question asks.
Distractor C: yield from [] on an empty list — plausible because
  it produces no values, but it completes normally.
Bloom level: Understand.
```

```text
Blueprint sample (midterm, 60 min):
Objective | Item | Type        | Bloom      | Pts | Time
O1        | Q1   | MCQ         | Remember   |  2  | 1 min
O1        | Q2   | MCQ         | Understand |  3  | 2 min
O2        | Q3   | Short ans.  | Apply      |  6  | 8 min
O3        | Q4   | Scenario    | Analyze    | 10  | 18 min
O4        | Q5   | Essay       | Evaluate   | 12  | 25 min
                                          = 33 pts, 54 min + 6 min buffer
```

```text
Peer-review form (3 criteria):
1. Argument clarity (1-4): does the thesis map to body paragraphs?
2. Evidence quality (1-4): are sources credible and cited correctly?
3. Mechanics (1-4): grammar, spelling, citation format.
Calibration sample: anchor paper at level 3 attached.
```
