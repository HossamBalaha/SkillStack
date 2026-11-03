---
name: early-stopping-configurator
description: Configure early stopping when training a model that may plateau, overfit, or waste compute. Triggers on "early stopping", "patience", "min_delta", "restore best weights", "val_loss monitor", "Lightning EarlyStopping", "stopped epoch".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [early-stopping, patience, min-delta, val-loss, callbacks]
related: [ml-engineering/pytorch-lightning-scaffold, ml-engineering/hyperparameter-tuner, ml-engineering/model-checkpoint-manager]
prerequisites: [ml-engineering/pytorch-lightning-scaffold]
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1090
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Early Stopping Configurator

## When To Use

- Training a model that may plateau well before `max_epochs`.
- Preventing overfitting by monitoring a validation metric.
- Restoring the best weights rather than the last epoch's weights.
- Logging the exact epoch at which training stopped.

## Workflow

1. Pick the monitor metric (`val_loss`, `val_auc`, `val_f1`).
2. Choose the mode (`min` for loss, `max` for accuracy/AUC).
3. Set `patience` (epochs without improvement before stopping).
4. Set `min_delta` (minimum change to qualify as improvement).
5. Enable `restore_best_weights=True` so the best checkpoint is reloaded.
6. Instantiate `pytorch_lightning.callbacks.EarlyStopping` or a custom impl.
7. Log the epoch at which training stopped.

## Inputs

- `Configs/Config.yaml` with `Monitor`, `Mode`, `Patience`, `MinDelta`.
- The trainer or training loop instance.

## Outputs

- A callback that stops training when the metric plateaus.
- A logged `StoppedEpoch` value in `Aggregated/TrainingLog.json`.

## Key Rules

- `min` mode for losses; `max` mode for accuracy/AUC.
- `restore_best_weights=True` must be set so the best epoch is kept.
- `min_delta` must be a small positive number (e.g. 1e-4) to avoid noise stopping.
- Log the epoch at which training actually stopped.
- Reference only real Lightning API at https://lightning.ai.

## Examples

```python
# Lightning EarlyStopping + custom implementation fallback.
import json
import numpy as np
from pytorch_lightning.callbacks import EarlyStopping


def BuildLightningEarlyStopping(Config):
  """Build a Lightning EarlyStopping callback from config."""
  # Construct the callback with the configured monitor.
  callback = EarlyStopping(
    monitor=Config["Monitor"],
    mode=Config["Mode"],
    patience=Config["Patience"],
    min_delta=Config["MinDelta"],
    verbose=True
  )
  return callback


class CustomEarlyStopping:
  """Custom early stopping for non-Lightning training loops."""

  def __init__(self, Monitor, Mode, Patience, MinDelta):
    # Store configuration.
    self.Monitor = Monitor
    self.Mode = Mode
    self.Patience = Patience
    self.MinDelta = MinDelta
    # Internal bookkeeping.
    self.BestScore = None
    self.Counter = 0
    self.ShouldStop = False
    self.StoppedEpoch = None

  def Step(self, CurrentScore):
    """Update the counter and return True if training should stop."""
    # First observation initializes the best score.
    if (self.BestScore is None):
      self.BestScore = CurrentScore
      return False
    # Determine whether the score improved.
    if (self.Mode == "min"):
      improved = (CurrentScore < self.BestScore - self.MinDelta)
    else:
      improved = (CurrentScore > self.BestScore + self.MinDelta)
    # Update or increment the counter.
    if (improved):
      self.BestScore = CurrentScore
      self.Counter = 0
    else:
      self.Counter += 1
    # Trigger stop when patience is exhausted.
    if (self.Counter >= self.Patience):
      self.ShouldStop = True
    return self.ShouldStop

  def LogStoppedEpoch(self, Epoch, OutputPath):
    """Persist the stopped epoch for reproducibility reports."""
    self.StoppedEpoch = Epoch
    with open(OutputPath + "TrainingLog.json", "w") as f:
      json.dump({"StoppedEpoch": Epoch}, f, indent=2)
```
