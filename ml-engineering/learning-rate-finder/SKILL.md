---
name: learning-rate-finder
description: Run an LR range test to pick a sensible initial learning rate before full training. Triggers on "LR range test", "Smith 2015 cyclical learning rates", "torch_lr_finder", "Lightning Tuner.lr_find", "steepest loss descent", "log-scale LR plot".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [lr-finder, range-test, learning-rate, smith-2015, lightning-tuner]
related: [ml-engineering/pytorch-lightning-scaffold, ml-engineering/hyperparameter-tuner, ml-engineering/early-stopping-configurator]
prerequisites: [ml-engineering/pytorch-lightning-scaffold]
outputs: [python, svg, csv]
difficulty: intermediate
estimated_tokens: 990
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Learning Rate Finder

## When To Use

- Choosing a starting learning rate for a new architecture.
- Sanity-checking whether the chosen LR is in the descending region of the loss curve.
- Picking an LR for cyclical learning rate schedules.
- Generating the canonical loss-vs-LR log-scale plot.

## Workflow

1. Load the model, data loader, and optimizer from `Configs/Config.yaml`.
2. Initialize LR at a very small value (e.g. 1e-7) and exponentially grow to ~1e1.
3. Iterate over a few epochs while logging loss at each LR step.
4. Plot loss vs LR on a log scale.
5. Identify the steepest descent point on the curve.
6. Pick the LR at that steepest descent (often one order below the divergence point).
7. Persist the plot to `Aggregated/LrFinder.png`.
8. Write the picked LR to `Aggregated/SuggestedLr.json`.

## Inputs

- A model factory, a data loader, and a loss function.
- `Configs/Config.yaml` with `StartLr`, `EndLr`, `NumIter`.

## Outputs

- `Aggregated/LrFinder.png` log-scale plot.
- `Aggregated/SuggestedLr.json` with the picked LR.

## Key Rules

- Start LR around 1e-7 and grow exponentially to ~1e1.
- Plot loss vs LR on a LOG scale.
- Pick the LR at the steepest descent, not at the minimum loss.
- Use `torch_lr_finder` or Lightning's `Tuner.lr_find()` — do not reimplement the math.
- Reference Smith 2015, "Cyclical Learning Rates for Training Neural Networks".

## Examples

```python
# LR range test using torch_lr_finder.
import json
import matplotlib.pyplot as plt
from torch_lr_finder import LRFinder


def RunLrRangeTest(Model, DataLoader, Optimizer, LossModule, Device, OutputDir):
  """Run an exponential LR range test and persist outputs."""
  # Move model and loss module to device.
  Model.to(Device)
  LossModule.to(Device)
  # Construct the LR finder.
  lrFinder = LRFinder(Model, Optimizer, LossModule, device=Device)
  # Run the range test from 1e-7 to 1e1.
  lrFinder.range_test(
    DataLoader,
    start_lr=1e-7,
    end_lr=1e1,
    num_iter=100
  )
  # Plot the loss curve on a log scale.
  fig, ax = plt.subplots()
  lrFinder.plot(skip_start=5, skip_end=5, log_lr=True, ax=ax)
  fig.savefig(OutputDir + "LrFinder.png", bbox_inches="tight")
  plt.close(fig)
  # Suggest the LR at the steepest descent.
  suggestedLr = SuggestLrAtSteepestDescent(lrFinder)
  with open(OutputDir + "SuggestedLr.json", "w") as f:
    json.dump({"LearningRate": suggestedLr}, f, indent=2)
  # Reset the model so the run does not pollute weights.
  lrFinder.reset()
  return suggestedLr


def SuggestLrAtSteepestDescent(LrFinder):
  """Pick the LR at the steepest loss descent."""
  # Extract logged LRs and losses.
  lrs = LrFinder.history["lr"]
  losses = LrFinder.history["loss"]
  # Compute the negative gradient of the loss curve.
  gradients = []
  for i in range(1, len(losses)):
    # Guard against division by zero.
    if (lrs[i] == lrs[i - 1]):
      continue
    gradients.append((losses[i] - losses[i - 1]) / (lrs[i] - lrs[i - 1]))
  # Pick the LR at the most negative gradient.
  minIdx = gradients.index(min(gradients))
  return lrs[minIdx + 1]
```
