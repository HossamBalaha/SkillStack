# SkillStack — Public Roadmap

> What's shipped, what's planned, what's on the maybe-pile.
> Dates are targets, not commitments. Subscribe to GitHub Releases for
> actual ship dates.
>
> 168 skills · 9 themes today · 14 themes planned · MIT License · by Hossam
> Magdy Balaha.

---

## Status Legend

- 🟢 **Released** — shipped on `main`, tagged, in `CHANGELOG_SKILLS.md`.
- 🟡 **Planned** — accepted on the roadmap, scope drafted, target version
  assigned.
- 🔵 **Considering** — actively discussed, scope not yet stable.
- ⚪ **Backlog** — captured for the future, no concrete plan yet.

---

## v1.0.0 — Released 2026-11-02 🟢

**Scope:** the initial public release of SkillStack.

- 168 skills organized into 9 independent theme folders.
- 1 maestro orchestrator (`maestro/SKILL.md`) with the 9-theme routing table,
  conflict resolver, fallback chain, and confidence-scoring heuristic.
- 11 CamelCase Python helper scripts under `scripts/` (linter, manifest
  generator, skill CLI, citation verifier, link checker, coverage report,
  graph renderer, audit logger, cacher, exporter, skill-health).
- 50-prompt routing regression suite in `maestro/test-cases.md`.
- MCP server wrapper under `mcp-server/`.
- Trilingual maestro (`SKILL.md`, `SKILL.ar.md`, `SKILL.zh.md`).
- Doc set: `README.md`, `QUICKSTART.md`, `COOKBOOK.md`, `FAQ.md`,
  `COMPARISON.md`, `AUTHORING_GUIDE.md`, `Coverage.md`.
- MIT-licensed, authored by Hossam Magdy Balaha.

The 9 shipped themes:

1. `academic-research` — 20 skills (research planning & writing).
2. `style-integrity` — 18 skills (LaTeX, prose, coding conventions).
3. `ml-engineering` — 22 skills (PyTorch, training, validation).
4. `data-engineering` — 18 skills (ETL, schemas, lineage).
5. `visualization` — 18 skills (figures, TikZ, posters).
6. `writing-citation` — 18 skills (BibTeX, editing, paraphrasing).
7. `ai-text` — 15 skills (detect & humanize AI text).
8. `ai-output-judgement` — 18 skills (judge & verify AI outputs).
9. `project-tooling` — 20 skills (packaging, Docker, CI/CD).

---

## v1.1 — Planned 🟡 (target: Q1 2027)

**Scope:** five new themes, bringing the total from 9 → 14.

1. **`prompt-engineering`** — prompt templates, few-shot scaffolding,
   chain-of-thought guards, prompt-injection hardening, system-prompt
   audits. Planned ~12 skills.
2. **`ethics-compliance`** — IRB protocols, GDPR / CCPA workflows, AI-act
   risk classification, model-card authoring, impact-assessment drafts.
   Planned ~10 skills.
3. **`devops`** — Terraform / Pulumi patterns, Kubernetes manifests,
   observability (Prometheus, OpenTelemetry), SLO/SLI authoring, on-call
   runbooks. Planned ~12 skills.
4. **`teaching-pedagogy`** — lesson plans, Bloom-taxonomy mapping, rubric
   authoring, formative-assessment design, course-syllabus scaffolding.
   Planned ~10 skills.
5. **`data-storytelling`** — narrative from data, dataviz annotation,
   audience-tailored decks, infographic drafting, executive summaries.
   Planned ~10 skills.

The maestro routing table will grow to 14 rows; the conflict resolver will
gain the obvious overlaps (`prompt-engineering` vs `ai-text`, `devops` vs
`project-tooling`, `teaching-pedagogy` vs `academic-research`,
`data-storytelling` vs `visualization`).

Total skill count after v1.1: **~222 skills** across 14 themes.

---

## v1.2 — Planned 🟡 (target: Q2 2027)

**Scope:** integrations and live-test infrastructure.

- **MCP live-test suite.** A Node + Python harness that boots the
  `mcp-server/`, routes the 50 maestro test prompts through it, and
  asserts the routed skill matches `maestro/test-cases.md`. Replaces the
  pure-Python keyword-matcher in `scripts/TestMaestro.py` with an
  end-to-end check.
- **Native Cursor extension.** A first-class Cursor integration that
  loads `maestro/SKILL.md` as a project rule, surfaces the routing table
  in the Cursor UI, and adds a `SkillStack: Route` command palette entry.
