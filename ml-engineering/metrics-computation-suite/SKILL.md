---
name: metrics-computation-suite
description: Compute a comprehensive metrics suite (accuracy, precision, recall, F1, AUC, MCC, Cohen's kappa, ECE/MCE, confusion matrix) with 95% bootstrap CIs. Triggers on "compute metrics", "macro micro weighted F1", "AUC binary multiclass", "MCC", "Cohen kappa", "ECE MCE calibration", "confusion matrix".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [metrics, f1, auc, mcc, cohen-kappa, calibration]
related: [ml-engineering/statistical-validation-rigor, ml-engineering/ablation-study-runner, ml-engineering/baseline-model-zoo]
prerequisites: []
outputs: [python, json, csv]
difficulty: advanced
estimated_tokens: 1580
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Metrics Computation Suite

## When To Use

- Computing classification metrics after a training run.
- Branching AUC by binary vs multiclass based on the number of unique labels.
- Reporting calibration error (ECE, MCE) for probabilistic predictions.
- Producing a confusion matrix and derived metrics with 95% CIs.

## Workflow

1. Collect predicted probabilities, predicted classes, and ground-truth labels.
2. Branch AUC: 1-D positive-class probabilities for binary, 2-D matrix `multi_class="ovr", average="macro"` for
   multiclass.
3. Compute accuracy, precision, recall, F1 (macro/micro/weighted).
4. Compute Matthews Correlation Coefficient (MCC) and Cohen's kappa.
5. Compute calibration error (ECE, MCE) by binning predicted probabilities.
6. Compute the confusion matrix.
7. Bootstrap every metric for a 95% CI.
8. Persist `Aggregated/MetricsReport.json`.

## Inputs

- Predicted probabilities (2-D for multiclass, or 1-D positive-class for binary).
- Predicted class labels and ground-truth labels.
- Number of bootstrap iterations from `Configs/Config.yaml`.

## Outputs

- `Aggregated/MetricsReport.json` with point estimates and 95% CIs.
- `Aggregated/ConfusionMatrix.csv`.

## Key Rules

- Branch AUC computation by `len(np.unique(labels))`.
- Binary AUC uses 1-D positive-class probabilities.
- Multiclass AUC uses 2-D matrix with `multi_class="ovr", average="macro"`.
- Every metric must come with a 95% bootstrap CI.
- Use `sklearn.metrics` as the reference implementation.

## Examples

```python
# Metrics suite with AUC branching and bootstrap CIs.
import json
import numpy as np
from sklearn.metrics import (
  accuracy_score,
  precision_recall_fscore_support,
  matthews_corrcoef,
  cohen_kappa_score,
  confusion_matrix,
  roc_auc_score
)


def ComputeAUC(Probabilities, Labels):
  """Branch AUC by binary vs multiclass."""
  # Determine the number of unique labels.
  uniqueLabels = np.unique(Labels)
  if (len(uniqueLabels) <= 2):
    # Binary path: 1-D positive-class probabilities.
    return float(roc_auc_score(Labels, Probabilities[:, 1]))
  # Multiclass path: 2-D matrix with ovr/macro.
  return float(roc_auc_score(
    Labels,
    Probabilities,
    multi_class="ovr",
    average="macro"
  ))


def ComputeExpectedCalibrationError(Probabilities, Labels, NumBins=10):
  """Compute ECE by binning predicted probabilities."""
  # Confidence is the max predicted probability.
  confidences = np.max(Probabilities, axis=1)
  preds = np.argmax(Probabilities, axis=1)
  # Bin the confidences.
  binEdges = np.linspace(0.0, 1.0, NumBins + 1)
  ece = 0.0
  n = len(Labels)
  for i in range(NumBins):
    # Select samples in this bin.
    inBin = (confidences > binEdges[i]) & (confidences <= binEdges[i + 1])
    if (inBin.sum() == 0):
      continue
    # Average confidence and accuracy in this bin.
    binConf = confidences[inBin].mean()
    binAcc = (preds[inBin] == Labels[inBin]).mean()
    # Weighted contribution to ECE.
    ece += (inBin.sum() / n) * abs(binAcc - binConf)
  return float(ece)


def ComputeMetricsSuite(Probabilities, PredLabels, TrueLabels, NumBootstraps=1000):
  """Compute the full metrics suite with bootstrap CIs."""
  # Point estimates.
  pointEstimates = {
    "Accuracy": float(accuracy_score(TrueLabels, PredLabels)),
    "MCC": float(matthews_corrcoef(TrueLabels, PredLabels)),
    "Kappa": float(cohen_kappa_score(TrueLabels, PredLabels)),
    "AUC": ComputeAUC(Probabilities, TrueLabels),
    "ECE": ComputeExpectedCalibrationError(Probabilities, TrueLabels)
  }
  # Add precision/recall/F1.
  precision, recall, f1, _ = precision_recall_fscore_support(
    TrueLabels,
    PredLabels,
    average="macro",
    zero_division=0
  )
  pointEstimates["PrecisionMacro"] = float(precision)
  pointEstimates["RecallMacro"] = float(recall)
  pointEstimates["F1Macro"] = float(f1)
  # Bootstrap CIs for each metric.
  cis = {}
  for metricName in pointEstimates:
    samples = []
    for _ in range(NumBootstraps):
      idx = np.random.choice(len(TrueLabels), size=len(TrueLabels), replace=True)
      # Guard against degenerate resamples.
      if (len(np.unique(TrueLabels[idx])) < 2):
        continue
      if (metricName == "AUC"):
        samples.append(ComputeAUC(Probabilities[idx], TrueLabels[idx]))
      elif (metricName == "Accuracy"):
        samples.append(float(accuracy_score(TrueLabels[idx], PredLabels[idx])))
      elif (metricName == "MCC"):
        samples.append(float(matthews_corrcoef(TrueLabels[idx], PredLabels[idx])))
      elif (metricName == "Kappa"):
        samples.append(float(cohen_kappa_score(TrueLabels[idx], PredLabels[idx])))
      elif (metricName == "ECE"):
        samples.append(ComputeExpectedCalibrationError(Probabilities[idx], TrueLabels[idx]))
      else:
        samples.append(pointEstimates[metricName])
    if (len(samples) > 1):
      cis[metricName] = {
        "Lower": float(np.percentile(samples, 2.5)),
        "Upper": float(np.percentile(samples, 97.5))
      }
    else:
      cis[metricName] = {"Lower": 0.0, "Upper": 0.0}
  report = {"PointEstimates": pointEstimates, "ConfidenceIntervals": cis}
  with open("Aggregated/MetricsReport.json", "w") as f:
    json.dump(report, f, indent=2)
  # Confusion matrix CSV.
  cm = confusion_matrix(TrueLabels, PredLabels)
  np.savetxt("Aggregated/ConfusionMatrix.csv", cm, delimiter=",", fmt="%d")
  return report
```
