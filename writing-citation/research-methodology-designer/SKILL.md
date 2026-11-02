---
name: research-methodology-designer
description: Designs complete research methodologies covering study design, sampling strategy, sample-size calculation, data-collection methods, and ethical considerations. Use when planning an empirical study (RCT, cohort, case-control, cross-sectional, or qualitative) and when a grant proposal or IRB protocol requires a defensible methods section.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [methodology, rct, sampling, sample-size, irb]
related: [writing-citation/imrad-thesis-writer, writing-citation/annotated-bibliography-builder]
prerequisites: []
outputs: [markdown]
difficulty: advanced
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Research Methodology Designer

## When To Use
- You are writing a grant proposal and need a rigorous methods section with sample-size justification.
- An IRB protocol requires explicit sampling strategy, data-collection instruments, and risk/benefit analysis.
- A supervisor asked you to justify why an RCT is more appropriate than a cohort study (or vice versa).
- A reviewer challenged the adequacy of your sample size or the representativeness of your sample.

## Workflow
1. Clarify the research question (PICO/PECO/SPIDER for qualitative) and the primary outcome.
2. Select the study design (RCT, cohort, case-control, cross-sectional, qualitative) and justify why alternatives were rejected.
3. Define the target population, accessible population, and sampling frame; choose probability (simple random, stratified, cluster) vs. non-probability (convenience, purposive, snowball) sampling.
4. Compute sample size via power analysis: alpha = 0.05 (two-sided), power = 0.80, effect size from pilot data or prior literature; report the formula and inputs.
5. Specify data-collection instruments (validated scales, interview guides, sensors, administrative data) and their psychometric properties.
6. Detail the analytic plan: descriptive statistics, primary inferential test, pre-specified subgroup analyses, and handling of missing data.
7. Address ethics: IRB oversight, informed consent process, data-anonymization, conflicts of interest, and benefit/risk balance.
8. Document threats to validity (internal, external, construct, statistical conclusion) and the mitigations for each.
9. Package the methodology as a single coherent methods section plus an appendix with instruments and power calculations.

## Inputs
- The research question and primary/secondary outcomes.
- Pilot effect size, expected variance, and attrition rate (for power analysis).
- Target population description and accessible sampling frame.
- Institutional IRB requirements and applicable regulatory frameworks (e.g., 45 CFR 46, GDPR).

## Outputs
- `methodology_design.md` — full methods section ready for a proposal or protocol.
- `power_calculation.md` — inputs, formula, software output (G*Power or R), and resulting N.
- `ethics_checklist.md` — IRB items, consent template pointers, data-management plan.
- `validity_matrix.csv` — threat → category → mitigation.

## Key Rules
- Sample-size calculation must state alpha, power, effect size, allocation ratio, and the assumed attrition adjustment.
- Probability sampling is the default for quantitative generalization; non-probability sampling must be justified.
- Every data-collection instrument must be named with a citation or attached as an appendix.
- Ethics must cover informed consent, confidentiality, and an explicit risk/benefit statement — not just "IRB approval will be obtained."
- Qualitative studies must report the analytic approach (thematic analysis, grounded theory, IPA) and trustworthiness criteria.
- Pre-registration of the analysis plan is recommended; if not pre-registered, that must be disclosed.

## Examples
```text
Before (vague):
"We will recruit about 100 patients and give them the new drug. We will
collect data on blood pressure and analyze it with statistics."

After (designed):
"Design: Single-center, parallel-group, double-blind RCT.
Population: Adults aged 18-65 with stage 2 hypertension (systolic BP
≥ 140 mmHg or diastolic ≥ 90 mmHg) at the cardiology outpatient clinic.
Sampling: Consecutive eligibility screening over a 6-month enrollment
window; 1:1 allocation via computer-generated block randomization
(block size 4), stratified by sex.
Sample size: Assuming a between-arm difference of 8 mmHg systolic BP,
common SD of 15 mmHg, alpha = 0.05 (two-sided), power = 0.80, and 15%
attrition, we require N = 88 (44 per arm) — computed in G*Power 3.1
(independent t-test, two-tailed).
Data collection: Seated office BP (mean of 3 readings, Omron HEM-7321T)
and 24-hour ambulatory BP at baseline and 12 weeks.
Ethics: Approved by the Institutional Review Board (protocol #2024-117);
written informed consent obtained prior to randomization; trial
registered at ClinicalTrials.gov (NCT0XXXXXXX)."
```

## Common Pitfalls
- Quoting a sample size without stating alpha, power, effect size, and attrition adjustment — reviewers will reject.
- Choosing a non-probability sample and then claiming generalizability to a population.
- Listing "IRB approval will be obtained" as the entire ethics section — consent, confidentiality, and risk/benefit are required.
- Forgetting to pre-register the analysis plan when the journal mandates it.
- Conflating a qualitative approach with a small quantitative study — qualitative sampling logic differs (information power, not statistical power).
- Skipping threats-to-validity; reviewers treat this as a fatal omission for empirical work.

## References
- Schulz, K. F., Altman, D. G., & Moher, D. (2010). CONSORT 2010 Statement. *BMJ*, 340, c332.
- G*Power statistical power-analysis software: https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower.
- 45 CFR 46 — U.S. Federal Policy for the Protection of Human Subjects.
- Creswell, J. W., & Creswell, J. D. (2018). *Research Design: Qualitative, Quantitative, and Mixed Methods Approaches*. SAGE.
