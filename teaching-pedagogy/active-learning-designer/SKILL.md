---
name: active-learning-designer
description: Design active-learning activities including think-pair-share, jigsaw, case-based learning, and peer instruction with ConcepTests. Use when the user asks to convert a lecture to active learning, build ConcepTests, or design small-group structures.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [active-learning, think-pair-share, jigsaw, peer-instruction, case-based]
related: [teaching-pedagogy/lesson-plan-builder, teaching-pedagogy/formative-feedback-writer, teaching-pedagogy/universal-design-builder]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 1600
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Active Learning Designer

## When To Use

- The user asks to "make this lecture active" or "add peer instruction".
- A concept is known to be misunderstood by most students (the misconception is documented).
- A 50-minute lecture needs to be broken into segments with student-produced artifacts.
- A jigsaw activity is needed for a topic that splits into independent sub-questions.
- Trigger keywords: active learning, think-pair-share, jigsaw, peer instruction, ConcepTest, case-based.

## Workflow

1. Identify the concept where students typically hold a misconception; this becomes the active-learning target.
2. Select the structure matched to the cognitive demand: think-pair-share (recall/apply), jigsaw (synthesize multiple
   sources), case-based (apply to authentic problem), peer instruction (resolve a misconception).
3. Draft the prompt as a ConcepTest: a focused question with one best answer and 2-3 plausible distractors.
4. Plan the timing: individual think (60-90 s), pair discuss (2-3 min), vote, instructor reveals histogram, re-discuss,
   re-vote.
5. For jigsaw: assign expert groups to sub-topics; each expert group produces a one-page brief before forming mixed
   groups.
6. For case-based: write a 1-page authentic case with stakes, ambiguity, and a decision point — not a pure narrative.
7. Define the formative artifact the activity must produce (vote, written answer, diagram, one-page brief).
8. Plan the instructor moves: when to circulate, when to cold-call, when to reveal the histogram.
9. Decide the debrief format: whole-class synthesis by the instructor or written reflection by the student.
10. Document the misconception targeted and the expected post-activity understanding.
11. Add a fallback if the activity stalls (e.g., if the first vote is too uniform, switch to a harder prompt).
12. End with a metacognitive prompt: "What changed in your thinking during the discussion?".

## Inputs

- The concept and the documented common misconception.
- Class size and seating (rows vs. tables vs. breakout rooms).
- Time available (5 min, 15 min, or full 50-min session).
- Prior knowledge students bring and the prerequisite chain.
- Polling tool or color-card voting system if peer instruction is used.

## Outputs

- `activity_brief.md` — structure, prompt, timing, and instructor moves.
- `conceptest.md` — question with distractors and the misconception each targets.
- `case_narrative.md` — case-based scenario with a clear decision point.
- `jigsaw_cards.md` — expert group assignments and the deliverable spec.
- `debrief_plan.md` — synthesis prompts and reflection questions.

## Key Rules

- Every active-learning segment must produce a visible artifact; invisible "discussion" is not measurable.
- Peer instruction ConcepTests must target a known misconception; opinion polls do not qualify.
- After the first vote, students must discuss before re-voting; revealing the answer immediately kills the learning.
- A shift from about 40% correct on the first vote to at least 70% on the second vote indicates a successful ConcepTest.
- Jigsaw expert groups must have a clear deliverable (one-page brief, diagram, slide) before forming mixed groups.
- Time per segment must be explicit and timed; "discuss until done" never finishes.
- Cases must contain a decision point; pure narrative cases drift back into lecture.

## Examples

```text
ConcepTest (peer instruction, Newtonian mechanics):
"A ball is thrown straight up. At the top of its flight, the
net force on it is:
A) zero                          (misconception: v = 0 implies F = 0)
B) downward, equal to mg         (correct)
C) downward, less than mg        (confusion with apparent weight)
D) upward, equal to mg            (confusion with direction of motion)

Expected first vote: ~50% A, ~35% B, ~10% C, ~5% D.
After 3-minute peer discussion: target ≥75% B.
If first vote is >80% B: skip peer discussion, move on.
If first vote is <30% B: do not reveal; re-teach first.
```

```text
Jigsaw (4 expert groups, 4 students each → 4 mixed groups of 4):
Expert group A: photosynthesis light reactions.
Expert group B: Calvin cycle.
Expert group C: cellular respiration glycolysis.
Expert group D: electron transport chain.
Deliverable per expert group: one-page brief + one diagram.
Mixed groups: each expert teaches their brief to the others;
the mixed group produces a comparison of photosynthesis
vs respiration.
```

```text
Case-based (case brief, 1 page):
"A 14-week-old infant presents with poor weight gain and
frequent vomiting. The pediatrician suspects pyloric
stenosis. What two findings on physical exam would
confirm, and what imaging study is first-line?"
Decision point: pick the two findings and justify over
alternatives; the case has one best answer.
```

## References

- Bonwell & Eison (1991), "Active Learning: Creating Excitement in the Classroom" — ASHE-ERIC Higher Education Report.
- Mazur (1997), "Peer Instruction: A User's Manual" — Prentice Hall.
- Felder & Brent (2016), "Teaching and Learning STEM: A Practical Guide" — Jossey-Bass.
- Cornell University Center for Teaching Innovation — Active
  learning: https://teaching.cornell.edu/teaching-resources/active-collaborative-learning
