# SkillStack — Governance

> How decisions get made in the SkillStack project. Who owns what, how to
> propose a change, how to deprecate a theme, and how conflicts get
> resolved.
>
> Companion to [`CONTRIBUTING.md`](../CONTRIBUTING.md) and
> [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md).
>
> 168 skills · 9 themes · MIT License · by Hossam Magdy Balaha.

---

## 1. Project Structure

SkillStack is **maintainer-led**. The maintainer (Hossam Magdy Balaha) acts
as **Benevolent Dictator For Life (BDFL)** until the v2.0 release. After
v2.0, the project transitions to a **steering committee** model with 3–5
maintainers elected from active contributors.

### 1.1 Roles

| Role            | Who                        | Powers                                                             |
|-----------------|----------------------------|--------------------------------------------------------------------|
| BDFL            | Hossam Magdy Balaha        | Final say on every decision until v2.0                             |
| Maintainer      | Appointed by BDFL          | Merge PRs in their theme, run the manual security review           |
| Contributor     | Anyone with an accepted PR | Propose changes, comment on RFCs, triage issues                    |
| Discussion Lead | Rotating maintainer        | Moderate GitHub Discussions, summarize consensus, escalate to BDFL |

### 1.2 Decision Authority

| Decision                                     | Required approver                | Review window |
|----------------------------------------------|----------------------------------|---------------|
| Doc-only change                              | Any maintainer                   | 2 days        |
| New skill in an existing theme               | Theme's maintainer               | 3 days        |
| New dependency in `requirements-scripts.txt` | BDFL                             | 5 days        |
| Change to a skill's `permissions` block      | BDFL                             | 5 days        |
| New theme                                    | BDFL (after RFC + 30-day review) | 30 days       |
| Deprecate a theme                            | BDFL (after 6-month notice)      | 6 months      |
| Change to `maestro/SKILL.md` routing table   | BDFL                             | 5 days        |
| Change to this governance document           | BDFL                             | 14 days       |
| Change to `LICENSE`                          | BDFL                             | 30 days       |

### 1.3 BDFL Powers And Limits

The BDFL can:

- Merge or reject any PR.
- Appoint or remove maintainers.
- Approve new themes and deprecate existing ones.
- Change the security policy and the governance model.

The BDFL cannot:

- Re-license SkillStack away from MIT without a 30-day community-review
  window.
- Remove the attribution "by Hossam Magdy Balaha" from the root
  `README.md` or the `CITATION.cff`.
- Delete the audit log or rewrite the git history of released tags.

---

## 2. How To Propose A New Theme

A new theme is the biggest structural change you can propose. Follow these
steps:

### Step 1 — Discussion (Day 0)

Open a GitHub Discussion under the "Ideas" category. Sketch:

- The proposed theme folder name (lowercase-kebab-case).
- The theme's purpose in one sentence.
- 8–20 candidate skills (names + one-line descriptions).
- Why none of the existing 9 themes cover this scope.
- The expected overlaps with existing themes.

### Step 2 — Community Review (Days 0–30)

The community discusses the proposal for **30 days**. The Discussion Lead
posts a weekly summary. At day 30, the Discussion Lead closes the discussion
with one of:

- **Consensus** — broad agreement; advance to Step 3.
- **Revision needed** — the proposal needs changes; restart the 30-day
  clock.
- **Rejection** — clear disagreement; close the discussion.

### Step 3 — RFC (Days 30–37)

Draft an RFC as a GitHub issue labelled `rfc`. Include:

- The theme folder name.
- The candidate skill list with one-line descriptions each.
- The proposed `README.md` for the theme.
- The diff to `maestro/SKILL.md`'s routing table (new row, new overlaps in
  the conflict resolver).
- The proposed maintainer for the theme (you, by default, if accepted).

### Step 4 — Maintainer Decision (Days 37–44)

The BDFL (or a delegated maintainer) reviews the RFC and decides:

- **Accept** — the theme is scheduled for the next minor release.
- **Accept with revisions** — the theme is accepted conditional on named
  changes; the proposer has 7 days to land them.
- **Reject** — the RFC is closed with a written explanation. The proposer
  may re-open after 90 days if circumstances have changed.

### Step 5 — Implement (Days 44 → release)

Once accepted:

1. The proposer creates a feature branch `feat/<theme-name>`.
2. The theme folder is added with a `README.md` and the candidate skills.
3. The maestro routing table is updated.
4. `docs/CHANGELOG_SKILLS.md` is updated to list the new theme under the
   upcoming version.
5. The proposer becomes the theme's maintainer (subject to BDFL approval).

### Acceptance Criteria

A new theme is accepted only if it meets **all** of:

- At least 8 skills, each with a complete `SKILL.md` passing the linter.
- A clear scope that does not duplicate more than 30% of any existing
  theme.
- At least one champion (the proposer) willing to maintain it.
- No unresolved objections from the BDFL.

---

## 3. How To Deprecate A Theme

Deprecating a theme is rare and slow on purpose.

### Step 1 — 6-Month Notice

