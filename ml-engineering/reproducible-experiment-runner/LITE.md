---
name: reproducible-experiment-runner-lite
description: Set up fully reproducible ML experiments when starting training, configuring devices, seeds, logging, progress bars, and output folders. Triggers on "reproducible training", "experiment folder", "device setup", "tqdm progress", "Results/DatasetName_Timestamp layout".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering

lite: true
full_version: reproducible-experiment-runner/SKILL.md
language: en
---

# Reproducible Experiment Runner (Lite)

> Condensed version. Load `reproducible-experiment-runner/SKILL.md` for the full workflow.

Sets up reproducible ML training: deterministic seeding, single-resolved device, dual logging, `tqdm` bars, and a
timestamped experiment folder with four split subfolders.

## Top 3 Workflow Steps

1. Read `Configs/Config.yaml` for seed, dataset name, and logging level; resolve
   `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` EXACTLY ONCE; seed `random`, `numpy`,
   `torch`, and CUDA deterministically.
2. Create `Results/{DatasetName}_{YYYYMMDD_HHMMSS}/` with subfolders `Train/`, `Validation/`, `Test/`, `Aggregated/`;
   configure dual logging (console INFO + file DEBUG at `Aggregated/execution.log`).
3. Wrap epoch, batch, and trial loops in `tqdm` bars; move the primary model AND every standalone `nn.Module` (loss,
   regularizer, calibrator) to `device` explicitly; save artifacts into the correct split subfolder WITHOUT per-file
   timestamps; write `Aggregated/Summary.json` at the end.

## Top 3 Key Rules

1. **`device` resolved ONCE and reused everywhere** — `model.to(device)` does NOT move sibling modules; call
   `.to(device)` on every standalone `nn.Module` (loss, regularizer, calibrator, auxiliary branch).
2. **One timestamped folder per experiment**; do NOT timestamp individual files; save each artifact into the correct
   split subfolder (`Train/`, `Validation/`, `Test/`, `Aggregated/`).
3. **Dual logging simultaneously** (console INFO + file DEBUG at `Aggregated/execution.log`); **`tqdm` bars on epochs,
   batches, AND trials**; only the four subfolders `Train/`, `Validation/`, `Test/`, `Aggregated/` are permitted.
