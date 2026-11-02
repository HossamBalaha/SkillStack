---
name: gitignore-builder
description: "Generate a `.gitignore` tailored to the project's stack: Python (`__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.egg-info/`, `.venv/`, `dist/`, `build/`), Node (`node_modules/`), R (`.Rhistory`, `.RData`), large data (`Datasets/`, `*.csv` if large, `*.parquet`), IDE (`.vscode/`, `.idea/`), and OS (`.DS_Store`, `Thumbs.db`). Use this when bootstrapping a repo or auditing an existing `.gitignore`. Triggers: gitignore, ignore file, node_modules, __pycache__, Datasets ignore, IDE files."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [gitignore, vcs, scaffolding, ignore-rules]
related: [project-tooling/license-selector, project-tooling/pyproject-toml-builder, project-tooling/contribution-guide-builder]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Gitignore Builder

## When To Use

- You are scaffolding a new repo and need a `.gitignore` that matches the stack from day one.
- An existing repo is committing junk (`__pycache__/`, `.DS_Store`, `Datasets/`) and you want to stop the bleed.
- You are combining multiple stacks (Python backend + Node frontend + R notebooks) in one repo.
- You want a single curated file instead of stitching together GitHub's templates by hand.

## Workflow

1. Detect the stack(s) by scanning for `pyproject.toml`, `package.json`, `DESCRIPTION`, `*.Rproj`, `renv.lock`.
2. Pick the matching section templates: Python, Node, R, Data, IDE, OS, plus the project-tooling specifics.
3. Compose the `.gitignore` in this fixed order: Python → Node → R → Data → IDE → OS → Local.
4. For the Data section, decide per-file: ignore large `Datasets/` wholesale but keep small fixtures under
   `tests/fixtures/`.
5. Add the project-specific artifacts: `ProjectArchive.zip`, `*.zip`, `results/`, `htmlcov/`, `.mypy_cache/`,
   `.ruff_cache/`.
6. Append a "Local overrides" comment block at the end so individuals can append personal ignores.
7. Verify with `git status --ignored` that intended paths show as ignored.
8. Commit the `.gitignore` and document the per-stack reasoning in a code comment header.

## Inputs

- The repo root (for stack detection).
- A list of large-data paths that should be ignored wholesale.
- A list of small fixture paths that must NOT be ignored.

## Outputs

- `.gitignore` at the repo root.
- A short note in the README about which directories are intentionally not tracked.

## Key Rules

- One file per concern; group with a `# ---` header so the file reads top to bottom.
- `Datasets/` is ignored by default; small committed fixtures go under `tests/fixtures/` and must be un-ignored with
  `!tests/fixtures/`.
- `*.zip` and `ProjectArchive.zip` are always ignored — the zip-packager output never commits.
- `.venv/` is ignored but the lock file (`requirements.lock`, `poetry.lock`, `uv.lock`) is committed.
- `.env` is always ignored; `.env.example` is always committed.
- Never ignore `LICENSE`, `README.md`, `CHANGELOG.md`, `pyproject.toml`, or `Requirements.txt`.
- Use trailing slashes for directories (`__pycache__/`) and glob stars sparingly.

## Examples

```gitignore
# .gitignore — generated for the project-tooling stack.

# --- Python ---
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
*.egg
.pytest_cache/
.mypy_cache/
.ruff_cache/
.tox/
.coverage
htmlcov/
coverage.xml
dist/
build/

# --- Virtual environments ---
.venv/
venv/
env/
.env

# --- Node ---
node_modules/
npm-debug.log*
yarn-error.log*
.pnpm-store/

# --- R ---
.Rhistory
.RData
.Rproj.user/
*.Rproj

# --- Large data (keep tests/fixtures/ small and tracked) ---
Datasets/
results/
*.parquet
*.h5
*.npy
!tests/fixtures/*.csv

# --- Build artifacts from project-tooling ---
ProjectArchive.zip
*.zip

# --- IDE ---
.vscode/
.idea/
*.swp

# --- OS ---
.DS_Store
Thumbs.db

# --- Local overrides (do not commit personal entries above this line) ---
```

Un-ignore helper for tiny fixtures:

```gitignore
# Force small test fixtures to be tracked despite the broad Datasets/ rule.
!tests/fixtures/
!tests/fixtures/*.csv
!tests/fixtures/*.json
```

Verify what is ignored:

```bash
# Confirm the ignore rules behave as expected.
git status --ignored --short
```

## References

- GitHub's gitignore templates — https://github.com/github/gitignore
- git documentation — https://git-scm.com/docs/gitignore
