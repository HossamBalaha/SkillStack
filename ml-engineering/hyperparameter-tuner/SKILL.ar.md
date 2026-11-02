---
name: hyperparameter-tuner
description: Drive Bayesian hyperparameter optimization with Optuna when tuning a model's learning rate, batch size, dropout, architecture depth, or any tunable knob. Triggers on "Optuna", "TPE sampler", "MedianPruner", "Bayesian optimization", "trials_dataframe", "Config.yaml search space".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [optuna, bayesian, tuning, hyperparameters]
related: [ml-engineering/reproducible-experiment-runner, ml-engineering/early-stopping-configurator]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python, json, csv]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: ar
---

# ضابط المعاملات الفائقة

## متى تستخدم
- ضبط أكثر من حفنة من المعاملات الفائقةّ حيث يصبح البحث الشبكيّ غير عمليّ.
- قراءة فضاء البحث من `Configs/Config.yaml` والتحسين تلقائيّاً.
- تقليم المحاولات غير الواعدة مبكّراً لتوفير الحساب.
- الاستمرار في تاريخ المحاولة الكاملّ إلى CSV لإمكانيّة التكرار.

## سير العمل
1. حمِّل `Configs/Config.yaml` واقرأ كتلة `SearchSpace`.
2. أنشئ `optuna.study.Study` بعيّنة TPE ومولّد أرقام عشوائيّة مُبذَر.
3. أرفق `MedianPruner` (أو `HyperbandPruner` للترقية متعدّدة الدقّة).
4. عرِّف `objective(trial)` الذي يقترح معاملات فائقةّ ويدرّب نموذجاً ويعيد مقياس التحقّق.
5. استدعِ `study.optimize(objective, n_trials=N, timeout=T)`.
6. استمرّ `study.trials_dataframe()` في `Aggregated/OptunaTrials.csv`.
7. سجّل رقم المحاولة الأفضل وقيمتها وقاموس المعاملات.
8. أعد تدريب النموذج بأفضل المعاملات واحفظه.

## المُدخلات
- `Configs/Config.yaml` يحوي كتلة `SearchSpace`.
- دالة تدريب تقبل قاموس معاملات فائقةّ وتعيد مقياس تحقّق.

## المُخرجات
- `Aggregated/OptunaTrials.csv` بكلّ محاولة.
- `Aggregated/BestParams.json` بالتكوين الفائز.
- نقطة فحص النموذج الأفضل المُعاد تدريبه.

## القواعد الأساسية
- استخدم `optuna.samplers.TPESampler(seed=...)` ببذرة ثابتة.
- استخدم `optuna.pruners.MedianPruner` افتراضيّاً؛ HyperbandPruner للدقّة المتعدّدة.
- يجب أن يستدعي الهدف `trial.report(metric, step)` ويتحقّق من `trial.should_prune()`.
- استمرّ `study.trials_dataframe()` بعد انتهاء التحسين.
- أشِر فقط إلى واجهة برمجة تطبيقات Optuna الحقيقيّة على https://optuna.org.

## أمثلة
```python
# Bayesian optimization with TPE and a median pruner.
import optuna
import pandas as pd
import json


def BuildStudy(Seed):
  """Construct a study with a deterministic TPE sampler."""
  # Seed the sampler so the search is reproducible.
  sampler = optuna.samplers.TPESampler(seed=Seed)
  # Median pruner cuts unpromising trials early.
  pruner = optuna.pruners.MedianPruner(
    n_startup_trials=5,
    n_warmup_steps=3
  )
  return optuna.create_study(
    direction="maximize",
    sampler=sampler,
    pruner=pruner
  )


def Objective(trial, TrainFunction):
  """Suggest hyperparameters and return the validation metric."""
  # Sample from the configured search space.
  learningRate = trial.suggest_float("LearningRate", 1e-5, 1e-2, log=True)
  dropout = trial.suggest_float("Dropout", 0.0, 0.5)
  hiddenSize = trial.suggest_categorical("HiddenSize", [64, 128, 256, 512])
  # Train with the suggested hyperparameters.
  metric = TrainFunction({
    "LearningRate": learningRate,
    "Dropout": dropout,
    "HiddenSize": hiddenSize
  })
  return metric


def RunTuning(SearchSpace, TrainFunction, N_trials, Seed, OutputPath):
  """Run optimization and persist the trial dataframe."""
  # Build and run the study.
  study = BuildStudy(Seed)
  study.optimize(
    lambda trial: Objective(trial, TrainFunction),
    n_trials=N_trials,
    timeout=3600
  )
  # Persist the trial history.
  df = study.trials_dataframe()
  df.to_csv(OutputPath + "OptunaTrials.csv", index=False)
  # Save the best parameters.
  bestParams = study.best_params
  with open(OutputPath + "BestParams.json", "w") as f:
    json.dump(bestParams, f, indent=2)
  return bestParams
```

## المراجع
- توثيق Optuna: https://optuna.org
- عيّنة TPE: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.samplers.TPESampler.html
- MedianPruner: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html
