---
name: tabular-data-sampler
description: Sample tabular data using random, stratified (preserve class proportions), weighted (oversample minority via WeightedRandomSampler), or reservoir sampling for streaming data. Use this skill when reducing dataset size for prototyping, balancing classes, or sampling from a stream that does not fit in memory, with a set random seed for reproducibility.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [sampling, stratified, weighted, reservoir, random-seed]
related: [data-engineering/data-quality-validator, data-engineering/feature-engineering-toolkit]
prerequisites: []
outputs: [python]
difficulty: beginner
estimated_tokens: 1200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Tabular Data Sampler

## When To Use

- A dataset is too large to fit in memory or to iterate quickly for prototyping.
- Class imbalance requires oversampling the minority or undersampling the majority.
- A streaming source must be sampled in one pass without knowing its length.
- Stratification is needed so the sample preserves class proportions.
- Results must be reproducible across runs (fixed seed).

## Workflow

1. Identify the goal: prototype, balance classes, or sample a stream.
2. Choose the strategy: random, stratified, weighted, or reservoir.
3. Set a random seed so the sample is reproducible.
4. Compute sampling parameters: fraction, target size, weights, or reservoir k.
5. Apply the sampler and verify the resulting distribution.
6. Emit a sampling report listing strategy, parameters, in/out sizes, and seed.
7. Persist the seed and parameters so the same sample can be regenerated.

## Inputs

- The source DataFrame or streaming iterator.
- The sampling strategy and its parameters (fraction, k, weights, strata column).
- A random seed for reproducibility.

## Outputs

- A sampled DataFrame.
- A sampling report (JSON) capturing strategy, parameters, in/out sizes, and seed.

## Key Rules

- Every run records its random seed so the sample is reproducible.
- Stratified sampling preserves class proportions within a declared tolerance.
- WeightedRandomSampler weights sum to one so the sampling probability is well-defined.
- Reservoir sampling is single-pass; it never holds more than k items in memory.
- The sampling report is emitted alongside the sampled data for audit.
- Sampling happens after the TRAIN/VAL/TEST split so leakage is impossible.

## Examples

```python
import json
import numpy as np
import pandas as pd
import torch
from torch.utils.data import WeightedRandomSampler


def RandomSample(df, fraction, seed=42):
  # Reproducible uniform random sample.
  return df.sample(frac=fraction, random_state=seed)


def StratifiedSample(df, strataColumn, fraction, seed=42):
  # Preserve class proportions declared by the strata column.
  return df.groupby(strataColumn, group_keys=False).apply(
    lambda group: group.sample(frac=fraction, random_state=seed)
  )


def WeightedSampler(df, labelColumn, seed=42):
  # Build a WeightedRandomSampler that oversamples minority classes.
  counts = df[labelColumn].value_counts()
  weightsPerClass = 1.0 / counts
  sampleWeights = df[labelColumn].map(weightsPerClass.to_dict()).values
  generator = torch.Generator().manual_seed(seed)
  sampler = WeightedRandomSampler(
    weights=sampleWeights,
    num_samples=len(df),
    replacement=True,
    generator=generator,
  )
  return sampler


class ReservoirSampler:
  # Single-pass sampler that keeps k items uniformly from a stream.
  def __init__(self, k, seed=42):
    self.K = k
    self.Rng = np.random.default_rng(seed)
    self.Reservoir = []
    self.Seen = 0

  def Update(self, item):
    # Algorithm R: keep the first k items, then replace with decreasing probability.
    self.Seen += 1
    if (self.Seen <= self.K):
      self.Reservoir.append(item)
    else:
      j = self.Rng.integers(0, self.Seen)
      if (j < self.K):
        self.Reservoir[j] = item

  def Finalize(self):
    return self.Reservoir


def EmitReport(strategy, inSize, outSize, seed, params):
  # Record everything needed to reproduce the sample.
  report = {
    "Strategy": strategy,
    "InSize": inSize,
    "OutSize": outSize,
    "Seed": seed,
    "Params": params,
  }
  return json.dumps(report, indent=2)
```

## References

- pandas sample: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html
- PyTorch WeightedRandomSampler: https://pytorch.org/docs/stable/data.html#torch.utils.data.WeightedRandomSampler
- Reservoir sampling (Vitter 1985): https://dl.acm.org/doi/10.1145/3147.3165
