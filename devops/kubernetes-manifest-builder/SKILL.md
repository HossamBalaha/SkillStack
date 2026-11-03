---
name: kubernetes-manifest-builder
description: Build production Kubernetes manifests covering Deployments, Services, ConfigMaps, Secrets, Ingress, and PersistentVolumeClaims with resource limits, probes, and security context. Use this when the user asks to write K8s YAML, deploy an app to a cluster, expose a service, or wire up ingress and persistent storage.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [kubernetes, manifests, deployment, configmap, ingress, pvc]
related: [devops/helm-chart-author, devops/health-endpoint-designer, devops/gitops-deployment-builder]
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

# Kubernetes Manifest Builder

## When To Use

- The user says "write me a Deployment + Service YAML" or "deploy this app to Kubernetes".
- The user needs to expose a service via Ingress with TLS, mount a ConfigMap or Secret, or attach persistent storage.
- The user is wiring up probes, resource requests/limits, or a non-root security context for the first time.
- Trigger keywords: deployment, service, ingress, configmap, secret, pvc, kubectl apply, manifest.

## Workflow

1. Ask for the app name, container image, port, and target namespace (default `default`).
2. Ask for replicas, CPU/memory request and limit, and the liveness/readiness probe paths.
3. Generate a `Deployment` with `strategy: RollingUpdate`, `revisionHistoryLimit: 10`, and a `securityContext`
   (runAsNonRoot, readOnlyRootFilesystem, allowPrivilegeEscalation: false).
4. Define `resources.requests` and `resources.limits` so the pod is schedulable and bounded.
5. Add a `Service` of type `ClusterIP` matching the deployment labels and exposing the container port.
6. Add a `ConfigMap` for non-sensitive config and a `Secret` (stringData, base64 handled by kubectl) for credentials;
   never inline secrets in the Deployment.
7. Add an `Ingress` with a host rule, path `/`, TLS secret reference, and an ingressClassName (e.g., `nginx`).
8. If stateful: add a `PersistentVolumeClaim` with the requested storage, access mode `ReadWriteOnce`, and a
   `volumeMounts` entry on the container.
9. Optionally add a `HorizontalPodAutoscaler` referencing the Deployment.
10. Validate the YAML locally with `kubectl apply --dry-run=client -f` and surface any errors.
11. Print the apply order: namespace, ConfigMap/Secret/PVC, Deployment, Service, Ingress.

## Inputs

- App name, container image (with digest preferred), container port, target namespace.
- Replica count, CPU/memory requests and limits.
- Liveness/readiness probe paths and ports (or TCP socket for startup).
- Ingress host, TLS secret name, ingressClassName.
- Optional PVC size and storageClassName for stateful workloads.

## Outputs

- `deployment.yaml` — Deployment with security context, resources, probes.
- `service.yaml` — ClusterIP Service exposing the app port.
- `configmap.yaml` — non-sensitive configuration.
- `secret.yaml` — opaque Secret with stringData placeholders.
- `ingress.yaml` — Ingress with host rules and TLS.
- `pvc.yaml` — PersistentVolumeClaim when stateful.
- `kustomization.yaml` (optional) — to bundle the above.

## Key Rules

- Always set `resources.requests` and `resources.limits`; pods without requests are un-schedulable cleanly.
- Always set a `securityContext` with `runAsNonRoot: true` and `readOnlyRootFilesystem: true` unless the app writes to
  disk (then mount a volume).
- Prefer image digests (`image@sha256:...`) over mutable tags for reproducibility.
- Never inline secrets in the Deployment; reference them by name and keep the Secret in a separate file (or external
  secret store).
- Readiness probe must check real readiness (e.g., a `/ready` endpoint that fails during startup and shutdown), not just
  TCP open.
- Set `revisionHistoryLimit` so `kubectl rollout undo` has revisions to roll back to.
- Use `app.kubernetes.io/name` and `app.kubernetes.io/instance` labels so Helm-style selectors work.

## Examples

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app.kubernetes.io/name: api
spec:
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/name: api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app.kubernetes.io/name: api
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
        - name: api
          image: registry.example.com/api:1.4.2@sha256:abc123...
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secret
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
```
