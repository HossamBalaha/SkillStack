---
name: ci-cd-pipeline-builder
description: Build CI/CD pipelines with build, test, scan, and deploy stages, environment promotion, rollback strategy, and artifact management. Use this when the user asks to wire up GitHub Actions or GitLab CI, promote artifacts across environments, or design a safe rollback flow.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [cicd, github-actions, gitlab-ci, pipeline, deployment, rollback]
related: [devops/container-image-hardener, devops/gitops-deployment-builder, devops/helm-chart-author]
prerequisites: []
outputs: [yaml, bash, markdown]
difficulty: intermediate
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

# CI/CD Pipeline Builder

## When To Use

- The user says "set up CI/CD for our service" or "build a deploy pipeline with promotion stages".
- The user wants GitHub Actions or GitLab CI stages: build → test → scan → deploy.
- The user needs environment promotion (dev → staging → prod) with manual approvals.
- The user wants a rollback strategy that doesn't require a redeploy.
- Trigger keywords: pipeline, github-actions, gitlab-ci, promote, rollback, artifact, workflow.

## Workflow

1. Pick the CI engine: GitHub Actions (`.github/workflows/`), GitLab CI (`.gitlab-ci.yml`), or Jenkins.
2. Define the build stage: produce a versioned artifact — a container image tagged with the git SHA (not `latest`).
3. Define the test stage: unit + integration tests; fail fast on lint and type errors before expensive tests.
4. Define the scan stage: SCA (`trivy image`), SAST (Semgrep), license check; fail the pipeline on HIGH/CRITICAL
   findings.
5. Push the image to the registry (GHCR, ECR, Harbor) with both the SHA tag and the branch tag.
6. Define the deploy-to-dev stage (auto on push to `main`), deploy-to-staging (auto after dev passes), deploy-to-prod
   (manual approval via `environment: production`).
7. Use GitOps for the deploy stages: the pipeline commits a new image tag to a manifest repo, and ArgoCD/FluxCD
   reconciles.
8. Define the rollback: re-pin the manifest to the previous image tag (no rebuild), surfaced as a one-click action or a
   CLI command.
9. Cache dependencies and the Docker layer cache to keep pipeline runs under 10 minutes.
10. Emit pipeline metrics (duration, failure rate) to Prometheus so the team can see regressions.

## Inputs

- CI engine (GitHub Actions, GitLab CI, Jenkins).
- Container registry and credential secret names.
- Environments and promotion gates (auto/manual).
- Scan tools (Trivy, Grype, Semgrep) and severity thresholds.
- GitOps manifest repo URL if using ArgoCD/FluxCD.

## Outputs

- `.github/workflows/ci.yml` (or `.gitlab-ci.yml`) — the pipeline definition.
- `scripts/promote.sh` — promote an image tag across environments.
- `scripts/rollback.sh` — re-pin manifest to a previous tag.
- `Dockerfile` reference for multi-stage build (see `container-image-hardener`).
- `README.md` — pipeline diagram, secret list, rollback procedure.

## Key Rules

- Always tag images by git SHA; never deploy `latest` because it is not reproducible.
- Always run the scan stage before deploy; fail on HIGH/CRITICAL findings.
- Promotion across environments must reuse the same artifact — never rebuild per environment.
- Production deploys require a manual approval gate, not auto-promotion from staging.
- Rollback must be a manifest re-pin, not a redeploy from an older commit; this is faster and safer.
- Cache Docker layers and dependencies; a pipeline over 10 minutes erodes developer flow.
- Pipeline secrets live in the CI secret store, never in the YAML; reference them as `${{ secrets.X }}`.
- Emit pipeline metrics so duration/failure regressions are visible.

## Examples

```yaml
# .github/workflows/ci.yml — build, test, scan, promote.
name: ci
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
  packages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      tag: ${{ steps.meta.outputs.tag }}
    steps:
      - uses: actions/checkout@v4
      - id: meta
        run: echo "tag=sha-$(git rev-parse --short HEAD)" >> "$GITHUB_OUTPUT"
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ steps.meta.outputs.tag }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r Requirements.txt && pytest --cov=src --cov-fail-under=80
  scan:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ needs.build.outputs.tag }}
          severity: HIGH,CRITICAL
          exit-code: '1'
  deploy-staging:
    needs: [test, scan]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./scripts/promote.sh staging ${{ needs.build.outputs.tag }}
  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./scripts/promote.sh prod ${{ needs.build.outputs.tag }}
```

```bash
# scripts/rollback.sh — re-pin to the previous image tag.
set -euo pipefail
ENV="${1:?env required}"
PREV_TAG=$(git log --format=%H -n 2 -- manifests/${ENV}/ | tail -1 | cut -c1-7)
yq -i ".spec.template.spec.containers[0].image = \"ghcr.io/org/api:sha-${PREV_TAG}\"" \
  manifests/${ENV}/deployment.yaml
git commit -am "rollback ${ENV} to sha-${PREV_TAG}"
git push
```
