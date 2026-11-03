---
name: metric-translation-writer
description: Translate technical metrics into human-scaled outcomes for non-technical readers, converting dollars into scholarships saved, percentages into absolute counts, and accuracy gains into prevented errors. Use when the user must make a model metric, a cost saving, or a lift number legible to a board, a donor, or the public.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [metric-translation, human-scale, framing, analogies, made-to-stick]
related: [data-storytelling/audience-tailor, data-storytelling/infographic-crafter, data-storytelling/data-journalism-writer]
prerequisites: []
outputs: [markdown, json]
difficulty: beginner
estimated_tokens: 850
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Metric Translation Writer

## When To Use

- The user says "make this number mean something" or "rewrite this in human terms".
- A slide or report leads with "$2.3M saved" or "F1 up 0.04" and the audience does not react.
- The number is true but inert; the reader has no anchor to feel it.
- Trigger keywords: human scale, translation, analogy, dollar-to-impact, percent-to-absolute.

## Workflow

1. List the metric, its unit, its direction (up is good or bad), and its current value.
2. Find the reference value the reader already knows (last year, industry average, a household budget).
3. Translate to a human-scaled unit: dollars into scholarships, hours, meals, or teachers; percentages into counts of
   people; F1 deltas into errors prevented per thousand cases.
4. Sanity-check the translation: the new unit must be true to the math and to the audience's world.
5. Pick the framing direction that matches the takeaway: gain (lives saved) or loss (lives lost) is not interchangeable.
6. Write two lines: the metric, then the translation. The translation carries the emotion, the metric carries the proof.
7. Flag any unit conversion that depends on an assumption (price, headcount, period); record the assumption.
8. Emit a Markdown translations file and a JSON unit-map so the same metric can be retranslated later.

## Inputs

- The metric, its value, and its unit.
- The audience's world (scholarships, meals, teachers, patients per week).
- Optional: reference value the reader already anchors to.
- Optional: assumptions needed for the unit conversion.

## Outputs

- `translations.md` — each metric paired with its human-scaled line.
- `unit_map.json` — machine-readable metric, unit, factor, assumption, anchor.
- `assumptions.md` — every assumption a translation relies on, with its source.

## Key Rules

- The translation is true to the math; rounding is allowed, distortion is not.
- The translation uses a unit the audience already feels; novel units lose readers.
- Gain framing and loss framing are not interchangeable; pick the one that matches the takeaway.
- Every conversion assumption is recorded; hidden assumptions erode trust.
- The metric stays in the text; the translation is added beside it, not replacing it.
- One translation per metric; multiple translations dilute the anchor.
- If no honest translation exists, the metric is presented raw with a stated limit.

## Examples

```text
Metric: "$2.3M annual cost saving from the new triage model."
Translation: "Funds 47 four-year scholarships, or hires 31 nurses,
or keeps the after-hours clinic open for 14 months."
Assumption: scholarship = $49,000/yr, nurse = $74,000/yr loaded,
clinic run cost = $165,000/month. Source: FY24 budget.

Metric: "F1 rose from 0.81 to 0.85 on the rare-class detector."
Translation: "On 10,000 cases a month, that is 260 fewer missed
rare cases every month, about 8 a day."
Assumption: rare-class prevalence 7.2%, base miss rate implied by F1.

Metric: "Churn dropped 0.4 percentage points."
Translation: "About 1,100 customers stayed who would have left;
that is a mid-sized town of subscribers retained."
Assumption: base 275,000 active subscribers. Source: product dashboard.
```

```json
{
  "metric": "annual_cost_saving_usd",
  "value": 2300000,
  "translations": [
    {"unit": "scholarships", "value": 47, "factor": 49000, "assumption": "scholarship_year_cost_usd"},
    {"unit": "nurses", "value": 31, "factor": 74000, "assumption": "nurse_loaded_cost_usd"},
    {"unit": "clinic_months", "value": 14, "factor": 165000, "assumption": "clinic_monthly_cost_usd"}
  ]
}
```
