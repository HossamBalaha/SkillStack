---
name: dataset-card-generator
description: Generate dataset cards in the model-card style documenting provenance, license, composition, intended use, out-of-scope use, limitations, and ethical considerations. Use this skill when publishing a dataset, requesting review, or onboarding downstream users to a new training corpus.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: data-engineering
tags: [dataset-card, documentation, ethics, provenance, model-card]
related: [data-engineering/data-lineage-tracker, data-engineering/data-quality-validator]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Dataset Card Generator

## When To Use
- A dataset is being released internally or to the public and needs documentation.
- Reviewers must understand provenance, license, and composition before approving use.
- Downstream model owners need to assess bias and out-of-scope use.
- Compliance (GDPR, HIPAA, copyright) requires explicit intended-use statements.
- A new version of the dataset ships and the card must be regenerated.

## Workflow
1. Collect provenance facts: who collected, when, where, and via which method.
2. Capture the license and any third-party data usage restrictions.
3. Profile composition: row count, columns, classes, demographic coverage, splits.
4. Describe intended use and out-of-scope use in plain language.
5. Surface known limitations: missing populations, collection bias, label noise.
6. Add ethical considerations: PII presence, sensitive attributes, vulnerable groups.
7. Compute maintenance metadata: version, owner contact, update cadence.
8. Render the card as Markdown plus a machine-readable YAML sidecar.
9. Pair the card with the dataset in storage and link from the catalog entry.

## Inputs
- Dataset location (file path, warehouse table, or HuggingFace repo id).
- Provenance notes (collector, date, method, consent basis).
- License file or SPDX identifier.
- Optional profiling summary (class counts, demographic stats).

## Outputs
- A `DATASET_CARD.md` describing the dataset for humans.
- A `dataset_card.yaml` sidecar describing the dataset for machines.
- An entry in the data catalog pointing at the card and the dataset.

## Key Rules
- Every card declares an explicit intended use and an explicit out-of-scope use.
- Provenance includes the collection method and consent basis; "unknown" is rejected.
- Sensitive attributes (demographics, PII) are called out, never buried.
- License is a SPDX identifier when one exists, otherwise a verbatim copy.
- Cards are versioned alongside the dataset; bumping the version re-renders the card.
- Maintenance metadata includes owner contact and update cadence.

## Examples

```python
import yaml


class DatasetCard:
  # Container that holds every field the card template expects.
  def __init__(self, name, version):
    self.Name = name
    self.Version = version
    self.Provenance = {}
    self.Composition = {}
    self.IntendedUse = ""
    self.OutOfScopeUse = ""
    self.Limitations = []
    self.EthicalConsiderations = []


def BuildCard(datasetMeta, profileSummary):
  # Assemble a card from human notes plus machine profile.
  card = DatasetCard(datasetMeta["Name"], datasetMeta["Version"])
  card.Provenance = {
    "Collector": datasetMeta["Collector"],
    "CollectedAt": datasetMeta["CollectedAt"],
    "Method": datasetMeta["CollectionMethod"],
    "ConsentBasis": datasetMeta["ConsentBasis"],
  }
  card.Composition = {
    "RowCount": profileSummary["RowCount"],
    "Classes": profileSummary["ClassCounts"],
    "DemographicCoverage": profileSummary["Demographics"],
  }
  card.IntendedUse = datasetMeta["IntendedUse"]
  card.OutOfScopeUse = datasetMeta["OutOfScopeUse"]
  card.Limitations = datasetMeta["Limitations"]
  card.EthicalConsiderations = datasetMeta["EthicalConsiderations"]
  return card


def RenderCard(card, outputPath):
  # Write a human Markdown card plus a machine YAML sidecar.
  markdown = f"# {card.Name} (v{card.Version})\n\n"
  markdown += f"## Provenance\n{yaml.safe_dump(card.Provenance)}"
  markdown += f"## Composition\n{yaml.safe_dump(card.Composition)}\n"
  markdown += f"## Intended Use\n{card.IntendedUse}\n"
  markdown += f"## Out-of-Scope Use\n{card.OutOfScopeUse}\n"
  with open(outputPath, "w", encoding="utf-8") as handle:
    handle.write(markdown)
  return {"Path": outputPath, "Version": card.Version}
```

## References
- Model Cards paper (Mitchell et al. 2019): https://arxiv.org/abs/1810.03977
- HuggingFace Dataset Cards: https://huggingface.co/docs/datasets/dataset-card
- Dataset Nutrition Label: https://datasetnutritionlabel.com
