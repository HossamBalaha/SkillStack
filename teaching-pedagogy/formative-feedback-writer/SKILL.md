---
name: formative-feedback-writer
description: Write formative feedback that is specific, actionable, timely, and growth-oriented using the Hattie and Timperley feedback model. Use when the user asks to draft feedback on student work, peer-review comments, or coaching notes.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [feedback, formative, hattie-timperley, growth-oriented, actionable]
related: [teaching-pedagogy/assessment-designer, teaching-pedagogy/rubric-builder, teaching-pedagogy/active-learning-designer]
prerequisites: []
outputs: [markdown]
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

# Formative Feedback Writer

## When To Use

- The user asks to "give feedback on this essay" or "what should I tell the student?".
- A graded submission needs comments students can act on before the next attempt.
- A peer-review round needs structured prompts so reviewers go beyond "good job".
- A coach is preparing notes for a one-on-one with a learner.
- Trigger keywords: feedback, formative, Hattie, Timperley, growth-oriented, actionable, where-am-I-going.

## Workflow

1. Identify the feedback level: task (the work), process (the strategy), self-regulation (the learner's plan), or self
   (avoid this last one).
2. Restate the goal in the student's own words to anchor the "where am I going?" question.
3. Cite two pieces of evidence showing "how am I going?" — what the student did that met or missed the goal.
4. State one to three specific, actionable next steps answering "where to next?".
5. Choose a forward-looking verb: revise, add, restructure, test — avoid "you should have".
6. Time the feedback so it arrives while the student can still act (before the next attempt, not after the term ends).
7. Calibrate the dose: three to seven points maximum; more overwhelms and reduces revision.
8. Match the feedback channel to the work: written for prose, audio or video for performance, in-person for nuance.
9. Invite a response: ask the student to summarize the feedback in their own words and restate the next step.
10. Track whether the student acted on the feedback in the next submission; flag silent rejection of feedback.
11. Avoid praise-only or self-referential feedback ("you are smart") that does not move the work forward.
12. End with a growth-oriented closing that names the trajectory, not the grade.

## Inputs

- Student work artifact (essay, lab report, project milestone, performance).
- The rubric or success criteria the work is judged against.
- Time available before the student's next attempt.
- Prior feedback the student has received on this skill.

## Outputs

- `feedback.md` — task / process / self-regulation feedback per work, with the three questions answered.
- `feedback_log.csv` — student × feedback point × acted-on (yes / no / partial).
- `feedback_templates.md` — reusable templates per assignment type.
- `student_response_prompt.md` — the prompt asking the student to restate the feedback.

## Key Rules

- Feedback must answer three questions: Where am I going? How am I going? Where to next?
- Self-level feedback ("good job", "you are smart") is the least effective and should be minimized.
- One to three actionable points per submission; more dilutes the effect and overwhelms the student.
- Feedback must be timely: it has no value if it arrives after the student has moved on.
- Feedback is most powerful when it is about the task, then the process, then self-regulation.
- Praise should be effort- or strategy-specific, not trait-based; "your reorganization made the argument clearer" beats
  "you are smart".
- Students must have a chance to act on the feedback before the next graded event.

## Examples

```text
Task-level feedback (essay):
Goal (your words): "Argue that policy X is unjust using two
independent reasons."
How am I going: Your thesis (last sentence of paragraph 1)
names the policy but not the stance, so the reader cannot
predict the argument.
Where to next: Rewrite the thesis as "Policy X is unjust
because [reason 1] and [reason 2]." Then check that each
body paragraph's topic sentence maps to one of those reasons.
```

```text
Process-level feedback (lab report):
How am I going: You calculated the standard deviation for
each group but did not compare them.
Where to next: State which group has the higher spread and
what that means for your hypothesis; one sentence is enough.
```

```text
Self-regulation feedback (project plan):
How am I going: You set a final deadline but no checkpoint,
so slippage will be invisible until too late.
Where to next: Add a midpoint review on the calendar and
define what "on track" looks like at that date.
```

```text
Feedback log sample:
Student | Point                          | Acted on next submission
0123    | Rewrite thesis with two reasons| Yes — thesis now has two reasons
0124    | Compare SDs across groups      | No — same omission in lab 4
Action for 0124: schedule 5-minute office hour before lab 5.
```
