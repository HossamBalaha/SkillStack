---
name: interactive-narrative-builder
description: Build interactive scrollytelling narratives using D3.js and IntersectionObserver, with step-by-step chart reveals and branch choices for reader-driven exploration. Use when the user needs an article that responds to scroll, swaps charts in place, or lets readers pick a branch such as a region, persona, or scenario.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [scrollytelling, d3, intersection-observer, branch-choice, interactive]
related: [data-storytelling/narrative-arc-designer, data-storytelling/data-story-storyboarder, visualization/interactive-plot-builder]
prerequisites: []
outputs: [html, python, markdown]
difficulty: advanced
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Interactive Narrative Builder

## When To Use

- The user says "I want a scrolly story" or "let the reader pick their region".
- The narrative needs charts that morph as the reader scrolls, not a stack of static figures.
- The reader should drive: choose a branch, filter a dataset, or step through a scenario.
- The piece will publish on the web and must work without a backend.
- Trigger keywords: scrollytelling, scrollama, IntersectionObserver, D3, branch choice, step reveal.

## Workflow

1. Take the narrative arc and split each beat into a step: a text block and a chart state.
2. Define chart states per step: which marks exist, what is highlighted, which axis range.
3. Choose the scroll framework: scrollama (recommended) or a hand-rolled IntersectionObserver.
4. For branch choices, define the branching variable and the distinct chart state per branch.
5. Build the D3 enter/update/exit pipeline so transitions are smooth, not reloads.
6. Bind the scroll trigger to chart state via a single `SetStep(index)` function.
7. Add a progress indicator so the reader knows where they are in the story.
8. Wire keyboard navigation (arrow keys, space) and a mobile fallback that stacks content.
9. Smoke-test: every step transitions, the back button works, and mobile does not break.
10. Emit a self-contained HTML file, the D3 script, and a Markdown step map.

## Inputs

- A narrative arc with at least three beats.
- The dataset (CSV or inlined JSON).
- Optional: branching variable and its levels.
- Optional: brand palette and fonts.

## Outputs

- `narrative.html` — self-contained scrollytelling page.
- `narrative.js` — D3 chart logic and step-binding.
- `step_map.yaml` — step index, text, chart state, branch.
- `narrative_notes.md` — fallbacks, accessibility, and load-test results.

## Key Rules

- One chart mutates through states; do not stack ten charts and toggle visibility.
- Transitions are 400-600 ms; faster reads as a glitch, slower as a stall.
- Branch choices must lead to distinct chart states, not cosmetic swaps.
- Keyboard navigation is required; scroll is not the only path.
- The progress indicator is visible at all times; lost readers abandon the page.
- Mobile fallback stacks text above chart; the chart still mutates on scroll.
- Every step works backward: scrolling up restores the previous state cleanly.
- No external API calls; the page must run from a static host.

## Examples

```html
<!-- Scrollytelling scaffold with scrollama + D3. -->
<div class="scrolly" id="scrolly">
  <figure class="chart">
    <svg id="vis" width="640" height="420"></svg>
  </figure>
  <article>
    <div class="step" data-step="0"><p>System-wide readmissions are flat since 2020.</p></div>
    <div class="step" data-step="1"><p>One district breaks the trend: District 4.</p></div>
    <div class="step" data-step="2"><p>The gap traces to a single discharge protocol.</p></div>
    <div class="step" data-step="3"><p>Swap the protocol and the gap closes in 90 days.</p></div>
  </article>
</div>
<script src="https://unpkg.com/scrollama"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
function SetStep(index) {
  // One function mutates the same chart per step.
  const svg = d3.select("#vis");
  if (index === 0) DrawTrend(svg, "all");
  if (index === 1) HighlightDistrict(svg, "D4");
  if (index === 2) AnnotateProtocol(svg, "D4");
  if (index === 3) DrawCounterfactual(svg, "D4");
}
const scroller = scrollama();
scroller.setup({ step: ".step", graphic: "figure.chart", offset: 0.7 })
  .onStepEnter((resp) => SetStep(resp.index));
window.addEventListener("resize", scroller.resize);
</script>
```

```yaml
# step_map.yaml (excerpt)
- step: 0
  text: "System-wide readmissions are flat since 2020."
  chart_state: { marks: trend, highlight: none, y_range: [0, 250] }
- step: 1
  text: "One district breaks the trend: District 4."
  chart_state: { marks: trend, highlight: D4, y_range: [0, 250] }
- step: 2
  text: "The gap traces to a single discharge protocol."
  chart_state: { marks: trend, highlight: D4, callout: protocol_gap }
- step: 3
  text: "Swap the protocol and the gap closes in 90 days."
  chart_state: { marks: counterfactual, highlight: D4, callout: protocol_swap }
```