The BDFL opens an issue labelled `deprecation` with:

- The theme name and the sunset date (today + 6 months).
- The reason for deprecation (low usage, superseded by another theme,
  broken upstream, security concern, etc.).
- A draft migration guide.

### Step 2 — Migration Guide (Days 0–30)

A migration guide is added to `docs/MIGRATIONS.md` showing how to move each
skill in the deprecated theme to:

- Another surviving theme, **or**
- A new home outside SkillStack (with a fork link), **or**
- The trash (if the skill is no longer useful).

### Step 3 — Routing-Table Notice (Days 30 → sunset)

The maestro routing table marks the theme as `deprecated: true` with the
sunset date. Every skill in the deprecated theme gains a banner at the top
of its `SKILL.md`:

```markdown
> **⚠ Deprecated.** This skill will be removed on <sunset date>. See
> `docs/MIGRATIONS.md` for the migration path.
```

### Step 4 — Sunset (Month 6)

At sunset:

1. The theme folder is moved to `_archived/<theme>/`.
2. The maestro routing table drops the row.
3. `docs/CHANGELOG_SKILLS.md` lists the removal under the released version.
4. `skills.yaml` is regenerated.

### No-Theme-Left-Behind Rule

A theme cannot be deprecated until **every** skill in it has a documented
migration target. If a skill has nowhere to go, the deprecation is blocked
until the BDFL finds a home or accepts the skill's removal.

---

## 4. Conflict Resolution

### 4.1 Technical Conflicts (Two Skills Seem To Apply)

The maestro's own conflict resolver (`maestro/SKILL.md`, "Skill Conflict
Resolver" section) handles runtime conflicts at the agent level. At the **governance** level, conflicts are resolved by:

1. **Specificity wins.** The more specific skill is preferred.
2. **Primary-artifact wins.** When a task spans themes, route to the
   theme whose declared `Outputs` match the user's primary need.
3. **Asking the user.** When unclear, the maestro asks the user one
   clarifying question with at most 3 options.

### 4.2 Maintainer Conflicts

When two maintainers disagree on a PR:

1. The PR is paused for 48 hours.
2. The Discussion Lead moderates a synchronous (or async) discussion in
   GitHub Discussions.
3. If consensus is reached, the PR proceeds.
4. If consensus is not reached in 7 days, the BDFL decides.

### 4.3 Contributor Conflicts

When a contributor disagrees with a maintainer's rejection:

1. The contributor may ask for a second opinion from another maintainer.
2. The second maintainer may uphold the rejection, overturn it, or ask
   for revisions.
3. If the contributor still disagrees, they may escalate to the BDFL by
   opening an issue labelled `escalation`.
4. The BDFL's decision is final until v2.0.

### 4.4 Code Of Conduct Violations

Reported under [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md). The
maintainer team (currently just the BDFL) reviews reports within 72 hours
and acts within 7 days. See the Code of Conduct for the full enforcement
ladder.

---

## 5. Maintainer Succession

Until v2.0, the BDFL is the sole maintainer. If the BDFL becomes
unresponsive for **90 days** (no commits, no PR reviews, no Discussion
replies), the following succession plan activates:

1. The most-active contributor in the prior 12 months becomes the **acting maintainer**.
2. The acting maintainer has all BDFL powers except: re-licensing, removing
   attribution, and changing this governance document.
3. If the BDFL returns within 12 months, they resume their role.
4. If the BDFL does not return within 12 months, the acting maintainer
   becomes the new BDFL, and the project transitions to the steering
   committee model early.

After v2.0, the project transitions to a **steering committee** of 3–5
maintainers elected from active contributors (defined as: ≥10 merged PRs
in the prior 12 months). The committee elects a chair every 12 months.

---

## 6. Security Governance

Security decisions follow a stricter path:

- Only the BDFL can accept a PR that adds or changes a `permissions`
  block, especially flipping `network: true` or `execute_code: true`.
- Only the BDFL can add a new dependency to `requirements-scripts.txt` or
  `mcp-server/package.json`.
- The full security review process is documented in
  [`docs/SECURITY.md`](SECURITY.md).
- The threat model lives in [`docs/THREAT_MODEL.md`](THREAT_MODEL.md).

---

## 7. License And Attribution

SkillStack is **MIT-licensed** (see [`LICENSE`](../LICENSE)). The
attribution "by Hossam Magdy Balaha" appears in:

- the root `README.md`,
- the `CITATION.cff` (for the GitHub "Cite this repository" button),
- every `SKILL.md`'s `metadata.author` field,
- the maestro's `metadata.author` field,
- the `NOTICE` file.

This attribution is **permanent**. The BDFL cannot remove it (see §1.3
above). Forks must preserve it under the MIT license's attribution clause.

---

## 8. Amendments

This document is amended by the BDFL after a **14-day** community-review
window. Proposed amendments are opened as GitHub issues labelled
`governance-amendment`. At day 14, the BDFL merges, revises, or rejects.

| SkillStack version | Last amended |
|--------------------|--------------|
| 1.0.0              | 2026-11-02   |
