---
name: data-pitch-deck-builder
description: Build data-driven pitch decks with a problem slide anchored by evidence, a solution slide backed by data, a market slide sized as TAM/SAM/SOM, and a traction slide that proves momentum. Use when the user is preparing a Sequoia-style or YC Demo Day deck and every slide must carry a number that survives a diligence question.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [pitch-deck, problem-solution, tam-sam-som, traction, demo-day]
related: [data-storytelling/audience-tailor, data-storytelling/presentation-slide-builder, data-storytelling/data-annotation-writer]
prerequisites: []
outputs: [markdown, latex, pdf]
difficulty: intermediate
estimated_tokens: 1350
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Data Pitch Deck Builder

## When To Use

- The user says "I am pitching at Demo Day" or "draft me a pitch deck".
- An investor deck has slides without numbers and diligence will fail on each.
- The user must size a market with TAM, SAM, and SOM, each with a stated method.
- Traction must be shown as a chart, not as a vanity metric.
- Trigger keywords: pitch deck, Sequoia, Demo Day, problem slide, TAM, SAM, SOM, traction.

## Workflow

1. Lock the 10-slide spine: problem, solution, market, product, traction, business model, team, competition, financials,
   ask.
2. Problem slide: state the problem in one sentence, then anchor it with a number and a source.
3. Solution slide: state the solution in one sentence, then show the evidence the solution works.
4. Market slide: build TAM (top-down), SAM (filtered), and SOM (reachable in 3-5 years); cite each method.
5. Product slide: one screenshot or one diagram, plus the metric that defines "it works".
6. Traction slide: a chart with at least three points in time; growth rate stated; cohort if churn matters.
7. Business model slide: revenue per unit, contribution margin, payback period.
8. Team slide: each named founder with one credibility anchor.
9. Competition slide: a 2x2 with axes the startup wins on, not axes the incumbents win on.
10. Ask slide: the amount, the runway it buys, and the milestones it unlocks; no vague "growth capital".

## Inputs

- The problem and the solution, in plain language.
- Market sizing inputs: total population, filter rates, capture rate, time horizon.
- Traction data: revenue, users, or usage over time, with cohort if available.
- Unit economics: price, cost, payback.
- Team names and credibility anchors.

## Outputs

- `deck.tex` — Beamer skeleton, one frame per slide.
- `slide_plan.md` — per-slide assertion, evidence, source, and diligence answer.
- `market_sizing.yaml` — TAM, SAM, SOM with method and citations.
- `traction_chart.svg` — vector chart of the traction metric over time.
- `ask.md` — the amount, runway, and milestone plan.

## Key Rules

- Every slide carries a number that survives a diligence question; unquantified slides fail.
- The problem is anchored by a number, not a story; "many people" is not a number.
- The solution slide shows evidence the solution works, not just that it exists.
- TAM, SAM, and SOM each cite a method; top-down TAM without a source is fiction.
- Traction is a chart with at least three points; a single number is not traction.
- The ask names the amount, the runway, and the milestones; "growth capital" is vague.
- Competition axes are chosen so the startup wins, not the incumbents.

## Examples

```text
Problem slide:
  Assertion: "Hospital readmissions cost US payers $52B a year; 23% are
  avoidable with a known protocol that 40% of hospitals do not follow."
  Evidence: figures/readmissions_cost.png.
  Sources: CMS 2023 readmissions report; NEJM protocol study.
  Diligence answer: "Cost figure is CMS gross; 23% avoidable is NEJM meta."

Market slide:
  TAM: $52B annual US readmission cost (CMS, top-down).
  SAM: $19B in the 60% of hospitals without the protocol (filtered).
  SOM: $310M in 3-5 years across 3 pilot states (bottom-up: 2,400 hospitals
       x $130K average annual contract).

Traction slide:
  Chart: monthly recurring revenue, 8 quarters.
  Assertion: "MRR up 3.2x in 8 quarters, net revenue retention 118%."
  Cohort: 2023-Q1 cohort retains 91% at 24 months.
```

```yaml
# market_sizing.yaml (excerpt)
tam:
  value_usd: 52000000000
  method: top-down
  source: CMS 2023 readmissions report
sam:
  value_usd: 19000000000
  method: filtered by protocol-absence rate (40%)
  source: AHA hospital survey 2024
som:
  value_usd: 310000000
  method: bottom-up, 3 pilot states, 3-5 yr horizon
  assumptions:
    - 2400 target hospitals in pilot states
    - 130000 average annual contract USD
```
