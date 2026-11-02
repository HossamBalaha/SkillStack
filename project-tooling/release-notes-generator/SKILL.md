---
name: release-notes-generator
description: "Generate release notes from the git log since the last tag, grouping commits by Conventional Commits type (`feat:` → Features, `fix:` → Bug Fixes, `docs:` → Documentation, `refactor:` → Refactoring) and emit the body as a GitHub Release. Use this when cutting a release or auto-drafting notes for review. Triggers: release notes, git log, conventional commits, github release, auto-bump, tag push."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [release-notes, git, conventional-commits, github-release]
related: [project-tooling/changelog-writer, project-tooling/github-actions-research-ci]
prerequisites: []
outputs: [markdown, bash]
difficulty: intermediate
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Release Notes Generator

## When To Use

- You are cutting a release and need a structured body for the GitHub Release.
- You want every `feat:` / `fix:` / `docs:` commit grouped under a clear heading.
- You want to auto-bump the version and push a tag in one step.
- You are auditing a repo whose release notes have drifted from the git log.

## Workflow

1. Determine the last tag with `git describe --tags --abbrev=0`.
2. Collect commits since that tag with `git log <lastTag>..HEAD --pretty=format:"- %s"`.
3. Parse each commit's Conventional Commits type prefix (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`).
4. Group commits under headings: Features (feat), Bug Fixes (fix), Documentation (docs), Refactoring (refactor),
   Performance (perf), Tests (test), Miscellaneous (chore).
5. Decide the bump: any `feat!` or breaking footer → major; any `feat:` → minor; otherwise patch.
6. Compose the release body and print it for review.
7. Optionally create the tag (`git tag -a vx.y.z -m "..."`) and push it.
8. Optionally call `gh release create vx.y.z --notes-file <file>` to publish the GitHub Release.
9. Mirror the entry into `CHANGELOG.md` under a new `## [x.y.z] - YYYY-MM-DD` heading.

## Inputs

- The last tag (auto-detected via `git describe`, or passed explicitly).
- The next version (auto-bumped by default; explicit override if provided).
- Today's date in ISO 8601.
- Whether to push the tag and create the GitHub Release (default: dry-run only).

## Outputs

- A release-notes body printed to stdout.
- A new git tag `vx.y.z` (when push is enabled).
- A GitHub Release (when `gh` is available and push is enabled).
- An appended `CHANGELOG.md` entry.

## Key Rules

- Only commits since the last tag are included; never re-list already-released commits.
- Commits without a Conventional Commits prefix go under "Miscellaneous".
- Breaking changes (`feat!:` or a `BREAKING CHANGE:` footer) force a major bump and are listed at the top.
- The generated body is reviewed by a human before publishing; auto-publish requires an explicit flag.
- Tags are annotated (`git tag -a`), never lightweight, so the tag message is preserved.
- The GitHub Release body is sourced from a file (`--notes-file`), not a long CLI string.
- The `CHANGELOG.md` entry uses the same grouping and ordering as the release body.

## Examples

`GenerateReleaseNotes.py`:

```python
# GenerateReleaseNotes.py — draft release notes from the git log.
import subprocess
import re
import sys
from collections import defaultdict

GroupOrder = [
  ("feat", "Features"),
  ("fix", "Bug Fixes"),
  ("docs", "Documentation"),
  ("refactor", "Refactoring"),
  ("perf", "Performance"),
  ("test", "Tests"),
  ("chore", "Miscellaneous"),
]


def LastTag():
  # Return the most recent tag, or empty string if none.
  try:
    return subprocess.check_output(
      ["git", "describe", "--tags", "--abbrev=0"], text=True
    ).strip()
  except subprocess.CalledProcessError:
    return ""


def CommitsSince(tag):
  # List commit subjects since the given tag (or from the root if empty).
  refRange = f"{tag}..HEAD" if (tag) else "HEAD"
  out = subprocess.check_output(
    ["git", "log", refRange, "--pretty=format:%s"], text=True
  )
  return out.splitlines()


def GroupCommits(subjects):
  grouped = defaultdict(list)
  breaking = []
  for subject in subjects:
    # Match "type(scope): subject" or "type!: subject".
    match = re.match(r"^([a-z]+)(\([^)]*\))?(!)?:\s*(.+)$", subject)
    if (not match):
      grouped["chore"].append(subject)
      continue
    type_, _, breakingMark, message = match.groups()
    if (breakingMark):
      breaking.append(message)
    grouped[type_].append(message)
  return grouped, breaking


def DraftBody():
  tag = LastTag()
  grouped, breaking = GroupCommits(CommitsSince(tag))
  lines = []
  if (breaking):
    lines.append("### Breaking Changes")
    lines.extend(f"- {item}" for item in breaking)
    lines.append("")
  for type_, heading in GroupOrder:
    items = grouped.get(type_, [])
    if (not items):
      continue
    lines.append(f"### {heading}")
    lines.extend(f"- {item}" for item in items)
    lines.append("")
  return "\n".join(lines).strip()


if (__name__ == "__main__"):
  print(f"Comparing since last tag: {LastTag() or '(root)'}")
  print(DraftBody())
```

Publish:

```bash
# Save the draft, then create the GitHub Release.
python GenerateReleaseNotes.py > release_notes.md
git tag -a v0.3.0 -m "Release 0.3.0"
git push origin v0.3.0
gh release create v0.3.0 --notes-file release_notes.md
```

## References

- Conventional Commits — https://www.conventionalcommits.org
- GitHub CLI `gh release create` — https://cli.github.com/manual/gh_release_create
- `git describe` — https://git-scm.com/docs/git-describe
