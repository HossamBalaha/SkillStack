---
name: project-zip-packager
description: "Generate a `CreateProjectZip.py` script that bundles the entire repository into a single `ProjectArchive.zip`. Use this when you need to ship, archive, or share a self-contained snapshot of the repo, especially before submission or handoff. Triggers: bundle repo, package project, zip archive, CreateProjectZip."
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: project-tooling
tags: [zip, packaging, distribution]
related: [project-tooling/requirements-pinner, project-tooling/docker-research-container, project-tooling/release-notes-generator]
prerequisites: []
outputs: [python, bash]
difficulty: beginner
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Project Zip Packager

## When To Use
- You need a single archive file that reproduces the repo layout for handoff, review, or archival.
- A submission portal (journal, conference, grant) requires a flat `.zip` of the project.
- You want a reproducible snapshot at a known commit without pushing the `.git` history.
- You are packaging code that pairs with large `Datasets/` or `results/` directories that must NOT travel with the source.

## Workflow
1. Inspect the repo root and list top-level directories to confirm what exists.
2. Build the denylist of paths and glob patterns that must never enter the archive.
3. Generate `CreateProjectZip.py` at the repo root using `zipfile` + `os.walk`.
4. Write the output to `ProjectArchive.zip` at the repo root.
5. Run the script once locally to confirm it terminates without recursion.
6. Verify the resulting `.zip` is smaller than the repo (heavy dirs excluded) and opens cleanly.
7. Add `ProjectArchive.zip` and `*.zip` to `.gitignore` so the artifact is never committed.
8. Document the script in the README under a "Build Archive" section.

## Inputs
- The repository root path (default: current working directory).
- An optional denylist override if the caller wants extra exclusions.
- An optional output filename (default: `ProjectArchive.zip`).

## Outputs
- `CreateProjectZip.py` — runnable packaging script at the repo root.
- `ProjectArchive.zip` — the produced archive (gitignored, never committed).
- A short log printed to stdout listing how many files were added and skipped.

## Key Rules
- The script MUST exclude its own output (`ProjectArchive.zip`) AND every `*.zip` file, otherwise the next run will recurse on the previous archive and grow unbounded.
- Heavy directories are excluded unconditionally: `Datasets/`, `results/`, `.git/`, `__pycache__/`, `.venv/`, `dist/`, `build/`, `.pytest_cache/`.
- Match by both directory name and path suffix so nested copies (e.g. `subpkg/__pycache__/`) are caught.
- Use `zipfile.ZIP_DEFLATED` to compress; never use `ZIP_STORED` for source archives.
- Preserve relative paths inside the archive so the unpacked layout matches the repo.
- The script must be idempotent: re-running overwrites `ProjectArchive.zip` cleanly.
- Never walk into symlinks that point outside the repo; guard with `os.path.realpath` checks.

## Examples
```python
# CreateProjectZip.py — bundle this repo into ProjectArchive.zip.
import os
import zipfile

ArchiveName = "ProjectArchive.zip"

# Directories that must never enter the archive.
ExcludedDirs = {
  "Datasets",
  "results",
  ".git",
  "__pycache__",
  ".venv",
  "dist",
  "build",
  ".pytest_cache",
}

# Glob patterns excluded at the file level.
ExcludedSuffixes = (".zip", ".pyc", ".pyo")


def ShouldExclude(relPath):
  # Reject any path that touches a denied directory.
  parts = relPath.split(os.sep)
  for part in parts:
    if (part in ExcludedDirs):
      return True
  # Reject by file suffix.
  if (relPath.endswith(ExcludedSuffixes)):
    return True
  # Reject the archive itself to prevent recursive growth.
  if (relPath == ArchiveName):
    return True
  return False


def BuildArchive(rootDir, archivePath):
  # Walk the repo once and write each surviving file.
  added = 0
  skipped = 0
  with zipfile.ZipFile(archivePath, "w", zipfile.ZIP_DEFLATED) as archive:
    for currentDir, dirNames, fileNames in os.walk(rootDir):
      # Prune denied directories in place so os.walk skips them.
      dirNames[:] = [d for d in dirNames if (d not in ExcludedDirs)]
      for fileName in fileNames:
        absPath = os.path.join(currentDir, fileName)
        relPath = os.path.relpath(absPath, rootDir)
        if (ShouldExclude(relPath)):
          skipped += 1
          continue
        archive.write(absPath, relPath)
        added += 1
  print(f"Added {added} files, skipped {skipped} files.")


if (__name__ == "__main__"):
  rootDir = os.path.dirname(os.path.abspath(__file__))
  archivePath = os.path.join(rootDir, ArchiveName)
  BuildArchive(rootDir, archivePath)
  print(f"Wrote {archivePath}")
```

Run it:

```bash
# Produce the archive from the repo root.
python CreateProjectZip.py
```

## References
- Python `zipfile` module — https://docs.python.org/3/library/zipfile.html
- Python `os.walk` with in-place pruning — https://docs.python.org/3/library/os.html#os.walk
