---
name: model-checkpoint-manager
description: Save and resume checkpoints with model, optimizer, scheduler, epoch, val metric, and RNG states. Triggers on "model checkpoint", "save state_dict", "resume training", "top-K checkpoints", "Lightning ModelCheckpoint", "torch.load map_location".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [checkpoint, state-dict, resume, top-k, lightning]
related: [ml-engineering/pytorch-lightning-scaffold, ml-engineering/early-stopping-configurator, ml-engineering/reproducible-experiment-runner]
prerequisites: [ml-engineering/pytorch-lightning-scaffold]
outputs: [python, bash]
difficulty: intermediate
estimated_tokens: 1130
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Model Checkpoint Manager

## When To Use

- Saving a checkpoint after every epoch or after each improvement.
- Resuming training from a previous run without losing optimizer state.
- Keeping only the top-K checkpoints by validation metric.
- Using Lightning's `ModelCheckpoint` callback.

## Workflow

1. Define the checkpoint payload: model `state_dict`, optimizer `state_dict`, scheduler `state_dict`, epoch, val metric,
   RNG states.
2. Save via `torch.save(payload, path)`.
3. Load via `torch.load(path, map_location=device)`.
4. Reconstruct model, optimizer, scheduler, and RNG states from the payload.
5. Keep at most top-K checkpoints by validation metric.
6. For Lightning, use `ModelCheckpoint` with `save_top_k=K`, `monitor="ValMetric"`.
7. Log the best checkpoint path to `Aggregated/BestCheckpoint.json`.

## Inputs

- The model, optimizer, scheduler, epoch, val metric.
- `Configs/Config.yaml` with `SaveTopK`, `Monitor`, `Mode`.

## Outputs

- Checkpoint files under `Results/{DatasetName}_{Timestamp}/Train/`.
- `Aggregated/BestCheckpoint.json` with the path to the best checkpoint.

## Key Rules

- Always save RNG states so resume is byte-identical.
- Load with `map_location=device` to move across CPU/GPU safely.
- Keep at most top-K checkpoints; delete the rest.
- For Lightning, set `save_top_k=K` and `monitor` + `mode` correctly.
- Reference real `torch.save` / `torch.load` patterns.

## Examples

```python
# Checkpoint manager with top-K pruning.
import os
import json
import random
import numpy as np
import torch


def SaveCheckpoint(Model, Optimizer, Scheduler, Epoch, ValMetric, Path, Seed):
  """Persist model, optimizer, scheduler, epoch, val metric, and RNG states."""
  # Collect every RNG state for byte-identical resume.
  payload = {
    "ModelState": Model.state_dict(),
    "OptimizerState": Optimizer.state_dict(),
    "SchedulerState": Scheduler.state_dict() if (Scheduler is not None) else None,
    "Epoch": Epoch,
    "ValMetric": ValMetric,
    "RandomState": random.getstate(),
    "NumpyState": np.random.get_state(),
    "TorchState": torch.get_rng_state(),
    "CudaState": torch.cuda.get_rng_state_all() if (torch.cuda.is_available()) else None
  }
  # Persist atomically.
  torch.save(payload, Path)
  return Path


def LoadCheckpoint(Path, Model, Optimizer, Scheduler, Device):
  """Load a checkpoint into model, optimizer, scheduler."""
  # Load with map_location for cross-device resume.
  payload = torch.load(Path, map_location=Device)
  # Restore states.
  Model.load_state_dict(payload["ModelState"])
  Optimizer.load_state_dict(payload["OptimizerState"])
  if (Scheduler is not None and payload["SchedulerState"] is not None):
    Scheduler.load_state_dict(payload["SchedulerState"])
  # Restore RNG states for byte-identical resume.
  random.setstate(payload["RandomState"])
  np.random.set_state(payload["NumpyState"])
  torch.set_rng_state(payload["TorchState"])
  if (payload["CudaState"] is not None and torch.cuda.is_available()):
    torch.cuda.set_rng_state_all(payload["CudaState"])
  return payload["Epoch"], payload["ValMetric"]


def PruneTopK(CheckpointDir, KeepK, Mode, OutputPath):
  """Keep only the top-K checkpoints by val metric."""
  # List all checkpoint files.
  files = [f for f in os.listdir(CheckpointDir) if (f.endswith(".pt"))]
  metrics = []
  for f in files:
    # Load just the metric for pruning decisions.
    payload = torch.load(os.path.join(CheckpointDir, f), map_location="cpu")
    metrics.append((f, payload["ValMetric"]))
  # Sort descending for max, ascending for min.
  reverse = (Mode == "max")
  metrics.sort(key=lambda x: x[1], reverse=reverse)
  # Delete everything beyond the top K.
  for f, _ in metrics[KeepK:]:
    os.remove(os.path.join(CheckpointDir, f))
  # Persist the best path.
  if (metrics):
    with open(OutputPath + "BestCheckpoint.json", "w") as fh:
      json.dump({"Path": metrics[0][0], "ValMetric": metrics[0][1]}, fh, indent=2)
```

## References

- torch.save / torch.load: https://pytorch.org/docs/stable/generated/torch.save.html
- Lightning
  ModelCheckpoint: https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html
- Saving and loading models
  recipe: https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_models_for_inference.html
