# Contributing to SkillStack

First off — thank you for taking the time to contribute to **SkillStack**. 🧱

SkillStack is a composable library of 168 skills across 9 independent theme
folders. The project is authored and maintained by **Hossam Magdy Balaha** and
released under the MIT License. This document explains how to file bugs,
propose changes, set up a local dev environment, and author brand-new skills
that fit the existing stack.

> **TL;DR.** File bugs via GitHub Issues. Propose changes via Pull Requests.
> Lint before you push with `python scripts/LintSkills.py`. Follow the
> five-rule Python style in
> [`style-integrity/coding-conventions-enforcer/SKILL.md`](./style-integrity/coding-conventions-enforcer/SKILL.md).
> Read [`docs/AUTHORING_GUIDE.md`](./docs/AUTHORING_GUIDE.md) before writing a
> new skill.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Development Setup](#development-setup)
- [Coding Style](#coding-style)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Authoring a New Skill](#authoring-a-new-skill)
- [Updating the Maestro and README](#updating-the-maestro-and-readme)
- [License](#license)

---

## Code of Conduct

Participation in this project is governed by the
[Contributor Covenant v2.1](./CODE_OF_CONDUCT.md). By participating, you agree
to uphold that code. Please report unacceptable behavior to
**hmbala01@louisville.edu**.

---

## Reporting Bugs

Bugs are tracked as [GitHub Issues](https://github.com/Hossam-Balaha/SkillStack/issues).

1. Search the existing issues to avoid duplicates.
2. Open a new issue and pick the **Bug report** template.
3. Fill in every section: description, reproduction steps, expected vs.
   actual behavior, environment (OS, Python version, SkillStack version),
   and any relevant logs or stack traces.
4. Keep the issue focused on one bug. Open a second issue for a second bug.

A good bug report is **reproducible**. Include the exact command, the skill
name (e.g., `style-integrity/coding-conventions-enforcer`), and a minimal
snippet of input. If the bug touches a specific theme, mention the theme
folder in the issue title (e.g., `[ml-engineering] ...`).

---

## Suggesting Enhancements

Enhancements are also tracked via
[GitHub Issues](https://github.com/Hossam-Balaha/SkillStack/issues) using the
**Feature request** template. Describe:

- The **problem** you are trying to solve.
- The **proposed solution** at the skill level (which theme, which skill
  name, which workflow step).
- Any **alternatives** you considered.
- **Additional context** — links, examples, prior art.

SkillStack favors small, composable skills over giant ones. If your
enhancement would change a skill's purpose or break its existing workflow,
propose a **new** skill instead of expanding an existing one.

---

## Development Setup

SkillStack is a documentation-and-code library. The Python scripts that lint,
link-check, and generate the manifest live under `scripts/` and have minimal
dependencies.

```bash
# 1. Clone the repo.
git clone https://github.com/Hossam-Balaha/SkillStack.git
cd SkillStack

# 2. Create and activate a virtual environment.
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

# 3. Install the script dependencies.
pip install -r requirements-scripts.txt

# 4. (Optional) Install pre-commit hooks for local checks.
pip install pre-commit
pre-commit install

# 5. Run the linter to confirm the local tree is clean.
python scripts/LintSkills.py

# 6. (Optional) Re-run the manifest generator and link checker.
python scripts/GenerateManifest.py
python scripts/CheckLinks.py
```

That's it. There is no package to build and no compiled artifact — every
skill is a `SKILL.md` file the agent loads on demand.

---

## Coding Style

All Python code in this repo (the `scripts/` directory and any inline
examples inside skill files) follows the five strict rules enforced by the
[`coding-conventions-enforcer`](./style-integrity/coding-conventions-enforcer/SKILL.md)
skill:

1. **Variables** use `camelCase` — e.g., `dataSourceUrl`.
2. **Functions, classes, file names, and dict keys** use `CamelCase` — e.g.,
   `ProcessData`, `DataProcessor`, `DataUtils.py`, `"ValidationStatus"`.
3. **`if` / `elif` / `while` conditions** are wrapped in parentheses —
   `if (condition):`.
4. **Comments** sit on the line directly above each statement and end with a
   period — `# Initialize the data source URL.`
5. **String literals** use double quotes `"..."` everywhere except inside
   docstrings (which keep the triple-double-quote form).

Indentation is **2 spaces**. Framework-mandated lowercase method names
(`forward`, `backward`, `training_step`, `validation_step`,
`configure_optimizers`, `setUp`, `tearDown`) are exempt.

Read the full skill — including the canonical docstring template and the
`Configs/Config.yaml` rule — at
[`style-integrity/coding-conventions-enforcer/SKILL.md`](./style-integrity/coding-conventions-enforcer/SKILL.md).

Markdown files use a soft wrap at ~100 columns, sentences separated by a
single space, and a trailing newline at the end of every file.

---

## Branch Naming

Branch off `main` and use one of the following prefixes:

| Prefix     | Use when                                                                  |
|------------|---------------------------------------------------------------------------|
| `feature/` | Adding a new skill, theme, or capability.                                |
| `fix/`     | Fixing a bug in an existing skill, the maestro, or the master README.     |
| `docs/`    | Documentation-only changes (typos, README updates).                       |
| `refactor/`| Internal reorganization with no observable behavior change.              |
| `chore/`   | Tooling, dependency bumps, `.gitignore` updates.                          |
| `test/`    | Adding or fixing tests for the `scripts/` directory.                      |

Examples:

```
feature/ai-output-judgement/prompt-injection-detector
fix/style-integrity/latex-style-guard-double-quotes
docs/master-readme-themes-table
chore/pre-commit-bump-ruff
```

---

## Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/).
Each commit message begins with a type, an optional scope in parentheses, an
optional `!` for a breaking change, a colon, and a short imperative summary.

```
<type>(<scope>)!: <summary>

<body>

<footer>
```

Allowed types:

| Type         | When to use it                                                                |
|--------------|-------------------------------------------------------------------------------|
| `feat`       | A new skill, new theme, or new user-facing capability.                        |
| `fix`        | A bug fix in an existing skill, script, or doc.                               |
| `docs`       | Documentation-only changes (README, CONTRIBUTING, NOTICE).                |
| `refactor`   | Code or doc restructuring with no behavior change.                            |
| `perf`       | Performance improvement to a script.                                           |
| `test`       | Adding or fixing tests.                                                        |
| `build`      | Changes to build tooling, dependencies, or `requirements-*.txt`.              |
| `chore`      | Routine maintenance that doesn't fit any of the above.                        |
| `revert`     | Reverting a previous commit.                                                   |

Examples:

```
feat(ai-output-judgement): add prompt-injection-detector skill
fix(style-integrity): correct latex-style-guard em-dash rule
docs(readme): update theme counts after adding a skill
refactor(maestro): simplify routing table layout
chore(deps): bump ruff to 0.7.4 in pre-commit
```

Use the imperative mood in the summary: "add skill" rather than "added skill"
or "adds skill". Keep the summary under 72 characters. Reference issues or
PRs in the footer using `Closes #123`, `Fixes #123`, or `Refs #123`.

Breaking changes use `!` after the scope (or a `BREAKING CHANGE:` footer):

```
feat(maestro)!: drop legacy numbered theme routing

Replaces the ordinal-based theme router with folder-name routing.
Existing themes keep working without renumbering. Closes #42.
```

When a commit adds or changes a skill, also update the master `README.md`
index and the maestro routing table in the same commit.

---

## Pull Requests

PRs are the only path changes land on `main`. Before opening one:

1. **Lint.** Run `python scripts/LintSkills.py` locally and ensure it exits
   with status `0`.
2. **Link-check.** Run `python scripts/CheckLinks.py` if your change adds
   or renames a skill path or a markdown link.
3. **Regenerate the manifest.** Run `python scripts/GenerateManifest.py`
   and commit `skills.yaml` if it changes.
4. **Update docs.** If your PR adds or renames a skill, update the master
   `README.md` index and the maestro routing table in the same PR.
5. **Open the PR against `main`** with a clear summary, the type of change
   (bug/feature/breaking/docs), and the theme touched.

A maintainer will review, request changes if needed, and squash-merge once
the pre-commit hooks pass.

---

## Authoring a New Skill

Read the full guide at [`docs/AUTHORING_GUIDE.md`](./docs/AUTHORING_GUIDE.md)
before you start. The short version:

1. **Pick the theme.** SkillStack has 9 theme folders. Pick exactly one. If
   the skill spans two themes, route to the **primary** theme first and
   chain to the second.
2. **Name the skill.** Use lowercase-kebab-case (e.g., `prompt-injection-detector`).
   Create `<theme>/<skill-name>/SKILL.md`.
3. **Write YAML frontmatter** with `name`, `description`, and `metadata`
   (`author`, `version`, `theme`).
4. **Write the workflow body** in this canonical order:
   `## When To Use` → `## Workflow` → `## Inputs` → `## Outputs` →
   `## Key Rules` → `## Examples` → `## References`.
5. **Follow the style.** Any Python snippets inside the skill must pass the
   `coding-conventions-enforcer` rules.
6. **Add an optional `references/`** subfolder only if the skill needs
   deeper rule files the agent should read on demand.
7. **Update the master README index** for your theme's table and bump the
   theme count.
8. **Update the maestro** routing table count if a new skill changes a
   theme's skill count.
9. **Lint, link-check, manifest.** Then open the PR.

Do **not** number skill files — the maestro routes by folder name, not by
ordinal. New skills always go at the end of their theme folder.

---

## Updating the Maestro and README

The master `README.md` and `maestro/SKILL.md` are kept in sync. When you add,
rename, or remove a skill:

- Update the theme's count in **both** files (the README repo-layout block,
  the README master-index table, and the maestro routing table).
- If you add a brand-new theme, also update `NOTICE` (the canonical theme
  list) and the master README badge count.

---

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](./LICENSE) that covers this repository. You also confirm that
your contributions are your own original work, written in your own words, and
do not reproduce third-party proprietary content verbatim. See
[`NOTICE`](./NOTICE) for the project's attribution and provenance statement.

---

Thank you for helping make SkillStack better.
