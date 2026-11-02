---
name: model-explainer
description: Generate model explanations with SHAP, LIME, or Integrated Gradients when interpreting predictions, auditing feature importance, or satisfying explainability requirements. Triggers on "SHAP", "TreeExplainer", "DeepExplainer", "KernelExplainer", "Integrated Gradients", "Captum", "beeswarm plot", "feature ranking".
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ml-engineering
tags: [shap, lime, integrated-gradients, captum, explainability]
related: [ml-engineering/inference-pipeline-builder, ml-engineering/metrics-computation-suite, ml-engineering/transformer-finetuner]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python, svg, html]
difficulty: advanced
estimated_tokens: 1000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Model Explainer

## When To Use
- Interpreting a tree model with `TreeExplainer`.
- Explaining a PyTorch neural network with `DeepExplainer` or Captum.
- Generating a kernel-based explanation for an arbitrary black-box model.
- Producing beeswarm, dependence, waterfall, or decision plots.
- Auditing which features drive a model's predictions.

## Workflow
1. Identify the model family (tree, deep, kernel) and pick the matching explainer.
2. Prepare a background dataset (sample of training data) for kernel/deep explainers.
3. Compute SHAP values on a held-out evaluation set.
4. Cluster correlated features before reporting importance.
5. Render the beeswarm summary plot for global importance.
6. Render the dependence plot for the top feature.
7. Render the waterfall plot for a single prediction of interest.
8. Render the decision plot for cumulative risk view.
9. Persist mean-absolute-SHAP ranking as a CSV.

## Inputs
- Trained model object.
- Background dataset (training sample).
- Evaluation dataset (held-out).
- Feature names list.

## Outputs
- `Aggregated/ShapBeeswarm.png` global summary.
- `Aggregated/ShapDependence.png` top-feature dependence.
- `Aggregated/ShapWaterfall.png` single-prediction explanation.
- `Aggregated/ShapDecision.png` cumulative decision view.
- `Aggregated/FeatureRanking.csv` mean-absolute-SHAP table.

## Key Rules
- `TreeExplainer` for tree models, `DeepExplainer` for PyTorch, `KernelExplainer` for general black-box.
- SHAP reflects model behavior, NOT causality.
- Cluster correlated features to avoid double-counting importance.
- Always pass a representative background dataset to kernel/deep explainers.
- Disable gradients when computing DeepExplainer values on eval mode.

## Examples
```python
# SHAP for a tree model, with a beeswarm plot and ranking CSV.
import shap
import matplotlib.pyplot as plt
import pandas as pd


def ExplainTreeModel(Model, Background, Evaluation, FeatureNames, OutputDir):
  """Explain a tree model and persist plots + ranking."""
  # Use the tree-specific explainer.
  explainer = shap.TreeExplainer(Model)
  # Compute SHAP values on the evaluation set.
  shapValues = explainer.shap_values(Evaluation)
  # Beeswarm summary plot.
  plt.figure()
  shap.summary_plot(shapValues, Evaluation, feature_names=FeatureNames, show=False)
  plt.savefig(OutputDir + "ShapBeeswarm.png", bbox_inches="tight")
  plt.close()
  # Dependence plot for the top feature.
  meanAbs = pd.DataFrame(shapValues, columns=FeatureNames).abs().mean()
  topFeature = meanAbs.idxmax()
  plt.figure()
  shap.dependence_plot(
    topFeature,
    shapValues,
    Evaluation,
    feature_names=FeatureNames,
    show=False
  )
  plt.savefig(OutputDir + "ShapDependence.png", bbox_inches="tight")
  plt.close()
  # Persist the ranking CSV.
  ranking = meanAbs.sort_values(ascending=False)
  ranking.to_csv(OutputDir + "FeatureRanking.csv", header=["MeanAbsShap"])
  return ranking


def ExplainPyTorchModel(Model, Background, Evaluation, OutputDir):
  """Explain a PyTorch model using DeepExplainer."""
  # Wrap with DeepExplainer using a background sample.
  explainer = shap.DeepExplainer(Model, Background)
  # Compute SHAP values on the evaluation set.
  shapValues = explainer.shap_values(Evaluation)
  return shapValues
```

## References
- SHAP documentation: https://shap.readthedocs.io
- Captum (Integrated Gradients): https://captum.ai
- LIME: https://github.com/marcotcr/lime
