---
name: microlearning-designer
description: Design microlearning modules of 3-5 minute units, each with a single learning objective, spaced-repetition hooks, and mobile-first delivery. Use when the user asks to build short learning bites, mobile study cards, or spaced-repetition decks.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [microlearning, spaced-repetition, mobile-first, learning-bites, microcontent]
related: [teaching-pedagogy/lesson-plan-builder, teaching-pedagogy/accessible-content-designer, teaching-pedagogy/active-learning-designer]
prerequisites: []
outputs: [markdown, html]
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

# Microlearning Designer

## When To Use

- The user asks for "microlearning", "learning bites", "study cards", or "spaced-repetition deck".
- A long lecture must be decomposed into 3-5 minute units for mobile delivery.
- A spaced-repetition schedule (Anki, Mochi, FSRS) needs cards built from source material.
- Field workers or commuters need to study in short sessions on a phone.
- Trigger keywords: microlearning, spaced repetition, mobile-first, microcontent, Ebbinghaus, FSRS.

## Workflow

1. Decompose the source material into atomic objectives — each module addresses exactly one objective.
2. Write a 3-5 minute module brief: hook (30 s), core content (90-120 s), application (60 s), recall check (30 s).
3. Limit cognitive load to 3-5 new items per module; more causes overload and reduces recall.
4. Design for mobile-first delivery: vertical layout, 16-18 pt body, tap targets at least 44 px.
5. Embed a single recall check (1-2 questions) at the end of each module; unchecked modules are passive consumption.
6. Tag each module with prerequisite and follow-up modules for the spaced-repetition schedule.
7. Set the spaced-repetition schedule: same day, +1 day, +3 days, +7 days, +21 days (Ebbinghaus curve).
8. Use the SM-2 or FSRS algorithm for card scheduling; FSRS is preferred for newer decks because it adapts to the
   learner.
9. Add a progress indicator so learners see their streak; streaks improve adherence.
10. Produce media: short video (≤3 min), audio narration, and text fallback — provide all three for UDL compliance.
11. Track completion and recall accuracy per module; retire modules with first-attempt accuracy below 50%.
12. Run a 4-week pilot and measure retention at day 21; revise modules below the retention target.

## Inputs

- Source material (textbook chapter, lecture recording, standard operating procedure).
- Target audience and access device (mobile, tablet, desktop).
- Time per session available to the learner.
- Spaced-repetition engine (Anki, Mochi, custom scheduler).

## Outputs

- `module_briefs.md` — one brief per atomic objective with timing and media spec.
- `storyboard.md` — visual storyboard per module with the hook, content, and recall check.
- `recall_cards.csv` — question × answer × schedule × tags for the spaced-repetition engine.
- `player.html` — mobile-first player prototype with captions and transcript fallback.
- `pilot_report.md` — completion, recall accuracy, and day-21 retention metrics.

## Key Rules

- One module, one objective; compound objectives split into multiple modules.
- Module length 3-5 minutes; shorter than 3 minutes lacks depth, longer than 5 minutes loses the "micro" promise.
- Cognitive load: 3-5 new items per module; more causes overload and reduces recall.
- Each module ends with a recall check; unchecked modules are passive consumption.
- Spaced-repetition schedule follows the Ebbinghaus forgetting curve: same day, +1, +3, +7, +21.
- Mobile-first: vertical layout, large tap targets, no horizontal scroll, captions for audio.
- Provide video, audio, and text versions of each module — UDL compliance.
- Retire modules with first-attempt accuracy below 50%; they are too hard or too vague.

## Examples

```text
Module: "Identify the sigmoid activation function"
Duration: 3 min 40 sec
Hook (30 s): "Why does a neural network squash outputs to 0-1?"
Core (120 s): formula, graph, two example inputs and outputs.
Application (60 s): "What is sigma(0)? sigma(2)? sigma(-2)?"
Recall check (30 s): 2 MCQs — formula and graph.
Spaced schedule: today, +1 d, +3 d, +7 d, +21 d.
```

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Microlearning: Sigmoid</title>
</head>
<body style="font-size:18px; line-height:1.6; max-width:480px;
             margin:auto; padding:16px;">
  <main>
    <h1>Sigmoid Activation</h1>
    <p>Time: 3 min 40 sec</p>
    <video controls preload="none" width="100%">
      <source src="sigmoid.mp4" type="video/mp4">
      <track kind="captions" src="sigmoid.vtt"
             srclang="en" label="English">
    </video>
    <details>
      <summary>Read instead (transcript)</summary>
      <p>The sigmoid function maps any real number to a value
      between 0 and 1 ...</p>
    </details>
    <form id="check">
      <p>What is sigma(0)?</p>
      <label><input type="radio" name="q1" value="0"> 0</label>
      <label><input type="radio" name="q1" value="0.5"> 0.5</label>
      <label><input type="radio" name="q1" value="1"> 1</label>
    </form>
  </main>
</body>
</html>
```

```text
Pilot metrics (4-week run, 40 learners):
Module 12 — first-attempt accuracy 38%  → retire or revise.
Module 14 — first-attempt accuracy 71%, day-21 retention 64%.
  Action: keep, schedule +28 d review.
Module 15 — completion 22%, accuracy 80%.  Action: investigate
  why completion is low (length? device? notifications?).
```

## References

- Kapp & Defelice (2019), "Microlearning Short and Sweet" — ATD Press.
- Ebbinghaus (1885/1913), "Memory: A Contribution to Experimental Psychology" — Teachers College Press. Forgetting
  curve.
- FSRS algorithm — open-spaced-repetition project: https://github.com/open-spaced-repetition/fsrs4anki
- Anki documentation on spaced repetition: https://docs.ankiweb.net/
