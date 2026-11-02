---
name: image-dataset-loader
description: Load image datasets from directory structures (`train/cat/`, `train/dog/`) using torchvision ImageFolder, apply augmentations (RandomResizedCrop, HorizontalFlip, ColorJitter, Normalize with ImageNet stats), and batch with DataLoader (num_workers, pin_memory, prefetch_factor) to overlap data loading and compute. Use this skill when feeding CNN/ViT training loops.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [images, torchvision, augmentation, dataloader, cnn]
related: [data-engineering/tabular-data-sampler, data-engineering/text-preprocessor]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1300
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Image Dataset Loader

## When To Use

- An image classification or detection model needs a data pipeline.
- The dataset is organised as `<split>/<class>/<image>.jpg` on disk.
- Augmentations differ between TRAIN (heavy) and VAL/TEST (deterministic).
- Batching must overlap with compute via `num_workers`, `pin_memory`, and `prefetch_factor`.
- Normalization must use the same stats (e.g., ImageNet) at train and inference.

## Workflow

1. Confirm the directory layout matches `<split>/<class>/<image>`.
2. Build the class index from TRAIN subdirectory names and persist it as JSON.
3. Compose TRAIN transforms: RandomResizedCrop, HorizontalFlip, ColorJitter, Normalize.
4. Compose VAL/TEST transforms: Resize, CenterCrop, Normalize (deterministic).
5. Instantiate `ImageFolder` per split with the matching transform.
6. Wrap each dataset in a `DataLoader` with `num_workers`, `pin_memory`, `prefetch_factor`.
7. Sanity-check: one batch from each split, shape and label range validation.
8. Persist the normalization stats and class index alongside the model artifact.

## Inputs

- Dataset root path containing `train/`, `val/`, `test/` subdirectories.
- Image size, batch size, number of workers, prefetch factor.
- Normalization stats (default: ImageNet mean and std).

## Outputs

- TRAIN, VAL, TEST `DataLoader` instances.
- A class index JSON (class name to integer) persisted with the model.
- Normalization stats persisted so inference matches training.

## Key Rules

- VAL and TEST transforms are deterministic; no random crops or flips.
- Normalization stats are identical at train and inference.
- `num_workers > 0` for training; `pin_memory=True` when GPU is used.
- The class index is built from TRAIN only and reused for VAL/TEST/inference.
- Augmentations are encoded as code, not notebooks.
- Batch shape is checked on the first batch of every loader before training starts.

## Examples

```python
import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def BuildTrainTransforms(imageSize):
  # Heavy augmentation for the TRAIN split.
  return transforms.Compose([
    transforms.RandomResizedCrop(imageSize, antialias=True),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])


def BuildEvalTransforms(imageSize):
  # Deterministic transforms for VAL and TEST splits.
  return transforms.Compose([
    transforms.Resize(int(imageSize * 1.14)),
    transforms.CenterCrop(imageSize),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])


def BuildLoaders(rootPath, imageSize=224, batchSize=64, numWorkers=4, prefetchFactor=2):
  # Build ImageFolder datasets and wrap them in DataLoaders.
  rootPath = Path(rootPath)
  trainDs = datasets.ImageFolder(rootPath / "train", transform=BuildTrainTransforms(imageSize))
  valDs = datasets.ImageFolder(rootPath / "val", transform=BuildEvalTransforms(imageSize))
  testDs = datasets.ImageFolder(rootPath / "test", transform=BuildEvalTransforms(imageSize))
  trainLoader = DataLoader(
    trainDs, batch_size=batchSize, shuffle=True,
    num_workers=numWorkers, pin_memory=True, prefetch_factor=prefetchFactor, drop_last=True,
  )
  valLoader = DataLoader(
    valDs, batch_size=batchSize, shuffle=False,
    num_workers=numWorkers, pin_memory=True,
  )
  testLoader = DataLoader(
    testDs, batch_size=batchSize, shuffle=False,
    num_workers=numWorkers, pin_memory=True,
  )
  return trainLoader, valLoader, testLoader, trainDs.classes


def SanityCheck(loaders, classIndex):
  # Validate shapes and label ranges before training starts.
  for name, loader in loaders.items():
    images, labels = next(iter(loader))
    if (images.dim() != 4):
      raise ValueError(f"{name} batch shape unexpected: {images.shape}")
    if (labels.max().item() >= len(classIndex)):
      raise ValueError(f"{name} label out of range: {labels.max().item()}")


def PersistClassIndex(classIndex, path):
  # Save the class-to-index mapping so inference matches training.
  with open(path, "w", encoding="utf-8") as handle:
    json.dump({"ClassIndex": classIndex, "Mean": IMAGENET_MEAN, "Std": IMAGENET_STD}, handle)
```

## References

- torchvision datasets: https://pytorch.org/vision/stable/datasets.html
- torchvision transforms: https://pytorch.org/vision/stable/transforms.html
- albumentations: https://albumentations.ai
- PyTorch DataLoader: https://pytorch.org/docs/stable/data.html
