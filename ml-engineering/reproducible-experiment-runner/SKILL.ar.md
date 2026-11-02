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
language: ar
---

# مشغّل التجربة القابلة للتكرار

## متى تستخدم

- بدء تشغيل تدريب يجب أن يكون قابلاً للتكرار عبر الآلات.
- إعداد موضع الجهاز للنموذج الأساسي والوحدات الإضافيّة.
- إعداد تسجيل مزدوج (وحدة تحكّم + ملفّ) وأشرطة تقدّم `tqdm`.
- تنظيم المنتجات في مجلد تجربة واحد بختم زمنيّ.
- عندما يذكر المستخدم تخطيط "Results/{DatasetName}_{Timestamp}".

## سير العمل

1. اقرأ `Configs/Config.yaml` للبذرة واسم مجموعة البيانات ومستوى التسجيل.
2. حلّ `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` مرة واحدة تماماً.
3. ابذر `random` و`numpy` و`torch` وCUDA حتميّاً.
4. أنشئ `Results/{DatasetName}_{YYYYMMDD_HHMMSS}/` بمجلدات فرعيّة `Train/` و`Validation/` و`Test/` و`Aggregated/`.
5. إعداد التسجيل المزدوج: وحدة تحكّم INFO + ملفّ DEBUG في `Aggregated/execution.log`.
6. لُفّ حلقة العصر وحلقة الدفعة وحلقة المحاولة في أشرطة تقدّم `tqdm`.
7. انقل النموذج الأساسي وكلّ `nn.Module` مستقلّ إلى `device` صراحةً.
8. احفظ كلّ منتَج في المجلد الفرعيّ الصحيح للتقسيم بدون ختم زمنيّ لكلّ ملفّ.
9. في النهاية، اكتب `Aggregated/Summary.json` بكلّ المقاييس.

## المُدخلات

- `Configs/Config.yaml` يحوي على الأقلّ `Seed` و`DatasetName` و`Epochs` و`BatchSize`.
- مصنع نموذج ومصنع مجموعة بيانات.

## المُخرجات

- `Results/{DatasetName}_{Timestamp}/` يحوي أربعة مجلدات فرعيّة للتقسيم.
- `Aggregated/execution.log` بتتبّع DEBUG كامل.
- ملفّات JSON للمقاييس لكلّ تقسيم.

## القواعد الأساسية

- يجب حلّ `device` مرة واحدة وإعادة استخدامه في كلّ مكان.
- استدعِ `.to(device)` على كلّ `nn.Module` مستقلّ (خسارة، منظّم، معاير، فرع إضافيّ) — `model.to(device)` لا ينقل الوحدات
  الشقيقة.
- مجلد واحد بختم زمنيّ لكلّ تجربة؛ لا تختم ملفّات فرديّة بالزمن.
- تسجيل مزدوج: وحدة تحكّم INFO وملفّ DEBUG في وقت واحد.
- أشرطة `tqdm` على العصور والدفعات والمحاولات.
- أربعة مجلدات فرعيّة فقط: `Train/` و`Validation/` و`Test/` و`Aggregated/`.

## أمثلة

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

## المراجع

- دليل قابلية التكرار في PyTorch: https://pytorch.org/docs/stable/notes/randomness.html
- توثيق tqdm: https://tqdm.github.io/
- كتاب طبخ التسجيل في Python: https://docs.python.org/3/howto/logging-cookbook.html
