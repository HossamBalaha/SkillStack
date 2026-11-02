---
name: outlier-detector
description: Detect outliers using statistical methods (IQR and z-score), distance-based methods (DBSCAN), tree-based methods (Isolation Forest), and local methods (Local Outlier Factor). Use this skill when flagging anomalous rows, attaching scores, and documenting the threshold and rationale per column.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [outliers, iqr, isolation-forest, dbscan, lof]
related: [data-engineering/data-quality-validator, data-engineering/missing-data-imputer]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
---

# Outlier Detector

## When To Use

- Anomalous rows must be flagged for review before model training or serving.
- Different feature distributions suit different detectors (IQR vs Isolation Forest).
- Each flagged row needs a numeric score for ranking and triage.
- Thresholds must be documented so reviewers understand why a row was flagged.
- The detector must be fit on TRAIN only and applied unchanged to VAL/TEST.

## Workflow

1. Choose the detector family per column or per feature block.
2. Fit the detector on the TRAIN split; record the parameters used.
3. Score VAL and TEST rows using the fitted detector.
4. Apply a threshold (IQR fence, |z| > 3, contamination rate) to flag outliers.
5. Attach the score and the flag as new columns on the input frame.
6. Emit a report listing flagged indices, scores, and the threshold rationale.
7. Persist the fitted detector (joblib) for inference reuse.
8. Validate that the flag rate on TRAIN matches the declared contamination rate.

## Inputs

- TRAIN, VAL, TEST DataFrames with numeric features.
- Detector configuration: method, threshold, contamination, hyperparameters.

## Outputs

- DataFrames with `<feature>_score` and `<feature>_is_outlier` columns appended.
- A detection report (JSON) with flagged counts, threshold, and rationale.
- A fitted detector artifact (joblib) for inference reuse.

## Key Rules

- Detectors fit on TRAIN only; VAL and TEST are scored, never fit.
- Every flag carries a numeric score for ranking and audit.
- Thresholds and rationale are documented in the report, not just code.
- Contamination rate on TRAIN must match the declared value within tolerance.
- Persisted detectors are versioned alongside the model artifact.
- Flagged rows are surfaced, not silently dropped.

## Examples

```python
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest


def IqrFence(series, k=1.5):
  # Compute the IQR fence for univariate outlier detection.
  q1 = series.quantile(0.25)
  q3 = series.quantile(0.75)
  iqr = q3 - q1
  return {"Low": q1 - k * iqr, "High": q3 + k * iqr, "K": k}


def FlagIqr(df, column, fence):
  # Return scores (distance beyond fence) and a boolean flag.
  values = df[column]
  flag = (values < fence["Low"]) | (values > fence["High"])
  score = np.where(
    values < fence["Low"], fence["Low"] - values,
    np.where(values > fence["High"], values - fence["High"], 0.0),
  )
  return flag, score


class IsolationForestDetector:
  # Wraps IsolationForest with documented thresholds and persistence.
  def __init__(self, contamination=0.05, randomState=42):
    self.Contamination = contamination
    self.RandomState = randomState
    self.Model = IsolationForest(contamination=contamination, random_state=randomState)

  def Fit(self, df, featureColumns):
    # Fit on TRAIN only and remember the feature block.
    self.FeatureColumns = featureColumns
    self.Model.fit(df[featureColumns])

  def Score(self, df):
    # Return anomaly scores (higher = more anomalous) and a flag.
    rawScores = self.Model.decision_function(df[self.FeatureColumns])
    # Convert so positive = anomalous, matching intuition.
    scores = -rawScores
    flag = self.Model.predict(df[self.FeatureColumns]) == -1
    return flag, scores

  def Persist(self, path):
    joblib.dump(self, path)
```

## References

- scikit-learn Isolation Forest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
- scikit-learn Local Outlier
  Factor: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
- scikit-learn DBSCAN: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
