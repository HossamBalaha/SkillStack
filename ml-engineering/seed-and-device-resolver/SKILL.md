---
name: seed-and-device-resolver
description: Resolve the torch device once and seed every RNG when starting a reproducible run. Triggers on "device resolution", "torch.cuda.is_available", "seed everything", "cudnn deterministic", "model.to(device) does not move sibling modules", "auxiliary branch returns zero tensor".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [seed, device, cuda, cudnn, determinism]
related: [ml-engineering/reproducible-experiment-runner, ml-engineering/pytorch-lightning-scaffold, ml-engineering/modular-ml-architect]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1040
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Seed And Device Resolver

## When To Use

- Starting any training run that requires determinism.
- Moving a primary model AND every standalone `nn.Module` to the device.
- Wrapping external or frozen auxiliary branches that may be `None` at runtime.
- Resolving the device once for the entire process.

## Workflow

1. Resolve `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` exactly once.
2. Call `random.seed(seed)`, `np.random.seed(seed)`, `torch.manual_seed(seed)`.
3. Call `torch.cuda.manual_seed_all(seed)` when CUDA is available.
4. Set `torch.backends.cudnn.deterministic = True` and `torch.backends.cudnn.benchmark = False`.
5. Move the primary model to `device`.
6. Move every standalone `nn.Module` (loss, regularizer, calibrator, auxiliary branch) explicitly.
7. For auxiliary branches wrapping external models, short-circuit if the wrapped model is `None`.

## Inputs

- A `Seed` integer from `Configs/Config.yaml`.
- The primary model and any auxiliary modules.

## Outputs

- A `device` constant reused across the process.
- Deterministic behavior across reruns with the same seed.

## Key Rules

- Resolve `device` exactly once; never call `torch.device(...)` per function.
- `model.to(device)` does NOT transitively move sibling modules — move each explicitly.
- Auxiliary branches wrapping external/frozen models MUST short-circuit and return a zero/identity tensor on the correct
  device if the wrapped model is `None`.
- Set `cudnn.deterministic = True` AND `cudnn.benchmark = False` together.
- Seed `random`, `numpy`, `torch`, and CUDA together.

## Examples

```python
# Resolve device once and seed every RNG.
import random
import numpy as np
import torch
import torch.nn as nn


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def SeedEverything(Seed):
  """Seed random, numpy, torch, and CUDA deterministically."""
  # Python random.
  random.seed(Seed)
  # NumPy random.
  np.random.seed(Seed)
  # Torch CPU.
  torch.manual_seed(Seed)
  # Torch CUDA if available.
  if (torch.cuda.is_available()):
    torch.cuda.manual_seed_all(Seed)
  # cuDNN determinism.
  torch.backends.cudnn.deterministic = True
  # Disable autotuner for reproducibility.
  torch.backends.cudnn.benchmark = False


class AuxiliaryBranch(nn.Module):
  """Wraps an external model; short-circuits to zero when None."""

  def __init__(self, WrappedModel=None):
    # Store the optional wrapped model.
    super().__init__()
    self.WrappedModel = WrappedModel

  def forward(self, X):
    # Short-circuit when the wrapped model is missing.
    if (self.WrappedModel is None):
      # Return a zero tensor matching the input device.
      return torch.zeros(X.shape[0], 1, device=X.device)
    # Otherwise delegate to the wrapped model.
    return self.WrappedModel(X)


def MoveAllToDevice(Model, LossModule, Regularizer, Calibrator, Auxiliary):
  """Move the primary model and every standalone module to device."""
  # Primary model.
  Model.to(device)
  # Loss module moved separately — model.to does not propagate.
  LossModule.to(device)
  # Regularizer moved separately.
  Regularizer.to(device)
  # Calibrator moved separately.
  Calibrator.to(device)
  # Auxiliary branch moved separately.
  Auxiliary.to(device)
```

## References

- PyTorch reproducibility: https://pytorch.org/docs/stable/notes/randomness.html
- torch.cuda manual: https://pytorch.org/docs/stable/cuda.html
