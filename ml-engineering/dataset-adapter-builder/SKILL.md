---
name: dataset-adapter-builder
description: Build defensive dataset adapters when wiring external datasets into a training pipeline. Triggers on "FileNotFoundError suggestions", "dataset directory empty", "pandas to numpy pre-conversion", "dataset adapter", "skip dataset with --datasets filter".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [dataset, adapter, pandas, numpy, defensive-loading]
related: [ml-engineering/modular-ml-architect, ml-engineering/data-leakage-guard, ml-engineering/train-val-test-splitter]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python]
difficulty: intermediate
estimated_tokens: 1150
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Dataset Adapter Builder

## When To Use

- Adding a new dataset to an existing training pipeline.
- When the user reports that a dataset directory is missing or empty.
- Pre-converting pandas splits to numpy arrays to avoid per-batch overhead.
- Implementing the `--datasets` CLI filter to skip unavailable datasets.

## Workflow

1. Resolve the expected dataset path from `Configs/Config.yaml`.
2. List the expected files for this dataset (e.g. images, CSV shards).
3. If the directory is empty or files are missing, raise `FileNotFoundError` with 4 actionable suggestions.
4. Otherwise load the files lazily into a `pandas.DataFrame` per split.
5. Pre-convert each split to `numpy.ndarray` once at training start via a dedicated utility.
6. Slice numpy arrays directly when building batches.
7. Expose a `DatasetAdapter` interface with `LoadTrain`, `LoadValidation`, `LoadTest`.

## Inputs

- `Configs/Config.yaml` with `Dataset.Path` and `Dataset.ExpectedFiles`.
- An optional `--datasets` CLI filter list.

## Outputs

- A `DatasetAdapter` instance exposing numpy-backed splits.
- A clear `FileNotFoundError` with remediation steps when files are absent.

## Key Rules

- Check that input directory contains matching files BEFORE processing.
- On empty input, raise `FileNotFoundError` listing 4 actionable suggestions.
- Pre-convert pandas splits to numpy once; never slice pandas DataFrames per batch.
- Support a `--datasets` filter to skip unavailable datasets.
- All public methods return numpy arrays, not pandas objects.

## Examples

```python
# Defensive dataset adapter with pre-conversion to numpy.
import os
import numpy as np
import pandas as pd


class FileNotFoundErrorWithSuggestions(FileNotFoundError):
  """FileNotFoundError enriched with four remediation suggestions."""

  def __init__(self, DatasetName, ExpectedPath):
    # Compose the message with 4 actionable suggestions.
    message = (
      f"Dataset '{DatasetName}' has no matching files at {ExpectedPath}.\n"
      f"Suggestions:\n"
      f"  (a) Download the dataset from the official source.\n"
      f"  (b) Move files to {ExpectedPath}.\n"
      f"  (c) Check the configured path in Configs/Config.yaml.\n"
      f"  (d) Use --datasets filter to skip this dataset.\n"
    )
    super().__init__(message)


def ConvertDataFramesToNumpy(DataFrameSplits):
  """Pre-convert each pandas split to numpy once at startup."""
  # Avoid per-batch pandas overhead by converting up front.
  numpySplits = {}
  for splitName, df in DataFrameSplits.items():
    # Convert features and labels separately.
    numpySplits[splitName] = {
      "Features": df.drop(columns=["Label"]).to_numpy(dtype=np.float32),
      "Labels": df["Label"].to_numpy(dtype=np.int64)
    }
  return numpySplits


class DatasetAdapter:
  """Loads a dataset directory and exposes numpy-backed splits."""

  def __init__(self, Name, Path, ExpectedFiles):
    # Store configuration.
    self.Name = Name
    self.Path = Path
    self.ExpectedFiles = ExpectedFiles

  def VerifyDirectory(self):
    """Raise FileNotFoundErrorWithSuggestions if files are missing."""
    # Check existence and emptiness.
    if (not os.path.isdir(self.Path)):
      raise FileNotFoundErrorWithSuggestions(self.Name, self.Path)
    # List actual files present.
    present = set(os.listdir(self.Path))
    # Confirm at least one expected file exists.
    if (not (present & set(self.ExpectedFiles))):
      raise FileNotFoundErrorWithSuggestions(self.Name, self.Path)

  def LoadSplits(self):
    """Load CSV shards into a dict of pandas splits."""
    # Verify before loading.
    self.VerifyDirectory()
    splits = {}
    for fileName in self.ExpectedFiles:
      # Skip non-existent files gracefully.
      fullPath = os.path.join(self.Path, fileName)
      if (os.path.exists(fullPath)):
        splits[fileName] = pd.read_csv(fullPath)
    # Pre-convert to numpy.
    return ConvertDataFramesToNumpy(splits)
```
