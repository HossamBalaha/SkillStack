---
name: feature-engineering-toolkit
description: Build numeric features (polynomial, log, sqrt, binning), categorical features (one-hot, ordinal, target/mean encoding with CV, frequency), interaction features, datetime features, and lag/rolling window features with closed='right' to prevent leakage. Use this skill when constructing features for tabular models.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [feature-engineering, polynomial, binning, lag-features, datetime]
related: [data-engineering/categorical-encoder, data-engineering/missing-data-imputer]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1300
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
---

# Feature Engineering Toolkit

## When To Use
- A model needs derived features beyond the raw columns.
- Target encoding must avoid leakage via k-fold cross-validation.
- Time series features need lag and rolling windows with the right closure side.
- Datetime columns must yield calendar features (day_of_week, is_weekend, hour).
- Feature transforms must be fit on TRAIN and reused unchanged at inference.

## Workflow
1. Split into TRAIN/VAL/TEST before engineering to avoid leakage.
2. Profile each column: dtype, cardinality, missingness, distribution.
3. Pick a transform per column: numeric, categorical, datetime, interaction, window.
4. Fit transforms on TRAIN only and persist them (joblib).
5. Apply transforms to VAL and TEST with the fitted state.
6. Attach a feature manifest recording transform, parameters, and source columns.
7. Validate: no leakage (no future data in TRAIN features), no NaN unless intended.
8. Emit the engineered matrix plus the manifest and the persisted transforms.

## Inputs
- TRAIN, VAL, TEST DataFrames sharing the same schema.
- Per-column transform configuration.
- Optional target column for supervised encoders (target/mean encoding).

## Outputs
- Engineered TRAIN, VAL, TEST feature matrices.
- A feature manifest (JSON) listing transform per column and parameters.
- Persisted transform artifacts (joblib) for inference reuse.

## Key Rules
- All transforms fit on TRAIN only; VAL and TEST are transformed.
- Target/mean encoding uses k-fold CV on TRAIN to avoid leakage.
- Rolling windows use `closed='right'` so the current row's target is excluded.
- Lag features shift by a positive integer; negative shifts are forbidden.
- Datetime features derive from TRAIN timestamps only; no future lookups.
- Feature names are deterministic and stable across runs.
- The manifest is the single source of truth for what was engineered.

## Examples

```python
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import KFold


def AddNumericFeatures(df, column):
  # Attach log and sqrt transforms for skewed numeric columns.
  df[f"{column}_log"] = np.log1p(df[column].clip(lower=0))
  df[f"{column}_sqrt"] = np.sqrt(df[column].clip(lower=0))
  return df


def AddDatetimeFeatures(df, tsColumn):
  # Derive calendar features without leaking future information.
  ts = pd.to_datetime(df[tsColumn])
  df[f"{tsColumn}_day_of_week"] = ts.dt.dayofweek
  df[f"{tsColumn}_is_weekend"] = ts.dt.dayofweek.isin([5, 6]).astype(int)
  df[f"{tsColumn}_hour"] = ts.dt.hour
  return df


def AddRollingFeatures(df, valueColumn, groupColumn, window=7):
  # Rolling mean and std with closed='right' so the current row is excluded.
  grouped = df.groupby(groupColumn)[valueColumn]
  df[f"{valueColumn}_rolling_mean_{window}"] = (
    grouped.transform(lambda s: s.shift(1).rolling(window, closed="right").mean())
  )
  df[f"{valueColumn}_rolling_std_{window}"] = (
    grouped.transform(lambda s: s.shift(1).rolling(window, closed="right").std())
  )
  return df


class TargetEncoder:
  # k-fold target encoder that fits only on TRAIN to prevent leakage.
  def __init__(self, nSplits=5, smoothing=10.0):
    self.NSplits = nSplits
    self.Smoothing = smoothing
    self.GlobalMean = None
    self.Mapping = {}

  def Fit(self, series, target):
    # Compute per-category means and the global mean from TRAIN.
    self.GlobalMean = target.mean()
    stats = pd.DataFrame({"cat": series, "y": target}).groupby("cat")["y"]
    counts = stats.count()
    means = stats.mean()
    smoothed = (counts * means + self.Smoothing * self.GlobalMean) / (counts + self.Smoothing)
    self.Mapping = smoothed.to_dict()

  def Transform(self, series):
    # Map categories to smoothed means; unseen categories fall back to global mean.
    return series.map(self.Mapping).fillna(self.GlobalMean)

  def FitTransform(self, series, target):
    # Out-of-fold encoding so TRAIN is not overfitted to its own target.
    kf = KFold(n_splits=self.NSplits, shuffle=True, random_state=42)
    encoded = pd.Series(index=series.index, dtype=float)
    for trainIdx, validIdx in kf.split(series):
      self.Fit(series.iloc[trainIdx], target.iloc[trainIdx])
      encoded.iloc[validIdx] = self.Transform(series.iloc[validIdx])
    self.Fit(series, target)
    return encoded

  def Persist(self, path):
    joblib.dump(self, path)
```

## References
- scikit-learn preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html
- pandas rolling: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html
- Target encoding (Micci-Barreca 2001): https://kaggle.com/code/ogrellier/python-target-encoding-for-categorical-features
