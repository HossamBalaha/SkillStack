---
name: baseline-model-zoo
description: Implement standard baseline models for fair comparison when the user needs reference points against a proposed model. Triggers on "baseline models", "Logistic Regression", "Random Forest", "XGBoost LightGBM", "simple MLP", "k-NN", "fair comparison pipeline".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [baselines, logistic-regression, random-forest, xgboost, comparison]
related: [ml-engineering/ablation-study-runner, ml-engineering/metrics-computation-suite, ml-engineering/modular-ml-architect]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1010
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Baseline Model Zoo

## When To Use
- Building reference models to compare against a proposed model.
- Running the same preprocessing pipeline for every model.
- Documenting per-baseline hyperparameter search.
- Avoiding the deprecated `multi_class=` parameter in `LogisticRegression`.

## Workflow
1. Load the SAME preprocessed train/validation/test splits for every baseline.
2. Instantiate each baseline: Logistic Regression, Random Forest, XGBoost/LightGBM, simple MLP, k-NN.
3. Fit a per-baseline hyperparameter search using `Configs/Config.yaml`.
4. NEVER pass `multi_class=` to `sklearn.linear_model.LogisticRegression`.
5. Train each baseline with the same seed.
6. Evaluate each baseline on the same test split.
7. Save per-baseline metrics to `Aggregated/BaselineResults.json`.

## Inputs
- Preprocessed train/validation/test splits.
- `Configs/Config.yaml` with per-baseline hyperparameter grids.

## Outputs
- Trained baseline models.
- `Aggregated/BaselineResults.json` with metrics per baseline.

## Key Rules
- Every baseline must use the SAME data pipeline as the proposed model.
- NEVER pass `multi_class=` to `sklearn.linear_model.LogisticRegression` — it is deprecated.
- Document hyperparameter search per baseline.
- Fix the same seed across baselines.
- Report the same metrics computed by `metrics-computation-suite`.

## Examples
```python
# Baseline zoo with a shared pipeline and NO multi_class parameter.
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier


def BuildBaselines(Seed):
  """Instantiate all baselines with a shared seed."""
  # LogisticRegression WITHOUT multi_class (deprecated).
  logReg = LogisticRegression(
    C=1.0,
    solver="lbfgs",
    max_iter=1000,
    random_state=Seed
  )
  # Random Forest baseline.
  rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=Seed
  )
  # k-NN baseline.
  knn = KNeighborsClassifier(n_neighbors=5)
  return {
    "LogisticRegression": logReg,
    "RandomForest": rf,
    "KNN": knn
  }


def TrainAndEvaluateBaselines(TrainFeatures, TrainLabels, TestFeatures, TestLabels, Seed, OutputPath):
  """Train every baseline and persist metrics."""
  from sklearn.metrics import accuracy_score, f1_score
  baselines = BuildBaselines(Seed)
  results = {}
  for name, model in baselines.items():
    # Fit on the same training split.
    model.fit(TrainFeatures, TrainLabels)
    # Predict on the same test split.
    preds = model.predict(TestFeatures)
    # Compute shared metrics.
    results[name] = {
      "Accuracy": float(accuracy_score(TestLabels, preds)),
      "F1Macro": float(f1_score(TestLabels, preds, average="macro"))
    }
  # Persist the results JSON.
  with open(OutputPath + "BaselineResults.json", "w") as f:
    json.dump(results, f, indent=2)
  return results
```

## References
- sklearn LogisticRegression: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
- RandomForestClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- XGBoost: https://xgboost.readthedocs.io
- LightGBM: https://lightgbm.readthedocs.io
