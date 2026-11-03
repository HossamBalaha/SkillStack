---
name: docker-research-container
description: "Build a `Dockerfile` for reproducible research that installs system deps, copies `Requirements.txt`, runs `pip install --no-cache-dir`, creates a non-root user, sets `WORKDIR`, and defines an `ENTRYPOINT`. Use this when shipping a runnable container for a paper's code, a shared compute cluster job, or a journal artifact review. Triggers: Dockerfile, reproducible research container, CUDA image, non-root user, multi-stage build."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [docker, container, reproducibility]
related: [project-tooling/github-actions-research-ci, project-tooling/environment-yaml-builder]
prerequisites: []
outputs: [dockerfile, bash]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Docker Research Container

## When To Use

- A journal or conference asks for a Docker artifact so reviewers can run your code.
- You need to reproduce results on a cluster where the host Python version differs from your dev box.
- Your training requires CUDA and you want a pinned `nvidia/cuda` base image.
- You want a multi-stage build that strips build tools from the final runtime image.

## Workflow

1. Decide CPU vs GPU base: `python:3.11-slim` for CPU, `nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04` for GPU.
2. Set `WORKDIR /app` and install system dependencies with `apt-get` in one `RUN` to keep layers small.
3. Copy only `Requirements.txt` first, then `pip install --no-cache-dir -r Requirements.txt` to leverage layer caching.
4. Copy the rest of the source (`COPY src/ ./src/`, `COPY Main.py ./`).
5. Create a non-root user and switch to it (`useradd -m appuser && USER appuser`).
6. Expose any port the app needs (optional, only if a service runs).
7. Set `ENTRYPOINT ["python", "Main.py"]` (or the script that runs the pipeline).
8. If using multi-stage, build in a `builder` stage then copy only the runtime venv into the final image.
9. Add a `.dockerignore` that excludes `Datasets/`, `results/`, `.git/`, `*.zip`, `__pycache__/`.
10. Validate with `docker build -t researchkit .` then `docker run --rm researchkit --help`.

## Inputs

- Base image choice (CPU or GPU).
- System-level dependencies (e.g. `git`, `build-essential`, `libgl1` for OpenCV).
- The `Requirements.txt` file from the repo root.
- The entrypoint command (default `python Main.py`).

## Outputs

- `Dockerfile` at the repo root.
- `.dockerignore` excluding heavy and non-reproducible paths.
- Optional `docker-compose.yml` for multi-container setups.
- A one-line `docker run` command documented in the README.

## Key Rules

- Never run the final image as `root`; always create and switch to a non-root user.
- Always use `pip install --no-cache-dir` to keep the image layer small.
- Pin the base image by digest or full tag (`python:3.11-slim`, not `python:latest`).
- Copy `Requirements.txt` before the source so dependency changes don't bust the source layer.
- Keep `apt-get install` on a single line with `rm -rf /var/lib/apt/lists/*` cleanup.
- Multi-stage builds must copy only what the runtime needs; never copy the builder's compilers.
- For GPU images, document the `--gpus all` flag in the run command.
- Never bake secrets, tokens, or dataset files into the image.

## Examples

Single-stage CPU image:

```dockerfile
# Dockerfile — reproducible research container, CPU.
FROM python:3.11-slim

# Install system deps and clean up in one layer.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgl1 \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory.
WORKDIR /app

# Copy and install Python deps first for layer caching.
COPY Requirements.txt ./
RUN pip install --no-cache-dir -r Requirements.txt

# Copy the source tree.
COPY src/ ./src/
COPY Main.py ./

# Create and switch to a non-root user.
RUN useradd -m appuser
USER appuser

# Default entrypoint.
ENTRYPOINT ["python", "Main.py"]
```

Multi-stage GPU image:

```dockerfile
# Dockerfile — multi-stage GPU build for reproducible research.
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    build-essential git libgl1 \
  && rm -rf /var/lib/apt/lists/*

FROM base AS builder
WORKDIR /build
COPY Requirements.txt ./
RUN pip3 install --no-cache-dir --user -r Requirements.txt

FROM base AS runtime
WORKDIR /app
# Copy installed user-site packages from the builder.
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY src/ ./src/
COPY Main.py ./
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
ENTRYPOINT ["python3", "Main.py"]
```

Run command:

```bash
# CPU run.
docker run --rm -v $(pwd)/Datasets:/app/Datasets researchkit

# GPU run.
docker run --rm --gpus all -v $(pwd)/Datasets:/app/Datasets researchkit
```
