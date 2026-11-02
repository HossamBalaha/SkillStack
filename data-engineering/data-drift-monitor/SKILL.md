---
name: data-drift-monitor
description: Monitor data drift between TRAIN and production data using Population Stability Index (PSI), Kolmogorov-Smirnov test, and Wasserstein distance per feature. Use this skill to alert when PSI exceeds 0.2 on any top-10 feature and to integrate with evidently AI or alibi-detect.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [drift, psi, monitoring, mlops]
related: [data-engineering/data-quality-validator, ml-engineering/metrics-computation-suite]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
---

# Data Drift Monitor

## When To Use

- A model has shipped and you need to detect when production data drifts from TRAIN.
- Per-feature drift scores (PSI, KS, Wasserstein) must be reported on a dashboard.
- Alerts must fire when any top-10 feature crosses a defined PSI threshold.
- The reference (TRAIN) snapshot is immutable and versioned per training run.
- You are integrating with evidently AI or alibi-detect.

## Workflow

1. Snapshot the TRAIN distribution per feature (bin edges + frequencies) and version it.
2. Collect the current production window (e.g., last 7 days) for the same features.
3. Compute PSI per feature using the shared bin edges from TRAIN.
4. Compute the KS statistic and p-value per feature for distribution shift.
5. Compute the Wasserstein distance for a scale-aware comparison.
6. Rank features by PSI; flag any in the top 10 with PSI > 0.2.
7. Emit a drift report (JSON) and push to the alerting system.
8. Track drift trends over time so slow drift is visible, not only spikes.
9. Refresh the reference snapshot only when a retrain is approved.

## Inputs

- A versioned TRAIN reference snapshot (bin edges, counts, hash).
- A production sample (DataFrame) covering the desired window.
- Feature list (typically the model's top features).
- Alerting config: PSI thresholds (0.1, 0.25), top-k, alert channel.

## Outputs

- A drift report (JSON) with PSI, KS, and Wasserstein per feature.
- An alert payload if any top-10 feature exceeds the configured threshold.
- A trend file appended on each run for historical drift tracking.

## Key Rules

- The TRAIN reference snapshot is immutable; refresh only on an approved retrain.
- PSI bins are derived from TRAIN and reused for production, never recomputed.
- PSI < 0.1 stable, 0.1–0.25 moderate drift, > 0.25 significant.
- Alert when any top-10 feature by importance exceeds PSI 0.2.
- Report all three metrics (PSI, KS, Wasserstein) so reviewers can cross-check.
- Trend history is append-only; past runs are never overwritten.

## Examples

```python
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, wasserstein_distance


def BuildBins(trainValues, nBins=10):
  # Compute quantile bin edges from the TRAIN reference so PSI is comparable.
  quantiles = np.linspace(0, 1, nBins + 1)
  edges = np.quantile(trainValues, quantiles)
  edges[0] = -np.inf
  edges[-1] = np.inf
  return edges


def ComputePsi(trainValues, prodValues, edges):
  # PSI comparing the production distribution against TRAIN on shared bins.
  trainCounts = np.histogram(trainValues, bins=edges)[0]
  prodCounts = np.histogram(prodValues, bins=edges)[0]
  trainFreq = (trainCounts + 1) / (trainCounts.sum() + len(edges))
  prodFreq = (prodCounts + 1) / (prodCounts.sum() + len(edges))
  return np.sum((prodFreq - trainFreq) * np.log(prodFreq / trainFreq))


def DriftReport(trainDf, prodDf, features):
  # Compute PSI, KS, and Wasserstein per feature and rank by PSI.
  rows = []
  for feature in features:
    trainValues = trainDf[feature].dropna().values
    prodValues = prodDf[feature].dropna().values
    edges = BuildBins(trainValues)
    psi = ComputePsi(trainValues, prodValues, edges)
    ksStat, ksPvalue = ks_2samp(trainValues, prodValues)
    wasserstein = wasserstein_distance(trainValues, prodValues)
    rows.append({
      "Feature": feature,
      "Psi": psi,
      "KsStat": ksStat,
      "KsPvalue": ksPvalue,
      "Wasserstein": wasserstein,
    })
  reportDf = pd.DataFrame(rows).sort_values("Psi", ascending=False)
  return reportDf


def AlertIfDrift(reportDf, topK=10, threshold=0.2):
  # Fire an alert when any top-K feature by PSI exceeds the threshold.
  topRows = reportDf.head(topK)
  flagged = topRows[topRows["Psi"] > threshold]
  if (len(flagged) > 0):
    return {"Alert": True, "FlaggedFeatures": flagged.to_dict("records")}
  return {"Alert": False}
```

## References

- evidently AI: https://www.evidentlyai.com
- alibi-detect: https://docs.seldon.io/projects/alibi-detect
- PSI (Yurdakul 2018): https://scholarworks.wmich.edu/dissertations/3514/
- KS test (scipy): https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
