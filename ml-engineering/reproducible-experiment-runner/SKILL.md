---
name: reproducible-experiment-runner
description: Set up fully reproducible ML experiments when starting training, configuring devices, seeds, logging, progress bars, and output folders. Triggers on "reproducible training", "experiment folder", "device setup", "tqdm progress", "Results/DatasetName_Timestamp layout".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [reproducibility, seeds, device, tqdm, experiment-folder]
related: [ml-engineering/seed-and-device-resolver, ml-engineering/experiment-folder-organizer, ml-engineering/modular-ml-architect]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python, bash]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Reproducible Experiment Runner

## When To Use

- Starting a training run that must be reproducible across machines.
- Configuring device placement for primary model AND auxiliary modules.
- Setting up dual logging (console + file) and `tqdm` progress bars.
- Organizing artifacts into a single timestamped experiment folder.
- When the user mentions "Results/{DatasetName}_{Timestamp}" layout.

## Workflow

1. Read `Configs/Config.yaml` for seed, dataset name, and logging level.
2. Resolve `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` exactly once.
3. Seed `random`, `numpy`, `torch`, and CUDA deterministically.
4. Create `Results/{DatasetName}_{YYYYMMDD_HHMMSS}/` with subfolders `Train/`, `Validation/`, `Test/`, `Aggregated/`.
5. Configure dual logging: console INFO + file DEBUG at `Aggregated/execution.log`.
6. Wrap epoch loop, batch loop, and trial loop in `tqdm` progress bars.
7. Move the primary model AND every standalone `nn.Module` to `device` explicitly.
8. Save every artifact into the correct split subfolder without per-file timestamps.
9. At the end, write an `Aggregated/Summary.json` with all metrics.

## Inputs

- `Configs/Config.yaml` with at least `Seed`, `DatasetName`, `Epochs`, `BatchSize`.
- A model factory and a dataset factory.

## Outputs

- `Results/{DatasetName}_{Timestamp}/` containing four split subfolders.
- `Aggregated/execution.log` with full DEBUG trace.
- Per-split metrics JSON files.

## Key Rules

- `device` must be resolved ONCE and reused everywhere.
- Call `.to(device)` on every standalone `nn.Module` (loss, regularizer, calibrator, auxiliary branch) —
  `model.to(device)` does NOT move sibling modules.
- One timestamped folder per experiment; do NOT timestamp individual files.
- Dual logging: console INFO and file DEBUG simultaneously.
- `tqdm` bars on epochs, batches, and trials.
- Four subfolders only: `Train/`, `Validation/`, `Test/`, `Aggregated/`.

## Examples

```python
# Resolve device exactly once at startup.
import torch
import logging
from tqdm import tqdm

# device is a module-level constant after resolution.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def ConfigureLogging(LogPath):
  """Wire console INFO and file DEBUG handlers to the root logger."""
  # Reset any pre-existing handlers.
  logging.basicConfig(level=logging.DEBUG)
  logger = logging.getLogger()
  # Console handler at INFO.
  consoleHandler = logging.StreamHandler()
  consoleHandler.setLevel(logging.INFO)
  # File handler at DEBUG.
  fileHandler = logging.FileHandler(LogPath)
  fileHandler.setLevel(logging.DEBUG)
  # Attach both handlers.
  logger.addHandler(consoleHandler)
  logger.addHandler(fileHandler)
  return logger


def TrainLoop(Model, TrainLoader, Optimizer, LossModule, Epochs):
  """Run epochs with tqdm bars and explicit device movement."""
  # Move the primary model and the loss module.
  Model.to(device)
  LossModule.to(device)
  for epoch in tqdm(range(Epochs), desc="Epochs"):
    # Training phase over batches.
    Model.train()
    for batch in tqdm(TrainLoader, desc="Batches", leave=False):
      # Forward, backward, step.
      Optimizer.zero_grad()
      logits = Model(batch[0].to(device))
      loss = LossModule(logits, batch[1].to(device))
      loss.backward()
      Optimizer.step()
```

## References

- PyTorch reproducibility guide: https://pytorch.org/docs/stable/notes/randomness.html
- tqdm documentation: https://tqdm.github.io/
- Python logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
