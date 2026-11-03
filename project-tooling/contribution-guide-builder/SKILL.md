---
name: contribution-guide-builder
description: "Build a `CONTRIBUTING.md` covering bug reporting, change suggestions via PRs, development setup (clone, install dev deps, run tests), coding style (links to the repo's `coding-conventions-enforcer`), branch naming (`feature/`, `fix/`, `docs/`), and Conventional Commits messages. Use this when opening a repo to external contributors or formalising the team's workflow. Triggers: CONTRIBUTING.md, contribution guide, PR workflow, branch naming, conventional commits, dev setup."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [contributing, onboarding, workflow, community]
related: [project-tooling/readme-generator, project-tooling/code-of-conduct-generator, project-tooling/pr-template-builder, project-tooling/issue-template-builder]
prerequisites: []
outputs: [markdown]
difficulty: beginner
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

# Contribution Guide Builder

## When To Use

- You are opening a repo to external contributors and need a single onboarding doc.
- The team has inconsistent branch names and commit messages and you want to standardise.
- You want every contributor to run the same dev setup (clone → install dev deps → run tests).
- You need to link out to the repo's `coding-conventions-enforcer` skill so style is enforced uniformly.

## Workflow

1. Scaffold `CONTRIBUTING.md` with a short opening that links to the README for project context.
2. Add a "Reporting Bugs" section: open an issue, fill in the bug template, attach reproduction steps.
3. Add a "Suggesting Enhancements" section: open an issue with the feature template first, then a PR.
4. Add a "Development Setup" section: clone, `pip install -e ".[dev,test]"`, run `make test`.
5. Add a "Coding Style" section that links to `style-integrity/coding-conventions-enforcer/SKILL.md`.
6. Add a "Branch Naming" section: `feature/<short-slug>`, `fix/<short-slug>`, `docs/<short-slug>`.
7. Add a "Commit Messages" section mandating Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`).
8. Add a "Pull Request Workflow" section: branch off `develop`, open PR against `main`, fill the PR template.
9. Add a "Testing" section requiring new tests for new code and `--cov-fail-under=80` to pass.
10. Add a "Code of Conduct" link pointing at `CODE_OF_CONDUCT.md`.
11. Commit and link from the README.

## Inputs

- The default branch name (`main`, sometimes `develop`).
- The dev install command (`pip install -e ".[dev,test]"` or equivalent).
- The repo's coding-conventions skill path (default `style-integrity/coding-conventions-enforcer`).
- Whether the project uses Conventional Commits (default yes).

## Outputs

- `CONTRIBUTING.md` at the repo root.
- A README link pointing at it.
- Consistent branch and commit conventions across the team.

## Key Rules

- Every section must be actionable; avoid "be excellent to each other" filler.
- Branch names use lowercase-kebab-case slugs: `feature/zip-denylist`, not `Feature_ZipDenylist`.
- Commit messages follow Conventional Commits: `<type>(<scope>): <subject>` where type is one of `feat`, `fix`, `docs`,
  `style`, `refactor`, `perf`, `test`, `chore`.
- A PR must reference its issue (`Closes #42`); never merge a PR with no issue link unless it's a trivial doc fix.
- New public code requires new tests; the CI `--cov-fail-under=80` gate blocks regressions.
- The coding-style section MUST link to `style-integrity/coding-conventions-enforcer/SKILL.md` so style is a single
  source of truth.
- Do not duplicate the Code of Conduct content here; link to `CODE_OF_CONDUCT.md`.

## Examples

```markdown
# Contributing to researchkit

Thanks for considering a contribution! Please read this file in full before opening an issue or PR.

## Reporting Bugs
Open an issue using the **Bug Report** template.
Include a minimal reproduction, the exact command, the Python version, and the full traceback.

## Suggesting Enhancements
Open an issue using the **Feature Request** template first.
After a maintainer agrees, open a PR against `main` referencing the issue (`Closes #42`).

## Development Setup
\`\`\`bash
git clone https://github.com/example/researchkit
cd researchkit
pip install -e ".[dev,test]"
make test
\`\`\`

## Coding Style
This repo enforces a strict style. Read and follow
[`style-integrity/coding-conventions-enforcer/SKILL.md`](../style-integrity/coding-conventions-enforcer/SKILL.md):
camelCase variables, CamelCase functions, 2-space indent, double quotes, period-ended comments.

## Branch Naming
- `feature/<short-slug>` for new functionality.
- `fix/<short-slug>` for bug fixes.
- `docs/<short-slug>` for documentation-only changes.

## Commit Messages
Use Conventional Commits:
\`\`\`
feat(zip): exclude *.zip from the archive denylist
fix(splitter): handle single-sample classes
docs(readme): add quick-start examples
\`\`\`

## Pull Request Workflow
1. Branch off `main` using the naming scheme above.
2. Write tests for every new public function.
3. Run `make lint test` locally before pushing.
4. Open a PR against `main` and fill in the PR template.
5. Ensure `--cov-fail-under=80` passes on CI.

## Code of Conduct
Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
```
