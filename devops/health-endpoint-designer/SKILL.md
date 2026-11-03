---
name: health-endpoint-designer
description: Design Kubernetes health endpoints distinguishing liveness, readiness, and startup probes, plus dependency checks and graceful shutdown. Use this when the user asks to add probes to a Deployment, design a /healthz endpoint, or wire graceful shutdown to avoid dropped requests.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [health, liveness, readiness, startup-probe, graceful-shutdown, kubernetes]
related: [devops/kubernetes-manifest-builder, devops/disaster-recovery-planner]
prerequisites: [devops/kubernetes-manifest-builder]
outputs: [yaml, markdown]
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

# Health Endpoint Designer

## When To Use

- The user says "add liveness and readiness probes to my Deployment".
- The user wants a `/healthz`, `/ready`, and `/startup` endpoint set.
- The user is seeing 5xx spikes during deploys and needs graceful shutdown.
- The user wants probes that distinguish "app is up" from "app can serve traffic".
- Trigger keywords: liveness, readiness, startup-probe, healthz, graceful-shutdown, signal-handling.

## Workflow

1. Define three endpoints with distinct semantics:
    - `/healthz` (liveness) — app process is alive; never check downstream dependencies.
    - `/ready` (readiness) — app can serve traffic; check downstream dependencies (DB, cache, downstream APIs).
    - `/startup` (startup) — app has finished initialization; used to gate liveness during slow boots.
2. Implement each endpoint with an HTTP 200 on success and 503 on failure; return JSON with `status` and optional
   `checks`.
3. In the Deployment, set `startupProbe` with a high `failureThreshold` and short `periodSeconds` to allow slow boots
   without restarts.
4. Set `livenessProbe` with conservative `initialDelaySeconds` and `periodSeconds` so transient blips don't restart the
   pod.
5. Set `readinessProbe` with a short `periodSeconds` (5s) so the pod is removed from the Service endpoints quickly when
   unready.
6. Implement graceful shutdown: catch SIGTERM, stop accepting new requests, drain in-flight requests, then exit.
7. Set `terminationGracePeriodSeconds` (default 30s) larger than the longest in-flight request.
8. Make `/ready` fail during shutdown so the Service stops sending traffic before SIGKILL.
9. Document the three endpoints, their failure semantics, and the probe thresholds in a README.

## Inputs

- App boot time (slow vs fast) to size the startup probe.
- Downstream dependencies (DB, cache, downstream services) to gate readiness.
- Max in-flight request duration for `terminationGracePeriodSeconds`.
- Probe transport (HTTP path, TCP socket, exec command).

## Outputs

- `probes.md` — endpoint semantics and probe thresholds table.
- `health_handlers.py` — `/healthz`, `/ready`, `/startup` handlers.
- `graceful-shutdown.md` — SIGTERM handling and drain procedure.
- `deployment-patch.yaml` — probe snippet to merge into the Deployment.

## Key Rules

- Liveness probes must not check downstream dependencies; a flapping DB would cause cascading restarts.
- Readiness probes must check downstream dependencies; an unready DB means the pod should not serve traffic.
- Startup probes gate liveness during slow boots; without one, a slow-booting app gets restarted before it can serve.
- `/ready` must return 503 during shutdown so the Service stops routing before SIGKILL.
- `terminationGracePeriodSeconds` must be longer than the longest in-flight request; otherwise requests are dropped.
- Set `periodSeconds` and `failureThreshold` deliberately; defaults (10s × 3) are too aggressive for many apps.
- Use a `preStop` hook to introduce a sleep so the endpoint has time to deregister from the Service.

## Examples

```python
# health_handlers.py — Flask health endpoints.
from flask import Flask, jsonify
import signal, threading, time

app = Flask(__name__)
SHUTTING_DOWN = threading.Event()

def db_ok():
    # ping the DB connection pool
    return True

@app.get("/healthz")
def healthz():
    # Liveness: only confirm the process is alive.
    return jsonify({"status": "ok"}), 200

@app.get("/ready")
def ready():
    if SHUTTING_DOWN.is_set():
        return jsonify({"status": "shutting_down"}), 503
    if not db_ok():
        return jsonify({"status": "db_unavailable"}), 503
    return jsonify({"status": "ready"}), 200

@app.get("/startup")
def startup():
    # True once initial migrations and warmup are done.
    return jsonify({"status": "started"}), 200

def handle_sigterm(signum, frame):
    SHUTTING_DOWN.set()
    time.sleep(15)  # let the Service deregister, then drain
    # stop accepting new requests, wait for in-flight to finish

signal.signal(signal.SIGTERM, handle_sigterm)
```

```yaml
# deployment-patch.yaml — probe snippet.
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: api
          startupProbe:
            httpGet:
              path: /startup
              port: 8080
            failureThreshold: 30
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
            timeoutSeconds: 2
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
            failureThreshold: 1
            timeoutSeconds: 2
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 10"]
```

```text
Endpoint semantics table:
| Path      | Probe      | Checks downstream? | Fails during shutdown? | Restart on fail? |
|-----------|------------|--------------------|------------------------|-------------------|
| /startup  | startup    | no                 | no                     | yes (until boot)  |
| /healthz  | liveness   | no                 | no                     | yes               |
| /ready    | readiness  | yes                | yes (returns 503)      | no (just unready) |
```
