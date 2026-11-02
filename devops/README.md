# 🛠️ DevOps — Infrastructure, Delivery & Reliability

> Build Kubernetes manifests, Helm charts, and Terraform modules; wire CI/CD pipelines and GitOps; ship hardened
> container images; configure service meshes and secrets; stand up observability stacks; and author SRE runbooks,
> incident
> response plans, and disaster recovery playbooks. Skills span the full cloud-native delivery and reliability
> lifecycle —
> from `kubectl apply` to a blameless postmortem. Use this theme whenever the deliverable is platform infrastructure, a
> deploy pipeline, or an operational runbook.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-18-blue)]()
[![Theme](https://img.shields.io/badge/Theme-devops-green)]()

</div>

## Theme Overview

This folder contains **18 skills** in the `devops/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                 | Description                                                                                                                                                                                                                                                                                                                | Difficulty   | Tags                                                                                    | Related                                                                                                                                         |
|----|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`kubernetes-manifest-builder`](kubernetes-manifest-builder/SKILL.md) | Build production Kubernetes manifests covering Deployments, Services, ConfigMaps, Secrets, Ingress, and PersistentVolumeClaims with resource limits, probes, and security context. Use this when the user asks to write K8s YAML, deploy an app to a cluster, expose a service, or wire up ingress and persistent storage. | intermediate | `kubernetes`, `manifests`, `deployment`, `configmap`, `ingress`, `pvc`                  | `devops/helm-chart-author`, `devops/health-endpoint-designer`, `devops/gitops-deployment-builder`                                               |
| 2  | [`helm-chart-author`](helm-chart-author/SKILL.md)                     | Author Helm charts with a valid Chart.yaml, values.yaml, templates/ tree, _helpers.tpl, and lifecycle hooks. Use this when the user wants to package an app for Helm, parameterize an existing manifest, or add pre-install/post-upgrade hooks.                                                                            | intermediate | `helm`, `chart`, `templates`, `values`, `hooks`, `kubernetes`                           | `devops/kubernetes-manifest-builder`, `devops/gitops-deployment-builder`                                                                        |
| 3  | [`terraform-module-author`](terraform-module-author/SKILL.md)         | Author reusable Terraform modules with variables.tf, main.tf, outputs.tf, versions.tf, and a README following the standard module structure. Use this when the user asks to write IaC for AWS/GCP/Azure, factor a stack into modules, or publish a module to the Terraform Registry.                                       | intermediate | `terraform`, `iac`, `module`, `variables`, `outputs`, `aws`                             | `devops/secrets-management-builder`, `devops/ci-cd-pipeline-builder`                                                                            |
| 4  | [`prometheus-metrics-designer`](prometheus-metrics-designer/SKILL.md) | Design Prometheus metrics with correct types (counter, gauge, histogram, summary), naming conventions, bounded label cardinality, and recording rules for high-cardinality queries. Use this when the user asks to instrument an app for Prometheus, define SLI metrics, or precompute heavy queries with recording rules. | intermediate | `prometheus`, `metrics`, `labels`, `recording-rules`, `cardinality`, `sli`              | `devops/grafana-dashboard-builder`, `devops/observability-stack-builder`                                                                        |
| 5  | [`grafana-dashboard-builder`](grafana-dashboard-builder/SKILL.md)     | Build Grafana dashboards as JSON with chosen panel types, PromQL queries, templating variables, and alerting thresholds aligned to SLOs. Use this when the user asks to visualize Prometheus metrics, build a service overview dashboard, or wire alerts to a notification channel.                                        | intermediate | `grafana`, `dashboard`, `promql`, `templating`, `alerting`, `panels`                    | `devops/prometheus-metrics-designer`, `devops/observability-stack-builder`, `devops/sre-runbook-author`                                         |
| 6  | [`opentelemetry-instrumenter`](opentelemetry-instrumenter/SKILL.md)   | Instrument application code with OpenTelemetry traces, spans, metrics, and logs, with W3C context propagation and OTLP exporters wired to a collector. Use this when the user asks to add distributed tracing, propagate trace context across services, or export to OTLP/Jaeger/Zipkin.                                   | advanced     | `opentelemetry`, `traces`, `spans`, `metrics`, `logs`, `otel`, `otlp`                   | `devops/observability-stack-builder`, `devops/prometheus-metrics-designer`, `devops/log-aggregation-builder`                                    |
| 7  | [`sre-runbook-author`](sre-runbook-author/SKILL.md)                   | Author SRE runbooks tied to specific alerts, covering severity, symptoms, diagnosis steps, mitigation, escalation, and a blameless postmortem template. Use this when the user asks to write a runbook, document alert response, or formalize on-call playbooks.                                                           | intermediate | `runbook`, `sre`, `alert`, `postmortem`, `escalation`, `oncall`                         | `devops/incident-response-planner`, `devops/grafana-dashboard-builder`, `devops/observability-stack-builder`                                    |
| 8  | [`incident-response-planner`](incident-response-planner/SKILL.md)     | Plan incident response with a severity matrix, on-call rotation, communication channels, and a blameless postmortem process. Use this when the user asks to set up an on-call program, define severity levels, or formalize incident command and customer comms.                                                           | intermediate | `incident-response`, `oncall`, `severity`, `postmortem`, `communication`, `ic`          | `devops/sre-runbook-author`, `devops/disaster-recovery-planner`                                                                                 |
| 9  | [`ci-cd-pipeline-builder`](ci-cd-pipeline-builder/SKILL.md)           | Build CI/CD pipelines with build, test, scan, and deploy stages, environment promotion, rollback strategy, and artifact management. Use this when the user asks to wire up GitHub Actions or GitLab CI, promote artifacts across environments, or design a safe rollback flow.                                             | intermediate | `cicd`, `github-actions`, `gitlab-ci`, `pipeline`, `deployment`, `rollback`             | `devops/container-image-hardener`, `devops/gitops-deployment-builder`, `devops/helm-chart-author`                                               |
| 10 | [`container-image-hardener`](container-image-hardener/SKILL.md)       | Harden container images using distroless or scratch bases, non-root users, multi-stage builds, SBOM generation, and vulnerability scanning with Trivy or Grype. Use this when the user asks to write a production Dockerfile, reduce image attack surface, or meet NIST SP 800-190 controls.                               | advanced     | `container`, `distroless`, `sbom`, `trivy`, `hardening`, `dockerfile`, `non-root`       | `devops/ci-cd-pipeline-builder`, `devops/kubernetes-manifest-builder`                                                                           |
| 11 | [`gitops-deployment-builder`](gitops-deployment-builder/SKILL.md)     | Build GitOps deployments with ArgoCD or FluxCD application manifests, sync waves, health checks, and rollback via git revert. Use this when the user asks to set up GitOps, replace imperative kubectl apply with a reconciler, or wire sync waves for ordered deploys.                                                    | intermediate | `gitops`, `argocd`, `fluxcd`, `sync-wave`, `kubernetes`, `reconciler`                   | `devops/kubernetes-manifest-builder`, `devops/helm-chart-author`, `devops/ci-cd-pipeline-builder`                                               |
| 12 | [`service-mesh-configurator`](service-mesh-configurator/SKILL.md)     | Configure a service mesh with Istio VirtualService, DestinationRule, mTLS PeerAuthentication, traffic shifting, and circuit breakers. Use this when the user asks to set up Istio, do canary releases via traffic weights, or enforce mTLS across services.                                                                | advanced     | `istio`, `service-mesh`, `mtls`, `virtualservice`, `circuit-breaker`, `canary`          | `devops/kubernetes-manifest-builder`, `devops/opentelemetry-instrumenter`                                                                       |
| 13 | [`secrets-management-builder`](secrets-management-builder/SKILL.md)   | Build secrets management with HashiCorp Vault policies, Kubernetes External Secrets Operator, AWS Secrets Manager, and rotation schedules. Use this when the user asks to centralize secrets, replace K8s Secret manifests with external stores, or set up DB credential rotation.                                         | advanced     | `vault`, `secrets`, `external-secrets`, `rotation`, `kubernetes`, `aws-secrets-manager` | `devops/kubernetes-manifest-builder`, `devops/terraform-module-author`                                                                          |
| 14 | [`log-aggregation-builder`](log-aggregation-builder/SKILL.md)         | Build log aggregation pipelines with Loki or ELK plus Fluent Bit shippers, structured JSON logging, log levels, and retention policies. Use this when the user asks to centralize logs, replace stdout scraping, or enforce structured logging across services.                                                            | intermediate | `loki`, `elasticsearch`, `fluent-bit`, `structured-logging`, `retention`, `logs`        | `devops/observability-stack-builder`, `devops/opentelemetry-instrumenter`                                                                       |
| 15 | [`health-endpoint-designer`](health-endpoint-designer/SKILL.md)       | Design Kubernetes health endpoints distinguishing liveness, readiness, and startup probes, plus dependency checks and graceful shutdown. Use this when the user asks to add probes to a Deployment, design a /healthz endpoint, or wire graceful shutdown to avoid dropped requests.                                       | intermediate | `health`, `liveness`, `readiness`, `startup-probe`, `graceful-shutdown`, `kubernetes`   | `devops/kubernetes-manifest-builder`, `devops/disaster-recovery-planner`                                                                        |
| 16 | [`capacity-planner`](capacity-planner/SKILL.md)                       | Plan capacity with Kubernetes resource requests/limits, HorizontalPodAutoscaler, VerticalPodAutoscaler, cluster autoscaler, and cost forecasting. Use this when the user asks to right-size pods, set HPA targets, design cluster autoscaling, or forecast cloud spend.                                                    | advanced     | `autoscaling`, `hpa`, `vpa`, `capacity`, `cost`, `cluster-autoscaler`                   | `devops/kubernetes-manifest-builder`, `devops/grafana-dashboard-builder`, `devops/disaster-recovery-planner`                                    |
| 17 | [`disaster-recovery-planner`](disaster-recovery-planner/SKILL.md)     | Plan disaster recovery with RTO/RPO targets, backup strategies, multi-region failover, and restore testing. Use this when the user asks to write a DR plan, define RTO/RPO per workload, or schedule restore drills.                                                                                                       | advanced     | `disaster-recovery`, `rto`, `rpo`, `backup`, `failover`, `multi-region`                 | `devops/incident-response-planner`, `devops/capacity-planner`, `devops/secrets-management-builder`                                              |
| 18 | [`observability-stack-builder`](observability-stack-builder/SKILL.md) | Build an observability stack integrating metrics, logs, and traces with OpenTelemetry, plus SLO definition and error-budget tracking. Use this when the user asks to stand up the full observability stack, define SLOs per service, or wire error-budget burn-rate alerts.                                                | advanced     | `observability`, `slo`, `error-budget`, `traces`, `logs`, `metrics`                     | `devops/prometheus-metrics-designer`, `devops/grafana-dashboard-builder`, `devops/log-aggregation-builder`, `devops/opentelemetry-instrumenter` |

## Difficulty Breakdown

Across **18** skills in this theme, the difficulty distribution is:

- **Beginner** — 0 skill(s)
- **Intermediate** — 11 skill(s)
- **Advanced** — 7 skill(s)

There are no beginner skills in this theme; DevOps work assumes prior familiarity with the cloud-native stack.
Intermediate skills assume familiarity with Kubernetes, containers, and a CI engine. Advanced skills expect the operator
to have read the prerequisites first and to be comfortable with production-grade configuration.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`kubernetes` (5), `logs` (3), `metrics` (3), `deployment` (2), `oncall` (2), `postmortem` (2), `traces` (2), `alert`
(1), `alerting` (1), `argocd` (1), `autoscaling` (1), `aws` (1), `aws-secrets-manager` (1), `backup` (1), `canary` (1),
`capacity` (1), `cardinality` (1), `chart` (1), `cicd` (1), `circuit-breaker` (1), `cluster-autoscaler` (1),
`communication` (1), `configmap` (1), `cost` (1), `dashboard` (1), `disaster-recovery` (1), `distroless` (1),
`dockerfile` (1), `elasticsearch` (1), `error-budget` (1), `escalation` (1), `external-secrets` (1), `failover` (1),
`fluent-bit` (1), `fluxcd` (1), `github-actions` (1), `gitlab-ci` (1), `gitops` (1), `graceful-shutdown` (1),
`grafana` (1), `hardening` (1), `health` (1), `helm` (1), `hooks` (1), `hpa` (1), `iac` (1), `ic` (1),
`incident-response` (1), `ingress` (1), `istio` (1), `labels` (1), `liveness` (1), `loki` (1), `manifests` (1),
`module` (1), `mtls` (1), `multi-region` (1), `non-root` (1), `observability` (1), `opentelemetry` (1), `otel` (1),
`otlp` (1), `outputs` (1), `panels` (1), `pipeline` (1), `prometheus` (1), `promql` (1), `pvc` (1), `readiness` (1),
`reconciler` (1), `recording-rules` (1), `retention` (1), `rollback` (1), `rotation` (1), `rpo` (1), `rto` (1),
`runbook` (1), `sbom` (1), `secrets` (1), `service-mesh` (1), `severity` (1), `sli` (1), `slo` (1), `sre` (1),
`startup-probe` (1), `structured-logging` (1), `sync-wave` (1), `templates` (1), `templating` (1), `terraform` (1),
`trivy` (1), `values` (1), `variables` (1), `vault` (1), `virtualservice` (1), `vpa` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`kubernetes-manifest-builder` → `health-endpoint-designer` → `helm-chart-author` → `gitops-deployment-builder`** —
  manifest → probes → chart → GitOps reconciler.
- **`ci-cd-pipeline-builder` → `container-image-hardener` → `gitops-deployment-builder` → `helm-chart-author`** —
  pipeline → hardened image → GitOps deploy → chart packaging.
- **`prometheus-metrics-designer` → `grafana-dashboard-builder` → `sre-runbook-author` → `incident-response-planner`**
  — metrics → dashboard → runbook → incident program.
- **`opentelemetry-instrumenter` → `log-aggregation-builder` → `observability-stack-builder`** — traces → logs → full
  SLO and error-budget stack.
- **`terraform-module-author` → `secrets-management-builder` → `disaster-recovery-planner` → `capacity-planner`** —
  IaC → secrets → DR plan → capacity and cost.
- **`service-mesh-configurator` → `observability-stack-builder` → `sre-runbook-author`** — mesh → observability →
  per-alert runbooks.

## Cross-Theme Connections

Skills in `devops/` currently declare `related` pointers only within this theme; no cross-theme pointers are present
yet. The most natural cross-theme chains based on the artifacts these skills produce are:

- [`../project-tooling/README.md`](../project-tooling/README.md) — CI/CD pipelines emit GitHub Actions and pre-commit
  hooks; `pre-commit-hook-builder`, `github-actions-research-ci`, and `requirements-pinner` chain naturally.
- [`../style-integrity/README.md`](../style-integrity/README.md) — skills that emit Python
  (`opentelemetry-instrumenter`,
  health handlers) should run through `coding-conventions-enforcer`.
- [`../data-engineering/README.md`](../data-engineering/README.md) — ETL pipelines produced by `etl-pipeline-builder`
  deploy through the DevOps CI/CD and GitOps skills here.
- [`../ml-engineering/README.md`](../ml-engineering/README.md) — ML training pipelines ship as containers; the
  `container-image-hardener` and `kubernetes-manifest-builder` skills apply directly.

## Back to Master

← [Back to SkillStack README](../README.md)
