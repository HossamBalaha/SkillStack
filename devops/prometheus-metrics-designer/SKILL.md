---
name: prometheus-metrics-designer
description: Design Prometheus metrics with correct types (counter, gauge, histogram, summary), naming conventions, bounded label cardinality, and recording rules for high-cardinality queries. Use this when the user asks to instrument an app for Prometheus, define SLI metrics, or precompute heavy queries with recording rules.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [prometheus, metrics, labels, recording-rules, cardinality, sli]
related: [devops/grafana-dashboard-builder, devops/observability-stack-builder]
prerequisites: []
outputs: [yaml, markdown]
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

# Prometheus Metrics Designer

## When To Use

- The user says "what Prometheus metrics should my service expose" or "name my metrics".
- The user is choosing between counter, gauge, histogram, and summary for a given signal.
- The user is hitting high-cardinality blowups and needs to refactor labels or add recording rules.
- The user wants SLI/SLO metrics that feed alerting and dashboards.
- Trigger keywords: prometheus, counter, histogram, recording rule, cardinality, exposition.

## Workflow

1. List the user-facing signals: request rate, error rate, latency, queue depth, in-flight requests.
2. For each signal, pick the metric type:
    - counter for monotonic totals (requests, errors, bytes sent);
    - gauge for values that go up and down (queue depth, active connections);
    - histogram for latency distributions with bucketed SLO queries;
    - summary only for precomputed quantiles when bucketing is unacceptable.
3. Name metrics with `<namespace>_<subsystem>_<name>_<unit>` (e.g., `http_requests_total`,
   `http_request_duration_seconds`).
4. Add labels: `method`, `status`, `endpoint` — never `user_id`, `session_id`, or other unbounded labels.
5. Compute cardinality: product of label value counts; warn if it exceeds ~10 per series or 10k series per metric.
6. Define recording rules in a `rules.yaml` for expensive PromQL (e.g., `job:request_rate:5m`, `job:error_ratio:5m`).
7. Define alerting rules with `for:` durations to absorb flapping.
8. Provide the client library exposition snippet (Python `prometheus_client`, Go `prometheus`, etc.).
9. Validate the rules file with `promtool check rules rules.yaml`.

## Inputs

- Service name and namespace (e.g., `payments_api`).
- List of user-facing signals (rate, errors, latency, saturation).
- Existing label space and any unbounded dimensions to avoid.
- SLO targets (e.g., 99th percentile < 500ms for 99.9% of requests).

## Outputs

- `metrics_inventory.md` — table of metric name, type, labels, and SLO use.
- `rules.yaml` — recording and alerting rules.
- `prometheus.yml` snippet for scrape config (job_name, metrics_path, interval).
- Client library exposition code (Python/Go).

## Key Rules

- Always append `_total` to counters and `_seconds`/`_bytes` to units; Prometheus follows this convention.
- Never put `user_id`, `session_id`, `trace_id`, or full URLs in labels — they blow up cardinality.
- Prefer histograms over summaries; summaries can't be aggregated across instances.
- Pick histogram bucket boundaries around SLO thresholds (e.g., 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5,
  10).
- Always define the `le` bucket that covers the SLO target so `histogram_quantile` is accurate.
- Recording rules belong in a separate file from alerting rules so they can be evaluated at different intervals.
- Counter resets (restarts) are handled by PromQL `rate()` and `increase()`; never subtract raw counter values.

## Examples

```yaml
# rules.yaml — recording and alerting rules.
groups:
  - name: payments_api.rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job, method, status) (rate(http_requests_total[5m]))
      - record: job:http_errors:ratio_rate5m
        expr: |
          sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum by (job) (rate(http_requests_total[5m]))
      - alert: HighErrorRate
        expr: job:http_errors:ratio_rate5m > 0.01
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.job }} error ratio above 1% for 10m"
```

```python
# Python exposition snippet.
from prometheus_client import Counter, Histogram, start_http_server

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests.",
    ["method", "endpoint", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)

start_http_server(9100)
```
