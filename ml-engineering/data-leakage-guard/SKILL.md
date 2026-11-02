---
name: data-leakage-guard
description: Enforce strict train/validation/test isolation when preprocessing data, fitting transformers, or partitioning samples. Triggers on "data leakage", "fit on train only", "GroupShuffleSplit", "subject-level split", "stratified partitioning".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [data-leakage, train-test-isolation, preprocessing, fitting, partitioning]
related: [ml-engineering/train-val-test-splitter, ml-engineering/cross-validation-engine, ml-engineering/dataset-adapter-builder]
prerequisites: []
outputs: [python]
difficulty: advanced
estimated_tokens: 870
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Data Leakage Guard

## When To Use
- Fitting any transformer that computes global statistics (scaler, imputer, PCA, feature selector).
- Partitioning data into train/validation/test where subjects may have multiple samples.
- Auditing a preprocessing pipeline for leakage between splits.
- Designing a time-series split where future information must not leak into the past.
- Writing the methods section that documents the partitioning scheme.

## Workflow
1. Identify the highest hierarchical grouping (subject, patient, time-series window).
2. Partition at that level using `GroupShuffleSplit` or `StratifiedGroupKFold`.
3. Fit every statistical transformer EXCLUSIVELY on the training split.
4. Apply `.transform()` to validation and test splits only — never `.fit()`.
5. Fix the random seed for shuffle, weight init, and partitioning.
6. Record which groups landed in which split to a JSON manifest.
7. Document the partitioning scheme in the manuscript methods section.
8. Add a runtime assertion that no group appears in more than one split.

## Inputs
- Features and labels arrays.
- A `Groups` array identifying the hierarchical unit for each sample.
- A `Configs/Config.yaml` with split ratios and seed.

## Outputs
- Three isolated splits (train, validation, test).
- Fitted transformers persisted via `joblib.dump`.
- A `PartitionManifest.json` listing groups per split.

## Key Rules
- Scalers, imputers, PCA, and feature selectors MUST be fit on training data only.
- Partition at the highest hierarchical level — never at the sample level.
- The same seed must drive shuffle, weight init, and partitioning.
- Assert no overlap between training groups and test groups.
- Never call `.fit_transform()` on the validation or test split.
- Document the partitioning scheme so reviewers can reproduce it.

## Examples
```python
# Partition at subject level, then fit scaler on training only.
import json
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
import joblib


def SplitByGroup(Features, Labels, Groups, TestSize, Seed):
  """Split data so no subject leaks across train and test."""
  # Use GroupShuffleSplit to keep subjects whole.
  splitter = GroupShuffleSplit(n_splits=1, test_size=TestSize, random_state=Seed)
  # First split separates test from the rest.
  trainValIdx, testIdx = next(splitter.split(Features, Labels, groups=Groups))
  # Second split separates validation from train.
  trainIdx, valIdx = next(splitter.split(
    Features[trainValIdx],
    Labels[trainValIdx],
    groups=Groups[trainValIdx]
  ))
  return trainIdx, valIdx, testIdx


def FitScalersOnTrainOnly(TrainFeatures, ValFeatures, TestFeatures):
  """Fit scaler on train, then transform val and test."""
  # Fit exclusively on the training split.
  scaler = StandardScaler().fit(TrainFeatures)
  # Transform validation and test using the fitted scaler.
  scaledTrain = scaler.transform(TrainFeatures)
  scaledVal = scaler.transform(ValFeatures)
  scaledTest = scaler.transform(TestFeatures)
  # Persist the fitted scaler for deployment.
  joblib.dump(scaler, "Aggregated/Scaler.joblib")
  return scaledTrain, scaledVal, scaledTest
```

## References
- sklearn preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html
- GroupShuffleSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
