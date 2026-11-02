---
name: data-story-storyboarder
description: Storyboard a data story into panels with transitions, emotional beats, planned surprises, and a conclusion that lands the takeaway. Use when the user must plan a multi-scene narrative before drafting slides, scrolly, or video, and needs a McKee-style structure applied to evidence.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [storyboard, panels, emotional-beats, surprise, conclusion]
related: [data-storytelling/narrative-arc-designer, data-storytelling/presentation-slide-builder, data-storytelling/interactive-narrative-builder]
prerequisites: []
outputs: [markdown, yaml]
difficulty: intermediate
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

# Data Story Storyboarder

## When To Use

- The user says "storyboard this before I build it" or "I need a panel plan for my talk".
- A multi-scene narrative (video, scrolly, slide deck) needs structure before production.
- The story needs emotional beats and a planned surprise, not just a list of findings.
- Trigger keywords: storyboard, panel, beat sheet, surprise, kicker, scene plan.

## Workflow

1. Take the narrative arc and confirm the single takeaway the conclusion must land.
2. Break the arc into 6-12 panels; each panel is one scene the reader or viewer sees.
3. For each panel, write four fields: scene description, evidence shown, emotional beat, transition.
4. Place the inciting incident early: the question or anomaly that opens the story.
5. Build rising tension across the middle panels; each panel raises the stakes or narrows the cause.
6. Schedule one planned surprise: the moment the data contradicts the audience's prior belief.
7. Resolve the tension before the conclusion; a conclusion cannot land on unresolved conflict.
8. Land the conclusion on the takeaway, then add a kicker line that sticks after the reader leaves.
9. Emit a panel-by-panel storyboard as Markdown and a machine-readable YAML scene sheet.

## Inputs

- A narrative arc with a single takeaway.
- The evidence stack (charts, quotes, tables) the panels can draw on.
- Audience profile and prior beliefs, so the surprise lands.
- Output medium: slide deck, scrolly, video, or comic strip.

## Outputs

- `storyboard.md` — panel-by-panel plan with all four fields.
- `scene_sheet.yaml` — machine-readable scenes, beats, evidence pointers.
- `surprise_plan.md` — the planned surprise, its setup, and its payoff.
- `kicker.md` — the closing line plus its emotional residue.

## Key Rules

- Every panel serves the takeaway; a panel that does not is cut, however pretty.
- The inciting incident is on panel one or two; the story does not warm up.
- Rising tension escalates; two flat panels in a row means the storyboard stalls.
- The surprise is planned and earned; cheap shocks destroy trust.
- Conflict is resolved before the conclusion, never in the conclusion.
- The kicker is a single sentence the reader carries away.
- Emotional beats are named, not implied; "concern" and "relief" are valid beats, "interesting" is not.

## Examples

```text
Panel 1 (Inciting incident):
  Scene: System-wide readmission trend, flat for four years.
  Evidence: figures/readmissions_trend.png.
  Beat: Curiosity. Why is the line flat?
  Transition: "Flat overall, but one district breaks the line."

Panel 3 (Surprise setup):
  Scene: District scatter, D4 cluster highlighted.
  Evidence: figures/district_scatter.png + annotations/d4_callout.md.
  Beat: Suspicion. Something is wrong at D4.
  Transition: "If one district is the cause, what does it do differently?"

Panel 5 (Surprise payoff):
  Scene: Protocol diff table, D4 vs. system standard.
  Evidence: tables/protocol_diff.md.
  Beat: Surprise. D4 skips a step the rest take for granted.
  Transition: "Skip one step, double the readmissions. Can we close the gap?"

Panel 8 (Conclusion + kicker):
  Scene: Counterfactual chart, gap closes by 90 days post-swap.
  Evidence: figures/counterfactual.png.
  Beat: Relief. The gap is closable.
  Kicker: "One protocol, one district, 412 fewer readmissions a year."
```

```yaml
# scene_sheet.yaml (excerpt)
- panel: 1
  role: inciting-incident
  evidence: [figures/readmissions_trend.png]
  beat: curiosity
  transition: "Flat overall, but one district breaks the line."
- panel: 5
  role: surprise-payoff
  evidence: [tables/protocol_diff.md]
  beat: surprise
  transition: "Skip one step, double the readmissions. Can we close the gap?"
```

## References

- McKee, R. (1997). Story: Substance, Structure, Style, and the Principles of Screenwriting.
  Harper-Collins. https://www.mckeestory.com/
- Segel, E., and Heer, J. (2010). Narrative Visualization. IEEE TVCG, on narrative genres.
- Hullman, J. et al. (2013). A Framing Study on the Impact of Message Sequence. https://idl.cs.washington.edu/
- Lee, B. et al. (2015). More Than Telling a Story: Transforming Data into Visually Shared Stories. IEEE CG&A.
