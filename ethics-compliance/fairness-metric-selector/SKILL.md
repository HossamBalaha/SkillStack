---
name: fairness-metric-selector
description: Select fairness metrics appropriate to the task (demographic parity, equalized odds, predictive parity, calibration within groups) and conduct trade-off analysis so that the chosen metric aligns with the application context. Use when evaluating a classifier or risk-score model for fairness across protected subgroups.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [fairness-metrics, demographic-parity, equalized-odds, calibration, trade-off]
related: [ethics-compliance/algorithmic-audit-reporter, ethics-compliance/ai-impact-assessment, ethics-compliance/data-minimization-designer]
prerequisites: []
outputs: [markdown, python]
difficulty: advanced
estimated_tokens: 1600
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Fairness Metric Selector

## When To Use

- The user says "which fairness metric should I use?", "evaluate our model for fairness", or "is our classifier
  biased?".
- A model produces decisions affecting access to credit, employment, healthcare, housing, education, or justice.
- A regulator or internal review board has requested a fairness audit with justification for the metric choice.
- A team has multiple fairness metrics in conflict (e.g., demographic parity satisfied but equalized odds violated) and
  needs a documented choice.
- Trigger keywords: fairness, demographic parity, equalized odds, predictive parity, calibration, protected attribute,
  disparate impact.

## Workflow

1. Identify the protected or sensitive attributes in scope (race, gender, age band, disability status, etc.) and the
   relevant subgroups within each.
2. Determine the decision type: binary classification, multi-class, regression, ranking, or risk scoring.
3. Determine the harm orientation: allocative harm (who gets a resource) vs. representational harm (how groups are
   depicted). Allocative harms usually map to equalized odds or predictive parity.
4. Enumerate candidate metrics: demographic parity (statistical parity difference and disparate impact ratio), equalized
   odds (equal true positive and false positive rates), equal opportunity (equal true positive rate), predictive parity
   (equal positive predictive value), calibration within groups, and treatment equality.
5. For each metric, state its formal definition, its assumptions, and its failure modes (e.g., demographic parity
   forbids a perfect classifier when base rates differ).
6. Compute every candidate metric on the evaluation set per subgroup; report point estimates and bootstrap confidence
   intervals.
7. Visualise trade-offs: a metric × subgroup heatmap and a Pareto frontier of conflicting metrics.
8. Apply the Impossibility Theorem check: if base rates differ, demographic parity, equalized odds, and calibration
   cannot all hold simultaneously — choose explicitly.
9. Justify the chosen metric against the application context: "equalized odds for a hiring screen because false
   negatives and false positives both carry harm to candidates".
10. Specify acceptance thresholds: e.g., disparate impact ratio >= 0.8 (four-fifths rule) or equalized odds
    difference <= 0.05.
11. Provide a code snippet that computes the chosen metrics from a predictions file and produces the visualisations.
12. Document the limitations and the next-step mitigations: data augmentation, reweighting, threshold adjustment, or
    post-processing.

## Inputs

- Predictions file (true labels, predicted labels, predicted scores, subgroup attribute).
- Evaluation set with subgroup annotations (sufficient sample size per subgroup).
- Application context: what decision the model informs and which harms matter.
- Legal or regulatory constraints (e.g., four-fifths rule for US employment).
- Risk appetite and acceptance thresholds.

## Outputs

- `metric_catalog.md` — every metric with definition, assumptions, and failure modes.
- `metric_results.md` — point estimate and 95% bootstrap CI per subgroup for each candidate metric.
- `tradeoff_heatmap.svg` — metric × subgroup visualisation.
- `pareto_frontier.svg` — conflicting metrics Pareto frontier.
- `justification.md` — chosen metric, threshold, and rationale against the application context.
- `compute_fairness.py` — Python snippet that loads predictions and produces the metrics and figures.
- `limitations.md` — impossibility theorem implications and next-step mitigations.

## Key Rules

- The chosen metric must be justified against the application context; "we use demographic parity because it is common"
  is not acceptable.
- If base rates differ across subgroups, the Impossibility Theorem applies and a documented trade-off choice is
  mandatory.
- Sample size per subgroup must be sufficient for stable estimates; small subgroups require bootstrap CIs and a minimum
  cell size check.
- Calibration within groups is necessary but not sufficient; a calibrated model can still produce different error rates.
- Threshold tuning that improves fairness must be reported with its effect on overall accuracy and subgroup accuracy.
- "Fairness through unawareness" (dropping the protected attribute) is rarely sufficient; proxy attributes must be
  checked.
- Fairness metrics quantify disparity; they do not certify absence of bias, and they must be paired with a harm
  analysis.

## Examples

```text
Metric choice (credit default prediction):
  Harm orientation: allocative; false denials harm applicants.
  Candidate metrics: equalized odds, predictive parity, demographic parity.
  Base rates: defaulted at 12% (Group A) vs. 18% (Group B).
  Impossibility Theorem: applies; choose equalized odds.
  Threshold: equalized odds difference <= 0.05.
  Result: 0.07 → FAIL; mitigate by group-specific thresholds,
  re-evaluate, document trade-off against overall accuracy.
```

```python
# compute_fairness.py (excerpt)
from fairlearn.metrics import (
    demographic_parity_difference, equalized_odds_difference,
    selection_rate,
)
def report(y_true, y_pred, sensitive):
    return {
        "dp_diff": demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive),
        "eo_diff": equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive),
    }
```

## References

- Barocas, Hardt, and Narayanan "Fairness and Machine Learning" (2019): https://fairmlbook.org/
- Hardt, Price, and Srebro "Equality of Opportunity in Supervised Learning" (NeurIPS
  2016): https://arxiv.org/abs/1610.02413
- Chouldechova "Fair prediction with disparate impact" (2017): https://arxiv.org/abs/1703.00056
- Kleinberg, Mullainathan, Raghavan "Inherent Trade-Offs in the Fair Determination of Risk Scores" (ITCS
  2017): https://arxiv.org/abs/1609.05807
- Fairlearn toolkit documentation: https://fairlearn.org/
- US EEOC four-fifths rule: https://www.eeoc.gov/laws-guiadance/section-15-national-origin-discrimination#VI-A