- **Streamlit browser v2.** Upgrade `scripts/SkillBrowser.py` with theme
  coverage bars, tag cloud, related-skill sidebar, and a "run the
  Examples" button that delegates to `SmokeTest.py` on the selected
  skill.
- **Trilingual coverage.** Every theme's `README.md` translated to
  Arabic and Chinese, matching the existing trilingual maestro.

No new themes in v1.2; theme count stays at 14.

---

## v2.0 — Considering 🔵 (target: Q4 2027)

**Scope:** the multi-surface release.

- **VS Code extension.** A bundled extension that ships the maestro, the
  browser, and a side-panel "Route this task" button. Syntax-highlighted
  `SKILL.md` preview, one-click copy of the routed skill's path.
- **GitHub Pages site.** A static site generated from `skills.yaml` with
  browse-by-theme, browse-by-tag, full-text search, and a per-skill page
  rendering the `SKILL.md` body. The `docs/assets/overview.svg` infographic
  becomes the site hero.
- **Standalone website.** A marketing site at `skillstack.dev` with the
  hero infographic, the 14-theme circle, the maestro explainer, and a
  "Try SkillStack in your agent" call-to-action.
- **`pytorch` skill pack.** A new theme (`pytorch-deep`) covering custom
  autograd functions, Triton kernels, `torch.compile` recipes, FSDP
  patterns. Planned ~15 skills.

Theme count after v2.0: **15 themes** (14 + `pytorch-deep`).

---

## Backlog ⚪

Items captured but not yet scheduled:

- **Theme: `mlops`.** Model registry, feature-store ops, drift alerting,
  shadow-deploy patterns. Distinct from `devops` and `ml-engineering`.
- **Theme: `security`.** Threat-modeling skills, SBOM generation, secret
  scanning, dependency-vuln triage. Distinct from `ethics-compliance`.
- **Native Claude Code / Cursor / Continue integrations** for each theme.
- **Skill versioning.** Per-skill semver in the frontmatter, with a
  `migration.md` per skill when its workflow changes shape.
- **Skill composition graph.** A UI for browsing skill chains as a DAG (extends `scripts/GraphvizChains.py` with
  interactivity).
- **Trilingual expansion.** After Arabic + Chinese, add Spanish, French,
  German, Japanese.
- **Skill ratings.** Opt-in usage telemetry (locally stored) that ranks
  skills by invocation frequency, with a "most-used" leaderboard in the
  Streamlit browser.
- **AI-red-team theme.** Skills for red-teaming LLMs: adversarial prompt
  generation, jailbreak catalogues, automated jailbreak discovery,
  model-extraction attack patterns.

None of these have a target version. Open an issue on the SkillStack repo
to discuss scope before drafting an RFC.

---

## How To Propose A New Theme Or Skill

1. **Open a discussion** in GitHub Discussions under the "Ideas" category.
   Sketch the theme's purpose, its 8–20 candidate skills, and why the
   existing themes don't cover it.
2. **Wait for community feedback** (30-day review window, see
   `docs/GOVERNANCE.md`).
3. **Draft an RFC** as a GitHub issue labelled `rfc`. Include the proposed
   theme folder name, the candidate skill list, overlaps with existing
   themes, and the routing-table diff for `maestro/SKILL.md`.
4. **Maintainer decision.** The BDFL (Hossam) accepts, rejects, or asks
   for revisions.
5. **Implement.** Once accepted, the new theme lands in a feature branch
   and ships in the next minor release (`v1.1`, `v1.2`, …).

---

## How A Theme Gets Deprecated

1. The BDFL opens an issue labelled `deprecation` with a 6-month notice.
2. A migration guide is added to `docs/` showing how to move each skill
   to the surviving themes (or to a new home outside SkillStack).
3. The maestro routing table is updated to mark the theme as
   `deprecated: true` with the sunset date.
4. At sunset, the theme folder is moved to `_archived/<theme>/` and the
   manifest is regenerated.

No theme has been deprecated yet. See `docs/GOVERNANCE.md` for the full
deprecation policy.

---

## Release Cadence

| Version | Target     | Status      | Theme count | Skill count |
|---------|------------|-------------|-------------|-------------|
| 1.0.0   | 2026-11-02 | Released    | 9           | 168         |
| 1.1     | Q1 2027    | Planned     | 14          | ~222        |
| 1.2     | Q2 2027    | Planned     | 14          | ~225        |
| 2.0     | Q4 2027    | Considering | 15          | ~245        |

Dates are **targets**, not commitments. Subscribe to GitHub Releases for
actual ship dates.
