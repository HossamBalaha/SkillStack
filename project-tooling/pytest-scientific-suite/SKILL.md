---
name: pytest-scientific-suite
description: "Write pytest test suites for scientific and ML code with `conftest.py` fixtures, `@pytest.mark.parametrize` for edge cases (n=0, n=1, binary/multiclass, single-class), deterministic seeds, and coverage gating via `--cov-fail-under=80`. Use this when adding tests to data loaders, model forward passes, or metric computations. Triggers: pytest, conftest, parametrize, fixtures, coverage, scientific tests."
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: project-tooling
tags: [pytest, testing, fixtures, scientific]
related: [project-tooling/github-actions-research-ci, project-tooling/pre-commit-hook-builder, project-tooling/makefile-generator]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 2100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Pytest Scientific Suite

## When To Use
- You are adding tests to a research repo so refactors and seed changes are caught early.
- You need parametrized edge cases: empty input, single sample, binary vs multiclass labels, single-class batches.
- You want deterministic fixtures so flaky randomness never fails CI.
- You want a coverage gate (`--cov-fail-under=80`) so untested code blocks merges.

## Workflow
1. Create `tests/conftest.py` with shared fixtures: `tmpPath`, `sampleBatch`, `tinyDataset`, `deterministicSeed`.
2. Set the seed inside fixtures using `random.seed`, `numpy.random.seed`, and `torch.manual_seed`.
3. Add `tests/test_DataLoader.py`, `tests/test_Model.py`, `tests/test_Metrics.py` — one file per module.
4. Use `@pytest.mark.parametrize` with explicit `(input, expected)` tuples for edge cases.
5. For metrics, write tests with known inputs and known expected outputs (e.g. accuracy on a fixed batch).
6. For model forward passes, assert output shape, dtype, and finite values (`torch.isfinite`).
7. Add `pytest --cov=src --cov-report=html --cov-report=term-missing` to the CI test step.
8. Set `--cov-fail-under=80` in `pyproject.toml` `[tool.pytest.ini_options]` so coverage drops fail CI.
9. Run `pytest -n auto` with `pytest-xdist` to parallelise across cores.
10. Commit tests alongside the code they cover; never land code without its test.

## Inputs
- The package layout under `src/`.
- Sample data files (small CSV, NPZ, or synthetic tensors) — keep them tiny and committed under `tests/fixtures/`.
- The list of edge cases to parametrize.
- The coverage threshold (default 80%).

## Outputs
- `tests/conftest.py` with shared fixtures.
- One `tests/test_*.py` per public module.
- `htmlcov/` directory (gitignored) with the HTML coverage report.
- A coverage badge referenced in the README.

## Key Rules
- Every fixture that touches RNG must reset the seed at setup so tests are order-independent.
- Use `@pytest.mark.parametrize` with explicit cases: `n=0`, `n=1`, `binary`, `multiclass`, `single-class`.
- Never assert floating equality with `==`; use `pytest.approx(expected, rel=1e-5)`.
- Tests must run in under a few seconds total — use tiny synthetic batches, not full datasets.
- Coverage gating is mandatory: `--cov-fail-under=80` belongs in `pyproject.toml`, not just CI.
- Mark slow tests with `@pytest.mark.slow` and exclude them with `-m "not slow"` on quick runs.
- Test files mirror the module name: `src/DataLoader.py` → `tests/test_DataLoader.py`.

## Examples
`tests/conftest.py`:

```python
# tests/conftest.py — shared fixtures with deterministic seeds.
import random
import pytest
import numpy as np
import torch


@pytest.fixture(autouse=True)
def DeterministicSeed():
  # Reset every RNG before each test so order does not matter.
  random.seed(42)
  np.random.seed(42)
  torch.manual_seed(42)
  yield


@pytest.fixture
def TinyBatch():
  # A 4-sample batch with 3 features and binary labels.
  features = torch.tensor([[0.0, 0.1, 0.2], [1.0, 1.1, 1.2], [0.5, 0.5, 0.5], [0.9, 0.0, 0.1]])
  labels = torch.tensor([0, 1, 0, 1])
  return {"features": features, "labels": labels}
```

`tests/test_Metrics.py`:

```python
# tests/test_Metrics.py — parametrized metric tests.
import pytest
import torch
from src.Metrics import Accuracy


@pytest.mark.parametrize(
  "Predictions, Labels, Expected",
  [
    ([1, 0, 1, 0], [1, 0, 1, 0], 1.0),
    ([1, 1, 1, 1], [0, 0, 0, 0], 0.0),
    ([1, 0, 1, 0], [1, 1, 1, 0], 0.75),
    ([], [], 0.0),
    ([1], [1], 1.0),
  ],
)
def test_Accuracy(Predictions, Labels, Expected):
  # Edge cases: empty batch, single sample, perfect, all-wrong.
  pred = torch.tensor(Predictions)
  lab = torch.tensor(Labels)
  assert Accuracy(pred, lab) == pytest.approx(Expected, rel=1e-5)
```

`pyproject.toml` pytest config:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --cov=src --cov-report=term-missing --cov-fail-under=80"
markers = ["slow: marks tests as slow"]
```

## References
- pytest docs — https://docs.pytest.org
- `@pytest.mark.parametrize` — https://docs.pytest.org/en/stable/how-to/parametrize.html
- pytest-cov — https://pytest-cov.readthedocs.io
