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
language: zh
---

# 可复现实验运行器

## 何时使用
- 启动必须在跨机器上可复现的训练运行。
- 为主模型**以及**辅助模块配置设备放置。
- 设置双重日志（控制台 + 文件）和 `tqdm` 进度条。
- 将产物组织到单个带时间戳的实验文件夹中。
- 当用户提到 `Results/{DatasetName}_{Timestamp}` 布局时。

## 工作流程
1. 读取 `Configs/Config.yaml` 获取随机种子、数据集名称和日志级别。
2. 恰好解析一次 `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")`。
3. 以确定性方式为 `random`、`numpy`、`torch` 和 CUDA 播种。
4. 创建 `Results/{DatasetName}_{YYYYMMDD_HHMMSS}/`，包含子文件夹 `Train/`、`Validation/`、`Test/`、`Aggregated/`。
5. 配置双重日志：控制台 INFO + 文件 DEBUG，位于 `Aggregated/execution.log`。
6. 用 `tqdm` 进度条包裹 epoch、batch 和 trial 循环。
7. 显式地将主模型**以及**每个独立 `nn.Module` 移至 `device`。
8. 将每个产物保存到正确的划分子文件夹中，不对单个文件加时间戳。
9. 在结束时写入 `Aggregated/Summary.json`，包含所有指标。

## 输入
- `Configs/Config.yaml`，至少包含 `Seed`、`DatasetName`、`Epochs`、`BatchSize`。
- 一个模型工厂和一个数据集工厂。

## 输出
- `Results/{DatasetName}_{Timestamp}/`，包含四个划分子文件夹。
- `Aggregated/execution.log`，含完整 DEBUG 跟踪。
- 每个划分的指标 JSON 文件。

## 核心规则
- `device` 必须解析**一次**并在各处复用。
- 对每个独立 `nn.Module`（损失、正则化器、校准器、辅助分支）调用 `.to(device)` —— `model.to(device)` 不会移动兄弟模块。
- 每个实验一个带时间戳的文件夹；**不要**对单个文件加时间戳。
- 双重日志：同时记录控制台 INFO 与文件 DEBUG。
- 在 epoch、batch 和 trial 上有 `tqdm` 进度条。
- 仅四个子文件夹：`Train/`、`Validation/`、`Test/`、`Aggregated/`。

## 示例
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

## 参考资料
- PyTorch 可复现性指南：https://pytorch.org/docs/stable/notes/randomness.html
- tqdm 文档：https://tqdm.github.io/
- Python 日志手册：https://docs.python.org/3/howto/logging-cookbook.html
