---
name: ablation-study-runner
description: Run ablation studies by systematically removing or altering components of a proposed model. Triggers on "ablation study", "remove component", "ablation table", "metric delta", "identical seeds", "component necessity".
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ml-engineering
tags: [ablation, experiments, component-removal, metric-delta, controlled]
related: [ml-engineering/reproducible-experiment-runner, ml-engineering/baseline-model-zoo, ml-engineering/cross-validation-engine]
prerequisites: [ml-engineering/reproducible-experiment-runner]
outputs: [python, csv, json]
difficulty: advanced
estimated_tokens: 960
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Ablation Study Runner

## When To Use
- Justifying the necessity of each component in a proposed model.
- Producing an ablation table for a paper.
- Comparing a full model against its component-stripped variants.
- Validating design choices with identical seeds and data.

## Workflow
1. Enumerate all components of the proposed model (loss term, regularizer, branch, attention head).
2. For each component, define an ablation variant that removes or neutralizes it.
3. Train every variant with IDENTICAL seeds, data splits, and budget.
4. Evaluate every variant on the SAME held-out test set.
5. Compute the metric delta against the full model.
6. Assemble an ablation table mapping `ComponentRemoved -> Metric -> Delta`.
7. Persist the table to `Aggregated/AblationTable.csv`.
8. Write a short justification for each component's necessity.

## Inputs
- The full model factory and a list of variant factories.
- The shared train/validation/test splits.
- `Configs/Config.yaml` with `Seed`, `Epochs`, `BatchSize`.

## Outputs
- `Aggregated/AblationTable.csv` with one row per ablation.
- `Aggregated/AblationReport.json` with deltas and justifications.

## Key Rules
- Every ablation must use IDENTICAL seeds and data splits.
- Every ablation must be evaluated on the SAME test set.
- Report the metric delta versus the full model.
- Justify the necessity of each component in the report.
- Use the same evaluation harness as the proposed model.

## Examples
```python
# Ablation runner producing a CSV and JSON report.
import json
import csv


def RunAblation(Variants, TrainFunction, EvalFunction, Splits, Config, OutputDir):
  """Run every ablation variant and persist deltas."""
  # Compute the full-model reference.
  fullModel = TrainFunction(Variants["Full"], Splits, Config)
  fullMetric = EvalFunction(fullModel, Splits["Test"])
  table = []
  for variantName, factory in Variants.items():
    # Skip the reference variant.
    if (variantName == "Full"):
      table.append({
        "ComponentRemoved": "none",
        "Metric": fullMetric,
        "Delta": 0.0
      })
      continue
    # Train this variant with identical config.
    variantModel = TrainFunction(factory, Splits, Config)
    variantMetric = EvalFunction(variantModel, Splits["Test"])
    # Compute delta versus the full model.
    delta = variantMetric - fullMetric
    table.append({
      "ComponentRemoved": variantName,
      "Metric": variantMetric,
      "Delta": delta
    })
  # Persist the ablation table.
  with open(OutputDir + "AblationTable.csv", "w", newline="") as f:
    writer = csv.DictWriter(
      f,
      fieldnames=["ComponentRemoved", "Metric", "Delta"]
    )
    writer.writeheader()
    writer.writerows(table)
  # Persist a JSON report with justifications.
  report = {
    "FullMetric": fullMetric,
    "Ablations": table
  }
  with open(OutputDir + "AblationReport.json", "w") as f:
    json.dump(report, f, indent=2)
  return report
```

## References
- sklearn metrics for evaluation: https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
- Research methodology on ablation studies: https://en.wikipedia.org/wiki/Ablation_(artificial_intelligence)
