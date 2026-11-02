---
name: grafana-dashboard-builder
description: Build Grafana dashboards as JSON with chosen panel types, PromQL queries, templating variables, and alerting thresholds aligned to SLOs. Use this when the user asks to visualize Prometheus metrics, build a service overview dashboard, or wire alerts to a notification channel.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [grafana, dashboard, promql, templating, alerting, panels]
related: [devops/prometheus-metrics-designer, devops/observability-stack-builder, devops/sre-runbook-author]
prerequisites: [devops/prometheus-metrics-designer]
outputs: [json, markdown]
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

# Grafana Dashboard Builder

## When To Use

- The user says "build a Grafana dashboard for our API" or "visualize these Prometheus metrics".
- The user wants a USE (Utilization/Saturation/Errors) or RED (Rate/Errors/Duration) method layout.
- The user wants templating variables so the same dashboard serves multiple services/environments.
- The user wants alert thresholds wired into a panel and routed to a contact point.
- Trigger keywords: grafana, dashboard, panel, promql, templating, alerting, $service.

## Workflow

1. Pick the method: RED for request-driven services, USE for resources (CPU, disk, network).
2. Lay out panels top-to-bottom by abstraction: title row → KPIs → detailed panels → drill-down.
3. For each panel, pick the panel type: `stat` for KPIs, `timeseries` for trends, `table` for tabular, `heatmap` for
   latency distributions, `nodegraph` for topologies.
4. Write the PromQL query against recording rules first (cheaper); fall back to raw queries when no recording rule
   exists.
5. Add templating variables: `datasource` (Prometheus), `service` (label_values on a metric), `environment`, `status`.
6. Set panel thresholds aligned to SLOs (e.g., green below SLO, amber within burn-rate buffer, red above).
7. Add alerting rules inside the dashboard or as standalone Grafana alert rules with `for:` duration and notification
   policy.
8. Configure the dashboard JSON with `schemaVersion`, `uid`, `tags`, and a refresh interval (`30s` or `1m`).
9. Export the JSON, store it in a repo, and load via Grafana provisioning (`provisioning/dashboards/`).
10. Validate the JSON with `jq .` and a dry-run import into a local Grafana.

## Inputs

- Service name and namespace for templating defaults.
- SLO targets (e.g., 99.9% availability, p99 < 500ms) for threshold coloring.
- List of metrics exposed by the service (see `prometheus-metrics-designer`).
- Preferred refresh interval and time range defaults.

## Outputs

- `dashboard.json` — Grafana dashboard JSON.
- `provisioning/dashboards/dashboard.yaml` — Grafana provisioning config.
- `alerts.yaml` — standalone Grafana alert rules (optional).
- `README.md` — what each panel shows and how to use templating.

## Key Rules

- Always start with the recording rule version of a query (`job:http_requests:rate5m`), not the raw
  `rate(http_requests_total[5m])`.
- Use `$service` and `$environment` templating variables; never hardcode service names.
- For latency, prefer `histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))` against
  pre-recorded buckets.
- Set `legend` to `{{ method }} {{ status }}` so multi-series panels are readable.
- Annotate deploy events using Grafana annotations from a `deploy` metric or release tags.
- Set `decimals`, `unit`, and `min`/`max` on every axis so panels render sensibly across services.
- Keep dashboard JSON in version control; load via provisioning so changes are reviewable.

## Examples

```json
{
  "uid": "api-overview",
  "title": "API Overview (RED)",
  "schemaVersion": 39,
  "tags": ["api", "red", "overview"],
  "refresh": "30s",
  "time": { "from": "now-6h", "to": "now" },
  "templating": {
    "list": [
      {
        "name": "service",
        "type": "query",
        "datasource": { "type": "prometheus", "uid": "Prometheus" },
        "query": "label_values(http_requests_total, job)",
        "refresh": 2
      }
    ]
  },
  "panels": [
    {
      "type": "stat",
      "title": "Request rate (req/s)",
      "gridPos": { "x": 0, "y": 0, "w": 6, "h": 6 },
      "targets": [
        { "expr": "sum(rate(http_requests_total{job=\"$service\"}[5m]))", "legendFormat": "rate" }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "reqps",
          "thresholds": { "mode": "absolute", "steps": [
            { "color": "green", "value": null },
            { "color": "yellow", "value": 100 },
            { "color": "red", "value": 500 }
          ] }
        }
      }
    }
  ]
}
```

```yaml
# provisioning/dashboards/dashboard.yaml
apiVersion: 1
providers:
  - name: 'repo dashboards'
    folder: 'Services'
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

## References

- Grafana Dashboards: https://grafana.com/docs/grafana/latest/dashboards/
- Grafana Templating: https://grafana.com/docs/grafana/latest/dashboards/variables/
- Grafana Alerting: https://grafana.com/docs/grafana/latest/alerting/
- Grafana Provisioning: https://grafana.com/docs/grafana/latest/administration/provisioning/
- RED Method (Tom Wilkie): https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/
