# ⚙️ ML Engineering — PyTorch, Training & Validation

> Scaffold, train, tune, and validate PyTorch / Lightning models with strong reproducibility guarantees. Covers dataset
> adapters, leakage guards, training loops, hyperparameter search, ablation studies, explainability, and statistical
> rigor — every piece needed to take a model from notebook to publishable experiment. Output is always paired with a
> metrics report and a reproducibility manifest.

## Theme Overview

This folder contains **22 skills** in the `ml-engineering/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                       | Description                                                                                                                                                                 | Difficulty   | Tags                                                                               | Related                                                                                                                                                                  |
|----|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`ablation-study-runner`](ablation-study-runner/SKILL.md)                   | Run ablation studies by systematically removing or altering components of a proposed model.                                                                                 | advanced     | `ablation`, `experiments`, `component-removal`, `metric-delta`, `controlled`       | `ml-engineering/reproducible-experiment-runner`, `ml-engineering/baseline-model-zoo`, `ml-engineering/cross-validation-engine`                                           |
| 2  | [`baseline-model-zoo`](baseline-model-zoo/SKILL.md)                         | Implement standard baseline models for fair comparison when the user needs reference points against a proposed model.                                                       | intermediate | `baselines`, `logistic-regression`, `random-forest`, `xgboost`, `comparison`       | `ml-engineering/ablation-study-runner`, `ml-engineering/metrics-computation-suite`, `ml-engineering/modular-ml-architect`                                                |
| 3  | [`cross-validation-engine`](cross-validation-engine/SKILL.md)               | Run k-fold cross-validation (stratified, grouped, or time-series) when evaluating model generalization.                                                                     | advanced     | `cross-validation`, `kfold`, `stratified`, `grouped`, `timeseries`                 | `ml-engineering/train-val-test-splitter`, `ml-engineering/statistical-validation-rigor`, `ml-engineering/data-leakage-guard`                                             |
| 4  | [`data-leakage-guard`](data-leakage-guard/SKILL.md)                         | Enforce strict train/validation/test isolation when preprocessing data, fitting transformers, or partitioning samples.                                                      | advanced     | `data-leakage`, `train-test-isolation`, `preprocessing`, `fitting`, `partitioning` | `ml-engineering/train-val-test-splitter`, `ml-engineering/cross-validation-engine`, `ml-engineering/dataset-adapter-builder`                                             |
| 5  | [`dataset-adapter-builder`](dataset-adapter-builder/SKILL.md)               | Build defensive dataset adapters when wiring external datasets into a training pipeline.                                                                                    | intermediate | `dataset`, `adapter`, `pandas`, `numpy`, `defensive-loading`                       | `ml-engineering/modular-ml-architect`, `ml-engineering/data-leakage-guard`, `ml-engineering/train-val-test-splitter`                                                     |
| 6  | [`distributed-training-setup`](distributed-training-setup/SKILL.md)         | Set up Distributed Data Parallel (DDP) when training across multiple GPUs or nodes.                                                                                         | advanced     | `ddp`, `distributed`, `torchrun`, `multi-gpu`, `nccl`                              | `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/mixed-precision-trainer`, `ml-engineering/seed-and-device-resolver`                                         |
| 7  | [`early-stopping-configurator`](early-stopping-configurator/SKILL.md)       | Configure early stopping when training a model that may plateau, overfit, or waste compute.                                                                                 | intermediate | `early-stopping`, `patience`, `min-delta`, `val-loss`, `callbacks`                 | `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/hyperparameter-tuner`, `ml-engineering/model-checkpoint-manager`                                            |
| 8  | [`experiment-folder-organizer`](experiment-folder-organizer/SKILL.md)       | Create a single timestamped experiment folder with four split subfolders when starting a run, ensuring all artifacts land in the correct split.                             | beginner     | `experiment`, `folder`, `timestamps`, `artifacts`, `layout`                        | `ml-engineering/reproducible-experiment-runner`, `ml-engineering/model-checkpoint-manager`, `ml-engineering/seed-and-device-resolver`                                    |
| 9  | [`hyperparameter-tuner`](hyperparameter-tuner/SKILL.md)                     | Drive Bayesian hyperparameter optimization with Optuna when tuning a model's learning rate, batch size, dropout, architecture depth, or any tunable knob.                   | advanced     | `optuna`, `bayesian`, `tuning`, `hyperparameters`                                  | `ml-engineering/reproducible-experiment-runner`, `ml-engineering/early-stopping-configurator`                                                                            |
| 10 | [`inference-pipeline-builder`](inference-pipeline-builder/SKILL.md)         | Build a FastAPI inference endpoint when deploying a trained model as a service.                                                                                             | advanced     | `fastapi`, `serving`, `inference`, `deployment`                                    | `ml-engineering/model-checkpoint-manager`, `ml-engineering/metrics-computation-suite`                                                                                    |
| 11 | [`learning-rate-finder`](learning-rate-finder/SKILL.md)                     | Run an LR range test to pick a sensible initial learning rate before full training.                                                                                         | intermediate | `lr-finder`, `range-test`, `learning-rate`, `smith-2015`, `lightning-tuner`        | `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/hyperparameter-tuner`, `ml-engineering/early-stopping-configurator`                                         |
| 12 | [`metrics-computation-suite`](metrics-computation-suite/SKILL.md)           | Compute a comprehensive metrics suite (accuracy, precision, recall, F1, AUC, MCC, Cohen's kappa, ECE/MCE, confusion matrix) with 95% bootstrap CIs.                         | advanced     | `metrics`, `f1`, `auc`, `mcc`, `cohen-kappa`, `calibration`                        | `ml-engineering/statistical-validation-rigor`, `ml-engineering/ablation-study-runner`, `ml-engineering/baseline-model-zoo`                                               |
| 13 | [`mixed-precision-trainer`](mixed-precision-trainer/SKILL.md)               | Enable Automatic Mixed Precision (AMP) training when GPU memory is tight or throughput must improve.                                                                        | advanced     | `amp`, `autocast`, `gradscaler`, `fp16`, `bf16`                                    | `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/distributed-training-setup`, `ml-engineering/model-checkpoint-manager`                                      |
| 14 | [`model-checkpoint-manager`](model-checkpoint-manager/SKILL.md)             | Save and resume checkpoints with model, optimizer, scheduler, epoch, val metric, and RNG states.                                                                            | intermediate | `checkpoint`, `state-dict`, `resume`, `top-k`, `lightning`                         | `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/early-stopping-configurator`, `ml-engineering/reproducible-experiment-runner`                               |
| 15 | [`model-explainer`](model-explainer/SKILL.md)                               | Generate model explanations with SHAP, LIME, or Integrated Gradients when interpreting predictions, auditing feature importance, or satisfying explainability requirements. | advanced     | `shap`, `lime`, `integrated-gradients`, `captum`, `explainability`                 | `ml-engineering/inference-pipeline-builder`, `ml-engineering/metrics-computation-suite`, `ml-engineering/transformer-finetuner`                                          |
| 16 | [`modular-ml-architect`](modular-ml-architect/SKILL.md)                     | Enforce modular Python conventions across ML projects when scaffolding a new repository, refactoring a monolithic script, or auditing code structure.                       | intermediate | `modular`, `src-layout`, `refactoring`, `conventions`, `scaffolding`               | `style-integrity/coding-conventions-enforcer`, `ml-engineering/reproducible-experiment-runner`, `ml-engineering/dataset-adapter-builder`                                 |
| 17 | [`pytorch-lightning-scaffold`](pytorch-lightning-scaffold/SKILL.md)         | Scaffold PyTorch Lightning modules when starting a new training project, defining the LightningModule, LightningDataModule, callbacks, and loggers.                         | advanced     | `pytorch-lightning`, `lightningmodule`, `datamodule`, `callbacks`, `loggers`       | `ml-engineering/modular-ml-architect`, `ml-engineering/early-stopping-configurator`, `ml-engineering/model-checkpoint-manager`, `ml-engineering/mixed-precision-trainer` |
| 18 | [`reproducible-experiment-runner`](reproducible-experiment-runner/SKILL.md) | Set up fully reproducible ML experiments when starting training, configuring devices, seeds, logging, progress bars, and output folders.                                    | intermediate | `reproducibility`, `seeds`, `device`, `tqdm`, `experiment-folder`                  | `ml-engineering/seed-and-device-resolver`, `ml-engineering/experiment-folder-organizer`, `ml-engineering/modular-ml-architect`                                           |
| 19 | [`seed-and-device-resolver`](seed-and-device-resolver/SKILL.md)             | Resolve the torch device once and seed every RNG when starting a reproducible run.                                                                                          | intermediate | `seed`, `device`, `cuda`, `cudnn`, `determinism`                                   | `ml-engineering/reproducible-experiment-runner`, `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/modular-ml-architect`                                      |
| 20 | [`statistical-validation-rigor`](statistical-validation-rigor/SKILL.md)     | Apply rigorous statistical validation when reporting metrics, comparing models, or computing confidence intervals.                                                          | advanced     | `statistics`, `bootstrap-ci`, `mcnemar`, `wilcoxon`, `cohen-d`                     | `ml-engineering/metrics-computation-suite`, `ml-engineering/cross-validation-engine`, `ml-engineering/ablation-study-runner`                                             |
| 21 | [`train-val-test-splitter`](train-val-test-splitter/SKILL.md)               | Split data into train/validation/test with stratification at the highest hierarchical level when preparing data for training.                                               | intermediate | `train-val-test`, `split`, `stratified`, `groupshuffle`, `manifest`                | `ml-engineering/data-leakage-guard`, `ml-engineering/cross-validation-engine`, `ml-engineering/dataset-adapter-builder`                                                  |
| 22 | [`transformer-finetuner`](transformer-finetuner/SKILL.md)                   | Fine-tune Hugging Face transformers for text classification, token classification, or sequence-to-sequence tasks.                                                           | advanced     | `huggingface`, `transformers`, `finetuning`, `peft`                                | `ml-engineering/pytorch-lightning-scaffold`, `ml-engineering/model-explainer`, `ml-engineering/mixed-precision-trainer`                                                  |

## Difficulty Breakdown

Across **22** skills in this theme, the difficulty distribution is:

- **Beginner** — 1 skill(s)
- **Intermediate** — 9 skill(s)
- **Advanced** — 12 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`callbacks` (2), `device` (2), `stratified` (2), `ablation` (1), `adapter` (1), `amp` (1), `artifacts` (1), `auc` (1),
`autocast` (1), `baselines` (1), `bayesian` (1), `bf16` (1), `bootstrap-ci` (1), `calibration` (1), `captum` (1),
`checkpoint` (1), `cohen-d` (1), `cohen-kappa` (1), `comparison` (1), `component-removal` (1), `controlled` (1),
`conventions` (1), `cross-validation` (1), `cuda` (1), `cudnn` (1), `data-leakage` (1), `datamodule` (1), `dataset` (1),
`ddp` (1), `defensive-loading` (1), `deployment` (1), `determinism` (1), `distributed` (1), `early-stopping` (1),
`experiment` (1), `experiment-folder` (1), `experiments` (1), `explainability` (1), `f1` (1), `fastapi` (1),
`finetuning` (1), `fitting` (1), `folder` (1), `fp16` (1), `gradscaler` (1), `grouped` (1), `groupshuffle` (1),
`huggingface` (1), `hyperparameters` (1), `inference` (1), `integrated-gradients` (1), `kfold` (1), `layout` (1),
`learning-rate` (1), `lightning` (1), `lightning-tuner` (1), `lightningmodule` (1), `lime` (1), `loggers` (1),
`logistic-regression` (1), `lr-finder` (1), `manifest` (1), `mcc` (1), `mcnemar` (1), `metric-delta` (1), `metrics` (1),
`min-delta` (1), `modular` (1), `multi-gpu` (1), `nccl` (1), `numpy` (1), `optuna` (1), `pandas` (1), `partitioning`
(1), `patience` (1), `peft` (1), `preprocessing` (1), `pytorch-lightning` (1), `random-forest` (1), `range-test` (1),
`refactoring` (1), `reproducibility` (1), `resume` (1), `scaffolding` (1), `seed` (1), `seeds` (1), `serving` (1),
`shap` (1), `smith-2015` (1), `split` (1), `src-layout` (1), `state-dict` (1), `statistics` (1), `timeseries` (1),
`timestamps` (1), `top-k` (1), `torchrun` (1), `tqdm` (1), `train-test-isolation` (1), `train-val-test` (1),
`transformers` (1), `tuning` (1), `val-loss` (1), `wilcoxon` (1), `xgboost` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`train-val-test-splitter` → `data-leakage-guard` → `seed-and-device-resolver` → `experiment-folder-organizer`** —
  Split → isolate → seed → folder.
- **`pytorch-lightning-scaffold` → `mixed-precision-trainer` → `early-stopping-configurator` →
  `model-checkpoint-manager`** — Lightning → AMP → early stop → checkpoint.
- **`hyperparameter-tuner` → `early-stopping-configurator` → `model-checkpoint-manager` → `metrics-computation-suite` →
  `statistical-validation-rigor`** — Tune → stop → save → metrics → stats.
- **`transformer-finetuner` → `model-explainer` → `ablation-study-runner` → `cross-validation-engine`** — Train →
  explain → ablate → CV.

## Cross-Theme Connections

Skills in `ml-engineering/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../style-integrity/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../data-engineering/README.md`](data-engineering/README.md) — feature and dataset adapters feed the training loop.
- [`../visualization/README.md`](visualization/README.md) — training curves, confusion matrices, and attention maps plot
  experiments.
- [`../academic-research/README.md`](academic-research/README.md) — reproducible experiment runners back the methods
  section.
- [`../ai-output-judgement/README.md`](ai-output-judgement/README.md) — inference pipelines are audited for factuality
  and safety.

## Back to Master

← [Back to SkillStack README](../README.md)
