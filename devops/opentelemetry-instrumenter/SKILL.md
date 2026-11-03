---
name: opentelemetry-instrumenter
description: Instrument application code with OpenTelemetry traces, spans, metrics, and logs, with W3C context propagation and OTLP exporters wired to a collector. Use this when the user asks to add distributed tracing, propagate trace context across services, or export to OTLP/Jaeger/Zipkin.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [opentelemetry, traces, metrics, logs, otel, otlp]
related: [devops/observability-stack-builder, devops/prometheus-metrics-designer, devops/log-aggregation-builder]
prerequisites: []
outputs: [python, yaml, markdown]
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

# OpenTelemetry Instrumenter

## When To Use

- The user says "add distributed tracing to my service" or "instrument with OpenTelemetry".
- The user wants spans for HTTP handlers, DB calls, and downstream service calls automatically.
- The user needs W3C Trace Context (`traceparent` header) propagation across HTTP/gRPC boundaries.
- The user wants to ship traces, metrics, and logs via OTLP to a collector.
- Trigger keywords: opentelemetry, otel, span, trace, otlp, collector, w3c-trace-context.

## Workflow

1. Pick the SDK language (Python `opentelemetry-api`/`sdk`, Go `go.opentelemetry.io/otel`, Node
   `@opentelemetry/sdk-node`).
2. Configure a `TracerProvider`, a `MeterProvider`, and a `LoggerProvider` sharing the same `Resource` (`service.name`,
   `service.version`, `deployment.environment`).
3. Attach auto-instrumentation libraries: `opentelemetry-instrumentation-flask`,
   `opentelemetry-instrumentation-requests`, `opentelemetry-instrumentation-psycopg2`, etc.
4. Add the OTLP exporter (HTTP/gRPC) pointing at the collector endpoint (`http://otel-collector:4318`).
5. Configure propagators: `tracecontext` + `baggage` (W3C).
6. For each business operation, create a span with `tracer.start_as_current_span("name")` and set attributes (per the
   semantic conventions: `http.method`, `db.system`, `messaging.destination`).
7. Bridge logs to the trace context so every log line carries `trace_id` and `span_id`.
8. Wire the collector `otel-collector-config.yaml` with `otlp` receiver, `batch` processor, and exporters to
   Jaeger/Prometheus/Loki.
9. Validate: tail the collector, hit an endpoint, confirm the trace appears with the expected span tree.
10. Set `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_RESOURCE_ATTRIBUTES` from env vars; never hardcode in
    code.

## Inputs

- Language and framework (Python+Flask, Go+chi, Node+Express, etc.).
- Collector endpoint and protocol (OTLP/HTTP vs OTLP/gRPC).
- Downstream dependencies to instrument (Postgres, Redis, Kafka, HTTP clients).
- Service name and version for the Resource.

## Outputs

- `instrumentation.py` — provider setup and exporter wiring.
- `otel-collector-config.yaml` — collector pipeline.
- `docker-compose.yaml` snippet for the collector + Jaeger.
- `env.example` — OTel environment variables.
- `README.md` — what is auto-instrumented vs custom spans.

## Key Rules

- Always set `service.name`, `service.version`, and `deployment.environment` on the Resource; missing `service.name`
  makes traces ungroupable.
- Use semantic-convention attribute names (`http.method`, `http.status_code`, `db.system`); custom names break query
  tools.
- Prefer OTLP/HTTP for simplicity unless gRPC is required; both share port semantics differently.
- Set the batch processor with a max queue and timeout; never export span-by-span synchronously.
- Propagate context manually when crossing thread/process boundaries (Celery, async tasks) with `context.attach()`.
- Bridge structured logs so they carry `trace_id`/`span_id` — without this, logs and traces don't correlate.
- Sample in the collector, not the SDK, so head sampling is consistent across services.

## Examples

```python
# instrumentation.py — Python OTel bootstrap.
from opentelemetry import trace, metrics, logs
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

resource = Resource.create({
    "service.name": "payments-api",
    "service.version": "1.4.2",
    "deployment.environment": "prod",
})
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"),
        max_queue_size=2048,
        export_timeout_millis=5000,
    )
)
trace.set_tracer_provider(provider)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318
processors:
  batch:
    timeout: 5s
    send_batch_size: 1024
exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true
  prometheus:
    endpoint: 0.0.0.0:8889
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```
