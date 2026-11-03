---
name: log-aggregation-builder
description: Build log aggregation pipelines with Loki or ELK plus Fluent Bit shippers, structured JSON logging, log levels, and retention policies. Use this when the user asks to centralize logs, replace stdout scraping, or enforce structured logging across services.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [loki, elasticsearch, fluent-bit, structured-logging, retention, logs]
related: [devops/observability-stack-builder, devops/opentelemetry-instrumenter]
prerequisites: []
outputs: [yaml, markdown]
difficulty: intermediate
estimated_tokens: 1600
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Log Aggregation Builder

## When To Use

- The user says "centralize our logs in Loki" or "set up the ELK stack".
- The user wants Fluent Bit to ship stdout from Kubernetes pods to a backend.
- The user wants structured JSON logs with `trace_id`, `level`, and `service.name` fields.
- The user wants retention policies (hot 7 days, warm 30 days, cold 1 year).
- Trigger keywords: loki, elasticsearch, fluent-bit, structured-logging, retention, logql.

## Workflow

1. Pick the backend: Loki (index-light, Prometheus-like query), ELK (Elasticsearch + Kibana, full-text), or OpenSearch.
2. Deploy the backend (Helm chart) with persistent storage (S3, GCS, or local PVC).
3. Deploy Fluent Bit as a DaemonSet to scrape container stdout/stderr from `/var/log/containers/`.
4. Configure Fluent Bit parsers: a `docker` parser for the default JSON wrapper, plus a custom `json` parser for
   structured app logs.
5. Define the structured log schema: `timestamp`, `level`, `service.name`, `trace_id`, `span_id`, `message`,
   `error.stack`.
6. Map labels for Loki: `namespace`, `pod`, `container`, `service` — keep cardinality bounded.
7. Configure the backend's retention: hot tier on fast storage for 7 days, warm/cold in object storage for 30/365 days.
8. Wire dashboards: Grafana for Loki (LogQL queries), Kibana for ELK; both should pivot on `trace_id`.
9. Define log-level conventions: DEBUG dev only, INFO prod, WARN slow paths, ERROR user-impacting.
10. Validate with a test log line and confirm it appears in the backend with the right labels and structure.

## Inputs

- Backend choice (Loki, ELK, OpenSearch).
- Cluster type (Kubernetes, bare-metal) and shipping tool (Fluent Bit, Fluentd, Vector, Promtail).
- Retention requirements per environment.
- Required structured-log fields (service.name, trace_id, level).

## Outputs

- `fluent-bit/daemonset.yaml` — DaemonSet + ConfigMap.
- `fluent-bit/parsers.conf` — JSON and docker parsers.
- `loki/values.yaml` or `elasticsearch/values.yaml` — backend Helm values.
- `retention.yaml` — retention and lifecycle policy.
- `log-schema.md` — structured-log field reference.
- `README.md` — pipeline diagram, label cardinality rules, retention tiers.

## Key Rules

- Always log structured JSON from the app; a Fluent Bit regex parser for plaintext is brittle.
- Always include `trace_id` and `span_id` so logs correlate to traces in Jaeger/Tempo.
- Always set `level` consistently; mixing `INFO` and `info` breaks queries.
- Never log secrets, PII, or full request bodies without redaction.
- Keep Loki label cardinality bounded: never use `user_id`, `trace_id`, or `request_id` as labels.
- Set retention on the backend, not just on disk cleanup; old logs must age out automatically.
- DEBUG logs belong in dev only; shipping DEBUG to prod at scale will saturate the backend.

## Examples

```yaml
# fluent-bit/daemonset.yaml — ConfigMap with structured-log pipeline.
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: kube-system
data:
  fluent-bit.conf: |
    [SERVICE]
      Flush         5
      Log_Level     info
      Parsers_File  parsers.conf
    [INPUT]
      Name              tail
      Path              /var/log/containers/*.log
      Parser            docker
      Tag               kube.*
      Refresh_Interval  5
      Mem_Buf_Limit     50MB
    [FILTER]
      Name              parser
      Match             kube.*
      Key_Name          log
      Parser            json
      Reserve_Data      true
    [OUTPUT]
      Name              loki
      Match             kube.*
      Host              loki.observability.svc
      Port              3100
      Labels            namespace=$kubernetes['namespace_name'],pod=$kubernetes['pod_name'],container=$kubernetes['container_name']
      Line_Format       json
```

```python
# Structured log line emitted by the app.
import logging, json, structlog

structlog.configure(processors=[
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer(),
])
log = structlog.get_logger("payments-api")
log.info("payment_completed", payment_id="pay_123", amount=4999, currency="usd", trace_id=trace_id)
```

```yaml
# retention.yaml — Loki retention (compactor) and S3 lifecycle.
loki:
  compactor:
    working_directory: /data/loki/compactor
    retention_enabled: true
    retention_delete_delay: 2h
    delete_request_store: s3
  limits_config:
    retention_period: 30d
  storage_config:
    aws:
      s3: s3://loki-bucket
```
