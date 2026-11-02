---
name: requirements-pinner
description: "Generate dependency files for a Python project — either an unversioned `Requirements.txt` for broad environment compatibility or a pinned `requirements.lock` for exact reproducibility. Use this when setting up a repo, freezing a tested environment, or preparing a release. Triggers: requirements.txt, requirements.lock, pip freeze, dependency pinning, lock file."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [requirements, dependencies, pip, reproducibility]
related: [project-tooling/environment-yaml-builder, project-tooling/pyproject-toml-builder, project-tooling/docker-research-container]
prerequisites: []
outputs: [bash, markdown]
difficulty: beginner
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Requirements Pinner

## When To Use

- You are bootstrapping a new repo and need a `Requirements.txt` for collaborators to install against.
- You want to freeze a known-good environment into `requirements.lock` so future runs reproduce exactly.
- You are preparing a release and must distinguish "broad install" from "exact repro" inputs.
- A CI matrix needs the unversioned list, while a Docker image build needs the locked list.

## Workflow

1. Inspect the codebase to collect every `import` used in `src/`, tests, notebooks, and scripts.
2. Map each top-level import to its canonical PyPI package name (e.g. `cv2` → `opencv-python`).
3. Decide the variant: unversioned `Requirements.txt` for compatibility, or `requirements.lock` for reproducibility.
4. If unversioned: write one package per line, sorted alphabetically, no `==` pins.
5. If pinned: run `pip freeze` inside the tested virtualenv and capture exact `==X.Y.Z` lines.
6. Add a header comment to the file explaining its purpose and how it was generated.
7. Cross-check that `torch`, `numpy`, `pandas`, `optuna`, `tqdm` (or whatever the repo actually uses) are present.
8. Commit `Requirements.txt` always; commit `requirements.lock` only at release tags.
9. Document the tradeoff in the README so users know which file to install.

## Inputs

- The repo's import surface (scan `src/`, `tests/`, `notebooks/`, `scripts/`).
- An activated virtualenv with the working environment (only needed for the pinned variant).
- An optional extra-specs list (e.g. `--index-url`, `--extra-index-url`).

## Outputs

- `Requirements.txt` — unversioned list, one package per line, alphabetical.
- `requirements.lock` — exact pinned list from `pip freeze` (only when requested).
- A short note in `README.md` describing which file to install for which use case.

## Key Rules

- Never mix variants in one file: unversioned OR pinned, never both.
- The unversioned file must NOT contain `==`, `>=`, `<=`, `~=`, or `@` markers.
- The pinned file must contain an exact `==X.Y.Z` on every line; no ranges.
- Always include transitive runtime deps in the pinned file (that is what `pip freeze` produces).
- Group comments with `#` at the top only; never inline `#` next to a package line in the locked file.
- Pin the Python version in `pyproject.toml` or `environment.yml`, NOT in the requirements files.
- If a package is GPU-specific (e.g. `torch` with CUDA), note the index URL in a comment above the line.

## Examples

Unversioned `Requirements.txt`:

```text
# Requirements.txt — broad install list. Generated for environment compatibility.
# Install with: pip install -r Requirements.txt

numpy
optuna
pandas
tqdm
torch
```

Pinned `requirements.lock` (generated, not hand-written):

```bash
# Freeze the active environment into the lock file.
pip freeze > requirements.lock
```

Helper to regenerate the unversioned list from imports:

```python
# ExtractTopLevelImports.py — scan src for third-party imports.
import ast
import os
import sys

StdlibModules = set(sys.stdlib_module_names)


def CollectImports(rootDir):
  found = set()
  for currentDir, _, fileNames in os.walk(rootDir):
    for fileName in fileNames:
      if (not fileName.endswith(".py")):
        continue
      filePath = os.path.join(currentDir, fileName)
      with open(filePath, "r", encoding="utf-8") as handle:
        tree = ast.parse(handle.read(), filePath)
      for node in ast.walk(tree):
        if (isinstance(node, ast.Import)):
          for alias in node.names:
            found.add(alias.name.split(".")[0])
        elif (isinstance(node, ast.ImportFrom)):
          if (node.module):
            found.add(node.module.split(".")[0])
  return sorted(name for name in found if (name not in StdlibModules))


if (__name__ == "__main__"):
  print("\n".join(CollectImports("src")))
```

## References

- `pip freeze` — https://pip.pypa.io/en/stable/cli/pip_freeze/
- `pip install -r` — https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-r
- pip-tools for compiling unversioned → pinned — https://pip-tools.readthedocs.io
