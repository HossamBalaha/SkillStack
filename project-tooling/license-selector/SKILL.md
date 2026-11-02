---
name: license-selector
description: "Select an open-source license (MIT, Apache-2.0, GPL-3.0, AGPL-3.0, BSD-2/3-Clause) based on the project's use case, generate the matching `LICENSE` file text, and add the SPDX `license` field to `pyproject.toml`. Use this when bootstrapping a repo or auditing license consistency. Triggers: LICENSE, MIT, Apache-2.0, GPL, AGPL, BSD, choose a license, SPDX."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [license, mit, apache, gpl, spdx]
related: [project-tooling/readme-generator, project-tooling/pyproject-toml-builder, project-tooling/contribution-guide-builder]
prerequisites: []
outputs: [markdown, bash]
difficulty: beginner
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# License Selector

## When To Use

- You are bootstrapping a repo and need to pick a license before the first public commit.
- You are auditing an existing repo where `LICENSE` and `pyproject.toml` disagree.
- You need to weigh permissive vs copyleft vs network-copyleft for a specific distribution model.
- You need a patent grant (Apache-2.0) or strong copyleft (GPL/AGPL) for compliance reasons.

## Workflow

1. Ask the caller: who owns the copyright, will the project be distributed, will it run as a network service?
2. Map the answer to a license:
    - MIT / BSD-3-Clause — permissive, no patent grant, simplest.
    - Apache-2.0 — permissive + explicit patent grant, good for corporate contributions.
    - GPL-3.0 — copyleft, derivative works must also be GPL.
    - AGPL-3.0 — network copyleft, SaaS uses must share source.
    - BSD-2-Clause — permissive, minimal, no patent grant.
3. Generate the `LICENSE` file with the chosen license's full text.
4. Replace the placeholder year and copyright holder name in the header.
5. Add the SPDX `license` field to `pyproject.toml` (`license = { text = "Apache-2.0" }`).
6. Add a `LICENSE` link in the README and a badge if desired.
7. Verify consistency: the README, `pyproject.toml`, and `LICENSE` all cite the same SPDX id.
8. If the repo bundles third-party code, add a `NOTICE` file listing their licenses.

## Inputs

- Copyright holder name and year.
- Distribution model: distributed binary, source-only, or network service.
- Patent-grant preference (yes/no).
- Copyleft preference (permissive / copyleft / network-copyleft).

## Outputs

- `LICENSE` file at the repo root with the chosen license's full text.
- Updated `license` field in `pyproject.toml`.
- A README note pointing at the `LICENSE` file.
- Optional `NOTICE` file when third-party code is bundled.

## Key Rules

- The SPDX id in `pyproject.toml` MUST exactly match the license in `LICENSE` (e.g. `Apache-2.0`, not "Apache 2").
- The copyright line in `LICENSE` must include the year and the holder's name; never leave `<name>` or `[year]`
  placeholders.
- Never pick GPL-3.0 for a repo that bundles MIT-only dependencies without checking compatibility — MIT is
  GPL-compatible, but not everything is.
- AGPL-3.0 is the only option if the code will run as a network service and you want to enforce source sharing.
- The `LICENSE` file name is uppercase `LICENSE` (not `LICENSE.md` or `LICENSE.txt`) so GitHub renders the badge.
- Do not invent license text — only emit canonical text from choosealicense.com (paraphrased in this skill, reproduced
  verbatim in the file).
- If the project is dual-licensed, write both in the `LICENSE` file and list both SPDX ids in `pyproject.toml`.

## Examples

Decision helper:

```python
# ChooseLicense.py — pick an SPDX id from the caller's answers.
def ChooseLicense(distributed, networkService, patentGrant, copyleft):
  # Network services default to AGPL for strongest copyleft.
  if (networkService and copyleft == "network"):
    return "AGPL-3.0"
  if (copyleft == "strong"):
    return "GPL-3.0"
  if (patentGrant):
    return "Apache-2.0"
  return "MIT"


if (__name__ == "__main__"):
  # Example: distributed source, no network service, want patent grant.
  print(ChooseLicense(distributed=True, networkService=False, patentGrant=True, copyleft="none"))
```

`pyproject.toml` snippet:

```toml
[project]
name = "researchkit"
license = { text = "Apache-2.0" }
```

README badge:

```markdown
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
```

`LICENSE` header (Apache-2.0 example):

```text
Apache License 2.0

Copyright 2026 Lab Tooling

Licensed under the Apache License, Version 2.0 (the "License");
... (full Apache-2.0 text follows) ...
```

## References

- Choose a License — https://choosealicense.com
- SPDX license list — https://spdx.org/licenses/
- GitHub licensing a
  repository — https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
