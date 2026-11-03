---
name: readme-generator
description: "Generate a `README.md` for any project with a title and one-line hook, a \"What & Why\" section, a zero-to-working quick-start, real tested code examples, per-ecosystem install steps, and only the sections that project actually needs. Use this when scaffolding a new repo or auditing an existing README for source drift. Triggers: README.md, readme generator, quick-start, install instructions, readme audit."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [ readme, documentation, onboarding ]
related: [ project-tooling/sphinx-docs-builder, project-tooling/contribution-guide-builder ]
prerequisites: [ ]
outputs: [ markdown ]
difficulty: beginner
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: [ ]
---

# Readme Generator

## When To Use

- You are starting a new repo and need a README that gets a reader from clone to working in minutes.
- An existing README has drifted from the code (commands fail, paths moved) and needs auditing.
- You want to ship a README that avoids boilerplate ("Contributing", "License" sections that don't apply yet).
- You need per-ecosystem install instructions (Python, Node, R) without copy-pasting templates.

## Workflow

1. Read the repo to identify the language, build tool, entrypoint, and the single most common task.
2. Write a `# Project Name` heading followed by a one-line hook (≤12 words).
3. Add a "What & Why" section (2–4 sentences) answering what the project does and why it exists.
4. Write a "Quick Start" section: clone → install → run, each command tested by actually running it.
5. Add a "Usage" section with 1–2 real, tested code examples — never pseudocode.
6. Add per-ecosystem install notes (Python: `pip install -e .`, Node: `npm ci`, R: `install.packages`).
7. Only add sections this repo needs: skip "Contributing" until there are contributors, skip "Citation" until there's a
   paper.
8. Cross-check every command against the repo: do `pip install -e .` and `python Main.py` actually work?
9. Add a license badge or line only if `LICENSE` exists.
10. Keep the file under ~300 lines; link out to `docs/` for depth.

## Inputs

- The repo root (so the agent can verify commands and paths).
- The primary language / ecosystem.
- The single most important user task (what does a new user do first?).
- Optional badges: CI status, coverage, PyPI version, DOI.

## Outputs

- `README.md` at the repo root.
- A list of any drift found during audit (commands that fail, paths that don't exist).

## Key Rules

- Every command in the README must be runnable as written; if you can't test it, mark it `# Untested:` and stop.
- No pseudocode in examples — only real, copy-pasteable snippets.
- Drop sections that don't apply; an empty "FAQ" is worse than no "FAQ".
- The hook line is mandatory and ≤12 words.
- Install instructions must match the actual ecosystem (don't show `npm` for a Python repo).
- Link to `docs/`, `CHANGELOG.md`, `CONTRIBUTING.md` rather than duplicating their content.
- Use a single `# H1` for the project name; lower-level sections use `##` and `###`.

## Examples

```markdown
# researchkit — Reproducible research utilities that don't get in your way.

## What & Why

researchkit packages the small helpers every lab project ends up writing:
config loaders, seed setters, dataset adapters, and metric calculators.
It exists so we stop copy-pasting the same 200 lines across repos and so
reviewers can rerun results without bespoke setup.

## Quick Start

\`\`\`bash
git clone https://github.com/example/researchkit
cd researchkit
pip install -e ".[dev]"
python Main.py --config configs/QuickStart.yaml
\`\`\`

## Usage

\`\`\`python

# Load a config and run a single training pass.

from src.ConfigLoader import LoadConfig
from src.Trainer import Trainer

config = LoadConfig("configs/QuickStart.yaml")
trainer = Trainer(config)
trainer.Fit()
\`\`\`

## Installation

Python 3.10+ is required.
\`\`\`bash
pip install -e .
\`\`\`

For development extras:
\`\`\`bash
pip install -e ".[dev,test,docs]"
\`\`\`

## License

MIT — see [LICENSE](LICENSE).
```

Audit helper:

```python
# AuditReadme.py — list README commands and try each one.
import re
import subprocess


def ExtractCommands(readmePath):
  # Pull every ```bash block from the README.
  with open(readmePath, "r", encoding="utf-8") as handle:
    text = handle.read()
  blocks = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
  return [line.strip() for block in blocks for line in block.splitlines() if line.strip()]


def RunCommands(commands):
  results = []
  for cmd in commands:
    # Run each command and capture the return code.
    code = subprocess.call(cmd, shell=True)
    results.append((cmd, code))
  return results


if (__name__ == "__main__"):
  for cmd, code in RunCommands(ExtractCommands("README.md")):
    status = "ok" if (code == 0) else "fail"
    print(f"{status}: {cmd}")
```
