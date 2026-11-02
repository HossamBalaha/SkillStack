---
name: incident-response-planner
description: Plan incident response with a severity matrix, on-call rotation, communication channels, and a blameless postmortem process. Use this when the user asks to set up an on-call program, define severity levels, or formalize incident command and customer comms.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [incident-response, oncall, severity, postmortem, communication, ic]
related: [devops/sre-runbook-author, devops/disaster-recovery-planner]
prerequisites: [devops/sre-runbook-author]
outputs: [markdown, yaml]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Incident Response Planner

## When To Use

- The user says "set up our incident response process" or "define severity levels".
- The user is standing up an on-call rotation and needs a coverage plan and escalation policy.
- The user wants a clear incident commander (IC) role and a customer communication cadence.
- The user wants a blameless postmortem template rolled out across the team.
- Trigger keywords: incident response, oncall, severity, IC, postmortem, status page.

## Workflow

1. Define the severity matrix (SEV1/SEV2/SEV3) keyed to user impact, response time, and escalation path.
2. Map each severity to a target response time (SEV1: 5 min ack, 30 min mitigation; SEV2: 30 min ack, 4 hr mitigation;
   SEV3: next business day).
3. Define the on-call rotation: primary, secondary, and a manager-on-call; rotate weekly; honor follow-the-sun where
   possible.
4. Pick the paging tool (PagerDuty, Opsgenie) and define escalation policies (5 min primary → 5 min secondary →
   manager).
5. Define communication channels: a dedicated `#incident-<slug>` Slack channel, a status page (Atlassian Statuspage,
   Better Stack), and a war-room Zoom link.
6. Assign incident roles: Incident Commander, Comms Lead, Scribe, Operations Lead. The IC does not fix the bug — they
   coordinate.
7. Draft the timeline template: every action gets a timestamped entry in the Slack channel, captured by the Scribe.
8. Define the customer communication cadence: initial update within 15 min of SEV1 declaration, then every 30 min until
   resolved.
9. Define the postmortem process: open within 24 hr of resolution, blameless, action items with owners and due dates,
   reviewed in a weekly meeting.
10. Run a tabletop exercise quarterly to test the plan; capture gaps as action items.

## Inputs

- Org size and time-zone coverage (single-region vs follow-the-sun).
- Paging tool and escalation policy.
- Customer communication channel (status page, email list, in-app banner).
- Severity thresholds based on the service catalog and SLOs.

## Outputs

- `incident-response-policy.md` — severity matrix, roles, comms cadence.
- `oncall-schedule.yaml` — rotation definition (PagerDuty/Opsgenie compatible).
- `incident-template.md` — Slack channel + status-page scaffold for a declared incident.
- `postmortem-template.md` — blameless postmortem skeleton.
- `tabletop-exercise.md` — quarterly drill scenario.

## Key Rules

- Severity is determined by user impact, not by root cause; a small bug blocking paying customers is SEV1.
- The Incident Commander coordinates; they do not type commands. Keep this separation explicit.
- Customer comms must go out within 15 minutes of a SEV1 declaration, even if all you know is "we are investigating".
- Postmortems are blameless; the Scribe captures facts, not finger-pointing.
- Every action item must have an owner and a due date; a postmortem without owners learns nothing.
- Run a tabletop exercise quarterly; plans that aren't rehearsed decay.

## Examples

```yaml
# oncall-schedule.yaml
schedules:
  - name: payments-primary
    rotation_type: weekly
    layers:
      - name: primary
        members: [alice, bob, carol]
        rotation_length: 1w
        handoff_time: "10:00:00"
        time_zone: UTC
      - name: secondary
        members: [dave, eve, frank]
        rotation_length: 1w
        handoff_time: "10:00:00"
        time_zone: UTC
  escalation_policy:
    name: payments-sev1
    repeat_count: 3
    rules:
      - delay: 300  # 5 min
        targets: [payments-primary]
      - delay: 300
        targets: [payments-secondary]
      - delay: 600
        targets: [payments-manager]
```

```markdown
# Severity Matrix
| SEV | Definition | Ack | Mitigation | Comms |
|-----|------------|-----|------------|-------|
| SEV1 | Customer-facing outage or data loss | 5 min | 30 min | Status page + exec loop, every 30 min |
| SEV2 | Degraded for a segment | 30 min | 4 hr | Status page, every 2 hr |
| SEV3 | No customer impact, cleanup needed | 1 business day | 1 week | Internal only |
```

```markdown
# Incident Command Roles
- **Incident Commander (IC):** coordinates, doesn't type. Declares severity, opens the channel, drives the timeline.
- **Operations Lead:** executes mitigation, runs commands.
- **Comms Lead:** owns status-page updates and the exec loop.
- **Scribe:** timestamps every action in the channel for the postmortem.
```

## References

- PagerDuty Incident Response: https://response.pagerduty.com/
- Atlassian Incident Handbook: https://www.atlassian.com/incident-management/handbook
- Google SRE Book — Incident Response: https://sre.google/sre-book/incident-response/
