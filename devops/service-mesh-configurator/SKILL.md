---
name: service-mesh-configurator
description: Configure a service mesh with Istio VirtualService, DestinationRule, mTLS PeerAuthentication, traffic shifting, and circuit breakers. Use this when the user asks to set up Istio, do canary releases via traffic weights, or enforce mTLS across services.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [istio, service-mesh, mtls, virtualservice, circuit-breaker, canary]
related: [devops/kubernetes-manifest-builder, devops/opentelemetry-instrumenter]
prerequisites: [devops/kubernetes-manifest-builder]
outputs: [yaml, markdown]
difficulty: advanced
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Service Mesh Configurator

## When To Use

- The user says "set up Istio" or "do a canary deploy with traffic weights".
- The user needs mTLS between services without touching application code.
- The user wants circuit breakers, retries, and timeouts at the mesh layer.
- The user wants traffic shifting between versions (90/10, 50/50) without new deploys.
- Trigger keywords: istio, virtualservice, destinationrule, peerauthentication, circuit-breaker, mtls, canary.

## Workflow

1. Install Istio via the official Helm chart or `istioctl install` with a minimal profile.
2. Label the namespace with `istio-injection=enabled` so sidecars inject automatically on pod creation.
3. Author a `PeerAuthentication` enforcing STRICT mTLS in the namespace.
4. Author a `DestinationRule` defining subsets (`v1`, `v2`) and their load-balancing + outlier-detection policy.
5. Author a `VirtualService` routing traffic by weight across subsets, with retries, timeouts, and fault injection.
6. Configure circuit breakers via `trafficPolicy.outlierDetection` (consecutive5xxErrors, interval, baseEjectionTime).
7. Add a `ServiceEntry` for external services (third-party APIs) so the mesh can apply policy to egress.
8. Wire observability: enable Istio's Prometheus integration, Kiali for topology, and Jaeger for distributed traces.
9. Validate mTLS with `istioctl authn tls-check <pod>` and confirm STRICT mode rejects plaintext.
10. Validate routing with a curl loop hitting the service and verifying weight distribution.

## Inputs

- Mesh tool (Istio, Linkerd, Consul Connect).
- Namespace(s) to enroll and injection strategy (sidecar vs ambient).
- Service versions and traffic split (e.g., 90% v1, 10% v2).
- mTLS mode (STRICT, PERMISSIVE, DISABLE).
- Circuit-breaker thresholds (consecutive errors, ejection time, max ejection percent).

## Outputs

- `namespace.yaml` — labeled for injection.
- `peerauthentication.yaml` — mTLS mode.
- `destinationrule.yaml` — subsets and outlier detection.
- `virtualservice.yaml` — routing, retries, timeouts, weights.
- `serviceentry.yaml` — external service entry (optional).
- `README.md` — topology, traffic weights, mTLS posture, rollback plan.

## Key Rules

- Always set `PeerAuthentication` to STRICT once sidecars are deployed; PERMISSIVE is a transition state, not
  steady-state.
- Always define `DestinationRule` subsets before `VirtualService` routes them; otherwise routes 502.
- Always set timeouts on `VirtualService` routes; without them, a hung upstream cascades.
- Circuit-breaker `outlierDetection` must be conservative — too aggressive and healthy pods get ejected.
- Canary traffic weights must be reviewed against the SLO burn-rate; a 10% bad version still burns the SLO at 10%.
- mTLS STRICT requires all clients in the mesh; external clients need an `Ingress` with TLS termination.
- Don't enable mesh features the app doesn't need; every feature adds latency and cognitive load.

## Examples

```yaml
# peerauthentication.yaml — STRICT mTLS in the namespace.
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: payments
spec:
  mtls:
    mode: STRICT
```

```yaml
# destinationrule.yaml — subsets + circuit breaker.
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payments-api
  namespace: payments
spec:
  host: payments-api
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels:
        version: "1"
    - name: v2
      labels:
        version: "2"
```

```yaml
# virtualservice.yaml — 90/10 canary with retries and timeouts.
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: payments-api
  namespace: payments
spec:
  hosts: [payments-api]
  http:
    - name: canary
      route:
        - destination:
            host: payments-api
            subset: v1
          weight: 90
        - destination:
            host: payments-api
            subset: v2
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx,reset,connect-failure
      timeout: 5s
```
