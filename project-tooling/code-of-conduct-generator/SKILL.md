---
name: code-of-conduct-generator
description: "Generate a `CODE_OF_CONDUCT.md` based on the Contributor Covenant (latest version), with the enforcement contact filled in. Use this when opening a repo to public contributors or when an existing code of conduct is missing or outdated. Triggers: CODE_OF_CONDUCT.md, contributor covenant, code of conduct, enforcement contact."
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: project-tooling
tags: [code-of-conduct, community, contributor-covenant, scaffolding]
related: [project-tooling/contribution-guide-builder, project-tooling/license-selector]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Code Of Conduct Generator

## When To Use
- You are opening a repo to public contributors and need a code of conduct.
- An existing `CODE_OF_CONDUCT.md` references an outdated Contributor Covenant version.
- A funding body or venue requires a code of conduct as part of submission.
- You need to point contributors at a clear enforcement contact.

## Workflow
1. Confirm the latest stable Contributor Covenant version (currently 2.1).
2. Ask the caller for the enforcement contact email (e.g. `conduct@example.org`).
3. Emit the canonical Contributor Covenant text with the contact placeholder filled in.
4. Save the file as `CODE_OF_CONDUCT.md` at the repo root.
5. Add a one-line link in the README and in `CONTRIBUTING.md`.
6. Cross-check that the email is reachable and that a human monitors it.
7. If the project has multiple maintainers, append a short "Maintenance team" section listing who handles reports.
8. Re-verify the version pin if a new Contributor Covenant release ships.

## Inputs
- Enforcement contact email (mandatory).
- Optional: a list of maintainers who handle reports.
- Optional: project-specific additions (e.g. an offline reporting address for events).

## Outputs
- `CODE_OF_CONDUCT.md` at the repo root.
- A README link to it.
- An updated `CONTRIBUTING.md` that references the code of conduct.

## Key Rules
- Use the canonical Contributor Covenant text verbatim — do not paraphrase its core pledges.
- The enforcement contact MUST be a real, monitored address; never a placeholder like `you@example.com`.
- Pin the version explicitly at the top (`Contributor Covenant Code of Conduct v2.1`) so audits are unambiguous.
- Do not invent project-specific rules that contradict the Covenant (e.g. "no politics allowed").
- Reports are handled in confidence; the file must state this.
- If the project hosts in-person events, add the event-specific reporting path.

## Examples
`CODE_OF_CONDUCT.md` (excerpt):

```markdown
# Contributor Covenant Code of Conduct

## Our Pledge
We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards
Examples of behavior that contributes to a positive environment for our
community include:
- Demonstrating empathy and kindness toward other people.
- Being respectful of differing opinions, viewpoints, and experiences.
- Giving and gracefully accepting constructive feedback.
- Accepting responsibility and apologizing to those affected by our mistakes.

Examples of unacceptable behavior include:
- The use of sexualized language or imagery, and sexual attention or advances.
- Trolling, insulting or derogatory comments, and personal or political attacks.
- Public or private harassment.
- Publishing others' private information without explicit permission.

## Enforcement Responsibilities
Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

## Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at
**conduct@example.org**. All complaints will be reviewed and investigated
promptly and fairly. All community leaders are obligated to respect the privacy
and security of the reporter of any incident.

## Enforcement Guidelines
Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:
1. Correction.
2. Warning.
3. Temporary Ban.
4. Permanent Ban.

## Attribution
This Code of Conduct is adapted from the Contributor Covenant, version 2.1,
available at https://www.contributor-covenant.org/version/2/1/code_of_conduct.html.
```

README link:

```markdown
This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
```

## References
- Contributor Covenant — https://www.contributor-covenant.org
- Contributor Covenant v2.1 text — https://www.contributor-covenant.org/version/2/1/code_of_conduct.html
- GitHub community code of conduct docs — https://docs.github.com/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project
