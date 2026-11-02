---
name: modular-ml-architect
description: Enforce modular Python conventions across ML projects when scaffolding a new repository, refactoring a monolithic script, or auditing code structure. Triggers on keywords like "modular ML project", "src layout", "split code into modules", "reusable functions", "Config.yaml".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [modular, src-layout, refactoring, conventions, scaffolding]
related: [style-integrity/coding-conventions-enforcer, ml-engineering/reproducible-experiment-runner, ml-engineering/dataset-adapter-builder]
prerequisites: []
outputs: [python, markdown]
difficulty: intermediate
estimated_tokens: 1080
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Modular ML Architect

## When To Use
- Scaffolding a new ML repository that needs a maintainable layout.
- Refactoring a monolithic `Main.py` into reusable modules.
- Auditing a codebase for adherence to modular, reusable conventions.
- Setting up a project so that data, models, and utilities are isolated.
- When the user asks for "src/data", "src/models", "src/utils" separation.

## Workflow
1. Inspect the existing repository root and identify monolithic scripts.
2. Create the canonical directory tree: `src/data/`, `src/models/`, `src/utils/`, `Configs/`, `Results/`.
3. Move dataset classes into `src/data/`, model definitions into `src/models/`, helper logic into `src/utils/`.
4. Author `Configs/Config.yaml` with all tunable parameters (seed, batch size, learning rate, paths).
5. Rewrite root `Main.py` so it ONLY orchestrates: load config, build data, build model, train, evaluate, save artifacts.
6. Ensure every function is generic (no hardcoded dataset names, no absolute paths).
7. Apply the strict coding style: camelCase variables, CamelCase identifiers, 2-space indent, double quotes.
8. Add comprehensive docstrings to every function and class.
9. Add an `__init__.py` to each package directory.
10. Run a smoke import to confirm no circular dependencies.

## Inputs
- Existing repository layout (or empty directory for greenfield).
- A draft configuration if the user supplied one.

## Outputs
- A standardized directory tree.
- `Configs/Config.yaml` populated with sensible defaults.
- Root `Main.py` reduced to orchestration only.
- Package `__init__.py` files.

## Key Rules
- Root `Main.py` must contain ONLY orchestration calls, never domain logic.
- Functions must be generic and reusable across datasets.
- camelCase for variables; CamelCase for functions, classes, file names, and dict keys.
- Every `if` statement must wrap its condition in parentheses.
- Every statement must be preceded by a period-ended comment explaining intent.
- 2-space indentation, double-quoted strings, no tabs.
- Framework-mandated lowercase names (`forward`, `training_step`, `setUp`) are exempt.
- Every public function and class needs a docstring.

## Examples
```python
# Standard project layout.
# src/data/DatasetLoader.py
"""Dataset loading utilities shared across experiments."""

import torch
from torch.utils.data import Dataset


class TabularDataset(Dataset):
  """Wraps a numpy array into a torch Dataset.

  Args:
    Features: 2-D numpy array of input features.
    Labels: 1-D numpy array of targets.
  """

  def __init__(self, Features, Labels):
    # Store tensors on CPU; move later via .to(device).
    self.Features = torch.tensor(Features, dtype=torch.float32)
    self.Labels = torch.tensor(Labels, dtype=torch.long)

  def __len__(self):
    # Return the sample count for the sampler.
    return len(self.Labels)

  def __getitem__(self, Index):
    # Index into pre-converted tensors.
    return self.Features[Index], self.Labels[Index]


def BuildDataLoader(Dataset, BatchSize, Shuffle):
  """Generic DataLoader factory reused by every experiment."""
  # Delegate construction to torch's DataLoader.
  return torch.utils.data.DataLoader(
    Dataset,
    batch_size=BatchSize,
    shuffle=Shuffle
  )
```

```yaml
# Configs/Config.yaml
Dataset:
  Name: "Cifar10"
  Path: "Data/Cifar10/"
Training:
  BatchSize: 64
  LearningRate: 0.001
  Epochs: 50
  Seed: 42
Device: "auto"
```

## References
- Python packaging guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- The "src" layout discussion: https://hynek.me/articles/testing-packaging/
