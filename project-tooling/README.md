# 🧰 Project Tooling — Packaging, Docker & CI/CD

> Bootstrap, package, test, and ship research code with the same hygiene as production software. Covers
> pyproject/Makefile/environment/Docker scaffolding, licenses, READMEs, contribution guides, GitHub Actions CI, pytest
> suites, pre-commit hooks, Sphinx docs, and release/changelog tooling. Drop a single skill into a fresh repo to get the
> rest of the bundle as a chain.

## Theme Overview

This folder contains **20 skills** in the `project-tooling/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                 | Description                                                                                                                                                                                                                                                                                                                         | Difficulty   | Tags                                                                  | Related                                                                                                                                                          |
|----|-----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`changelog-writer`](changelog-writer/SKILL.md)                       | Write a `CHANGELOG.md` in the Keep a Changelog format with `## [Unreleased]` and dated release sections, subsections for `### Added`, `### Changed`, `### Deprecated`, `### Removed`, `### Fixed`, `### Security`, and correct semantic-version bumps (major/minor/patch).                                                          | beginner     | `changelog`, `semver`, `releases`, `keep-a-changelog`                 | `project-tooling/release-notes-generator`, `project-tooling/contribution-guide-builder`                                                                          |
| 2  | [`code-of-conduct-generator`](code-of-conduct-generator/SKILL.md)     | Generate a `CODE_OF_CONDUCT.md` based on the Contributor Covenant (latest version), with the enforcement contact filled in.                                                                                                                                                                                                         | beginner     | `code-of-conduct`, `community`, `contributor-covenant`, `scaffolding` | `project-tooling/contribution-guide-builder`, `project-tooling/license-selector`                                                                                 |
| 3  | [`contribution-guide-builder`](contribution-guide-builder/SKILL.md)   | Build a `CONTRIBUTING.md` covering bug reporting, change suggestions via PRs, development setup (clone, install dev deps, run tests), coding style (links to the repo's `coding-conventions-enforcer`), branch naming (`feature/`, `fix/`, `docs/`), and Conventional Commits messages.                                             | beginner     | `contributing`, `onboarding`, `workflow`, `community`                 | `project-tooling/readme-generator`, `project-tooling/code-of-conduct-generator`, `project-tooling/pr-template-builder`, `project-tooling/issue-template-builder` |
| 4  | [`docker-research-container`](docker-research-container/SKILL.md)     | Build a `Dockerfile` for reproducible research that installs system deps, copies `Requirements.txt`, runs `pip install --no-cache-dir`, creates a non-root user, sets `WORKDIR`, and defines an `ENTRYPOINT`.                                                                                                                       | intermediate | `docker`, `container`, `reproducibility`                              | `project-tooling/github-actions-research-ci`, `project-tooling/environment-yaml-builder`                                                                         |
| 5  | [`environment-yaml-builder`](environment-yaml-builder/SKILL.md)       | Build an `environment.yml` (conda) with channels (`conda-forge`, `defaults`) and dependencies including a `- pip:` block plus `-r requirements.txt`, or a `Pipfile` for pipenv, or a `pixi.toml` for pixi.                                                                                                                          | intermediate | `conda`, `environment`, `pip`, `reproducibility`                      | `project-tooling/requirements-pinner`, `project-tooling/docker-research-container`, `project-tooling/pyproject-toml-builder`                                     |
| 6  | [`github-actions-research-ci`](github-actions-research-ci/SKILL.md)   | Build GitHub Actions workflows in `.github/workflows/ci.yml` with jobs for install, lint, test, docs, and optional Docker push to GHCR.                                                                                                                                                                                             | intermediate | `github-actions`, `ci-cd`, `automation`                               | `project-tooling/pytest-scientific-suite`, `project-tooling/pre-commit-hook-builder`                                                                             |
| 7  | [`gitignore-builder`](gitignore-builder/SKILL.md)                     | Generate a `.gitignore` tailored to the project's stack: Python (`__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.egg-info/`, `.venv/`, `dist/`, `build/`), Node (`node_modules/`), R (`.Rhistory`, `.RData`), large data (`Datasets/`, `*.csv` if large, `*.parquet`), IDE (`.vscode/`, `.idea/`), and OS (`.DS_Store`, `Thumbs.db`). | beginner     | `gitignore`, `vcs`, `scaffolding`, `ignore-rules`                     | `project-tooling/license-selector`, `project-tooling/pyproject-toml-builder`, `project-tooling/contribution-guide-builder`                                       |
| 8  | [`issue-template-builder`](issue-template-builder/SKILL.md)           | Build GitHub issue templates as YAML form schemas: `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, and a `question.md` config-based template.                                                                                                                                                                       | beginner     | `issue-template`, `github`, `bug-report`, `feature-request`           | `project-tooling/pr-template-builder`, `project-tooling/contribution-guide-builder`                                                                              |
| 9  | [`jupyter-to-script-converter`](jupyter-to-script-converter/SKILL.md) | Convert a `.ipynb` notebook into a clean `.py` module by stripping metadata, extracting code cells into named functions, removing `display()` calls and `!` shell escapes, preserving cell outputs as `# Output:` comments, adding a module docstring, and wrapping runnable code in `if __name__ == "__main__":`.                  | intermediate | `jupyter`, `nbconvert`, `notebook`, `refactoring`                     | `project-tooling/pytest-scientific-suite`, `project-tooling/makefile-generator`                                                                                  |
| 10 | [`license-selector`](license-selector/SKILL.md)                       | Select an open-source license (MIT, Apache-2.0, GPL-3.0, AGPL-3.0, BSD-2/3-Clause) based on the project's use case, generate the matching `LICENSE` file text, and add the SPDX `license` field to `pyproject.toml`.                                                                                                                | beginner     | `license`, `mit`, `apache`, `gpl`, `spdx`                             | `project-tooling/readme-generator`, `project-tooling/pyproject-toml-builder`, `project-tooling/contribution-guide-builder`                                       |
| 11 | [`makefile-generator`](makefile-generator/SKILL.md)                   | Generate a `Makefile` with targets `install`, `test`, `lint`, `format`, `typecheck`, `docs`, `run`, `clean`, and `zip`, all marked `.PHONY`.                                                                                                                                                                                        | intermediate | `makefile`, `automation`, `build`, `developer-entrypoint`             | `project-tooling/pytest-scientific-suite`, `project-tooling/pre-commit-hook-builder`, `project-tooling/github-actions-research-ci`                               |
| 12 | [`pr-template-builder`](pr-template-builder/SKILL.md)                 | Build `.github/PULL_REQUEST_TEMPLATE.md` with a Summary (what + why), a Type of change checklist (bug/feature/breaking/docs), a verification Checklist (tests added, docs updated, coding style, no new warnings), a Breaking Changes section, and an optional Screenshots section.                                                 | beginner     | `pr-template`, `github`, `code-review`, `checklist`                   | `project-tooling/issue-template-builder`, `project-tooling/contribution-guide-builder`                                                                           |
| 13 | [`pre-commit-hook-builder`](pre-commit-hook-builder/SKILL.md)         | Build a `.pre-commit-config.yaml` wiring up `pre-commit/pre-commit-hooks` (trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files), `charliermarsh/ruff` (lint + format), `psf/black`, `pre-commit/mirrors-mypy`, and optionally `python-poetry/poetry`.                                                       | intermediate | `pre-commit`, `linting`, `hooks`, `automation`                        | `project-tooling/makefile-generator`, `project-tooling/github-actions-research-ci`, `project-tooling/pyproject-toml-builder`                                     |
| 14 | [`project-zip-packager`](project-zip-packager/SKILL.md)               | Generate a `CreateProjectZip.py` script that bundles the entire repository into a single `ProjectArchive.zip`.                                                                                                                                                                                                                      | beginner     | `zip`, `packaging`, `distribution`                                    | `project-tooling/requirements-pinner`, `project-tooling/docker-research-container`, `project-tooling/release-notes-generator`                                    |
| 15 | [`pyproject-toml-builder`](pyproject-toml-builder/SKILL.md)           | Build a `pyproject.toml` file with the `[project]` table, a `[build-system]` backend, and tool config sections (`[tool.ruff]`, `[tool.black]`, `[tool.mypy]`, `[tool.pytest.ini_options]`).                                                                                                                                         | intermediate | `pyproject`, `packaging`, `pep-621`, `build-system`                   | `project-tooling/requirements-pinner`, `project-tooling/environment-yaml-builder`, `project-tooling/pre-commit-hook-builder`, `project-tooling/license-selector` |
| 16 | [`pytest-scientific-suite`](pytest-scientific-suite/SKILL.md)         | Write pytest test suites for scientific and ML code with `conftest.py` fixtures, `@pytest.mark.parametrize` for edge cases (n=0, n=1, binary/multiclass, single-class), deterministic seeds, and coverage gating via `--cov-fail-under=80`.                                                                                         | intermediate | `pytest`, `testing`, `fixtures`, `scientific`                         | `project-tooling/github-actions-research-ci`, `project-tooling/pre-commit-hook-builder`, `project-tooling/makefile-generator`                                    |
| 17 | [`readme-generator`](readme-generator/SKILL.md)                       | Generate a `README.md` for any project with a title and one-line hook, a "What & Why" section, a zero-to-working quick-start, real tested code examples, per-ecosystem install steps, and only the sections that project actually needs.                                                                                            | beginner     | `readme`, `documentation`, `onboarding`                               | `project-tooling/sphinx-docs-builder`, `project-tooling/contribution-guide-builder`                                                                              |
| 18 | [`release-notes-generator`](release-notes-generator/SKILL.md)         | Generate release notes from the git log since the last tag, grouping commits by Conventional Commits type (`feat:` → Features, `fix:` → Bug Fixes, `docs:` → Documentation, `refactor:` → Refactoring) and emit the body as a GitHub Release.                                                                                       | intermediate | `release-notes`, `git`, `conventional-commits`, `github-release`      | `project-tooling/changelog-writer`, `project-tooling/github-actions-research-ci`                                                                                 |
| 19 | [`requirements-pinner`](requirements-pinner/SKILL.md)                 | Generate dependency files for a Python project — either an unversioned `Requirements.txt` for broad environment compatibility or a pinned `requirements.lock` for exact reproducibility.                                                                                                                                            | beginner     | `requirements`, `dependencies`, `pip`, `reproducibility`              | `project-tooling/environment-yaml-builder`, `project-tooling/pyproject-toml-builder`, `project-tooling/docker-research-container`                                |
| 20 | [`sphinx-docs-builder`](sphinx-docs-builder/SKILL.md)                 | Build Sphinx documentation with `conf.py` (autodoc, napoleon, intersphinx, doctest extensions), `index.rst` with a toctree, an `api/` folder of `automodule` directives, a `tutorial/` folder of narrative docs, and the Read the Docs theme.                                                                                       | intermediate | `sphinx`, `documentation`, `autodoc`, `rtd`                           | `project-tooling/readme-generator`, `project-tooling/contribution-guide-builder`                                                                                 |

## Difficulty Breakdown

Across **20** skills in this theme, the difficulty distribution is:

- **Beginner** — 10 skill(s)
- **Intermediate** — 10 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`automation` (3), `reproducibility` (3), `community` (2), `documentation` (2), `github` (2), `onboarding` (2),
`packaging` (2), `pip` (2), `scaffolding` (2), `apache` (1), `autodoc` (1), `bug-report` (1), `build` (1),
`build-system` (1), `changelog` (1), `checklist` (1), `ci-cd` (1), `code-of-conduct` (1), `code-review` (1), `conda`
(1), `container` (1), `contributing` (1), `contributor-covenant` (1), `conventional-commits` (1), `dependencies` (1),
`developer-entrypoint` (1), `distribution` (1), `docker` (1), `environment` (1), `feature-request` (1), `fixtures` (1),
`git` (1), `github-actions` (1), `github-release` (1), `gitignore` (1), `gpl` (1), `hooks` (1), `ignore-rules` (1),
`issue-template` (1), `jupyter` (1), `keep-a-changelog` (1), `license` (1), `linting` (1), `makefile` (1), `mit` (1),
`nbconvert` (1), `notebook` (1), `pep-621` (1), `pr-template` (1), `pre-commit` (1), `pyproject` (1), `pytest` (1),
`readme` (1), `refactoring` (1), `release-notes` (1), `releases` (1), `requirements` (1), `rtd` (1), `scientific` (1),
`semver` (1), `spdx` (1), `sphinx` (1), `testing` (1), `vcs` (1), `workflow` (1), `zip` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`pyproject-toml-builder` → `requirements-pinner` → `environment-yaml-builder` → `docker-research-container`** —
  Project setup → deps → env → container.
- **`gitignore-builder` → `license-selector` → `readme-generator` → `contribution-guide-builder` →
  `code-of-conduct-generator`** — Repo bootstrapping bundle.
- **`github-actions-research-ci` → `pytest-scientific-suite` → `pre-commit-hook-builder` → `makefile-generator`** — CI →
  tests → hooks → Makefile.
- **`issue-template-builder` → `pr-template-builder` → `contribution-guide-builder` → `changelog-writer` →
  `release-notes-generator`** — Issue → PR → contributing → changelog → release.

## Cross-Theme Connections

Skills in `project-tooling/` declare `related` pointers to skills in other themes. The most common destinations are:

- No cross-theme related pointers found in this theme.

Themes that commonly chain with this one:

- [`../ml-engineering/README.md`](ml-engineering/README.md) — CI runs reproducible experiment suites on every push.
- [`../data-engineering/README.md`](data-engineering/README.md) — ETL pipelines are packaged into Docker containers.
- [`../academic-research/README.md`](academic-research/README.md) — research repos are scaffolded with READMEs,
  licenses, and contribution guides.
- [`../style-integrity/README.md`](style-integrity/README.md) — pre-commit hooks enforce coding and LaTeX conventions.

## Back to Master

← [Back to SkillStack README](../README.md)
