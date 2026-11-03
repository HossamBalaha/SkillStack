---
name: accessible-content-designer
description: 'Design accessible content meeting WCAG 2.2 AA: alt text, captioning, screen-reader friendly structure, color contrast, and keyboard navigation. Use when the user asks to make slides, documents, LMS pages, or videos accessible.'
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [accessibility, wcag, alt-text, captions, screen-reader, color-contrast]
related: [teaching-pedagogy/universal-design-builder, teaching-pedagogy/lesson-plan-builder, teaching-pedagogy/microlearning-designer]
prerequisites: []
outputs: [markdown, html]
difficulty: intermediate
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Accessible Content Designer

## When To Use

- The user asks to "make this accessible", "WCAG check", or "comply with Section 508".
- A slide deck, document, or LMS page must be remediated before publication.
- A video needs captions, and audio-only content needs a transcript.
- Color choices in a chart must be checked for contrast and color-only meaning.
- Trigger keywords: accessibility, WCAG 2.2 AA, alt text, captions, screen reader, color contrast, keyboard nav.

## Workflow

1. Classify the content type: document (DOCX/PDF), slide deck (PPTX), video (MP4), web page (HTML), interactive
   (SCORM/H5P).
2. Run WCAG 2.2 AA checks per principle: perceivable, operable, understandable, robust.
3. Provide alt text for every informative image; mark decorative images with empty alt so screen readers skip them.
4. Caption all video with a WebVTT track; provide a transcript for audio-only content.
5. Verify color contrast: 4.5:1 for normal text, 3:1 for large text, 3:1 for UI components and graphical objects.
6. Use semantic headings (H1 then H2 then H3) without skipping levels; do not use bold for structure.
7. Ensure full keyboard operability: tab order, visible focus indicator, and no keyboard traps.
8. Write link text that is descriptive ("download the syllabus"), not "click here" or bare URLs.
9. Avoid color as the only carrier of meaning; pair every color-coded cue with text, icon, or pattern.
10. Provide time extensions or remove time limits where time is not the construct being measured.
11. Test with a screen reader (NVDA on Windows, VoiceOver on macOS) and a keyboard-only pass.
12. Document remediation steps and re-check after every edit; accessibility is not a one-time audit.

## Inputs

- Source files (DOCX, PPTX, MP4, HTML, SCORM package).
- Target conformance level (A, AA, AAA) — default to AA.
- Audience needs: visual, motor, cognitive, auditory.
- Platform (LMS, public web, print fallback).

## Outputs

- `accessibility_report.md` — WCAG criterion × pass/fail per item, with severity.
- `alt_text.csv` — image filename × alt text (or empty for decorative).
- `caption_track.vtt` — WebVTT caption file for the video.
- `remediated_source/` — fixed source files exported with accessibility preserved.
- `remediation_log.md` — changes applied with rationale and the rule they satisfy.

## Key Rules

- Conformance target is WCAG 2.2 Level AA unless the institution requires AAA.
- Alt text describes purpose, not appearance: "chart showing enrollment growth 2019-2024", not "bar chart".
- Captions are verbatim for technical content and lightly edited for reading speed in narrative content.
- Never rely on color alone: pair every color-coded cue with text, icon, or pattern.
- Documents must export as tagged PDFs with reading order set; untagged PDFs fail screen readers.
- Forms must have programmatic labels (the `<label>` element), not placeholder-only labels.
- Test with real tools (axe DevTools, WAVE, NVDA), not by eye — eye checks miss keyboard and screen-reader failures.
- Re-run the audit after every edit; accessibility is not a one-time pass.

## Examples

```html
<!-- Bad: bare URL, color-only cue, no label -->
<a href="syllabus.pdf">Click here</a>
<button style="background:red">Submit</button>
<input type="email" placeholder="Email">

<!-- Good: descriptive link, labeled button, programmatic label -->
<a href="syllabus.pdf">Download the syllabus (PDF, 220 KB)</a>
<button aria-label="Submit the quiz">Submit</button>
<label for="email">Email address</label>
<input id="email" type="email" name="email">
```

```text
Alt text samples:
Informative image (enrollment chart):
  "<bar chart>: Enrollment grew from 120 in 2019 to 340 in
   2024, with steepest growth in 2022."

Decorative image (page border):
  "" (empty alt — screen reader skips it)

Functional image (download icon):
  "Download the syllabus (PDF, 220 KB)"
```

```text
Contrast check (WebAIM contrast checker):
- Body text #444444 on #FFFFFF: 9.7:1 — passes AA and AAA.
- Link text #0066CC on #FFFFFF: 5.3:1  — passes AA for normal text.
- Warning text #FF0000 on #FFFFFF: 4.0:1 — FAILS AA (need 4.5:1);
  darken to #CC0000 → 5.9:1, passes.
```
