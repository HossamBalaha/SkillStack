---
name: learning-objective-writer
description: Write measurable learning objectives using Bloom's revised taxonomy with observable action verbs (analyze, evaluate, create), conditions, and criteria. Use when the user asks to draft learning outcomes, ABCD objectives, or align objectives with assessments.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [learning-objectives, bloom, abcd, measurable, outcomes]
related: [teaching-pedagogy/course-syllabus-designer, teaching-pedagogy/lesson-plan-builder, teaching-pedagogy/exam-question-author]
prerequisites: []
outputs: [markdown, csv]
difficulty: beginner
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Learning Objective Writer

## When To Use

- The user asks to "write learning objectives", "draft outcomes", or "ABC D objectives".
- A course or module needs measurable outcomes before assessments are written.
- Existing objectives must be audited for measurability (e.g., "students will understand X" is rejected).
- Objectives need to be tagged by Bloom level for an alignment matrix.
- Trigger keywords: learning objective, outcome, Bloom, ABCD, measurable verb, condition, criterion.

## Workflow

1. Identify the audience and the cognitive target from Bloom's revised taxonomy: remember, understand, apply, analyze,
   evaluate, create.
2. Pick an observable action verb matched to that level — "analyze", "evaluate", "design" — and avoid "know", "learn",
   "understand".
3. State the condition: "Given [stimulus], the learner will...".
4. State the criterion: "...to [standard] within [constraint].".
5. Specify the audience only if it differs from the default learner.
6. Verify measurability by asking: could two graders agree on whether the objective was met?
7. Cluster objectives by Bloom level so coverage is visible (and gaps are visible too).
8. Map each objective to one assessment item that elicits the same behavior at the same cognitive level.
9. Run the "negation test": if the negation of the objective sounds odd, the objective is too vague.
10. Strip adjectives that cannot be measured ("thorough", "deep", "comprehensive") and replace with quantified criteria.

## Inputs

- Topic, learner level, and prerequisite knowledge.
- Program or course outcomes the objective must support.
- Assessment type planned (MCQ, project, performance, portfolio).
- Time available to teach and assess the objective.

## Outputs

- `objectives.md` — numbered objective list with Bloom level tags.
- `verb_matrix.md` — Bloom level × action verbs used (counts per level).
- `assessment_map.csv` — objective ID → assessment item ID mapping.
- `audit_log.md` — rejected vague verbs with revision rationale.

## Key Rules

- Never use unobservable verbs: "know", "learn", "understand", "be familiar with", "appreciate".
- Every objective must contain a condition and a measurable criterion.
- Bloom level of the objective must match the cognitive demand of its assessment; misalignment invalidates both.
- A single objective addresses one behavior — split compound objectives that have "and".
- Use the Anderson & Krathwohl (2001) revised verb list, not the original 1956 names.
- Avoid jargon the learner cannot operationalize; "synthesize" alone is insufficient without a deliverable.

## Examples

```text
Weak:   "Students will understand recursion."
Strong: "Given a recursive problem statement, the student will
        implement a recursive Python function that passes 8 of 10
        unit tests within 30 minutes."
Bloom level: Apply.
Condition:  "Given a recursive problem statement."
Criterion:  "passes 8 of 10 unit tests within 30 minutes."
```

```text
Verb matrix sample:
Remember:   list, identify, define           (2 objectives)
Understand: summarize, explain, classify     (3 objectives)
Apply:      implement, calculate, demonstrate (4 objectives)
Analyze:    compare, contrast, diagram        (2 objectives)
Evaluate:   critique, justify, prioritize      (1 objective)
Create:     design, compose, propose          (2 objectives)
```

```text
Negation test:
  Objective: "The student will explain photosynthesis."
  Negation: "The student will NOT explain photosynthesis."
  Verdict:  Odd but acceptable — the objective is observable.
  Compare:  "The student will appreciate photosynthesis."
  Negation: "The student will NOT appreciate photosynthesis."
  Verdict:  Sounds wrong because appreciation is internal —
            the objective is unmeasurable. Revise.
```
