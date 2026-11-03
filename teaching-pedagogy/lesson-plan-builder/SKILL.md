---
name: lesson-plan-builder
description: Build lesson plans using the Hunter lesson design with anticipatory hook, direct instruction, guided practice, independent practice, closure, and formative check. Use when the user asks to draft a single-class lesson plan or sequence daily lessons.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [lesson-plan, hunter-model, direct-instruction, formative-check, closure]
related: [teaching-pedagogy/learning-objective-writer, teaching-pedagogy/active-learning-designer, teaching-pedagogy/formative-feedback-writer]
prerequisites: []
outputs: [markdown]
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

# Lesson Plan Builder

## When To Use

- The user asks for "a lesson plan for one class" or "how to teach X tomorrow".
- A single class session needs a structured sequence with timing and formative check.
- A unit needs daily lesson plans sequenced to build toward a unit-level outcome.
- A substitute teacher needs a plan complete enough to run without the instructor.
- Trigger keywords: lesson plan, Hunter model, anticipatory set, guided practice, exit ticket, closure.

## Workflow

1. State the lesson objective(s) as measurable outcomes tagged to the course outcome map.
2. Set the anticipatory set (hook): a question, demonstration, or discrepant event lasting no more than 5 minutes.
3. Plan direct instruction: chunked explanation with a check for understanding every 4-5 minutes.
4. Design guided practice: instructor and students work examples together at the board or shared screen.
5. Design independent practice: students apply the skill while the instructor circulates and probes.
6. Plan closure: a student summarizes in their own words; the instructor confirms the key points.
7. Embed a formative check (exit ticket, poll, peer explanation) that produces a visible artifact before dismissal.
8. Allocate minutes per segment; reserve a 10% buffer for transitions and questions that run long.
9. List materials, handouts, slides, and required technology with setup notes.
10. Note differentiation: extensions for advanced learners, scaffolds for struggling learners.
11. Add a backup plan if the technology fails or the timing slips.
12. End with a one-line instructor reflection prompt: "What did the exit ticket reveal about tomorrow's plan?".

## Inputs

- Lesson objective(s) with Bloom level.
- Class duration and modality (in-person, online synchronous, hybrid).
- Prior knowledge assumed and the unit context.
- Class size, seating arrangement, and available technology.
- Required materials list and any handouts to distribute.

## Outputs

- `lesson_plan.md` — full plan with timing per segment.
- `slide_outline.md` — slide-by-slide outline with speaker notes.
- `exit_ticket.md` — formative check prompt with expected answers.
- `materials_list.md` — handouts, props, and tech setup checklist.
- `differentiation.md` — extensions for advanced learners and scaffolds for struggling learners.

## Key Rules

- Every lesson segment must connect to the stated objective; orphan activities are removed.
- Anticipatory set must be at most 5 minutes; longer hooks eat instruction time.
- Formative check must be at least 3 minutes and must produce a visible artifact (answer, poll, ticket).
- Closure must be student-voiced, not an instructor summary — the student speaks to confirm understanding.
- Timing must include a 10% buffer; do not fill every minute of the class.
- Materials list must be complete enough that a substitute could run the lesson.
- Direct instruction chunks must be followed by a check for understanding; do not lecture for 20 minutes straight.

## Examples

```text
Lesson: Photosynthesis (45 min, in-person)
0:00-0:05  Hook: "Why do leaves turn yellow in fall?" Show
           two leaves (green vs yellow), ask students to
           predict the difference.
0:05-0:20  Direct instruction: light reactions, Calvin
           cycle. Paired turn-and-talk every 4 min.
0:20-0:30  Guided practice: diagram the cycle on the board
           together, students fill their copy.
0:30-0:40  Independent practice: students label a diagram
           and answer 3 short questions.
0:40-0:43  Closure: one student summarizes the cycle in
           their own words.
0:43-0:45  Exit ticket: "Name two inputs and one output of
           the Calvin cycle."
```

```text
Exit ticket sample (with expected answer):
Q: "Name two inputs and one output of the Calvin cycle."
Expected: inputs — CO2, ATP, NADPH; output — G3P (or glucose).
Look for: at least 2 of 3 correct; if most students miss
"ATP", reteach energy carriers tomorrow.
```

```text
Backup plan (if tech fails):
- If the slide deck cannot load: use the printed diagram
  handout (already in materials_list.md) and proceed to
  guided practice.
- If the timer app fails: use the wall clock and the printed
  agenda taped to the podium.
```
