---
name: gitops-deployment-builder
description: Build GitOps deployments with ArgoCD or FluxCD application manifests, sync waves, health checks, and rollback via git revert. Use this when the user asks to set up GitOps, replace imperative kubectl apply with a reconciler, or wire sync waves for ordered deploys.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [gitops, argocd, fluxcd, sync-wave, kubernetes, reconciler]
related: [devops/kubernetes-manifest-builder, devops/helm-chart-author, devops/ci-cd-pipeline-builder]
prerequisites: [devops/kubernetes-manifest-builder]
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

# GitOps Deployment Builder

## When To Use

- The user says "set up GitOps with ArgoCD" or "deploy via FluxCD".
- The user wants a manifest repo to be the source of truth, with a reconciler applying changes.
- The user needs ordered deploys (CRDs → namespace → secrets → deployment → ingress) via sync waves.
- The user wants rollback to be a `git revert`, not a `kubectl rollout undo`.
- Trigger keywords: gitops, argocd, fluxcd, sync-wave, application manifest, kustomization, reconciler.

## Workflow

1. Pick the tool: ArgoCD (UI-first, `Application` CRD) or FluxCD (CRD-first, `Kustomization` + `GitRepository`).
2. Stand up the reconciler in the management cluster; for ArgoCD, install with the upstream Helm chart.
3. Create a manifest repo (or directory) per environment: `manifests/dev/`, `manifests/staging/`, `manifests/prod/`.
4. Author an `Application` (ArgoCD) or `Kustomization` (Flux) pointing at the repo, path, and target revision.
5. Annotate resources with `argocd.argoproj.io/sync-wave` so CRDs and namespaces apply before workloads.
6. Set sync policy to `automated` with `prune: true` and `selfHeal: true` for drift correction; disable for prod until
   the team is comfortable.
7. Wire health checks: set `argocd.argoproj.io/sync-options: Validate=false` where needed, and rely on built-in
   Deployment/StatefulSet health.
8. Configure the CI pipeline to commit a new image tag into `manifests/<env>/` instead of applying directly.
9. Test rollback by `git revert` of the image-tag commit; the reconciler applies the previous state.
10. Set up notifications (ArgoCD Notifications, Flux Receiver) to alert on sync failures or drift.

## Inputs

- Tool choice (ArgoCD, FluxCD).
- Manifest repo URL and per-env paths.
- Target namespace(s) and sync policy (automated vs manual).
- Sync-wave order if the stack has CRDs and namespaces.
- Notification channel (Slack, Teams).

## Outputs

- `argocd/apps/<env>-<app>.yaml` — ArgoCD `Application` manifests.
- `flux/<env>-<app>.yaml` — FluxCD `Kustomization` + `GitRepository`.
- `manifests/<env>/kustomization.yaml` — per-env kustomize bundle.
- `manifests/<env>/patch.yaml` — image-tag patch the CI pipeline updates.
- `README.md` — sync-wave order, rollback procedure, drift detection.

## Key Rules

- The manifest repo is the source of truth; never `kubectl apply` directly into a GitOps-managed namespace.
- Set sync waves so CRDs apply before their instances and namespaces apply before workloads.
- Enable `selfHeal: true` for non-prod to correct drift automatically; be deliberate about prod.
- Pin the `targetRevision` to a branch or tag; do not track `HEAD` in prod.
- Rollback is a `git revert` of the image-tag commit, not a `kubectl rollout undo` — the latter leaves drift.
- Sync failures must page someone; silent drift is the most common GitOps failure mode.
- Validate the manifest repo with `kustomize build` in CI before merge.

## Examples

```yaml
# argocd/apps/prod-api.yaml — ArgoCD Application.
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: prod-api
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/org/manifests
    targetRevision: main
    path: manifests/prod/api
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=false
      - Validate=true
      - PrunePropagationPolicy=foreground
```

```yaml
# manifests/prod/api/namespace.yaml — sync wave -10 applies first.
apiVersion: v1
kind: Namespace
metadata:
  name: prod
  annotations:
    argocd.argoproj.io/sync-wave: "-10"
---
# manifests/prod/api/deployment.yaml — sync wave 0.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: prod
  annotations:
    argocd.argoproj.io/sync-wave: "0"
spec:
  template:
    spec:
      containers:
        - name: api
          image: ghcr.io/org/api:sha-abc1234
```

```yaml
# flux/prod-api.yaml — FluxCD Kustomization + GitRepository.
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: manifests
  namespace: flux-system
spec:
  url: https://github.com/org/manifests
  ref:
    branch: main
  interval: 1m
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: prod-api
  namespace: flux-system
spec:
  sourceRef:
    kind: GitRepository
    name: manifests
  path: ./manifests/prod/api
  targetNamespace: prod
  interval: 5m
  prune: true
  wait: true
```

## References

- ArgoCD Documentation: https://argo-cd.readthedocs.io/
- ArgoCD Sync Waves: https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/
- FluxCD Documentation: https://fluxcd.io/flux/
- FluxCD Kustomization: https://fluxcd.io/flux/components/kustomize/kustomizations/
