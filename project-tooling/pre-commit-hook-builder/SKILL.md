---
name: pre-commit-hook-builder
description: "Build a `.pre-commit-config.yaml` wiring up `pre-commit/pre-commit-hooks` (trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files), `charliermarsh/ruff` (lint + format), `psf/black`, `pre-commit/mirrors-mypy`, and optionally `python-poetry/poetry`. Use this to enforce style and safety checks at commit time. Triggers: pre-commit, .pre-commit-config.yaml, ruff hook, black hook, mypy hook, trailing whitespace, large file guard."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [pre-commit, linting, hooks, automation]
related: [project-tooling/makefile-generator, project-tooling/github-actions-research-ci, project-tooling/pyproject-toml-builder]
prerequisites: []
outputs: [yaml]
difficulty: intermediate
estimated_tokens: 2100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Pre Commit Hook Builder

## When To Use

- You want style and safety checks to run automatically on every commit so bad code never lands.
- You want to block large files (datasets, binaries) from being committed by accident.
- You want ruff, black, and mypy to run locally before the CI pipeline does.
- You are onboarding contributors and want a one-command `pre-commit install` setup.

## Workflow

1. Create `.pre-commit-config.yaml` at the repo root.
2. Add `default_language_version: python: python3.11` (or the repo's minimum).
3. Add the `pre-commit/pre-commit-hooks` repo with `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`,
   `check-toml`, `check-added-large-files`, `check-merge-conflict`.
4. Add `charliermarsh/ruff-pre-commit` with `ruff` and `ruff-format` hooks.
5. Add `psf/black` with the `black` hook.
6. Add `pre-commit/mirrors-mypy` with the `mypy` hook and `additional_dependencies` for the project's type stubs.
7. Optionally add `python-poetry/poetry` if the repo uses Poetry.
8. Pin each hook's `rev` to a released tag; never use `main` or `master`.
9. Install locally with `pre-commit install` and run on all files with `pre-commit run --all-files`.
10. Add a `pre-commit` step to the CI workflow so the gate is enforced server-side too.

## Inputs

- The repo's Python version (for `default_language_version`).
- Whether the repo uses Poetry (to include the Poetry hook).
- A list of type-stub packages for mypy (e.g. `types-requests`, `pandas-stubs`).
- A max file size for `check-added-large-files` (default 500kb).

## Outputs

- `.pre-commit-config.yaml` at the repo root.
- A README section documenting `pre-commit install` and `pre-commit run --all-files`.
- A CI step that runs `pre-commit run --all-files` on every push.

## Key Rules

- Every hook `rev` is pinned to a released tag; updates are deliberate, never automatic.
- `check-added-large-files` must have a `args: [--maxkb=500]` so accidental dataset uploads are blocked.
- Mypy needs `additional_dependencies` listing the project's runtime deps so it can resolve imports.
- Run `pre-commit install` once per clone so the hooks fire on `git commit`.
- The CI workflow must run `pre-commit run --all-files` so server-side checks catch uncommitted hooks.
- Hooks must not depend on the network at commit time (cache them via `pre-commit autoupdate` periodically).
- Don't enable hooks that conflict: ruff-format and black both format; pick ruff-format and skip black unless the repo
  mandates black's exact output.

## Examples

`.pre-commit-config.yaml`:

```yaml
# .pre-commit-config.yaml — local quality gate for researchkit.
default_language_version:
  python: python3.11

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
        args: [--maxkb=500]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - pandas-stubs
          - numpy

  - repo: https://github.com/python-poetry/poetry
    rev: 1.8.3
    hooks:
      - id: poetry-check
      - id: poetry-lock
```

Install and run:

```bash
# Install hooks into the local git config.
pre-commit install

# Run every hook against every file once.
pre-commit run --all-files
```

CI step:

```yaml
# Snippet for .github/workflows/ci.yml.
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
- uses: actions/checkout@v4
- name: Run pre-commit
  run: |
    pip install pre-commit
    pre-commit run --all-files
```

## References

- pre-commit — https://pre-commit.com
- pre-commit-hooks — https://github.com/pre-commit/pre-commit-hooks
- ruff-pre-commit — https://github.com/astral-sh/ruff-pre-commit
- mirrors-mypy — https://github.com/pre-commit/mirrors-mypy
