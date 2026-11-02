---
name: cross-validation-engine
description: Run k-fold cross-validation (stratified, grouped, or time-series) when evaluating model generalization. Triggers on "k-fold CV", "StratifiedKFold", "GroupKFold", "TimeSeriesSplit", "nested CV", "mean plus minus std", "subject-level CV".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [cross-validation, kfold, stratified, grouped, timeseries]
related: [ml-engineering/train-val-test-splitter, ml-engineering/statistical-validation-rigour, ml-engineering/data-leakage-guard]
prerequisites: [ml-engineering/train-val-test-splitter]
outputs: [python, csv, json]
difficulty: advanced
estimated_tokens: 1050
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Cross Validation Engine

## When To Use

- Estimating model performance with limited held-out data.
- Grouping subjects so no subject appears in both train and test of a fold.
- Tuning hyperparameters with nested CV (outer evaluates, inner tunes).
- Time-series evaluation where future must not leak into the past.

## Workflow

1. Choose the CV strategy: `StratifiedKFold`, `GroupKFold`, `TimeSeriesSplit`, or nested.
2. For grouped CV, pass `Groups` so no subject appears in both train and test of a fold.
3. For each fold, train the model with identical seed and hyperparameters.
4. Evaluate on the held-out fold using the metrics suite.
5. Collect metrics across folds.
6. Report mean ± std across folds.
7. For nested CV, run the inner loop for hyperparameter tuning inside each outer fold.
8. Persist `Aggregated/CvResults.json` with per-fold metrics and aggregates.

## Inputs

- Features, labels, and optional `Groups` array.
- `Configs/Config.yaml` with `NumFolds`, `Strategy`, `Seed`.

## Outputs

- `Aggregated/CvResults.json` with per-fold metrics and mean/std.
- A summary table printed to the console.

## Key Rules

- For grouped CV, ensure no subject appears in both train and test of the same fold.
- Report mean ± std across folds (use `ddof=1`).
- For nested CV, the outer loop evaluates; the inner loop tunes.
- For `TimeSeriesSplit`, never shuffle.
- Use the same seed for every fold to keep runs comparable.

## Examples

```python
# K-fold CV with subject-level grouping and mean +/- std reporting.
import json
import numpy as np
from sklearn.model_selection import StratifiedKFold, GroupKFold, TimeSeriesSplit


def BuildCvSplitter(Strategy, NumFolds, Seed):
  """Return the configured CV splitter."""
  # Branch on the strategy name.
  if (Strategy == "Stratified"):
    return StratifiedKFold(n_splits=NumFolds, shuffle=True, random_state=Seed)
  if (Strategy == "Grouped"):
    return GroupKFold(n_splits=NumFolds)
  if (Strategy == "TimeSeries"):
    return TimeSeriesSplit(n_splits=NumFolds)
  raise ValueError(f"Unknown CV strategy: {Strategy}")


def RunCrossValidation(ModelFactory, Features, Labels, Groups, Config, OutputDir):
  """Run k-fold CV and persist per-fold metrics."""
  # Resolve the strategy and fold count.
  splitter = BuildCvSplitter(
    Config["Strategy"],
    Config["NumFolds"],
    Config["Seed"]
  )
  foldMetrics = []
  for foldIdx, (trainIdx, testIdx) in enumerate(splitter.split(Features, Labels, groups=Groups)):
    # Train this fold's model.
    model = ModelFactory(Config)
    # Branch on whether the splitter accepts groups.
    if (Config["Strategy"] == "Grouped"):
      model.fit(Features[trainIdx], Labels[trainIdx])
      preds = model.predict(Features[testIdx])
    else:
      model.fit(Features[trainIdx], Labels[trainIdx])
      preds = model.predict(Features[testIdx])
    # Compute accuracy for this fold.
    acc = float((preds == Labels[testIdx]).mean())
    foldMetrics.append({"Fold": foldIdx, "Accuracy": acc})
  # Compute mean and std across folds.
  accs = [m["Accuracy"] for m in foldMetrics]
  meanAcc = float(np.mean(accs))
  stdAcc = float(np.std(accs, ddof=1)) if (len(accs) > 1) else 0.0
  # Persist the results JSON.
  report = {
    "FoldMetrics": foldMetrics,
    "MeanAccuracy": meanAcc,
    "StdAccuracy": stdAcc
  }
  with open(OutputDir + "CvResults.json", "w") as f:
    json.dump(report, f, indent=2)
  return report
```

## References

- sklearn cross-validation: https://scikit-learn.org/stable/modules/cross_validation.html
- StratifiedKFold: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
- GroupKFold: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html
- TimeSeriesSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- Nested CV: https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html
