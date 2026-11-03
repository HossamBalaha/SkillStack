---
name: mixed-precision-trainer
description: Enable Automatic Mixed Precision (AMP) training when GPU memory is tight or throughput must improve. Triggers on "AMP", "autocast", "GradScaler", "fp16 bf16", "Ampere GPU", "memory savings", "training speedup".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [amp, autocast, gradscaler, fp16, bf16]
related: [ml-engineering/pytorch-lightning-scaffold, ml-engineering/distributed-training-setup, ml-engineering/model-checkpoint-manager]
prerequisites: [ml-engineering/pytorch-lightning-scaffold]
outputs: [python]
difficulty: advanced
estimated_tokens: 940
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Mixed Precision Trainer

## When To Use

- Training a model on a GPU with limited memory.
- Needing faster iteration on the same hardware.
- Using Ampere+ GPUs that support bf16 natively.
- Avoiding manual casting of every layer to half precision.

## Workflow

1. Detect the GPU compute capability to decide between fp16 and bf16.
2. On Ampere+ GPUs prefer bf16 (no scaler needed).
3. Otherwise use fp16 with a `torch.cuda.amp.GradScaler`.
4. Wrap the forward pass in `torch.cuda.amp.autocast()`.
5. Call `scaler.scale(loss).backward()` for the backward pass.
6. Call `scaler.step(optimizer)` and `scaler.update()`.
7. Document memory savings and measured speedup in `Aggregated/AmpReport.json`.

## Inputs

- Model, optimizer, loss module, and data loader.
- A flag in `Configs/Config.yaml` indicating `Precision: "fp16"` or `"bf16"`.

## Outputs

- A training loop using AMP.
- `Aggregated/AmpReport.json` documenting peak memory and wall-clock speedup.

## Key Rules

- fp16 requires a `GradScaler`; bf16 does not.
- Wrap the forward pass with `autocast()` — never cast tensors manually.
- Call `scaler.update()` after every step.
- Use bf16 on Ampere+ GPUs (compute capability >= 8.0).
- Reference the real PyTorch AMP docs.

## Examples

```python
# AMP training loop with fp16 GradScaler fallback.
import json
import time
import torch


def TrainOneEpochWithAmp(Model, DataLoader, Optimizer, LossModule, Device, UseBf16):
  """Train for one epoch with autocast and a GradScaler when fp16."""
  # Move model and loss module to device.
  Model.to(Device)
  LossModule.to(Device)
  Model.train()
  # Create a GradScaler only when fp16 is requested.
  if (not UseBf16):
    scaler = torch.cuda.amp.GradScaler()
  # Track peak memory for the report.
  torch.cuda.reset_peak_memory_stats()
  startTime = time.time()
  for batch in DataLoader:
    # Move data to device.
    X, y = batch[0].to(Device), batch[1].to(Device)
    Optimizer.zero_grad()
    # Forward under autocast.
    with torch.cuda.amp.autocast(dtype=torch.bfloat16 if (UseBf16) else torch.float16):
      logits = Model(X)
      loss = LossModule(logits, y)
    if (UseBf16):
      # bf16 does not require a scaler.
      loss.backward()
      Optimizer.step()
    else:
      # fp16 path uses the scaler.
      scaler.scale(loss).backward()
      scaler.step(Optimizer)
      scaler.update()
  elapsed = time.time() - startTime
  peakMemory = torch.cuda.max_memory_allocated() / (1024 ** 3)
  return {"ElapsedSeconds": elapsed, "PeakMemoryGiB": peakMemory}


def WriteAmpReport(Report, OutputDir):
  """Persist AMP memory and speedup numbers."""
  # Save the JSON report.
  with open(OutputDir + "AmpReport.json", "w") as f:
    json.dump(Report, f, indent=2)
```
