---
name: experiment-folder-organizer
description: Create a single timestamped experiment folder with four split subfolders when starting a run, ensuring all artifacts land in the correct split. Triggers on "Results/DatasetName_Timestamp", "Train Validation Test Aggregated subfolders", "no per-file timestamps", "outputDirectory parameter", "execution.log".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [experiment, folder, timestamps, artifacts, layout]
related: [ml-engineering/reproducible-experiment-runner, ml-engineering/model-checkpoint-manager, ml-engineering/seed-and-device-resolver]
prerequisites: []
outputs: [python, bash]
difficulty: beginner
estimated_tokens: 870
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Experiment Folder Organizer

## When To Use
- Starting a new experiment run that needs a clean output folder.
- Organizing plots, JSON reports, CSVs, and logs by split.
- Refactoring plotting functions to accept an `outputDirectory` parameter.

## Workflow
1. Compose the folder name as `Results/{DatasetName}_{YYYYMMDD_HHMMSS}/`.
2. Create exactly four subfolders: `Train/`, `Validation/`, `Test/`, `Aggregated/`.
3. Write a persistent `Aggregated/execution.log` for the whole run.
4. Route every artifact to its split subfolder (no per-file timestamps).
5. Refactor plotting helpers to accept an `outputDirectory` argument.
6. Return the four subfolder paths to the caller.

## Inputs
- `DatasetName` string from `Configs/Config.yaml`.
- The current timestamp at startup.

## Outputs
- A single experiment root with four subfolders.
- `Aggregated/execution.log` for the whole run.
- Per-split artifacts without redundant timestamps in file names.

## Key Rules
- One timestamped folder per experiment; do NOT timestamp individual files.
- Exactly four subfolders: `Train/`, `Validation/`, `Test/`, `Aggregated/`.
- All artifacts land in their respective split subfolder.
- Plotting functions MUST accept an `outputDirectory` parameter.
- The persistent log lives at `Aggregated/execution.log`.

## Examples
```python
# Create the canonical experiment folder layout.
import os
from datetime import datetime


def BuildExperimentFolders(DatasetName, Root="Results"):
  """Create Results/{DatasetName}_{Timestamp}/ with four subfolders."""
  # Compose the timestamp once at startup.
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  experimentRoot = os.path.join(Root, f"{DatasetName}_{timestamp}")
  # Define the four canonical subfolders.
  subfolders = {
    "Train": os.path.join(experimentRoot, "Train"),
    "Validation": os.path.join(experimentRoot, "Validation"),
    "Test": os.path.join(experimentRoot, "Test"),
    "Aggregated": os.path.join(experimentRoot, "Aggregated")
  }
  # Create each subfolder.
  for path in subfolders.values():
    os.makedirs(path, exist_ok=True)
  return subfolders


def SavePlot(Figure, FileName, OutputDirectory):
  """Save a matplotlib figure into the given output directory."""
  # Refactored to accept outputDirectory parameter.
  fullPath = os.path.join(OutputDirectory, FileName)
  # No timestamp in the file name.
  Figure.savefig(fullPath, bbox_inches="tight")
  return fullPath


def SaveMetrics(Metrics, FileName, OutputDirectory):
  """Save a metrics dict as JSON into the split subfolder."""
  import json
  # Build the full path inside the split folder.
  fullPath = os.path.join(OutputDirectory, FileName)
  with open(fullPath, "w") as f:
    json.dump(Metrics, f, indent=2)
  return fullPath
```

## References
- Python os.makedirs: https://docs.python.org/3/library/os.html#os.makedirs
- datetime strftime: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
