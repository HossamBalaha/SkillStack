---
name: pyproject-toml-builder
description: "Build a `pyproject.toml` file with the `[project]` table, a `[build-system]` backend, and tool config sections (`[tool.ruff]`, `[tool.black]`, `[tool.mypy]`, `[tool.pytest.ini_options]`). Use this when scaffolding a new Python package or standardising tooling across an existing repo. Triggers: pyproject.toml, build-system, setuptools, poetry, hatch, ruff config, mypy config."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [pyproject, packaging, pep-621, build-system]
related: [project-tooling/requirements-pinner, project-tooling/environment-yaml-builder, project-tooling/pre-commit-hook-builder, project-tooling/license-selector]
prerequisites: []
outputs: [bash]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Pyproject Toml Builder

## When To Use
- You are creating a new Python package and need a single config file for build, metadata, and tooling.
- You want to consolidate `setup.py`, `setup.cfg`, `ruff.toml`, `mypy.ini`, and `pytest.ini` into one file.
- You are migrating a project from `setup.py` to a modern PEP 621 layout.
- You need optional-dependencies groups (dev / docs / test) for clean `pip install -e .[dev]`.

## Workflow
1. Ask the caller for: package name, version, one-line description, author(s), license, and Python range.
2. Pick a build backend: `setuptools` (default, widely compatible), `poetry-core` (if using Poetry), or `hatchling` (Hatch).
3. Write the `[project]` table with `name`, `version`, `description`, `authors`, `requires-python`, `dependencies`, `license`.
4. Add `[project.optional-dependencies]` groups: `dev`, `docs`, `test`.
5. Add `[build-system]` with the chosen `requires` and `build-backend`.
6. Add `[project.urls]` (homepage, repository, issues) if the caller has them.
7. Add `[tool.ruff]` (line length, target version, select rules), `[tool.black]` (line length), `[tool.mypy]` (strict + plugin), `[tool.pytest.ini_options]` (testpaths, addopts).
8. Validate with `python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`.
9. Commit and reference it from the README install instructions.

## Inputs
- Package name, version, description, author list, license SPDX id.
- Minimum Python version (e.g. `>=3.10`).
- Runtime dependencies (unversioned or loosely pinned).
- Choice of build backend.

## Outputs
- `pyproject.toml` at the repo root.
- Optional dev/docs/test extras that collaborators can install with `pip install -e .[dev]`.

## Key Rules
- Always include `requires-python`; never leave the Python range ambiguous.
- Use SPDX identifiers for the license (e.g. `MIT`, `Apache-2.0`, `GPL-3.0-or-later`).
- Keep `dependencies` minimal — only what the package imports at runtime; move dev tools to optional groups.
- Pin build backend explicitly so a clean checkout builds the same wheel every time.
- Tool sections must agree: ruff and black share the same `line-length`; mypy `python_version` matches `requires-python` lower bound.
- Never put secrets, tokens, or absolute paths in `pyproject.toml`.
- Run `tomllib.load` (Python 3.11+) or `tomli` on older versions to validate before committing.

## Examples
```toml
[project]
name = "researchkit"
version = "0.1.0"
description = "Reproducible research utilities for the lab."
authors = [{ name = "Lab Tooling", email = "tooling@example.org" }]
license = { text = "MIT" }
requires-python = ">=3.10"
dependencies = [
  "numpy",
  "pandas",
  "torch",
  "optuna",
  "tqdm",
]

[project.optional-dependencies]
dev = ["ruff", "black", "mypy", "pre-commit"]
docs = ["sphinx", "furo", "myst-parser"]
test = ["pytest", "pytest-cov", "pytest-xdist"]

[project.urls]
Homepage = "https://example.org/researchkit"
Repository = "https://github.com/example/researchkit"
Issues = "https://github.com/example/researchkit/issues"

[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --cov=src --cov-report=term-missing"
```

Validator:

```python
# ValidateToml.py — confirm the file parses cleanly.
import tomllib

with open("pyproject.toml", "rb") as handle:
  config = tomllib.load(handle)
print(config["project"]["name"])
```

## References
- PEP 621 — https://packaging.python.org/en/latest/specifications/declaring-project-metadata/
- Writing pyproject.toml — https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- Poetry pyproject — https://python-poetry.org/docs/pyproject/
- Hatch backends — https://hatch.pypa.io/latest/config/build/
