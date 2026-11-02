---
name: statistical-validation-rigour
description: Apply rigorous statistical validation when reporting metrics, comparing models, or computing confidence intervals. Triggers on "bootstrap CI", "AUC binary vs multiclass", "Cohen's d", "McNemar test", "Wilcoxon signed-rank", "paired t-test", "LogisticRegression deprecated multi_class".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [statistics, bootstrap-ci, mcnemar, wilcoxon, cohen-d]
related: [ml-engineering/metrics-computation-suite, ml-engineering/cross-validation-engine, ml-engineering/ablation-study-runner]
prerequisites: [ml-engineering/metrics-computation-suite]
outputs: [python, csv, json]
difficulty: advanced
estimated_tokens: 1110
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Statistical Validation Rigour

## When To Use

- Reporting confidence intervals around accuracy, AUC, F1, or any metric.
- Comparing two models on the same test set (paired t-test, Wilcoxon, McNemar).
- Computing AUC for binary versus multiclass problems.
- Fitting a `sklearn.linear_model.LogisticRegression` baseline.
- Quantifying effect sizes between proposed and baseline models.

## Workflow

1. Collect the per-fold or per-trial metric values into a list.
2. Bootstrap the metric of interest to build a 95% confidence interval.
3. Guard `np.std(values, ddof=1)` with a length check to avoid NaN on single samples.
4. Branch AUC computation by the number of unique labels.
5. For paired comparisons, run the appropriate test (t-test, Wilcoxon, McNemar).
6. Compute effect sizes (Cohen's d, Cliff's delta) for practical significance.
7. Report mean, std, 95% CI, p-value, and effect size in a single table.

## Inputs

- A list/array of metric values across folds or trials.
- Predicted probabilities and ground-truth labels.
- For paired tests: two sets of predictions on the same test set.

## Outputs

- A JSON report with mean, std, CI lower/upper, p-value, effect size.
- A comparison table saved to `Aggregated/StatisticalReport.json`.

## Key Rules

- Graceful handling of n=0 (zeroed dict) and n=1 (single-value dict).
- Guard `np.std` with `float(np.std(values, ddof=1)) if (len(values) > 1) else 0.0`.
- Binary AUC uses 1-D positive-class probabilities; multiclass uses 2-D matrix with
  `multi_class="ovr", average="macro"`.
- NEVER pass `multi_class=` to `sklearn.linear_model.LogisticRegression` — it is deprecated.
- Paired tests require the same test set for both models.
- Report exact p-values, not thresholds.

## Examples

```python
# Bootstrap with graceful n=0 and n=1 handling.
import numpy as np
from sklearn.metrics import roc_auc_score
from scipy import stats


def BootstrapAUC(Probabilities, Labels, Iterations=1000):
  """Bootstrap a 95% confidence interval for AUC."""
  # Graceful empty-input path.
  if (len(Labels) == 0):
    return {"Mean": 0.0, "Std": 0.0, "Lower": 0.0, "Upper": 0.0}
  # Single-sample path returns a degenerate interval.
  if (len(Labels) == 1):
    return {"Mean": 0.0, "Std": 0.0, "Lower": 0.0, "Upper": 0.0}
  uniqueLabels = np.unique(Labels)
  # Branch on binary versus multiclass.
  if (len(uniqueLabels) <= 2):
    pointEstimate = roc_auc_score(Labels, Probabilities[:, 1])
  else:
    pointEstimate = roc_auc_score(
      Labels,
      Probabilities,
      multi_class="ovr",
      average="macro"
    )
  bootstrapped = []
  for i in range(Iterations):
    # Resample with replacement.
    idx = np.random.choice(len(Labels), size=len(Labels), replace=True)
    # Branch again on the resampled set.
    if (len(np.unique(Labels[idx])) <= 2):
      bootstrapped.append(roc_auc_score(Labels[idx], Probabilities[idx, 1]))
    else:
      bootstrapped.append(roc_auc_score(
        Labels[idx],
        Probabilities[idx],
        multi_class="ovr",
        average="macro"
      ))
  # Guard std computation for edge cases.
  stdValue = float(np.std(bootstrapped, ddof=1)) if (len(bootstrapped) > 1) else 0.0
  return {
    "Mean": float(pointEstimate),
    "Std": stdValue,
    "Lower": float(np.percentile(bootstrapped, 2.5)),
    "Upper": float(np.percentile(bootstrapped, 97.5))
  }


def CohensD(SeriesA, SeriesB):
  """Compute Cohen's d effect size."""
  # Pooled standard deviation.
  pooledStd = np.sqrt(
    (np.var(SeriesA, ddof=1) + np.var(SeriesB, ddof=1)) / 2.0
  )
  # Guard against division by zero.
  if (pooledStd == 0):
    return 0.0
  return float((np.mean(SeriesA) - np.mean(SeriesB)) / pooledStd)
```

## References

- sklearn metrics: https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
- scipy stats: https://docs.scipy.org/doc/scipy/reference/stats.html
- LogisticRegression deprecation
  notice: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
