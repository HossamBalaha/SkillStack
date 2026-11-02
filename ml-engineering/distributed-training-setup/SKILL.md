---
name: distributed-training-setup
description: Set up Distributed Data Parallel (DDP) when training across multiple GPUs or nodes. Triggers on "DDP", "torchrun", "nproc_per_node", "init_process_group", "DistributedSampler", "DistributedDataParallel", "find_unused_parameters", "nccl backend".
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ml-engineering
tags: [ddp, distributed, torchrun, multi-gpu, nccl]
related: [ml-engineering/pytorch-lightning-scaffold, ml-engineering/mixed-precision-trainer, ml-engineering/seed-and-device-resolver]
prerequisites: [ml-engineering/pytorch-lightning-scaffold]
outputs: [python, bash]
difficulty: advanced
estimated_tokens: 1020
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Distributed Training Setup

## When To Use
- Training on multiple GPUs on a single node.
- Training across multiple nodes over NCCL.
- Scaling batch size beyond a single GPU.
- Setting up `torchrun`-based launch with the correct environment variables.

## Workflow
1. Launch the script with `torchrun --nproc_per_node=N main.py`.
2. Read `RANK`, `WORLD_SIZE`, `LOCAL_RANK` from environment variables.
3. Call `torch.distributed.init_process_group(backend="nccl")`.
4. Pin the device to `LOCAL_RANK`: `torch.cuda.set_device(local_rank)`.
5. Wrap the model with `DDP(model, device_ids=[local_rank], find_unused_parameters=...)`.
6. Build a `DistributedSampler` for the dataloader.
7. Call `sampler.set_epoch(epoch)` at every epoch.
8. Only rank 0 writes artifacts to disk.
9. Call `torch.distributed.destroy_process_group()` at shutdown.

## Inputs
- `Configs/Config.yaml` with `WorldSize`, `Backend` (default `"nccl"`).
- A model factory and a dataset factory.

## Outputs
- A DDP-wrapped model training across all GPUs.
- Artifacts written by rank 0 only.

## Key Rules
- Use `torchrun --nproc_per_node=N main.py` to launch.
- Backend must be `"nccl"` for GPU training.
- Use `DistributedSampler` and call `set_epoch(epoch)` every epoch.
- Only rank 0 saves checkpoints and logs to file.
- `find_unused_parameters=True` is required when the model has conditionally unused submodules.
- Reference the real PyTorch DDP tutorial.

## Examples
```python
# DDP setup with rank-aware artifact writing.
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler


def InitDistributed(Backend="nccl"):
  """Initialize the process group and return local_rank."""
  # Read environment variables set by torchrun.
  localRank = int(os.environ["LOCAL_RANK"])
  worldSize = int(os.environ["WORLD_SIZE"])
  # Initialize the process group.
  dist.init_process_group(backend=Backend)
  # Pin the GPU to this rank.
  torch.cuda.set_device(localRank)
  return localRank, worldSize


def WrapModel(Model, LocalRank, FindUnused=False):
  """Wrap a model with DDP for the given local rank."""
  # Move model to the pinned GPU.
  Model.to(torch.device("cuda", LocalRank))
  # Wrap with DistributedDataParallel.
  return DDP(
    Model,
    device_ids=[LocalRank],
    find_unused_parameters=FindUnused
  )


def BuildDistributedLoader(Dataset, BatchSize, Shuffle, Seed):
  """Build a DataLoader with a DistributedSampler."""
  # Sampler that shards across ranks.
  sampler = DistributedSampler(Dataset, shuffle=Shuffle)
  return torch.utils.data.DataLoader(
    Dataset,
    batch_size=BatchSize,
    sampler=sampler,
    shuffle=False
  ), sampler


def SaveIfRankZero(Path, SaveFunction):
  """Call SaveFunction(Path) only on rank 0."""
  # Get the global rank.
  rank = dist.get_rank() if (dist.is_initialized()) else 0
  if (rank == 0):
    SaveFunction(Path)
```

## References
- PyTorch DDP tutorial: https://pytorch.org/tutorials/intermediate/ddp_tutorial.html
- torchrun launcher: https://pytorch.org/docs/stable/elastic/run.html
- DistributedSampler: https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler
