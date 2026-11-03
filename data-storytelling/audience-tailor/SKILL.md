---
name: audience-tailor
description: Tailor a data story for a named audience by reshaping the lead, depth, analogy, and caveats to match what each reader expects. Use when the user has one analysis but four audiences (executives, technical reviewers, the public, and skeptics) and needs four faithful retellings.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [audience, tailoring, analogy, framing, caveats]
related: [data-storytelling/narrative-arc-designer, data-storytelling/metric-translation-writer, data-storytelling/presentation-slide-builder]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 1000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Audience Tailor

## When To Use

- The user says "rewrite this for the board" or "I need a version for the public".
- One analysis must serve executives, technical reviewers, a lay audience, and skeptics.
- The lead, the analogy, the depth, and the caveats must shift without changing the findings.
- Trigger keywords: audience, executive summary, technical appendix, public explainer, skeptic rebuttal.

## Workflow

1. Pin the shared findings: the takeaway, the supporting numbers, and the known limits. These do not change.
2. Profile each audience: time budget, technical depth, decision authority, prior beliefs.
3. For each audience, choose a lead style:
    - Executive: one-slide summary, the decision and the ask.
    - Technical: full methods, assumptions, and uncertainty bands.
    - General public: analogy plus emotion, one number made human.
    - Skeptic: caveats prominent, with the strongest counter-evidence addressed first.
4. Pick the analogy that matches the audience's world; replace jargon with the analogy only if it lands the same
   finding.
5. Decide what to cut: executives lose the math, technical readers lose the analogy, the public loses both.
6. Front-load caveats for skeptics and the public; defer them for executives unless they change the decision.
7. Reorder the same beats per audience; never invent or drop findings.
8. Emit one tailored brief per audience plus a shared findings manifest.

## Inputs

- The shared findings manifest (takeaway, numbers, limits).
- A roster of audiences to tailor for, with their constraints.
- Optional: prior knowledge level and decision the audience must make.

## Outputs

- `findings_manifest.md` — the shared findings, frozen across all versions.
- `executive_summary.md` — one-slide version, decision and ask.
- `technical_methods.md` — full methods, assumptions, uncertainty.
- `public_explainer.md` — analogy plus emotion, one human number.
- `skeptic_brief.md` — caveats first, counter-evidence addressed.

## Key Rules

- The findings are frozen; only the framing, depth, and order change.
- Executives get the decision and the ask in the first two lines.
- Technical readers get the assumptions and the uncertainty bands, not just the point estimate.
- The public gets one analogy and one human-scaled number; both must be true.
- Skeptics get the caveats first and the strongest counter-evidence addressed, not dismissed.
- No audience version invents a finding that is not in the shared manifest.
- Analogies are tested: if they break under scrutiny, they are replaced, not softened.

## Examples

```text
Shared finding: "District 4 readmits 23% of patients within 30 days,
2.3x the system average; the gap is driven by a single discharge protocol."

Executive (excerpt):
"Approve a 90-day protocol swap in District 4. The current protocol
drives a 23% readmission rate, 2.3x our system average, and is the
largest controllable cost in the network."

Technical (excerpt):
"Readmission = any unplanned inpatient return within 30 days; planned
returns excluded. District 4 rate 23% (95% CI 21.5-24.6%), n=8,412.
Logistic regression controlling for age, payer, and DRG leaves the
district effect significant (OR 2.31, p<0.001)."

Public (excerpt):
"If you are discharged from a District 4 hospital, your odds of being
back within a month are about one in four, more than double the rest
of the city. The hospital knows which protocol is to blame."

Skeptic (excerpt):
"Two limits first: readmission is a noisy proxy for harm, and our
sample omits two hospitals that switched EHRs mid-year. Even after
controlling for age, payer, and DRG, the district effect holds
(OR 2.31, p<0.001), so the gap is not a coding artefact."
```
