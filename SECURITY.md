# Security Policy

## Reporting a Vulnerability

The SkillStack project takes security reports seriously. If you believe you have
found a security vulnerability in SkillStack itself — in a `SKILL.md` workflow, in
one of the `scripts/*.py` helpers, in the `maestro/SKILL.md` routing logic, or in
the MCP server wrapper under `mcp-server/` — please report it privately.

**Do not open a public GitHub issue for security reports.**

Send your report to **Hossam Magdy Balaha** at
[h3ossam@gmail.com](mailto:h3ossam@gmail.com) with the subject line
`[SkillStack Security] <short summary>`. A signed (PGP) report is welcome but not
required.

Please include the following so we can reproduce and triage quickly:

- A clear description of the issue and the impact you observed.
- The exact file path (e.g., `scripts/CacheSkill.py`, `maestro/SKILL.md`, or
  `<theme>/<skill>/SKILL.md`) where the issue lives.
- A minimal reproduction recipe — the smallest input that triggers the issue.
- The SkillStack version (`git rev-parse HEAD` of the commit you tested).
- Your environment: Python version, OS, and any installed packages listed in
  `requirements-scripts.txt` that differ from the pinned versions.
- Any suggested fix or mitigation, if you have one.

## Expected Response Time

| Stage                         | Target                                           |
|-------------------------------|--------------------------------------------------|
| Acknowledgement of receipt    | 72 hours                                         |
| Initial assessment + triage   | 7 days                                           |
| Fix or mitigation published   | 14 days                                          |
| Public disclosure (if agreed) | After fix is released, coordinated with reporter |

If a report requires deeper investigation (e.g., a routing-logic flaw that
affects multiple themes), we will share a revised timeline within the 7-day
assessment window and keep you informed at least every 72 hours until the fix
ships.

Reports that turn out to be bugs rather than security issues will be re-filed as
public GitHub issues with credit to the reporter (unless you ask to remain
anonymous).

## Supported Versions

SkillStack follows a single-live-major support model. Only the **latest major
release** on the `main` branch receives security fixes.

| Version | Supported          |
|---------|--------------------|
| 1.x     | Yes (latest minor) |
| < 1.0   | No                 |

Pre-release branches (`v1.1-rc`, `v2.0-dev`, etc.) are not supported for
security backports — pin to a tagged release on `main` for any production use.

## Scope

**In scope:**

- Every `SKILL.md` shipped under the 9 theme folders (`academic-research`,
  `style-integrity`, `ml-engineering`, `data-engineering`, `visualization`,
  `writing-citation`, `ai-text`, `ai-output-judgement`, `project-tooling`) and
  the `maestro/SKILL.md` orchestrator.
- Every helper script under `scripts/*.py` (the linter, citation verifier,
  coverage report generator, link checker, audit logger, exporter, browser,
  smoke test, maestro test, and skill CLI).
- The `mcp-server/` Node.js wrapper and its `package.json` dependency manifest.
- The auto-generated `skills.yaml` manifest and `export/anthropic/` outputs.

**Out of scope:**

- Third-party tools, libraries, and web services that SkillStack skills *reference* (Optuna, PyTorch Lightning, Hugging
  Face Hub, spaCy, Crossref,
  arXiv, Semantic Scholar, Connected Papers, Inciteful, Graphviz, Streamlit,
  FastAPI, Docker, etc.). Report their security issues to the upstream project.
- Vulnerabilities in the user's own data, codebase, or environment that a skill
  merely processes (e.g., a PII leak in a CSV the user passed to
  `data-anonymizer`). SkillStack skills operate on user-supplied data and do not
  transport it anywhere except where the skill explicitly documents.
- Findings from automated scanners that have not been manually triaged — please
  confirm a real exploit before reporting.

If you are unsure whether something is in scope, err on the side of reporting
privately — we will route it appropriately.

## Responsible Disclosure

We ask that you:

- Give us reasonable time (the targets above) to triage and fix the issue before
  any public disclosure.
- Avoid accessing or modifying data that does not belong to you.
- Do not degrade service availability (SkillStack ships no hosted service, but
  please do not hammer the Crossref / arXiv / Hugging Face endpoints a skill
  calls during your reproduction).
- Test only against your own repositories and your own SkillStack fork.

In return, we will:

- Acknowledge your report in the fix release notes (unless you prefer to remain
  anonymous).
- Credit you in `docs/CHANGELOG_SKILLS.md` under the relevant version.
- Coordinate public disclosure timing with you.

## Security Review Process

Every contribution that touches `scripts/*.py`, `maestro/SKILL.md`, the MCP
server, or any skill's `permissions` block must pass the following review before
merge:

1. **Lint pass** — `python scripts/LintSkills.py` must exit zero.
2. **Smoke pass** — `python scripts/SmokeTest.py` must report every skill as
   pass (no fenced Python code block in any `SKILL.md` may raise an unhandled
   exception within the 10-second subprocess timeout).
3. **Maestro routing pass** — `python scripts/TestMaestro.py` must report all
   50 routing cases as pass.
4. **Citation pass** — `python scripts/VerifyCitations.py` must exit zero.
5. **Link pass** — `python scripts/CheckLinks.py` must exit zero.
6. **Manual diff review** — a maintainer reviews the diff for any new outbound
   network call, new file write outside the declared `Outputs`, or any change to
   a skill's `permissions` block (especially `network: true` or
   `execute_code: true`).

Run `python scripts/LintSkills.py`, `python scripts/SmokeTest.py`, and `python scripts/TestMaestro.py` manually before
each release. Previously automated by
every push to `main` and on every pull request.

## Security Contact

The sole security contact is the project maintainer:

- **Hossam Magdy Balaha**
- Email: [h3ossam@gmail.com](mailto:h3ossam@gmail.com)
- GitHub: [@HossamBalaha](https://github.com/HossamBalaha)

A backup contact will be added if and when a co-maintainer is appointed (see
`docs/GOVERNANCE.md` for the maintainer-succession plan).
