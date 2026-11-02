---
name: universal-design-builder
description: Apply Universal Design for Learning (UDL) by providing multiple means of engagement, representation, and action/expression. Use when the user asks to design inclusive lessons, scaffold options, or build UDL-aligned activities.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [udl, universal-design, inclusion, engagement, representation, expression]
related: [teaching-pedagogy/accessible-content-designer, teaching-pedagogy/lesson-plan-builder, teaching-pedagogy/assessment-designer]
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

# Universal Design Builder

## When To Use

- The user asks to "apply UDL", "make this inclusive", or "give students choices".
- A lesson or unit needs options for how students engage, receive content, and show learning.
- An instructor wants to remove barriers without lowering the standard.
- A course is being redesigned to serve a heterogeneous learner population.
- Trigger keywords: UDL, Universal Design for Learning, engagement, representation, action and expression, CAST.

## Workflow

1. Identify the learning goal and the variability anticipated in the learner population.
2. Plan multiple means of engagement: recruit interest, sustain effort and persistence, support self-regulation.
3. Plan multiple means of representation: perception, language and symbols, comprehension.
4. Plan multiple means of action and expression: physical action, expression and communication, executive function.
5. For each goal, list at least two options per principle; a single option per principle is not UDL.
6. Build choice points where students select how they engage, how they receive content, and how they show learning.
7. Scaffold executive function with checklists, graphic organizers, and chunked deadlines that fade over time.
8. Provide goal-appropriate challenges without lowering the standard — UDL removes barriers, not rigor.
9. Map each option back to the goal; eliminate options that introduce new barriers (e.g., an uncaptioned video).
10. Document the UDL checkpoints addressed (1.1, 2.1, 3.3, etc.) using the CAST UDL Guidelines 3.0 numbering.
11. Pilot with students and revise based on which options went unused; unused options signal a mismatch.
12. Keep the "expert learner" trajectory in mind: purposeful, motivated, resourceful, knowledgeable, strategic,
    goal-directed.

## Inputs

- Learning goal (must be stable; the goal does not change, the means do).
- Learner variability: language, prior knowledge, motor/sensory, attention, executive function.
- Modality constraints (in-person, online, hybrid) and time available.
- Available materials, technologies, and the accessibility budget.

## Outputs

- `udl_plan.md` — goal × means × options matrix with checkpoint tags.
- `choice_menu.md` — student-facing choice points phrased as options.
- `scaffolds.md` — executive function supports and their fade schedule.
- `checkpoint_map.csv` — UDL checkpoint × activity × evidence collected.

## Key Rules

- The goal is fixed; only the means vary. Do not lower the standard in the name of inclusion.
- Each UDL principle needs at least two options; one option per principle is not UDL.
- Options must not introduce new barriers; an uncaptioned video is not a valid representation option.
- Choice must be authentic — both paths must reach the same goal at the same standard.
- Executive function scaffolds are introduced and faded; they are not permanent crutches.
- Every checkpoint cited must come from the CAST UDL Guidelines (3.0 or later).
- Unused options after a pilot should be revised or removed; they signal a mismatch with the goal.

## Examples

```text
Goal: Students will explain osmosis using the concentration
gradient. (Goal is fixed; means vary.)

Engagement (why): choose context — cooking, medicine, or
  plants — for the example problem.
  Checkpoint 7.1 — optimize choice and autonomy.

Representation (what): read text, watch a captioned animation,
  manipulate a simulation, or listen to a podcast.
  Checkpoints 1.2, 1.3 — alternatives for auditory and visual.

Action/Expression (how): write a paragraph, draw a labeled
  diagram, record a 60-second explanation, or build a physical
  model with osmosis chamber.
  Checkpoints 5.1, 5.2 — multiple media and tools.
```

```text
Scaffold fade schedule (executive function):
Week 1: provide a graphic organizer with all sections pre-filled.
Week 2: provide a graphic organizer with section headers only.
Week 3: students draw their own organizer from a checklist.
Week 4: organizer removed; students self-plan with a one-line
        prompt.
```

```text
Pilot audit:
Option "build physical model" was chosen by 3 of 30 students.
Interview: students did not know where to get materials.
Action: publish a materials kit list at the assignment release;
do not remove the option — the barrier was supply, not interest.
```

## References

- CAST UDL Guidelines (version 3.0) — https://udlguidelines.cast.org/
- Meyer, Rose & Gordon (2014), "Universal Design for Learning: Theory and Practice" — CAST Professional Publishing.
- CAST — UDL on Campus (higher education): https://udloncampus.cast.org/
- Higbee, Goff & Schultz (2017), "Pedagogy and Practice for Universal Design for Learning in Higher Education" — Stylus.
