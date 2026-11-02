---
name: categorical-encoder
description: Encode categorical columns using one-hot (low cardinality), ordinal (meaningful order), target/mean encoding with k-fold CV, frequency encoding, hash encoding (fixed dim for high cardinality), or entity embeddings learned via NN. Use this skill when picking the right encoding per column and documenting cardinality and strategy.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [categorical, encoding, one-hot, target-encoding, embeddings]
related: [data-engineering/feature-engineering-toolkit, data-engineering/data-quality-validator, data-engineering/data-schema-enforcer]
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

# Categorical Encoder

## When To Use
- A model requires numeric inputs but the source has categorical columns.
- Cardinality varies widely per column and one strategy does not fit all.
- Target/mean encoding must avoid leakage via k-fold cross-validation.
- High-cardinality columns need a fixed-dimension encoding (hash or embedding).
- An audit trail must record the chosen strategy per column.

## Workflow
1. Profile every categorical column: cardinality, top values, missingness.
2. Pick a strategy per column based on cardinality and presence of order.
3. Fit the encoder on TRAIN only and persist it for inference.
4. Transform VAL and TEST with the fitted encoder.
5. Handle unseen categories: hash encoders ignore them; target encoders fall back to global mean.
6. Record an encoding manifest: column, strategy, parameters, cardinality.
7. Validate: output shape matches expectation, no NaN unless explicit.
8. Emit the encoded matrices and the manifest.

## Inputs
- TRAIN, VAL, TEST DataFrames with categorical columns.
- Per-column strategy specification (one_hot, ordinal, target, frequency, hash, embedding).

## Outputs
- Encoded TRAIN, VAL, TEST matrices.
- An encoding manifest (JSON) listing strategy per column.
- Persisted encoder artifacts (joblib) for inference reuse.

## Key Rules
- Encoders fit on TRAIN only; VAL and TEST are transformed.
- Unseen categories at inference fall back to a declared default, never error silently.
- One-hot encoding is reserved for low cardinality (typically < 20 categories).
- Target encoding always uses k-fold CV on TRAIN to prevent leakage.
- Hash encoding uses a fixed dimension so cardinality cannot blow up the schema.
- The manifest is the single source of truth for the chosen strategy per column.
- Ordinal encoding requires an explicit category order, never alphabetical by default.

## Examples

```python
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction import FeatureHasher
from sklearn.model_selection import KFold


class FrequencyEncoder:
  # Encodes categories by their TRAIN frequency, stable across runs.
  def __init__(self):
    self.Mapping = {}

  def Fit(self, series):
    counts = series.value_counts(normalize=True)
    self.Mapping = counts.to_dict()

  def Transform(self, series):
    return series.map(self.Mapping).fillna(0.0)

  def Persist(self, path):
    joblib.dump(self, path)


class HashEncoder:
  # Fixed-dimension encoder for high-cardinality columns.
  def __init__(self, nFeatures=64):
    self.NFeatures = nFeatures
    self.Hasher = FeatureHasher(n_features=nFeatures, input_type="string")

  def Transform(self, series):
    matrix = self.Hasher.transform([[str(v)] for v in series.values])
    return np.asarray(matrix.todense())


class TargetEncoder:
  # k-fold target encoder that fits only on TRAIN.
  def __init__(self, nSplits=5, smoothing=10.0):
    self.NSplits = nSplits
    self.Smoothing = smoothing
    self.GlobalMean = None
    self.Mapping = {}

  def FitTransform(self, series, target):
    kf = KFold(n_splits=self.NSplits, shuffle=True, random_state=42)
    encoded = pd.Series(index=series.index, dtype=float)
    for trainIdx, validIdx in kf.split(series):
      self.GlobalMean = target.iloc[trainIdx].mean()
      stats = pd.DataFrame({"cat": series.iloc[trainIdx], "y": target.iloc[trainIdx]}).groupby("cat")["y"]
      counts = stats.count()
      means = stats.mean()
      smoothed = (counts * means + self.Smoothing * self.GlobalMean) / (counts + self.Smoothing)
      encoded.iloc[validIdx] = series.iloc[validIdx].map(smoothed.to_dict()).fillna(self.GlobalMean)
    self.GlobalMean = target.mean()
    stats = pd.DataFrame({"cat": series, "y": target}).groupby("cat")["y"]
    counts = stats.count()
    means = stats.mean()
    self.Mapping = ((counts * means + self.Smoothing * self.GlobalMean) / (counts + self.Smoothing)).to_dict()
    return encoded

  def Transform(self, series):
    return series.map(self.Mapping).fillna(self.GlobalMean)


def ChooseStrategy(cardinality, hasOrder, hasTarget):
  # Pick a strategy from cardinality and whether an order/target exists.
  if (cardinality <= 20):
    return "one_hot"
  if (hasOrder):
    return "ordinal"
  if (hasTarget):
    return "target"
  if (cardinality > 1000):
    return "hash"
  return "frequency"
```

## References
- scikit-learn encoders: https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
- FeatureHasher: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.FeatureHasher.html
- Entity embeddings (Guo & Berkhahn 2016): https://arxiv.org/abs/1604.06737
