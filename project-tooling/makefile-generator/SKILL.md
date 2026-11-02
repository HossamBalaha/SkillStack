---
name: makefile-generator
description: "Generate a `Makefile` with targets `install`, `test`, `lint`, `format`, `typecheck`, `docs`, `run`, `clean`, and `zip`, all marked `.PHONY`. Use this when standardising the developer entrypoint so every contributor runs the same commands. Triggers: Makefile, make install, make test, make lint, make docs, make zip, .PHONY targets."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [makefile, automation, build, developer-entrypoint]
related: [project-tooling/pytest-scientific-suite, project-tooling/pre-commit-hook-builder, project-tooling/github-actions-research-ci]
prerequisites: []
outputs: [bash]
difficulty: intermediate
estimated_tokens: 2100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Makefile Generator

## When To Use

- You want a single `make <target>` entrypoint so contributors don't have to memorise tool-specific commands.
- You are standardising across a team: everyone runs `make install`, `make test`, `make lint`.
- You want the `zip` target to invoke `python CreateProjectZip.py` so the archive is one command away.
- You want `make clean` to wipe every generated artifact (`__pycache__/`, `.pytest_cache/`, `dist/`, `build/`).

## Workflow

1. Detect the tools the repo uses by scanning for `pyproject.toml`, `ruff.toml`, `pytest.ini`, `docs/conf.py`.
2. Emit a `Makefile` with a `.PHONY` line listing every target.
3. Add `install`: `pip install -e ".[dev,test]"`.
4. Add `test`: `pytest --cov=src --cov-report=term-missing --cov-fail-under=80`.
5. Add `lint`: `ruff check .`.
6. Add `format`: `ruff format . && black .`.
7. Add `typecheck`: `mypy src/`.
8. Add `docs`: `sphinx-build -b html docs docs/_build/html`.
9. Add `run`: `python Main.py`.
10. Add `clean`: `rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache dist build htmlcov *.egg-info`.
11. Add `zip`: `python CreateProjectZip.py`.
12. Use tab indentation for recipe lines (Make requires tabs, not spaces).
13. Document each target in a comment header.

## Inputs

- The repo's tooling (ruff, black, mypy, pytest, sphinx).
- The package install command (`pip install -e ".[dev,test]"` by default).
- The entrypoint script (`Main.py` by default).

## Outputs

- `Makefile` at the repo root.
- A README section documenting the common targets.

## Key Rules

- Every target is listed under `.PHONY` so Make never treats a same-named file as up-to-date.
- Recipe lines start with a TAB character, never spaces; this is non-negotiable in Make.
- Targets are idempotent — running `make test` twice gives the same result.
- `make clean` must remove every artifact listed in `.gitignore` (caches, build dirs, coverage).
- `make zip` invokes the `CreateProjectZip.py` script, not a raw `zip` command, so the denylist is honoured.
- Default target (first in the file) is `install` so bare `make` does the sensible thing.
- Keep commands short; chain with `&&` so a failure stops the recipe.

## Examples

```makefile
# Makefile — standard developer entrypoints for researchkit.

.PHONY: install test lint format typecheck docs run clean zip help

help:
        @echo "Targets: install test lint format typecheck docs run clean zip"

install:
        pip install -e ".[dev,test]"

test:
        pytest --cov=src --cov-report=term-missing --cov-fail-under=80

lint:
        ruff check .

format:
        ruff format .
        black .

typecheck:
        mypy src/

docs:
        sphinx-build -b html docs docs/_build/html

run:
        python Main.py

clean:
        rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
        rm -rf dist build htmlcov *.egg-info
        rm -rf docs/_build

zip:
        python CreateProjectZip.py
```

Run it:

```bash
# One-shot: install deps, run tests, build the archive.
make install test zip
```

Note on tabs vs spaces:

```python
# VerifyMakefile.py — fail if any recipe line uses spaces instead of tabs.
def CheckTabs(path):
  # Each recipe line must start with a literal tab.
  with open(path, "r", encoding="utf-8") as handle:
    for lineNum, line in enumerate(handle, 1):
      if (line.startswith("    ") and not line.startswith("\t")):
        raise SystemExit(f"line {lineNum} uses spaces instead of a tab")
  print("ok")


if (__name__ == "__main__"):
  CheckTabs("Makefile")
```

## References

- GNU Make manual — https://www.gnu.org/software/make/manual/
- `.PHONY` targets — https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html
