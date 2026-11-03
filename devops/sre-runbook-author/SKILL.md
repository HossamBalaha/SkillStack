---
name: sre-runbook-author
description: Author SRE runbooks tied to specific alerts, covering severity, symptoms, diagnosis steps, mitigation, escalation, and a blameless postmortem template. Use this when the user asks to write a runbook, document alert response, or formalize on-call playbooks.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [runbook, sre, alert, postmortem, escalation, oncall]
related: [devops/incident-response-planner, devops/grafana-dashboard-builder, devops/observability-stack-builder]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 1400
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# SRE Runbook Author

## When To Use

- The user says "write a runbook for this alert" or "document how to handle HighLatency alerts".
- The user is building an on-call playbook and needs one runbook per alert.
- The user wants a blameless postmortem template the team can reuse after every incident.
- Trigger keywords: runbook, playbook, alert response, oncall, postmortem, severity.

## Workflow

1. List every alert that fires for the service (from Prometheus/Grafana alert rules).
2. For each alert, create a runbook file named after the alert: `runbooks/<AlertName>.md`.
3. Fill the header: alert name, severity (P1/P2/P3), owning team, source query, dashboard link, related SLI/SLO.
4. Document Symptoms: what the user/operator sees (error spike, latency p99 > threshold, queue backlog).
5. Document Diagnosis: ordered checks against dashboards, logs, traces, and dependency health pages.
6. Document Mitigation: short-term fix (rollback, scale out, drain a node, restart a pod) with exact commands.
7. Document Escalation: who to page next, in what order, with a 5-minute response expectation.
8. Document Resolution: how to verify the alert clears and the SLO recovers.
9. Append the blameless postmortem template at the bottom: summary, timeline, impact, root cause, contributing factors,
   action items with owners and due dates.
10. Link the runbook URL into the alert's `annotations.runbook_url` so it shows in alertmanager and PagerDuty.

## Inputs

- Alert name, expression, severity, and SLO it protects.
- Owning team and on-call rotation.
- Dashboards, logs, and traces the operator should consult.
- Runbook URL prefix for the alert annotations.

## Outputs

- `runbooks/<AlertName>.md` — one runbook per alert.
- `templates/postmortem.md` — blameless postmortem template.
- `runbooks/README.md` — index linking every runbook and the alert it maps to.

## Key Rules

- Every alert must have a runbook; alerts without runbooks are noise the on-call engineer has to triage cold.
- Severity maps to user impact: P1 = customer down, P2 = degraded for a segment, P3 = no customer impact but cleanup
  needed.
- Diagnosis steps must be copy-pasteable commands, not vague "check the dashboard" prose.
- Mitigation must include the rollback command, not just "consider rolling back".
- Blameless postmortems focus on systems and process, never on individuals; the template enforces this.
- Action items must have owners and due dates; without them, postmortems are theater.
- Re-test the runbook quarterly; a runbook that didn't survive an outage is worse than none.

## Examples

```markdown
# Runbook: HighErrorRate

- **Alert name:** HighErrorRate
- **Severity:** P1
- **Owner:** payments-team
- **Source:** `job:http_errors:ratio_rate5m > 0.01 for 10m`
- **Dashboard:** https://grafana.example.com/d/api-overview
- **SLI:** 99.9% of requests succeed over 28 days.

## Symptoms
- 5xx error ratio above 1% for 10 minutes.
- Customer reports of failed checkouts.

## Diagnosis
1. Open the API Overview dashboard, filter to the affected `job`.
2. Check `/var/log/payments/errors.log` for stack traces:
   `kubectl logs -n prod deploy/payments-api | grep -i error`
3. Check dependency health: Postgres connection pool, Redis, Stripe API status page.
4. Check recent deploys: `kubectl rollout history deploy/payments-api -n prod`.

## Mitigation
- Roll back to the last known-good version:
  `kubectl rollout undo deploy/payments-api -n prod`
- If a downstream is down, fail closed and surface a clean error.

## Escalation
1. Primary on-call (5-min ack) — PagerDuty schedule `payments-primary`.
2. Secondary on-call — PagerDuty schedule `payments-secondary`.
3. Service owner — Slack `#payments-team`.

## Resolution
- Confirm `job:http_errors:ratio_rate5m` drops below 0.01 for 10 minutes.
- Confirm the SLO burn-rate alert clears.
```

```markdown
# Postmortem Template

## Summary
One-paragraph description of what happened and customer impact.

## Timeline (UTC)
- 14:03 — Alert HighErrorRate fired.
- 14:05 — On-call acknowledged.
- 14:08 — Rollback initiated.
- 14:12 — Error ratio recovered.

## Impact
- 4,200 failed checkouts (~0.3% of traffic) over 9 minutes.
- 99.85% availability for the day; SLO burn-rate consumed 6 hours of 28-day budget.

## Root Cause
A migration added a NOT NULL column without a default; reads on the legacy code path threw.

## Contributing Factors
- No canary stage before full rollout.
- Migration linting CI check was disabled two weeks ago.

## Action Items
- [ ] Re-enable migration lint CI — @alice — 2025-02-15
- [ ] Add a canary stage to the deploy pipeline — @bob — 2025-02-28
- [ ] Add a synthetic checkout test — @carol — 2025-03-10
```
