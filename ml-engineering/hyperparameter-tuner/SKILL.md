---
name: hyperparameter-tuner
description: Drive Bayesian hyperparameter optimization with Optuna when tuning a model's learning rate, batch size, dropout, architecture depth, or any tunable knob. Triggers on "Optuna", "TPE sampler", "MedianPruner", "Bayesian optimization", "trials_dataframe", "Config.yaml search space".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [optuna, bayesian, tuning, hyperparameters]
related: [ml-engineering/reproducible-experiment-runner, ml-engineering/early-stopping-configurator]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python, json, csv]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Hyperparameter Tuner

## When To Use

- Tuning more than a handful of hyperparameters where grid search is infeasible.
- Reading the search space from `Configs/Config.yaml` and optimizing automatically.
- Pruning unpromising trials early to save compute.
- Persisting the full trial history to CSV for reproducibility.

## Workflow

1. Load `Configs/Config.yaml` and read the `SearchSpace` block.
2. Construct an `optuna.study.Study` with the TPE sampler and a seeded RNG.
3. Attach a `MedianPruner` (or `HyperbandPruner` for multi-fidelity promotion).
4. Define `objective(trial)` that suggests hyperparameters, trains a model, and returns the validation metric.
5. Call `study.optimize(objective, n_trials=N, timeout=T)`.
6. Persist `study.trials_dataframe()` to `Aggregated/OptunaTrials.csv`.
7. Log the best trial number, value, and parameter dict.
8. Re-train the model with the best parameters and save it.

## Inputs

- `Configs/Config.yaml` containing a `SearchSpace` block.
- A training function that accepts a hyperparameter dict and returns a validation metric.

## Outputs

- `Aggregated/OptunaTrials.csv` with every trial.
- `Aggregated/BestParams.json` with the winning configuration.
- The re-trained best model checkpoint.

## Key Rules

- Use `optuna.samplers.TPESampler(seed=...)` with a fixed seed.
- Use `optuna.pruners.MedianPruner` by default; HyperbandPruner for multi-fidelity.
- The objective must call `trial.report(metric, step)` and check `trial.should_prune()`.
- Persist `study.trials_dataframe()` after optimization ends.
- Reference only the real Optuna API at https://optuna.org.

## Examples

```python
# Bayesian optimization with TPE and a median pruner.
import optuna
import pandas as pd
import json


def BuildStudy(Seed):
  """Construct a study with a deterministic TPE sampler."""
  # Seed the sampler so the search is reproducible.
  sampler = optuna.samplers.TPESampler(seed=Seed)
  # Median pruner cuts unpromising trials early.
  pruner = optuna.pruners.MedianPruner(
    n_startup_trials=5,
    n_warmup_steps=3
  )
  return optuna.create_study(
    direction="maximize",
    sampler=sampler,
    pruner=pruner
  )


def Objective(trial, TrainFunction):
  """Suggest hyperparameters and return the validation metric."""
  # Sample from the configured search space.
  learningRate = trial.suggest_float("LearningRate", 1e-5, 1e-2, log=True)
  dropout = trial.suggest_float("Dropout", 0.0, 0.5)
  hiddenSize = trial.suggest_categorical("HiddenSize", [64, 128, 256, 512])
  # Train with the suggested hyperparameters.
  metric = TrainFunction({
    "LearningRate": learningRate,
    "Dropout": dropout,
    "HiddenSize": hiddenSize
  })
  return metric


def RunTuning(SearchSpace, TrainFunction, N_trials, Seed, OutputPath):
  """Run optimization and persist the trial dataframe."""
  # Build and run the study.
  study = BuildStudy(Seed)
  study.optimize(
    lambda trial: Objective(trial, TrainFunction),
    n_trials=N_trials,
    timeout=3600
  )
  # Persist the trial history.
  df = study.trials_dataframe()
  df.to_csv(OutputPath + "OptunaTrials.csv", index=False)
  # Save the best parameters.
  bestParams = study.best_params
  with open(OutputPath + "BestParams.json", "w") as f:
    json.dump(bestParams, f, indent=2)
  return bestParams
```

## References

- Optuna documentation: https://optuna.org
- TPE sampler: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.TPESampler.html
- MedianPruner: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html
