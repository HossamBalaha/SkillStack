---
name: container-image-hardener
description: Harden container images using distroless or scratch bases, non-root users, multi-stage builds, SBOM generation, and vulnerability scanning with Trivy or Grype. Use this when the user asks to write a production Dockerfile, reduce image attack surface, or meet NIST SP 800-190 controls.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [distroless, sbom, trivy, hardening, dockerfile, non-root]
related: [devops/ci-cd-pipeline-builder, devops/kubernetes-manifest-builder]
prerequisites: []
outputs: [dockerfile, bash, markdown]
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

# Container Image Hardener

## When To Use

- The user says "write a production Dockerfile" or "harden this image".
- The user wants to drop the Debian/Ubuntu base for a distroless or scratch image.
- The user needs an SBOM attached to the image for supply-chain attestation.
- The user needs Trivy or Grype to fail the build on HIGH/CRITICAL CVEs.
- Trigger keywords: distroless, scratch, sbom, trivy, grype, cosign, non-root, multi-stage.

## Workflow

1. Pick a base: `gcr.io/distroless/python3-debian12:nonroot`, `cgr.dev/chainguard/python:latest`, or `scratch` for
   static binaries.
2. Use a multi-stage build: a `builder` stage with the full toolchain, a `runtime` stage with only the binary and
   runtime deps.
3. In the runtime stage, set `USER nonroot:nonroot` (or a numeric UID 10001) and `WORKDIR /app`.
4. Copy only the compiled artifact(s) and required runtime files; never copy `.git`, `node_modules`, or caches.
5. Drop capabilities with a `docker run --read-only --cap-drop=ALL --security-opt=no-new-privileges` runtime flag.
6. Generate an SBOM with `syft sbom <image> -o spdx-json` and attach it as an artifact alongside the image.
7. Scan with `trivy image --severity HIGH,CRITICAL --exit-code 1 <image>` and `grype <image> --fail-on high`.
8. Sign the image with `cosign sign --key kms://... <image>` to enable verification at admission time.
9. Pin base images by digest, not tag, so a malicious push to `:latest` cannot slip into your build.
10. Build a slim CI test stage that runs unit tests in the builder stage so the runtime stage never ships test deps.

## Inputs

- Application language and build toolchain (Python pip, Go modules, Node npm).
- Base image preference (distroless, Chainguard, scratch).
- SBOM format (SPDX JSON, CycloneDX).
- Scan threshold (fail on HIGH, fail on CRITICAL only).
- Signing key (Cosign KMS, keyless with OIDC).

## Outputs

- `Dockerfile` — multi-stage, non-root, distroless runtime.
- `.dockerignore` — excludes `.git`, `node_modules`, test artifacts.
- `sbom.spdx.json` — image SBOM.
- `scan.sh` — Trivy + Grype scan script.
- `sign.sh` — Cosign signing script.
- `README.md` — hardening controls, scan procedure, base-image pinning.

## Key Rules

- Always pin base images by digest, never by tag — a mutated `:latest` bypasses your supply chain.
- Always run as a non-root user with a fixed UID; many distroless images ship a `nonroot` user (UID 65532).
- Always use multi-stage builds; the builder stage must not be in the final image.
- Always generate and store an SBOM; an SBOM-less image cannot be triaged after a CVE drops.
- Always fail the build on HIGH/CRITICAL CVEs unless explicitly waived with a documented exception.
- Always set `--read-only` at runtime and mount writable volumes only where the app needs to write.
- Never run `apk add` or `apt-get install` in the runtime stage; it bloats the image and re-introduces CVEs.
- Sign the image with Cosign and verify at admission time via a policy controller (Kyverno, OPA Gatekeeper).

## Examples

```dockerfile
# Dockerfile — Python distroless, multi-stage, non-root.
FROM python:3.12-slim AS builder
WORKDIR /app
COPY Requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r Requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["python", "-m", "api.main"]
```

```bash
# scan.sh — Trivy + Grype, fail on HIGH/CRITICAL.
set -euo pipefail
IMAGE="${1:?image required}"

syft sbom "$IMAGE" -o spdx-json=sbom.spdx.json
trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed "$IMAGE"
grype "$IMAGE" --fail-on high
```

```bash
# sign.sh — Cosign keyless signing with OIDC.
set -euo pipefail
IMAGE="${1:?image required}"
cosign sign --yes "$IMAGE"
cosign verify "$IMAGE" \
  --certificate-identity "https://github.com/org/repo/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com
```

```dockerignore
# .dockerignore
.git
.github
node_modules
__pycache__
*.pyc
tests/
.pytest_cache/
.venv/
```
