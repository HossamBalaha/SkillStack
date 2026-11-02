---
name: pre-registration-drafter
description: 'Draft pre-registration documents: AsPredicted (7 questions), OSF registrations, and Registered Report Stage 1 protocols. Includes hypotheses, design, sample size, exclusion criteria, and analysis plan BEFORE data collection. Use when the user is preparing to pre-register a study, commit to hypotheses, or submit a Registered Report Stage 1.'
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [pre-registration, aspredicted, osf, registered-report, hypotheses]
related: [academic-research/hypothesis-designer, academic-research/experimental-design-planner, academic-research/open-science-advocate]
prerequisites: [academic-research/hypothesis-designer]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 830
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Pre-Registration Drafter

## When To Use

- The user says "pre-register my study", "draft an AsPredicted", or "write an OSF registration".
- The user is submitting a Registered Report Stage 1 protocol before data collection.
- The user wants hypotheses, design, and analysis locked in before data exist.
- Trigger keywords: pre-registration, AsPredicted, OSF, Registered Report Stage 1, analysis plan, exclusion criteria.

## Workflow

1. Choose the format: AsPredicted (7-question, low overhead) for low-risk studies; OSF full registration for complex
   designs; Registered Report Stage 1 for venue-supported empirical studies.
2. Lock in the hypothesis table (from the hypothesis-designer step). No edits after registration without a formal
   amendment.
3. Specify the design family (RCT, factorial, crossover, repeated-measures, quasi-experimental) and rationale.
4. State the sample size and the power calculation that produced it (alpha, power, effect size, software).
5. List inclusion and exclusion criteria (and order: eligibility → screening → enrollment → analysis).
6. Define the primary outcome variable and its measurement protocol (instrument, timing, scorer).
7. Specify the primary statistical test, assumptions, and diagnostics.
8. Define secondary outcomes, multiplicity correction, and handling of missing data.
9. List data exclusion rules: outlier criteria (pre-specified), equipment failure, protocol deviations.
10. State the analysis population: intention-to-treat vs. per-protocol and the rule for switching.
11. Add a stopping rule for early termination (efficacy, futility, safety).
12. Output the pre-registration file in the chosen template.

## Inputs

- Hypothesis table (finalized).
- Study design (from the experimental-design-planner step).
- Power-calculation inputs.
- Eligibility and exclusion criteria.
- Chosen template (AsPredicted, OSF, Registered Report Stage 1).

## Outputs

- `aspredicted.md` — AsPredicted 7-question template (when chosen).
- `osf_registration.md` — OSF full registration (when chosen).
- `registered_report_stage1.md` — Stage 1 protocol (when chosen).
- `analysis_plan.md` — primary/secondary tests, multiplicity, missing-data plan.
- `exclusion_rules.md` — pre-specified exclusion criteria.
- `stopping_rule.md` — early-termination criteria.

## Key Rules

- Pre-registration MUST occur BEFORE data collection; post-hoc registrations are flagged.
- Hypotheses are frozen after registration; amendments require a versioned change log.
- Sample size must cite the power analysis (G*Power or equivalent).
- Exclusion criteria are pre-specified, not post-hoc.
- Analysis population and any switching rule are pre-registered.
- Stopping rule required for any study with interim analyses.

## Examples

```text
AsPredicted (excerpt, 7 questions):
  1. Have any data been collected for this study already? No.
  2. Hypothesis: RAGT + physiotherapy increases 6-min walk distance by >=30 m
     at 12 weeks compared with physiotherapy alone (one-sided, alpha=0.025).
  3. Dependent variable: 6-minute walk distance (meters).
  4. Conditions: (1) RAGT+PT, (2) PT alone.
  5. Analyses: independent two-sample t-test (Mann-Whitney if non-normal).
  6. Outliers/exclusions: baseline gait speed <0.4 m/s; protocol violations.
  7. Sample size: 60 per arm (51 from G*Power d=0.5, +15% attrition).
```

```text
Registered Report Stage 1 stopping rule:
  Interim analysis at n=40 per arm; O'Brien-Fleming boundary alpha=0.0051.
  Stop for efficacy if p < 0.0051; stop for futility if conditional power < 20%.
```

## References

- AsPredicted: https://aspredicted.org/
- Open Science Framework registrations: https://osf.io/registrations
- Registered Reports (Center for Open Science): https://www.cos.io/initiatives/registered-reports
- OSF Preregistration guidance: https://help.osf.io/article/345-create-registrations
- Nosek et al. "The Preregistration Revolution": https://doi.org/10.1073/pnas.1708274114

## Notes

- Stamp the registration timestamp and the OSF/AsPredicted ID prominently on the document.
- Any deviation between the pre-registered plan and the final analysis must be disclosed as a "departure".
- Embargoed registrations are acceptable, but they must be made public by the time of publication.
