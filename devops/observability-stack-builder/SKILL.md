---
name: observability-stack-builder
description: Build an observability stack integrating metrics, logs, and traces with OpenTelemetry, plus SLO definition and error-budget tracking. Use this when the user asks to stand up the full observability stack, define SLOs per service, or wire error-budget burn-rate alerts.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [observability, slo, error-budget, traces, logs, metrics]
related: [devops/prometheus-metrics-designer, devops/grafana-dashboard-builder, devops/log-aggregation-builder, devops/opentelemetry-instrumenter]
prerequisites: [devops/prometheus-metrics-designer, devops/log-aggregation-builder]
outputs: [yaml, markdown]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Observability Stack Builder

## When To Use

- The user says "set up observability for our platform" or "define SLOs and error budgets".
- The user wants the three pillars (metrics, logs, traces) integrated via OpenTelemetry.
- The user wants multi-window multi-burn-rate alerts aligned to Google SRE.
- The user wants one dashboard that pivots from metric → trace → log in a click.
- Trigger keywords: observability, slo, error-budget, burn-rate, three-pillars, otel.

## Workflow

1. Stand up the backend stack: Prometheus + Loki + Tempo (or Jaeger), fronted by Grafana.
2. Deploy the OpenTelemetry Collector with OTLP receiver and exporters per signal (Prometheus, Loki, Tempo).
3. Instrument each service with OTel SDKs and auto-instrumentation (see `opentelemetry-instrumenter`).
4. Define SLIs per service: availability (good/total requests), latency (p99 below threshold), freshness, correctness.
5. Define SLOs per service: a target (e.g., 99.9% availability over 28 days) and a corresponding error budget (0.1%).
6. Translate SLOs into recording rules: `job:slo_error_ratio:rate5m`, `job:slo_error_ratio:rate1h`,
   `job:slo_error_ratio:rate6h`.
7. Configure multi-window multi-burn-rate alerts (Google SRE pattern): 1h × 14.4× burn, 6h × 6× burn, 3d × 1× burn.
8. Wire Grafana dashboards with metric → trace → log correlation using `trace_id` exemplars.
9. Track error budget remaining in a panel so the team can see when releases should freeze.
10. Run a quarterly review of SLO targets; revise targets the team consistently overshoots or violates.

## Inputs

- Service catalog with user-facing criticality.
- SLO target per service (e.g., 99.9%, 99.95%) and the window (28 days).
- SLI definitions (good events / total events).
- Existing backend (Prometheus, Loki, Tempo, Jaeger, ELK).
- Alert notification channels (PagerDuty, Slack).

## Outputs

- `stack/docker-compose.yaml` — local full-stack (Prometheus, Loki, Tempo, Grafana, OTel Collector).
- `slo-definitions.yaml` — Sloth or Prometheus-slo-generator SLO specs.
- `slo-rules.yaml` — recording and alerting rules.
- `dashboards/observability-overview.json` — metric-trace-log pivot dashboard.
- `error-budget.md` — error-budget policy, freeze rules, review cadence.

## Key Rules

- SLOs must come from user impact, not from what the system happens to deliver.
- Error budget = (1 − SLO target) × window. A 99.9% SLO over 30 days = 43.2 min of error budget.
- Multi-window multi-burn-rate alerts fire on the same SLO with different sensitivities — page on fast burn, ticket on
  slow burn.
- Logs, metrics, and traces must share `trace_id`/`span_id` so Grafana can pivot between them in a click.
- The OTel Collector is the single integration point; do not have apps export directly to multiple backends.
- Error budget exhaustion should freeze releases until the budget recovers; without enforcement, the SLO is decorative.
- SLO targets must be reviewed quarterly; a target no one fails is too lax, and one everyone fails is too strict.

## Examples

```yaml
# slo-definitions.yaml — Sloth-style SLO spec for the payments API.
version: "prometheus/v1"
service: "payments-api"
slos:
  - name: "availability"
    objective: 99.9
    sli:
      events:
        total: "sum(rate(http_requests_total{job=\"payments-api\"}[{{.window}}]))"
        errors: "sum(rate(http_requests_total{job=\"payments-api\",status=~\"5..\"}[{{.window}}]))"
    alerting:
      name: PaymentsAPIAvailability
      page_alert: { labels: { severity: page } }
      ticket_alert: { labels: { severity: ticket } }
  - name: "latency-p99"
    objective: 99.0
    sli:
      raw:
        error_ratio_query: |
          sum(rate(http_request_duration_seconds_bucket{job="payments-api",le="0.5"}[{{.window}}]))
          /
          sum(rate(http_request_duration_seconds_count{job="payments-api"}[{{.window}}]))
```

```yaml
# Multi-window multi-burn-rate alerts (Google SRE pattern).
groups:
  - name: payments-api.slo
    rules:
      - alert: SLOHighErrorBudgetBurnPage
        expr: |
          (job:slo_error_ratio:rate5m > (14.4 * 0.001))
          and
          (job:slo_error_ratio:rate1h > (14.4 * 0.001))
        for: 2m
        labels: { severity: page }
        annotations:
          summary: "Fast SLO burn — 2% of monthly budget in 1h"
      - alert: SLOHighErrorBudgetBurnTicket
        expr: |
          (job:slo_error_ratio:rate30m > (6 * 0.001))
          and
          (job:slo_error_ratio:rate6h > (6 * 0.001))
        for: 15m
        labels: { severity: ticket }
        annotations:
          summary: "Slow SLO burn — 5% of monthly budget in 6h"
```

```yaml
# stack/docker-compose.yaml — local OTel + Prometheus + Loki + Tempo + Grafana.
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.103.0
    volumes: ["./otel-collector-config.yaml:/etc/otelcol/config.yaml"]
    command: ["--config=/etc/otelcol/config.yaml"]
    ports: ["4318:4318", "8889:8889"]
  prometheus:
    image: prom/prometheus:v2.54.1
    volumes: ["./prometheus.yml:/etc/prometheus/prometheus.yml"]
  loki:
    image: grafana/loki:3.1.1
  tempo:
    image: grafana/tempo:2.5.0
    command: ["-config.file=/etc/tempo.yaml"]
  grafana:
    image: grafana/grafana:11.2.0
    ports: ["3000:3000"]
```
