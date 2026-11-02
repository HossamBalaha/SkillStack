---
name: conference-talk-prep
description: Draft conference talks with slide-by-slide outline, speaker notes per slide, transition sentences, time-boxing per slide, anticipated Q&A with prepared answers, and accessibility checks (contrast, font size, alt text). Use when the user is preparing a conference presentation, keynote, or spotlight talk and needs a structured slide plan with delivery guidance.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: academic-research
tags: [conference, slides, talk, presentation, qa-prep]
related: [academic-research/journal-manuscript-writer, academic-research/research-portfolio-tracker, academic-research/peer-review-simulator]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 830
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Conference Talk Prep

## When To Use
- The user says "I am presenting at NeurIPS/CVPR/MICCAI", "help me prepare my talk", or "draft my slides".
- The user needs speaker notes, transitions, and time-boxing per slide.
- The user wants an anticipated Q&A with prepared answers.
- The user needs accessibility checks on their slide deck.
- Trigger keywords: conference talk, slides, speaker notes, transitions, time-boxing, Q&A, accessibility.

## Workflow
1. Confirm venue, talk format (long talk, spotlight, poster teaser, keynote), and total time budget.
2. Compute per-slide time budget: e.g., 20 slides × 1.5 min for a 30-min slot (minus 5 min Q&A buffer).
3. Draft the slide-by-slide outline. For each slide: title, key message, one visual, one equation or quote (optional).
4. Write speaker notes for each slide: 3-5 sentences covering what to say, what to emphasize, and what to skip if running long.
5. Write transition sentences linking every slide to the next ("This raises the question of...").
6. Mark time-critical slides ("hard cut at 12:00") so the speaker can pace.
7. Anticipate 5-10 audience questions. For each, write a prepared answer with a backup one-liner if pressed for time.
8. Run accessibility checks: contrast ratio >= 4.5:1, body font >= 24 pt, alt text on every figure, no color-only encoding.
9. Provide a fallback "if time is short" deck path that drops optional slides in priority order.
10. Provide a "if time overruns" message ("Happy to discuss in the poster session").
11. Output a printable speaker-notes PDF and the slide outline as Markdown.

## Inputs
- Venue name and talk format (long, spotlight, keynote, poster teaser).
- Total time budget (talk + Q&A).
- Accepted paper or abstract as the content source.
- Speaker preferences (pace, depth of math, audience expertise).
- Slide tool preference (Beamer, reveal.js, PowerPoint, Google Slides).

## Outputs
- `slides_outline.md` — slide-by-slide outline with titles and key messages.
- `speaker_notes.md` — per-slide notes and transitions.
- `time_budget.csv` — slide number, allocated seconds, cumulative time.
- `qa_bank.md` — anticipated questions and prepared answers.
- `accessibility_checklist.md` — contrast, font size, alt text, color-blind safety.
- `fallback_plan.md` — short/long runtime variants.

## Key Rules
- Every slide gets a single key message; if you cannot state it in one sentence, split the slide.
- Per-slide time budget must sum to (talk time − Q&A buffer).
- Transitions must connect consecutive slides; "Next slide" is not a transition.
- Alt text required on every figure; never rely on color alone.
- Body font >= 24 pt; math font sized to be legible from the back row.
- Prepare at least one fallback message for time overruns.

## Examples
```text
Slide 5 (1.5 min): "Problem Setup"
  Key message: Multi-site MRI suffers from inter-site shift, breaking standard
  federated baselines.
  Visual: 4 violin plots of intensity distributions across 4 sites.
  Speaker notes: Emphasize that the shift is not just statistical but
  topological (connectivity differences). Skip the per-site vendor list if
  short on time.
  Transition: "If the shift is topological, the aggregator must respect
  topology. This motivates our next component..."
  Accessibility: Violin plots use viridis colormap (color-blind safe); alt
  text reads "Violin plots of pixel intensities across four MRI sites
  showing 2x spread in median."
```
```text
Anticipated Q&A sample:
Q: "Why not use a domain-adversarial baseline like DANN?"
A: "DANN aligns feature distributions globally, which discards
   site-specific topology that we want to preserve. We compare against
   DANN in Table 3 (rows 7-8) and outperform it by 3.1 Dice."
   Backup one-liner: "Empirically it underperforms; details in Table 3."
```

## References
- NeurIPS speaker guidelines: https://neurips.cc/Conferences/2025/PaperInformation/SpeakerInstructions
- WCAG 2.1 color contrast: https://www.w3.org/WAI/WCAG21/quickref/
- De Cristo presentation design principles (Presentation Zen): https://www.presentationzen.com/
- Microsoft Accessibility checker: https://support.microsoft.com/accessibility
