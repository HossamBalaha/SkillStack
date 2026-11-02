---
name: environment-yaml-builder
description: "Build an `environment.yml` (conda) with channels (`conda-forge`, `defaults`) and dependencies including a `- pip:` block plus `-r requirements.txt`, or a `Pipfile` for pipenv, or a `pixi.toml` for pixi. Use this when pinning a reproducible environment across machines. Triggers: environment.yml, conda env, conda-forge, pip block, Pipfile, pixi.toml, reproducible env."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [conda, environment, pip, reproducibility]
related: [project-tooling/requirements-pinner, project-tooling/docker-research-container, project-tooling/pyproject-toml-builder]
prerequisites: []
outputs: [yaml, bash]
difficulty: intermediate
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Environment Yaml Builder

## When To Use
- You need a reproducible environment that mixes conda packages (CUDA, GDAL) with pip packages.
- Collaborators are on different OSes and a single `environment.yml` should work everywhere.
- You want to lock the environment by hash (pixi lockfile) for byte-exact reproducibility.
- You are migrating from raw `requirements.txt` to a richer dependency spec.

## Workflow
1. Ask the caller which manager they use: conda, pipenv, or pixi.
2. For conda: emit `environment.yml` with `channels: [conda-forge, defaults]`.
3. List the Python version pin (`python=3.11`) and conda-installable deps first (numpy, pandas, pytorch from conda-forge).
4. Add a `- pip:` block listing pip-only packages, or `- -r requirements.txt` to reuse the existing list.
5. For pipenv: emit a `Pipfile` with `[[source]]`, `[packages]`, `[dev-packages]`, and `[requires]` sections.
6. For pixi: emit `pixi.toml` with `[project]`, `[dependencies]`, `[feature.*]`, then run `pixi install` to produce the lockfile.
7. Validate the file with the manager's parser (`conda env create --dry-run`, `pipenv lock`, `pixi install`).
8. Document the recreate command in the README.

## Inputs
- The dependency manager (conda / pipenv / pixi).
- The Python version pin.
- The list of conda-installable packages (preferred over pip when available on conda-forge).
- The list of pip-only packages and/or an existing `Requirements.txt`.

## Outputs
- `environment.yml` (conda), `Pipfile` + `Pipfile.lock` (pipenv), or `pixi.toml` + `pixi.lock` (pixi).
- A README note with the recreate command.

## Key Rules
- Conda channels order matters; `conda-forge` should come before `defaults` to avoid pulling stale packages.
- Always pin the Python version in the env file (`python=3.11`), not just in `pyproject.toml`.
- Pip-only packages go in the `- pip:` block; never mix pip package names into the conda dependency list.
- For reproducibility, prefer pixi's lockfile or `conda-lock` over a bare `environment.yml`.
- The `name:` field in `environment.yml` becomes the conda env name; keep it lowercase and unique.
- Re-run the lockfile whenever a dependency changes; never commit a stale lock.
- Document CUDA / GPU packages in a comment so the env can be rebuilt on a CPU-only host.

## Examples
`environment.yml` (conda):

```yaml
# environment.yml — reproducible conda env for researchkit.
name: researchkit
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy
  - pandas
  - pytorch
  - pytorch-cuda=12.1
  - tqdm
  - pip
  - pip:
      - optuna
      - -r requirements.txt
```

`Pipfile` (pipenv):

```toml
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[packages]
numpy = "*"
pandas = "*"
tqdm = "*"

[dev-packages]
ruff = "*"
black = "*"
mypy = "*"
pytest = "*"
pytest-cov = "*"

[requires]
python_version = "3.11"
```

`pixi.toml` (pixi):

```toml
[project]
name = "researchkit"
version = "0.1.0"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-64", "win-64"]

[dependencies]
python = "3.11.*"
numpy = "*"
pandas = "*"
pytorch = "*"
tqdm = "*"

[pypi-dependencies]
optuna = "*"

[feature.dev.dependencies]
ruff = "*"
black = "*"
mypy = "*"
pytest = "*"
pytest-cov = "*"

[environments]
dev = ["dev"]
```

Recreate commands:

```bash
# Conda.
conda env create -f environment.yml
conda activate researchkit

# pipenv.
pipenv install --dev

# pixi (produces pixi.lock).
pixi install
```

## References
- Conda environment.yml — https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- pipenv Pipfile — https://pipenv.pypa.io/en/latest/pipfile.html
- pixi — https://pixi.sh/latest/
- conda-lock — https://conda.github.io/conda-lock/
