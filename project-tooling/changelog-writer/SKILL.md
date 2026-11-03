---
name: changelog-writer
description: "Write a `CHANGELOG.md` in the Keep a Changelog format with `## [Unreleased]` and dated release sections, subsections for `### Added`, `### Changed`, `### Deprecated`, `### Removed`, `### Fixed`, `### Security`, and correct semantic-version bumps (major/minor/patch). Use this when cutting a release or maintaining a continuous record of notable changes. Triggers: CHANGELOG.md, keep a changelog, semver bump, release notes, Unreleased section."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [ changelog, semver, releases, keep-a-changelog ]
related: [ project-tooling/release-notes-generator, project-tooling/contribution-guide-builder ]
prerequisites: [ ]
outputs: [ markdown ]
difficulty: beginner
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: [ ]
---

# Changelog Writer

## When To Use

- You are cutting a release and need to convert the `## [Unreleased]` backlog into a dated `## [x.y.z]` entry.
- You want every merged PR to append one bullet under the right subsection in `## [Unreleased]`.
- You need to decide whether the next version is a major, minor, or patch bump.
- You are auditing a repo whose `CHANGELOG.md` has drifted from the git history.

## Workflow

1. Open `CHANGELOG.md`; if absent, scaffold it with the Keep a Changelog header and an empty `## [Unreleased]` block.
2. Read the merged PRs / commits since the last tag using `git log $(git describe --tags --abbrev=0)..HEAD`.
3. Classify each change into one of: Added, Changed, Deprecated, Removed, Fixed, Security.
4. Append one bullet per change under the matching subsection of `## [Unreleased]`.
5. When cutting a release, decide the bump: breaking change → major, new feature → minor, fix → patch.
6. Rename `## [Unreleased]` to `## [x.y.z] - YYYY-MM-DD` and add a fresh empty `## [Unreleased]` above it.
7. Tag the release with `git tag -a vx.y.z -m "Release x.y.z"` and push the tag.
8. Cross-check the date is in ISO 8601 (`YYYY-MM-DD`) and the version matches the tag.

## Inputs

- The current `CHANGELOG.md` (or a request to create one).
- The git log range since the last tag.
- The bump policy (auto-detect by default; explicit override if provided).
- Today's date in ISO 8601.

## Outputs

- `CHANGELOG.md` updated with the new release entry.
- A git tag `vx.y.z` (when cutting a release).
- A short summary of which subsections received entries.

## Key Rules

- Always keep a `## [Unreleased]` section at the top, even when empty — that is where ongoing work lands.
- Dates are ISO 8601 `YYYY-MM-DD`, never `01/02/2026` or `Jan 1, 2026`.
- Version numbers are `MAJOR.MINOR.PATCH` with no `v` prefix inside the heading (the git tag carries the `v`).
- A breaking change forces a major bump even if no new feature landed.
- Each bullet is one sentence starting with a capital and ending with a period.
- Group bullets under the correct subsection; do not dump everything under `### Changed`.
- Never delete past release entries — the changelog is append-only.

## Examples

`CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for Pixi lock files in the environment builder.

### Fixed

- Off-by-one in the stratified splitter when a class has a single sample.

## [0.2.0] - 2026-01-15

### Added

- `environment-yaml-builder` skill for conda envs.
- `--cov-fail-under=80` gate in the pytest suite.

### Changed

- Switched the CI matrix to Python 3.10 / 3.11 / 3.12.

### Fixed

- Zip packager no longer recurses into its own output.

## [0.1.0] - 2025-11-02

### Added

- Initial public release with 20 project-tooling skills.
```

Bump decision helper:

```python
# ChooseBump.py — decide the next semver bump from the Unreleased entry.
def ChooseBump(entries):
  # Major if any breaking change is flagged.
  if (entries.get("Breaking")):
    return "major"
  if (entries.get("Added")):
    return "minor"
  if (entries.get("Fixed") or entries.get("Changed") or entries.get("Removed") or entries.get("Security")):
    return "patch"
  return "patch"


if (__name__ == "__main__"):
  entries = {"Added": ["new skill"], "Fixed": ["zip bug"], "Breaking": False}
  print(ChooseBump(entries))
```

Tag and push:

```bash
# Cut the release and push the tag.
git tag -a v0.2.0 -m "Release 0.2.0"
git push origin v0.2.0
```
