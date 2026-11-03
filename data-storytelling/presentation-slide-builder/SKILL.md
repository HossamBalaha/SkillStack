---
name: presentation-slide-builder
description: Build presentation slides that lead with an assertion, keep text sparse, let full-bleed charts carry the evidence, and chain into a narrative flow with planned transitions. Use when the user is preparing a data-driven talk, board deck, or demo-day pitch and needs slides that survive a back-row readability test.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [slides, assertion-evidence, full-bleed, narrative-flow, readability]
related: [data-storytelling/data-story-storyboarder, data-storytelling/audience-tailor, academic-research/conference-talk-prep]
prerequisites: []
outputs: [latex, markdown, pdf]
difficulty: intermediate
estimated_tokens: 1300
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Presentation Slide Builder

## When To Use

- The user says "I need to build my slides" or "fix this deck for a board meeting".
- The deck currently uses bullet-heavy slides where the chart is a footnote.
- The user has a narrative arc and needs it converted into a slide-by-slide plan.
- The talk must read clearly from the back row and survive projection on a low-lumen projector.
- Trigger keywords: assertion-evidence, full-bleed chart, slide plan, narrative flow, back row.

## Workflow

1. Take the narrative arc from `narrative-arc-designer` and break each beat into one or two slides.
2. For every slide, write the assertion first: a single full sentence the slide proves.
3. Pair the assertion with one piece of evidence: a full-bleed chart, a single table, or one quote.
4. Strip body text to at most two short supporting lines; anything more becomes speaker notes.
5. Size charts to fill at least 60% of the slide area; axes and labels above 18 pt.
6. Write the transition sentence that links each slide to the next; store it in speaker notes.
7. Sequence slides so each assertion builds on the previous one; no orphan slides.
8. Run a back-row check: title above 28 pt, assertion above 32 pt, chart labels above 18 pt.
9. Produce a Beamer skeleton (or reveal.js if requested) plus a Markdown slide plan and notes.

## Inputs

- A narrative arc or a set of key findings to convert into a talk.
- Audience profile and time budget.
- Source charts (PDF, PNG, or matplotlib script).
- Tool preference: Beamer, reveal.js, PowerPoint, Google Slides.

## Outputs

- `slides.tex` — Beamer skeleton with one frame per slide.
- `slide_plan.md` — per-slide assertion, evidence, transition, and notes.
- `speaker_notes.md` — full delivery notes including pace and fallbacks.
- `back_row_check.md` — font size and contrast audit per slide.

## Key Rules

- Every slide states one assertion in a full sentence; a topic phrase alone is not enough.
- Evidence fills most of the slide; text does not compete with the chart.
- Body text is at most two lines; deeper detail moves to speaker notes.
- Transitions are written, not improvised; "next slide" is forbidden.
- Title font is at least 28 pt; assertion at least 32 pt; chart labels at least 18 pt.
- One chart per slide unless a comparison is the whole point.
- No chart junk: drop shadows, 3D, gradient fills, decorative icons.

## Examples

```latex
% Beamer assertion-evidence frame.
\begin{frame}{District 4 readmissions}
  \begin{center}
    \textbf{\large Readmissions in District 4 are 2.3$\times$ the system average,
    concentrated in the first 14 days post-discharge.}
  \end{center}
  \vspace{0.5em}
  \includegraphics[width=0.92\textwidth]{figures/district_scatter.pdf}
  \vspace{0.3em}
  \small Source: system EHR, 2020--2024. $n=41{,}208$ discharges.
\end{frame}
```

```text
Slide plan (excerpt):
Slide 5 (90 s) — Assertion: "District 4 readmissions are 2.3x the average."
  Evidence: district_scatter.pdf, full-bleed.
  Transition: "If the cluster is real, what causes it? That brings us to the
  discharge protocol..."
  Notes: Emphasise the 14-day window; skip the per-hospital breakdown if short.
  Back-row check: assertion 32 pt, scatter labels 18 pt, source line 12 pt.
```
