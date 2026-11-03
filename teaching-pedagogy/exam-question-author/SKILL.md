---
name: exam-question-author
description: Author exam questions targeting higher-order thinking (Bloom's analyze, evaluate, create) with scenario-based stems, blueprints, and psychometric review. Use when the user asks to write midterm or final exam questions, build test blueprints, or review item statistics.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [exam-questions, higher-order-thinking, blueprint, psychometrics, item-analysis]
related: [teaching-pedagogy/learning-objective-writer, teaching-pedagogy/assessment-designer, teaching-pedagogy/rubric-builder]
prerequisites: []
outputs: [markdown, latex]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Exam Question Author

## When To Use

- The user asks to "write midterm questions", "build a test blueprint", or "draft final exam items".
- An objective at Bloom level Analyze or above must be assessed and bare recall will not suffice.
- An item bank needs psychometric review after the first administration (p-value, D-index, distractor analysis).
- The final exam form must be assembled to respect the blueprint's Bloom distribution.
- Trigger keywords: exam questions, test blueprint, scenario-based, Bloom, Haladyna, item analysis, psychometrics.

## Workflow

1. Build the test blueprint: objective × item count × Bloom level × points × time per item.
2. Match Bloom level to objective: do not assess "create" with multiple-choice; use constructed-response instead.
3. Write the stem first as a complete problem; avoid finishing the sentence if a full question works better.
4. Add a scenario when the objective is Analyze or above — bare recall cannot measure higher-order thinking.
5. Write the keyed response; verify it is unambiguously correct.
6. Write 3-4 distractors, each plausible to a learner with a specific documented misconception.
7. Remove clues: avoid grammatical mismatches, unequal-length distractors, "all of the above", "none of the above".
8. Pilot the items; compute difficulty (p-value, target 0.3-0.7) and discrimination (D-index, target ≥ 0.3).
9. Flag items with negative discrimination — high performers chose a wrong answer more often than low performers did.
10. Conduct a distractor analysis: each distractor should be chosen by at least 5% of students; remove non-functioning
    distractors.
11. For constructed-response items, draft a model answer and a 3-level rubric (full / partial / no credit).
12. Assemble the final form respecting the blueprint; balance Bloom levels and the time per item.

## Inputs

- Learning objectives to be assessed with their Bloom levels.
- Number of items, total points, and time budget.
- Class size and the prior cohort's performance distribution.
- Available item bank with prior statistics, if one exists.

## Outputs

- `test_blueprint.csv` — objective × item × Bloom level × points × time.
- `item_bank.md` — items with keyed response and the misconception each distractor targets.
- `scenario_briefs.md` — multi-item scenarios with context and the decision point.
- `rubric_constructed_response.md` — model answers and 3-level scoring guides.
- `item_analysis.csv` — p-value, D-index, distractor frequencies, action taken per item.

## Key Rules

- Bloom level of the item must match the Bloom level of the objective; misalignment invalidates the item.
- Every distractor must trace to a documented misconception; "plausible-looking" is not enough.
- Items with negative discrimination must be retired or revised, regardless of how well they read.
- Distractors chosen by fewer than 5% of students are non-functioning and dilute the item; remove or revise.
- Scenario-based stems are required for Analyze, Evaluate, and Create objectives.
- The final form must respect the blueprint's Bloom distribution; drifting toward recall is the most common failure.
- Time per item must be tested empirically; estimates that exceed actual time produce speeded, invalid tests.

## Examples

```latex
% Bloom: Analyze. Objective: O3 — diagnose bottlenecks in a
% distributed system given a trace.
\begin{itemize}
  \item Stem: A three-tier web service shows 95th-percentile
    latency of 4.2 s under load. The trace shows the database
    CPU at 30\%, the application server CPU at 92\%, and the
    network round-trip at 12 ms. Which is the most likely
    bottleneck, and what single change would confirm it?
  \item Keyed: Application server is the bottleneck; confirm
    by scaling it horizontally and observing latency drop.
  \item Distractor A: Database is the bottleneck — plausible
    because the DB is the usual suspect, but CPU is low.
    Misconception: latency = DB.
  \item Distractor B: Network latency is the bottleneck —
    plausible because 12 ms sounds high, but it is negligible
    vs 4.2 s. Misconception: any non-zero network delay is
    the cause.
  \item Distractor C: Cannot determine without more data —
    plausible because students fear underdetermined problems.
    Misconception: refuse to commit.
\end{itemize}
```

```text
Item statistics after pilot:
Item 12: p = 0.42 (good difficulty), D = 0.51 (good
  discrimination).
  Distractor frequencies: A 38%, B 12%, C 5% (low — revise
  or remove), D 45% (keyed).
Action: revise distractor C; keep item.

Item 15: p = 0.85 (too easy), D = -0.05 (negative — high
  performers chose A more than low performers did).
Action: retire the item; investigate why high performers
  preferred A (likely a hidden ambiguity in the stem).
```

```text
Test blueprint (final, 90 min):
Objective | Items | Bloom      | Pts | Time
O1        | Q1-Q5 | Remember   | 10  | 8 min
O2        | Q6-Q10| Understand | 15  | 12 min
O3        | Q11-13| Analyze    | 18  | 25 min
O4        | Q14-15| Evaluate   | 14  | 25 min
O5        | Q16   | Create     | 13  | 20 min
                                    = 70 pts, 90 min
```
