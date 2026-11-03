---
name: prompt-versioning-system
description: Version prompts like code with semantic versioning, A/B testing infrastructure, prompt diffing, and rollback support. Use when prompts ship to production, when a prompt change must be reviewable, when you A/B test variants, or when a regression forces a fast rollback to the last known-good prompt.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [versioning, semver, ab-testing, rollback, llm]
related: [prompt-engineering/prompt-testing-harness, prompt-engineering/system-prompt-architect, prompt-engineering/prompt-template-library]
prerequisites: []
outputs: [python, json, yaml, markdown]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Prompt Versioning System

## When To Use

- Prompts ship to production and a change must be reviewable and rollback-able.
- You run A/B tests between prompt variants and need stable version ids per arm.
- A prompt regression takes the assistant down and you must roll back in minutes, not hours.
- Trigger keywords: prompt versioning, semver, A/B testing, rollback, prompt diff, prompt registry.
- You want CI gates that block prompt merges without a passing eval run.

## Workflow

1. Store each prompt as a file with a frontmatter block: `id`, `version` (semver), `parent` (previous version),
   `changelog`, `eval_run_id`.
2. Apply semantic versioning: **major** for behavior-changing rewrites, **minor** for new optional clauses that preserve
   old behavior, **patch** for typo/format fixes.
3. Compute a deterministic diff between two prompt versions (line-level) and store it alongside the new version.
4. Tag every eval run with the prompt id and version it ran against; never overwrite an eval result.
5. For A/B tests, register two prompt versions as arms and route a percentage of traffic to each; log outcomes per arm.
6. Promote a variant to default only after its eval run beats the baseline on the gate metric within a confidence
   interval.
7. Keep every historical version — rollback is "promote the previous version id to default", not "git revert".
8. Wire a CI gate: a pull request touching a prompt must include an eval run id that passes the gate metric.
9. Maintain a `CHANGELOG.md` per prompt id with one entry per version.

## Inputs

- The prompt file with its current frontmatter.
- The eval run results for the new version (from `prompt-testing-harness`).
- The baseline version id and its eval run id.
- (Optional) A/B traffic split percentages.

## Outputs

- `prompts/<id>/v<major>.<minor>.<patch>.txt` — one file per version, immutable.
- `prompts/<id>/manifest.json` — list of versions with parent links and eval run ids.
- `diffs/<id>/<v1>__<v2>.diff` — line-level diff between consecutive versions.
- `CHANGELOG.md` — per-prompt human-readable changelog.
- `registry.yaml` — current default version per prompt id, used by the serving layer.

## Key Rules

- Prompt files are immutable once written; edits create a new version file.
- Semver discipline: behavior-changing rewrites are major, additive optional clauses are minor, typo fixes are patch.
- Every version must reference an eval run id — no version ships without measured behavior.
- A/B test outcomes must be logged per arm with timestamps; rollback must be a metadata flip, not a code deploy.
- The registry points to the current default version; the serving layer reads the registry, not the file tree.
- Rollback is always available — keep every historical version, even broken ones, for audit.

## Examples

```yaml
# registry.yaml — current default version per prompt id.
Prompts:
  summarization.abstract:
    DefaultVersion: "1.2.0"
    PreviousDefault: "1.1.4"
    RollbackCandidate: "1.1.4"
  support.bot.system:
    DefaultVersion: "3.0.0"
    PreviousDefault: "2.9.1"
    RollbackCandidate: "2.9.1"
```

```python
def PromoteVersion(PromptId, NewVersion, EvalRunId, GateMetric, BaselineMetric, ConfidenceInterval):
  # Compute the lift of the new version over the baseline.
  Lift = GateMetric["Mean"] - BaselineMetric["Mean"]
  # Promote only if the lift is positive and outside the confidence interval.
  if (Lift > 0 and Lift > ConfidenceInterval):
    # Update the registry to point at the new version.
    UpdateRegistry(PromptId, NewVersion, EvalRunId)
    # Append a changelog entry.
    AppendChangelog(PromptId, NewVersion, Lift, EvalRunId)
    # Return a promotion record.
    return {"Status": "Promoted", "Version": NewVersion, "Lift": Lift}
  # Otherwise reject the promotion and keep the baseline.
  return {"Status": "Rejected", "Reason": "Lift below confidence interval.", "Lift": Lift}

def RollbackVersion(PromptId):
  # Read the current registry entry for the prompt.
  Entry = ReadRegistry(PromptId)
  # Restore the previous default as the current default.
  UpdateRegistry(PromptId, Entry["PreviousDefault"], None)
  # Append a changelog entry recording the rollback.
  AppendChangelog(PromptId, Entry["PreviousDefault"], "Rollback from " + Entry["DefaultVersion"], None)
  # Return the rollback record.
  return {"Status": "RolledBack", "From": Entry["DefaultVersion"], "To": Entry["PreviousDefault"]}
```
