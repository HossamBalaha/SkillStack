---
name: missing-data-imputer
description: Impute missing values with simple strategies (mean, median, mode), KNN imputation, iterative imputation modeling each feature as a function of the others, or MICE for multiple imputation. Use this skill when fitting imputers on the TRAIN split only to prevent leakage and documenting which columns were imputed with which strategy.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [imputation, knn, mice, missing-data, leakage-prevention]
related: [data-engineering/feature-engineering-toolkit, data-engineering/outlier-detector]
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

# Missing Data Imputer

## When To Use
- A model cannot tolerate NaN values but the data has gaps.
- Different columns need different strategies (median for skewed, mode for categorical).
- Leakage must be prevented: imputation fits on TRAIN only, then transforms VAL and TEST.
- Multiple imputation (MICE) is required to capture uncertainty from missingness.
- An audit trail must record which columns were imputed and with what strategy.

## Workflow
1. Profile missingness per column: count, fraction, missingness pattern (MCAR/MAR/MNAR).
2. Choose a strategy per column: simple, KNN, iterative, or MICE.
3. Fit the imputer on the TRAIN split only.
4. Transform TRAIN, VAL, and TEST with the fitted imputer.
5. Record an imputation map: column to strategy to fit statistics.
6. Add an indicator column per imputed feature so the model knows what was filled.
7. Validate that no NaN remains after imputation unless explicitly allowed.
8. Persist the imputer (joblib) so the same transforms apply at inference.

## Inputs
- TRAIN, VAL, TEST DataFrames with the same schema.
- Per-column imputation strategy map.
- Optional hyperparameters for KNN/iterative/MICE (n_neighbors, max_iter, sample_posterior).

## Outputs
- Imputed TRAIN, VAL, TEST DataFrames.
- An imputation report (JSON) listing column, strategy, and fit statistics.
- A fitted imputer artifact (joblib) for inference reuse.
- Binary indicator columns flagging originally-missing values.

## Key Rules
- Imputers fit on TRAIN only; VAL and TEST are transformed, never fit.
- Every imputed column gets a paired `<col>_was_missing` indicator.
- Categorical columns are mode-imputed; never mean-imputed.
- Multiple imputation (MICE) produces M datasets; downstream models must average.
- The imputer artifact is versioned alongside the model for reproducibility.
- Documentation lists each imputed column, its strategy, and its fit statistic.

## Examples

```python
import joblib
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import KNNImputer, IterativeImputer, SimpleImputer
from sklearn.linear_model import BayesianRidge


class ImputationPlan:
  # Maps each column to a fitted imputer instance.
  def __init__(self):
    self.Strategies = {}
    self.Statistics = {}


def FitImputers(trainDf, strategyMap):
  # Fit one imputer per column using the declared strategy.
  plan = ImputationPlan()
  for column, strategy in strategyMap.items():
    if (strategy == "median"):
      imputer = SimpleImputer(strategy="median")
    elif (strategy == "mode"):
      imputer = SimpleImputer(strategy="most_frequent")
    elif (strategy == "knn"):
      imputer = KNNImputer(n_neighbors=5)
    elif (strategy == "iterative"):
      imputer = IterativeImputer(estimator=BayesianRidge(), max_iter=10, random_state=42)
    else:
      raise ValueError(f"Unknown strategy {strategy}")
    imputer.fit(trainDf[[column]])
    plan.Strategies[column] = imputer
    plan.Statistics[column] = strategy
  return plan


def TransformWithPlan(df, plan, addIndicator=True):
  # Apply fitted imputers and optionally attach missingness indicators.
  out = df.copy()
  for column, imputer in plan.Strategies.items():
    if (addIndicator):
      out[f"{column}_was_missing"] = out[column].isna()
    out[column] = imputer.transform(out[[column]]).ravel()
  return out


def PersistPlan(plan, path):
  # Save the imputation plan so inference reuses the same transforms.
  joblib.dump(plan, path)
```

## References
- scikit-learn imputation: https://scikit-learn.org/stable/modules/impute.html
- IterativeImputer: https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html
- MICE (van Buuren): https://stefvanbuuren.name/fimd/
