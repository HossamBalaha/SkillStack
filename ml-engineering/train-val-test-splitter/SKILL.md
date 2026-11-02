---
name: train-val-test-splitter
description: Split data into train/validation/test with stratification at the highest hierarchical level when preparing data for training. Triggers on "train validation test split", "GroupShuffleSplit", "StratifiedGroupKFold", "subject-level split", "PartitionManifest.json", "70/15/15 split".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [train-val-test, split, stratified, groupshuffle, manifest]
related: [ml-engineering/data-leakage-guard, ml-engineering/cross-validation-engine, ml-engineering/dataset-adapter-builder]
prerequisites: []
outputs: [python, json, csv]
difficulty: intermediate
estimated_tokens: 970
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Train Val Test Splitter

## When To Use

- Partitioning a dataset into train/validation/test before training.
- Ensuring subjects (or time-series windows) do not leak across splits.
- Documenting which subjects landed in which split.
- Producing a reproducible partitioning manifest for the methods section.

## Workflow

1. Identify the grouping column (subject ID, patient ID, time-series window ID).
2. Choose ratios (commonly 70/15/15 or 80/10/10) from `Configs/Config.yaml`.
3. Use `GroupShuffleSplit` when stratification is not required; `StratifiedGroupKFold` otherwise.
4. Fix the random seed for the splitter.
5. First split separates the test set from the remaining data.
6. Second split separates the validation set from the training set.
7. Assert no group appears in more than one split.
8. Write `Aggregated/PartitionManifest.json` listing groups per split.

## Inputs

- Features, labels, and a `Groups` array.
- Split ratios and seed from `Configs/Config.yaml`.

## Outputs

- Three index arrays (`TrainIdx`, `ValIdx`, `TestIdx`).
- `Aggregated/PartitionManifest.json` documenting the partitioning scheme.

## Key Rules

- Stratify at the highest hierarchical level — never at the sample level.
- Use `GroupShuffleSplit` or `StratifiedGroupKFold` when groups exist.
- Same seed for splitter, weight init, and shuffling.
- Assert no overlap between groups across splits.
- Document the partitioning scheme in the manifest and in the manuscript.

## Examples

```python
# Two-stage GroupShuffleSplit producing train/val/test indices.
import json
import numpy as np
from sklearn.model_selection import GroupShuffleSplit


def SplitTrainValTest(Features, Labels, Groups, TestSize, ValSize, Seed):
  """Split with subject-level isolation and a fixed seed."""
  # First split: separate test from the rest.
  outer = GroupShuffleSplit(n_splits=1, test_size=TestSize, random_state=Seed)
  trainValIdx, testIdx = next(outer.split(Features, Labels, groups=Groups))
  # Second split: separate validation from train.
  inner = GroupShuffleSplit(
    n_splits=1,
    test_size=ValSize,
    random_state=Seed
  )
  trainIdx, valIdx = next(inner.split(
    Features[trainValIdx],
    Labels[trainValIdx],
    groups=Groups[trainValIdx]
  ))
  return trainIdx, valIdx, testIdx


def AssertNoGroupLeak(Groups, TrainIdx, ValIdx, TestIdx):
  """Assert no group appears in more than one split."""
  # Collect unique groups per split.
  trainGroups = set(np.unique(Groups[TrainIdx]))
  valGroups = set(np.unique(Groups[ValIdx]))
  testGroups = set(np.unique(Groups[TestIdx]))
  # Assert pairwise disjoint sets.
  assert (len(trainGroups & valGroups) == 0), "Train/val group leak detected."
  assert (len(trainGroups & testGroups) == 0), "Train/test group leak detected."
  assert (len(valGroups & testGroups) == 0), "Val/test group leak detected."


def WriteManifest(Groups, TrainIdx, ValIdx, TestIdx, OutputPath):
  """Write a JSON manifest of groups per split."""
  # Build the manifest dict.
  manifest = {
    "TrainGroups": list(map(int, np.unique(Groups[TrainIdx]))),
    "ValidationGroups": list(map(int, np.unique(Groups[ValIdx]))),
    "TestGroups": list(map(int, np.unique(Groups[TestIdx])))
  }
  with open(OutputPath + "PartitionManifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
  return manifest
```

## References

- GroupShuffleSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
-

StratifiedGroupKFold: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html
