---
name: github-actions-research-ci
description: "Build GitHub Actions workflows in `.github/workflows/ci.yml` with jobs for install, lint, test, docs, and optional Docker push to GHCR. Use this when wiring up continuous integration for a research or ML repo so every push runs the full quality gate. Triggers: GitHub Actions, CI workflow, setup-python, pytest cov, ruff, GHCR push, matrix build."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [github-actions, ci-cd, automation]
related: [project-tooling/pytest-scientific-suite, project-tooling/pre-commit-hook-builder]
prerequisites: []
outputs: [yaml]
difficulty: intermediate
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# GitHub Actions Research CI

## When To Use

- You want every push and pull request to run install, lint, tests, and docs build automatically.
- You need to test against multiple Python versions (3.10 / 3.11 / 3.12) in a matrix.
- You want failed tests to block merges via a required status check.
- You want to publish a Docker image to the GitHub Container Registry on every release tag.

## Workflow

1. Create `.github/workflows/ci.yml` at the repo root.
2. Define `on: push` and `on: pull_request` triggers for `main` and `develop` branches.
3. Add an `install` job using `actions/setup-python@v5` with a `matrix.python-version` of `["3.10","3.11","3.12"]`.
4. Cache pip downloads with `actions/cache@v4` keyed on the OS, Python version, and `Requirements.txt` hash.
5. Install deps from `Requirements.txt` plus `dev`/`test` extras.
6. Add a `lint` job that runs `ruff check .` and `black --check .`.
7. Add a `test` job that runs `pytest --cov=src --cov-report=xml` and uploads coverage to `codecov/codecov-action`.
8. Add a `docs` job that builds Sphinx or MkDocs and deploys on `main` pushes.
9. Add an optional `docker` job that builds and pushes the image to `ghcr.io/<owner>/<repo>` on tag pushes.
10. Gate `docker` and `docs` behind `if:` conditions so they only run on tags or `main`.
11. Verify by pushing a small commit and watching the Actions tab.

## Inputs

- Python versions to test (default `3.10`, `3.11`, `3.12`).
- The OS matrix (default `ubuntu-latest`).
- Whether to enable the Docker push job (requires `packages: write` permission).
- Coverage threshold (default `--cov-fail-under=80`).

## Outputs

- `.github/workflows/ci.yml` — the main CI pipeline.
- Optional `.github/workflows/docs.yml` if docs are split out.
- Badges in the README pointing at the CI status.

## Key Rules

- Always pin `actions/setup-python@v5` (or the latest major) to avoid silent breaking changes.
- Cache pip by `hashFiles('Requirements.txt')` so a dep change busts the cache cleanly.
- Use `fail-fast: false` on the matrix so one Python version failing doesn't cancel the others.
- The `test` job must run with `--cov-fail-under=80` so coverage regressions fail CI.
- The Docker push job needs `permissions: packages: write` and must only run on tags or `main`.
- Never embed secrets directly in the YAML; reference `${{ secrets.X }}`.
- Keep job names lowercase-kebab-case and step names descriptive.

## Examples

```yaml
# .github/workflows/ci.yml — research CI pipeline.
name: ci

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  install-and-test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('Requirements.txt') }}
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r Requirements.txt
          pip install ruff black mypy pytest pytest-cov
      - name: Lint
        run: |
          ruff check .
          black --check .
      - name: Type check
        run: mypy src/
      - name: Test
        run: pytest --cov=src --cov-report=xml --cov-fail-under=80
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  docker:
    needs: install-and-test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/checkout@v4
      - name: Log in to GHCR
        run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
      - name: Build and push
        run: |
          docker build -t ghcr.io/${{ github.repository }}:${{ github.ref_name }} .
          docker push ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

Badge for the README:

```markdown
![ci](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)
```
