---
name: research-repo-builder
description: Scaffold a complete modular research repository from an approved plan, including src/data, src/models, src/utils, Configs/Config.yaml, manual/ chapters, Datasets.md, unversioned Requirements.txt, CreateProjectZip.py, and Main.py entry point. Use when the user asks to scaffold, bootstrap, or generate a research codebase skeleton.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [scaffolding, repository, project-structure]
related: [style-integrity/coding-conventions-enforcer, ml-engineering/modular-ml-architect, academic-research/reproducibility-checklist-author]
prerequisites: []
outputs: [python, markdown, bash]
difficulty: intermediate
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Research Repo Builder

## When To Use
- The user says "scaffold a research repo", "create a project skeleton", or "set up my codebase".
- The user has an approved plan and wants the directory tree materialized.
- The user wants reproducible structure: configs, manuals, scripts, datasets manifest.
- Trigger keywords: scaffold, bootstrap, repository tree, project structure, CreateProjectZip, Main.py.

## Workflow
1. Read the approved plan (executive summary, code menu, repo tree) from the ideation step or user input.
2. Create the root project directory named after the project slug.
3. Build the directory tree below. Place a `.gitkeep` in every directory that would otherwise be empty.
4. Write `Configs/Config.yaml` with sections for `data`, `model`, `training`, `evaluation`, `paths`, `random_seed`.
5. Stub `Main.py` as the orchestrator: parse config, build data loader, instantiate model, train loop, eval loop, save artifacts.
6. Stub `src/data/loader.py`, `src/data/preprocess.py`, `src/models/baseline.py`, `src/models/proposed.py`, `src/utils/metrics.py`, `src/utils/logger.py`.
7. Write `Datasets.md` documenting source, license, splits, preprocessing, and citation requirements.
8. Write `Requirements.txt` (unversioned by default; pin only when user requests).
9. Add `CreateProjectZip.py` that zips the repo, excluding `data/raw`, `outputs`, `.git`.
10. Add `.gitignore` covering `__pycache__/`, `*.pyc`, `data/raw/`, `outputs/`, `.venv/`, `.env`.
11. Add `README.md` with quickstart, install, train, eval commands, and citation block.
12. Print the resulting tree and confirm every directory has either content or a `.gitkeep`.

## Inputs
- Project slug (kebab-case).
- Approved plan with module menu and config schema.
- Optional: framework choice (PyTorch, JAX, TensorFlow).
- Optional: list of datasets to register in `Datasets.md`.

## Outputs
- A materialized directory tree under the project slug.
- `Configs/Config.yaml`, `Main.py`, `Requirements.txt`, `Datasets.md`, `README.md`, `CreateProjectZip.py`, `.gitignore`.
- `.gitkeep` in every empty directory.
- A printed tree diagram for verification.

## Key Rules
- Every directory must contain either real content or a `.gitkeep`; never leave an empty dir.
- `Requirements.txt` is unversioned unless the user explicitly asks for pinning.
- Config values must be referenced, not hardcoded, inside `Main.py` and modules.
- `Datasets.md` must include license and citation requirements for every dataset.
- `CreateProjectZip.py` must exclude raw data, outputs, and `.git` to keep archives small and shareable.
- Do not commit secrets; `.env` must be in `.gitignore`.

## Examples
```text
Project tree generated:
my-project/
├── Configs/
│   ├── Config.yaml
│   └── .gitkeep
├── Datasets.md
├── Main.py
├── Requirements.txt
├── CreateProjectZip.py
├── .gitignore
├── README.md
├── manual/
│   ├── chapters/
│   ├── images/
│   ├── scripts/
│   └── .gitkeep
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   ├── preprocess.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── baseline.py
│   │   ├── proposed.py
│   │   └── __init__.py
│   └── utils/
│       ├── metrics.py
│       ├── logger.py
│       └── __init__.py
```
```yaml
# Configs/Config.yaml (excerpt)
random_seed: 42
data:
  dataset_name: mri-multisite
  split: [0.7, 0.15, 0.15]
model:
  name: fedtopo
  hidden_dim: 256
training:
  epochs: 100
  batch_size: 16
  lr: 0.0001
```

## References
- Cookiecutter Data Science template: https://drivendata.github.io/cookiecutter-data-science/
- PyTorch Lightning project structure guide: https://lightning.ai/docs/pytorch/latest/starter/starter-guide.html
- Reproducible research repo checklist ( Nature Scientific Data ): https://www.nature.com/sdata/publish/author-guidelines
