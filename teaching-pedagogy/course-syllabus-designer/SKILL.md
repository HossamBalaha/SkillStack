---
name: course-syllabus-designer
description: Design course syllabi that align learning outcomes, weekly schedule, assessment plan, required materials, and policies using backward design. Use when the user asks to build a syllabus, plan a multi-week course, or align outcomes with assessments and policies.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [syllabus, backward-design, course-planning, outcomes, assessment]
related: [teaching-pedagogy/learning-objective-writer, teaching-pedagogy/assessment-designer, teaching-pedagogy/curriculum-mapper]
prerequisites: []
outputs: [markdown, csv]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Course Syllabus Designer

## When To Use

- The user asks for "a syllabus", "course outline", or "14-week plan".
- A new course is being proposed and the catalog entry needs the full document.
- An existing syllabus must be revised to align outcomes with assessments.
- The user wants a backward-design plan starting from desired results, not from a textbook table of contents.
- Trigger keywords: syllabus, backward design, course plan, weekly schedule, outcomes alignment.

## Workflow

1. Identify the desired results: list 4-7 course-level outcomes students should know, do, and value at the end.
2. Determine acceptable evidence: list the assessments (formative and summative) that will reveal mastery of each
   outcome.
3. Plan learning experiences backward from the assessments to weekly activities, not forward from chapter 1.
4. Build the weekly schedule table mapping outcomes, activities, assessments, and materials for every week.
5. Choose required and supplemental materials with ISBN or DOI so they can be verified.
6. Draft course policies: attendance, late work, academic integrity, accessibility accommodations, inclusion.
7. Write the front matter: course title, catalog description, credit hours, prerequisites, modality.
8. Build a transparent grading scheme that weights assessments by Bloom level and outcome.
9. Add the institutional boilerplate required by the registrar (Title IX, disability services, counseling).
10. Stress-test the alignment matrix: every outcome must appear in at least one assessment and one weekly activity.
11. Reserve at least one buffer week for review, catch-up, or guest sessions.
12. Add a student-facing "How to succeed in this course" section with concrete study habits.

## Inputs

- Course title, level (undergrad/grad), credit hours, modality.
- Catalog description and prerequisite chain.
- Program outcomes the course must serve (for the alignment matrix).
- Class size, instructor bandwidth, term length, and holidays.
- Required textbook or open educational resource (OER) choice.

## Outputs

- `syllabus.md` — full syllabus document, ready to export.
- `weekly_schedule.csv` — columns: Week / Topic / Outcomes / Activities / Assessments / Materials.
- `alignment_matrix.md` — outcomes × assessments coverage table.
- `policies.md` — institutional and course-level policies.
- `grading_scheme.md` — weights per category mapped to Bloom level.

## Key Rules

- Every stated outcome must map to at least one assessment; orphan outcomes are removed, not left in.
- Assessment weights must sum to 100% (or to a stated point total) with no hidden categories.
- Required materials must list ISBN or DOI for verification; "any textbook" is not acceptable.
- Policies must include accessibility accommodations and an academic integrity statement.
- Schedule must reserve at least one buffer week for review or catch-up.
- Bloom-level alignment: the cognitive level of the activity must match the cognitive level of the outcome.
- Backward design means evidence comes before activities, never the reverse.

## Examples

```text
Course: CS 350 — Distributed Systems (3 credits, 14 weeks)
Outcome O3: "Diagnose bottlenecks in a distributed system given a trace."
O3 appears in: Week 7 (lecture + lab), Week 11 (case study),
  Final exam Q4-Q6.
```

```text
Weekly row sample (Week 7):
Topic:      Replication and consistency
Outcomes:   O3 (analyze), O5 (evaluate)
Activities: lecture, lab on multi-leader replication, peer code review
Assessments: formative quiz, lab notebook check
Materials:  Tanenbaum Ch 7, assignment 3 brief, trace dataset
```

```text
Grading scheme sample:
Quizzes (formative, weekly)      15%  Bloom: Understand/Apply
Lab notebooks (formative)         15%  Bloom: Apply
Project milestones (summative)    25%  Bloom: Analyze/Evaluate
Midterm (summative)               20%  Bloom: Understand/Apply
Final exam (summative)           25%  Bloom: Analyze/Evaluate
Total                           100%
```
