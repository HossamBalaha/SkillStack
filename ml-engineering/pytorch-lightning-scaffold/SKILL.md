---
name: pytorch-lightning-scaffold
description: Scaffold PyTorch Lightning modules when starting a new training project, defining the LightningModule, LightningDataModule, callbacks, and loggers. Triggers on "PyTorch Lightning", "LightningModule", "LightningDataModule", "EarlyStopping callback", "ModelCheckpoint", "W&B logger", "training_step", "configure_optimizers".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [pytorch-lightning, lightningmodule, datamodule, callbacks, loggers]
related: [ml-engineering/modular-ml-architect, ml-engineering/early-stopping-configurator, ml-engineering/model-checkpoint-manager, ml-engineering/mixed-precision-trainer]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python]
difficulty: advanced
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: false
language: en
---

# PyTorch Lightning Scaffold

## When To Use

- Starting a fresh training project with PyTorch Lightning.
- Migrating a vanilla `torch.nn` training loop to Lightning.
- Wiring callbacks for early stopping, checkpointing, and LR monitoring.
- Attaching loggers (W&B, MLflow, TensorBoard) to a trainer.

## Workflow

1. Define a `LightningModule` subclass with `__init__`, `forward`, `training_step`, `validation_step`,
   `configure_optimizers`.
2. Define a `LightningDataModule` with `setup`, `train_dataloader`, `val_dataloader`, `test_dataloader`.
3. Build a callback list: `EarlyStopping`, `ModelCheckpoint`, `LearningRateMonitor`.
4. Build a logger list: `WandbLogger`, `MLFlowLogger`, or `TensorBoardLogger`.
5. Instantiate `L.Trainer` with callbacks, logger, accelerator, devices.
6. Call `trainer.fit(model, datamodule)` then `trainer.test(...)`.
7. Persist the best checkpoint path to `Aggregated/BestCheckpoint.json`.

## Inputs

- `Configs/Config.yaml` with model hyperparameters, batch size, max epochs.
- A model factory producing a `nn.Module`.
- A dataset path or `LightningDataModule`.

## Outputs

- A reproducible Lightning training script.
- Best checkpoint under `Results/{DatasetName}_{Timestamp}/Train/`.
- Logged metrics in W&B / MLflow / TensorBoard.

## Key Rules

- `LightningModule` methods (`forward`, `training_step`, `validation_step`, `configure_optimizers`) are
  framework-mandated lowercase and exempt from CamelCase.
- Every other function and class name is CamelCase.
- `configure_optimizers` must return either an optimizer or a tuple of (optimizer, scheduler).
- Use `self.log("ValLoss", loss, prog_bar=True)` to expose metrics to callbacks.
- Reference only the real Lightning API at https://lightning.ai.

## Examples

```python
# Lightning module + datamodule + callbacks + logger.
import pytorch_lightning as L
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


class TabularModel(L.LightningModule):
  """A simple MLP exposed as a LightningModule."""

  def __init__(self, InputDim, HiddenDim, OutputDim, LearningRate):
    # Initialize the parent class.
    super().__init__()
    # Save hyperparameters for checkpoint reproducibility.
    self.save_hyperparameters()
    # Build the network layers.
    self.net = nn.Sequential(
      nn.Linear(InputDim, HiddenDim),
      nn.ReLU(),
      nn.Linear(HiddenDim, OutputDim)
    )
    # Reusable loss module.
    self.lossFn = nn.CrossEntropyLoss()

  def forward(self, X):
    # Forward pass without gradient bookkeeping.
    return self.net(X)

  def training_step(self, Batch, BatchIdx):
    # Compute and log training loss.
    X, y = Batch
    logits = self(X)
    loss = self.lossFn(logits, y)
    self.log("TrainLoss", loss, prog_bar=True)
    return loss

  def validation_step(self, Batch, BatchIdx):
    # Compute and log validation loss.
    X, y = Batch
    logits = self(X)
    loss = self.lossFn(logits, y)
    self.log("ValLoss", loss, prog_bar=True)
    return loss

  def configure_optimizers(self):
    # Return the optimizer Lightning will use.
    return torch.optim.Adam(self.parameters(), lr=self.hparams.LearningRate)


def BuildTrainer(MaxEpochs, Callbacks, Logger):
  """Construct a Trainer with callbacks and logger."""
  # Use GPU if available.
  accelerator = "gpu" if (torch.cuda.is_available()) else "cpu"
  return L.Trainer(
    max_epochs=MaxEpochs,
    accelerator=accelerator,
    devices=1,
    callbacks=Callbacks,
    logger=Logger
  )
```

## References

- PyTorch Lightning documentation: https://lightning.ai/docs/pytorch/stable/
- Lightning callbacks: https://lightning.ai/docs/pytorch/stable/api_references.html#callbacks
