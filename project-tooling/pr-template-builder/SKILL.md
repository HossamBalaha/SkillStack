---
name: pr-template-builder
description: "Build `.github/PULL_REQUEST_TEMPLATE.md` with a Summary (what + why), a Type of change checklist (bug/feature/breaking/docs), a verification Checklist (tests added, docs updated, coding style, no new warnings), a Breaking Changes section, and an optional Screenshots section. Use this when standardising PR descriptions so reviewers get consistent context. Triggers: PULL_REQUEST_TEMPLATE.md, PR template, type of change, verification checklist, breaking changes."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [pr-template, github, code-review, checklist]
related: [project-tooling/issue-template-builder, project-tooling/contribution-guide-builder]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# PR Template Builder

## When To Use

- You want every PR to arrive with a clear summary, type, and verification checklist.
- Reviewers are missing context because PR descriptions are empty or inconsistent.
- You want to make breaking-change disclosures mandatory on every PR.
- You are migrating from per-author PR styles to a single repo-wide template.

## Workflow

1. Create `.github/PULL_REQUEST_TEMPLATE.md` at the repo root.
2. Add a "Summary" section: what changed and why, linked to the issue (`Closes #N`).
3. Add a "Type of change" checklist: bug fix, new feature, breaking change, docs, refactor.
4. Add a "Checklist" section: tests added/updated, docs updated, coding style followed, no new warnings, `CHANGELOG.md`
   updated.
5. Add a "Breaking changes" section that is mandatory to fill (even with "None").
6. Add an optional "Screenshots" section for UI changes.
7. Optionally create `.github/PULL_REQUEST_TEMPLATE/<branch>.md` for branch-specific templates.
8. Commit and verify by opening a test PR on GitHub.
9. Cross-link the template from `CONTRIBUTING.md` so contributors know what's expected.

## Inputs

- The default branch the PR targets (`main` or `develop`).
- Whether screenshots are relevant (skip the section for non-UI repos).
- Any project-specific checklist items (e.g. "updated `CHANGELOG.md`").

## Outputs

- `.github/PULL_REQUEST_TEMPLATE.md`.
- A note in `CONTRIBUTING.md` referencing the template.

## Key Rules

- The template uses GitHub-flavoured Markdown checkboxes (`- [ ]`) so they render as clickable.
- The "Breaking changes" section is mandatory; "None" is a valid answer.
- Every PR must reference its issue with `Closes #N` (or `Fixes #N`, `Resolves #N`).
- The checklist must include a "tests added" item and a "no new warnings" item.
- Keep the template under ~40 lines; long templates get skipped by contributors.
- Never embed project secrets or URLs that rotate (use repo-relative links).

## Examples

`.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary
<!-- What does this PR change, and why? Link the issue with "Closes #N". -->

Closes #

## Type of change
- [ ] Bug fix (non-breaking change that fixes an issue).
- [ ] New feature (non-breaking change that adds functionality).
- [ ] Breaking change (fix or feature that would cause existing usage to break).
- [ ] Documentation update.
- [ ] Refactor (no functional change).

## Checklist
- [ ] I have read and followed the [coding conventions](../style-integrity/coding-conventions-enforcer/SKILL.md).
- [ ] I have added tests for every new public function.
- [ ] I have updated the relevant documentation.
- [ ] I have updated `CHANGELOG.md` under `## [Unreleased]`.
- [ ] `make lint test` passes locally with `--cov-fail-under=80`.
- [ ] I have introduced no new compiler or linter warnings.

## Breaking changes
<!-- If this PR introduces breaking changes, describe them and the migration path. -->
<!-- If none, write "None". -->

None.

## Screenshots
<!-- For UI changes only: paste before/after screenshots. -->
<!-- Delete this section for non-UI PRs. -->
```

Validate rendering:

```bash
# Confirm the file is valid Markdown and renders on GitHub.
python -c "import pathlib; t = pathlib.Path('.github/PULL_REQUEST_TEMPLATE.md').read_text(); assert '## Summary' in t and '## Checklist' in t; print('ok')"
```

## References

- GitHub PR
  templates — https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
- Closing keywords (`Closes`, `Fixes`,
  `Resolves`) — https://docs.github.com/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
