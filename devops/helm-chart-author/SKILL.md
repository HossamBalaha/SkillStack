---
name: helm-chart-author
description: Author Helm charts with a valid Chart.yaml, values.yaml, templates/ tree, _helpers.tpl, and lifecycle hooks. Use this when the user wants to package an app for Helm, parameterize an existing manifest, or add pre-install/post-upgrade hooks.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [helm, chart, templates, values, hooks, kubernetes]
related: [devops/kubernetes-manifest-builder, devops/gitops-deployment-builder]
prerequisites: [devops/kubernetes-manifest-builder]
outputs: [yaml, markdown]
difficulty: intermediate
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Helm Chart Author

## When To Use

- The user says "turn this K8s manifest into a Helm chart" or "package our service for Helm".
- The user needs parameterized values across environments (dev/staging/prod) without forking YAML.
- The user wants pre-install, post-upgrade, or pre-rollback hooks (e.g., run a DB migration job).
- The user needs a `_helpers.tpl` for shared label and name templates.
- Trigger keywords: helm, chart, values.yaml, templates, helm install, _helpers.tpl.

## Workflow

1. Scaffold the chart layout: `Chart.yaml`, `values.yaml`, `templates/`, `templates/_helpers.tpl`, `templates/tests/`.
2. Author `Chart.yaml` with `apiVersion: v2`, `name`, `description`, `type: application`, `version` (chart), and
   `appVersion` (app).
3. Author `values.yaml` with sensible defaults: `replicaCount`, `image.repository`/`tag`/`pullPolicy`, `resources`,
   `service`, `ingress`, `env`, `probes`.
4. Write `templates/_helpers.tpl` defining `chart.fullname`, `chart.labels`, and `chart.selectorLabels` so all templates
   share consistent names.
5. Convert Deployment, Service, ConfigMap, Secret, Ingress, and HPA manifests to templated versions under `templates/`.
6. Use `{{ include "chart.labels" . | nindent 4 }}` for labels and `{{ .Values.replicaCount }}` for parameters.
7. Wrap optional resources (Ingress, HPA) in `{{- if .Values.ingress.enabled }}` blocks so they can be toggled.
8. Add hook templates under `templates/` with `annotations: "helm.sh/hook": pre-install, post-upgrade, etc.
9. Add a `templates/tests/test-connection.yaml` using `helm.sh/hook: test` for `helm test`.
10. Lint with `helm lint ./chart` and template with `helm template ./chart` to catch rendering errors.
11. Document overrides in a `README.md` and per-env `values-dev.yaml` / `values-prod.yaml`.

## Inputs

- App name, semantic chart version, and app version.
- Default values: replicas, image repo and tag, resources, service type and port, ingress host.
- Environment-specific overrides (dev/staging/prod values files).
- Optional hook requirements (DB migration, smoke test).

## Outputs

- `Chart.yaml` — chart metadata.
- `values.yaml` — default values.
- `values-{env}.yaml` — environment overrides.
- `templates/_helpers.tpl` — shared named templates.
- `templates/deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`, `ingress.yaml`, `hpa.yaml`.
- `templates/tests/test-connection.yaml` — `helm test` hook.
- `README.md` — values reference.

## Key Rules

- Always use `apiVersion: v2` for new charts; `v1` is deprecated.
- Never hardcode names; use `{{ include "chart.fullname" . }}` so releases don't collide.
- Always set `resources` in `values.yaml` defaults, even if minimal — empty defaults lead to un-schedulable pods.
- Use `{{- with .Values.podSecurityContext }}` blocks so values can be overridden per-env cleanly.
- Keep image tag and repository separate values so prod can pin a digest while dev tracks `latest`.
- Hooks must set `"helm.sh/hook-weight"` if order matters and `"helm.sh/hook-delete-policy"` to avoid leaking jobs.
- Lint before publishing: `helm lint` catches YAML errors and missing required values.

## Examples

```yaml
# Chart.yaml
apiVersion: v2
name: api
description: REST API for the platform
type: application
version: 0.3.0
appVersion: "1.4.2"
maintainers:
  - name: platform-team
```

```yaml
# values.yaml
replicaCount: 3
image:
  repository: registry.example.com/api
  tag: "1.4.2"
  pullPolicy: IfNotPresent
resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: false
  className: nginx
  host: api.example.com
```

```yaml
# templates/_helpers.tpl
{{- define "api.fullname" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "api.labels" -}}
app.kubernetes.io/name: {{ include "api.fullname" . }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
```
