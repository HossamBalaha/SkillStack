---
name: disaster-recovery-planner
description: Plan disaster recovery with RTO/RPO targets, backup strategies, multi-region failover, and restore testing. Use this when the user asks to write a DR plan, define RTO/RPO per workload, or schedule restore drills.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [disaster-recovery, rto, rpo, backup, failover, multi-region]
related: [devops/incident-response-planner, devops/capacity-planner, devops/secrets-management-builder]
prerequisites: [devops/incident-response-planner]
outputs: [markdown, yaml]
difficulty: advanced
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Disaster Recovery Planner

## When To Use

- The user says "write a DR plan" or "define RTO/RPO for our services".
- The user wants to design multi-region failover (active-active vs active-passive).
- The user wants a backup strategy for stateful workloads (Postgres, Kafka, object storage).
- The user wants to schedule and run restore drills.
- Trigger keywords: disaster recovery, rto, rpo, failover, backup, restore, multi-region, dr-drill.

## Workflow

1. Classify each service by criticality tier (Tier 1 = customer-facing critical, Tier 2 = internal critical, Tier 3 =
   best-effort).
2. Assign RTO/RPO per tier (Tier 1: RTO 15 min, RPO 1 min; Tier 2: RTO 4 hr, RPO 1 hr; Tier 3: RTO 24 hr, RPO 24 hr).
3. Pick a failover topology per tier:
    - active-active for Tier 1 (both regions serve live traffic);
    - active-passive with warm standby for Tier 2;
    - backup-restore for Tier 3.
4. Define backup strategy per data store:
    - Postgres: WAL streaming to standby + daily snapshot to object storage;
    - Kafka: MirrorMaker 2 cross-region replication;
    - object storage (S3): cross-region replication.
5. Define the failover runbook: detect failure → declare → route DNS to standby → verify → communicate.
6. Define the restore runbook: identify backup → restore to staging → verify integrity → cut over.
7. Schedule quarterly restore drills; capture the time-to-restore as evidence the RTO is achievable.
8. Define data validation checks post-restore (row counts, checksums, business-level spot checks).
9. Document the blast radius per failure scenario (single AZ, single region, vendor outage).
10. Review the plan annually; capture changes from architecture drift between drills.

## Inputs

- Service catalog with criticality tiers.
- Data stores and their backup tools (pgBackRest, Velero, AWS Backup, MirrorMaker 2).
- Region topology (single-region, multi-region active-active, pilot-light).
- Regulatory constraints (data residency, retention).

## Outputs

- `dr-plan.md` — tier table, RTO/RPO, failover and restore runbooks.
- `backup-strategy.md` — per-data-store backup config and retention.
- `failover-runbook.md` — step-by-step regional failover.
- `restore-runbook.md` — step-by-step restore from backup.
- `dr-drill.md` — quarterly drill scenario, scope, and pass criteria.

## Key Rules

- RTO is what the business can tolerate; RPO is how much data the business can afford to lose. Never set them from what
  the tool can do — set them from what the business needs.
- Backups that are never restored are untested assumptions; schedule drills and treat them as production events.
- Multi-region failover requires DNS to be the routing layer; use Route53 health checks or Cloudflare load balancer.
- Cross-region replication must be measured; if RPO is 1 min, replication lag must be under 60s under load.
- Restore drills must validate data, not just that the command succeeded — run row counts and business spot checks.
- Each tier's RTO/RPO must be achievable end-to-end; partial restores that miss a dependent service fail the tier.
- Document the blast radius so the team knows which user journeys break per failure scenario.

## Examples

```text
# dr-plan.md — tier table.
| Tier | Service              | RTO    | RPO   | Topology         | Backup                    |
|------|----------------------|--------|-------|------------------|---------------------------|
| 1    | payments-api         | 15 min | 1 min | active-active    | WAL streaming + snapshot  |
| 1    | payments-db (RDS)    | 15 min | 1 min | multi-AZ + cross | pgBackRest + S3 copy      |
| 2    | reporting-api        | 4 hr   | 1 hr  | active-passive   | daily snapshot            |
| 3    | batch-loader         | 24 hr  | 24 hr | backup-restore   | daily snapshot            |
```

```yaml
# backup-strategy.md — per-data-store config.
postgres:
  tool: pgBackRest
  mode: archive + full
  full_schedule: "0 2 * * 0"  # weekly full
  diff_schedule: "0 2 * * 1-6"  # daily diff
  archive: true
  retention_full: 4
  retention_diff: 7
  copy_to_s3: true
  s3_bucket: dr-pgbackrest
kafka:
  tool: MirrorMaker 2
  mode: active-active
  checkpoint_interval: 5s
  sync_group_offsets: true
s3:
  replication: cross-region
  versioning: true
  mfa_delete: false
```

```text
# dr-drill.md — quarterly scenario.
Scenario: Region us-east-1 outage (simulated by blocking the VPC peering).

Scope: Tier 1 services (payments-api, payments-db).

Pass criteria:
  - DNS failover to us-west-2 completes within 5 minutes.
  - Payments API serving live traffic in us-west-2 within 15 minutes of failure detection.
  - Replication lag measured at the moment of failure < 60s (RPO met).
  - Zero data loss on completed payments; pending payments drained to DLQ.

Drill date: 2025-Q1.
Drill owner: DR on-call (rotate).
Result: PASS / FAIL with action items.
```

## References

- AWS Well-Architected Reliability
  Pillar: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
- AWS Disaster Recovery
  Strategies: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/disaster-recovery-dr.html
- Google SRE Workbook — Disaster Recovery: https://sre.google/workbook/disaster-recovery/
- pgBackRest: https://pgbackrest.org/
