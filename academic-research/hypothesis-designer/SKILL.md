---
name: hypothesis-designer
description: Design testable hypotheses with explicit null (H0) and alternative (H1) statements, effect-size framing, expected direction, and the statistical test that will evaluate each hypothesis. Use when the user is converting a research question into formal hypotheses or planning the inferential step of a study.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: academic-research
tags: [hypothesis, h0-h1, effect-size, statistical-test, finer]
related: [academic-research/research-question-formulator, academic-research/experimental-design-planner, academic-research/pre-registration-drafter]
prerequisites: [academic-research/research-question-formulator]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Hypothesis Designer

## When To Use
- The user says "write my hypotheses", "what is the null hypothesis", or "formalize H0/H1".
- The user is moving from a research question to a statistical test plan.
- The user needs effect-size framing and direction before sample-size calculation.
- Trigger keywords: hypothesis, null, alternative, effect size, direction, two-sided, statistical test.

## Workflow
1. Read the finalized research question from the formulator step.
2. Identify the primary outcome variable and its scale (continuous, binary, ordinal, time-to-event).
3. Draft the null hypothesis (H0): the "no effect" statement, with explicit parameter and equality sign.
4. Draft the alternative hypothesis (H1): directional (one-sided) or non-directional (two-sided), with the expected effect.
5. Specify the effect size with magnitude (e.g., Cohen's d = 0.5, OR = 2.0, hazard ratio = 0.7) and justify from prior literature or pilot data.
6. State the expected direction (improvement, decrease, non-inferiority margin).
7. Match the statistical test: t-test, Mann-Whitney, ANCOVA, mixed-effects model, log-rank, chi-square, Fisher exact.
8. List test assumptions (normality, independence, sphericity, proportional hazards) and the diagnostic check for each.
9. Define the decision rule: alpha, one/two-sided, power, and minimum detectable effect.
10. Repeat for each secondary hypothesis; mark primary vs. secondary.
11. Output the hypothesis table feeding the experimental-design step.

## Inputs
- Finalized research question.
- Primary outcome variable and its type.
- Pilot data or prior literature for effect-size estimation.
- Planned alpha (default 0.05) and power (default 0.80).
- One-sided vs. two-sided preference.

## Outputs
- `hypothesis_table.csv` — columns: ID, H0, H1, effect size, direction, test, primary/secondary.
- `effect_size_justification.md` — source for each effect-size estimate.
- `test_assumptions.md` — assumptions and diagnostic checks per test.
- `decision_rule.md` — alpha, power, MDE, one/two-sided statement.

## Key Rules
- H0 and H1 must be mutually exclusive and collectively exhaustive.
- Effect size must come from prior literature or pilot data; never guessed.
- Directional hypotheses must be justified; default to two-sided otherwise.
- Every statistical test must list its assumptions and the diagnostic used to verify them.
- Primary hypothesis is unique; multiple secondary hypotheses are allowed but flagged.
- H0 uses "=", H1 uses "≠" (two-sided) or ">" / "<" (one-sided).

## Examples
```text
Primary hypothesis:
  H0: μ_RAGT - μ_control = 0  (no difference in 6-minute walk distance at 12 weeks)
  H1: μ_RAGT - μ_control > 0  (RAGT improves distance; one-sided)
  Effect size: Cohen's d = 0.5 (medium), justified by Dobkin et al. 2020 meta-analysis.
  Test: independent two-sample t-test (or Mann-Whitney if Shapiro-Wilk p<0.05).
  Assumptions: independence, normality (Shapiro-Wilk), homoscedasticity (Levene).
  Decision rule: alpha=0.025 one-sided, power=0.80, MDE ≥ 30 m.
```
```text
Secondary hypothesis (binary outcome):
  H0: OR = 1  (no association between RAGT and independent ambulation)
  H1: OR ≠ 1  (two-sided)
  Effect size: OR = 2.0 from Langhorne 2017 cohort.
  Test: logistic regression adjusting for age and baseline NIHSS.
  Assumptions: linearity in logit for continuous covariates; checked by Box-Tidwell.
```

## References
- Cohen's effect-size conventions: https://www.utexas.edu/cola/statistics/faculty/jcohen/
- Wasserman "All of Statistics" hypothesis testing chapter.
- Kleinbaum "Logistic Regression" assumptions: https://www.sas.com/store/prodBrowse_1_2.html?parentCategory=252
- G*Power sample-size tool: https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower

## Notes
- H0 always carries the equality sign; H1 carries the strict inequality or "not equal" sign.
- Non-inferiority hypotheses need a pre-specified margin (delta) drawn from clinical or domain precedent.
- When multiple endpoints are co-primary, the family-wise error rate must be controlled explicitly.
