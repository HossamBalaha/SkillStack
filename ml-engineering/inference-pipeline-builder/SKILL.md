---
name: inference-pipeline-builder
description: Build a FastAPI inference endpoint when deploying a trained model as a service. Triggers on "FastAPI", "/predict endpoint", "pydantic schema", "torch.no_grad inference", "model.eval", "/healthz", "batch inference".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ml-engineering
tags: [fastapi, serving, inference, deployment]
related: [ml-engineering/model-checkpoint-manager, ml-engineering/metrics-computation-suite]
prerequisites: [ml-engineering/pytorch-lightning-scaffold]
outputs: [python, bash]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Inference Pipeline Builder

## When To Use

- Serving a trained model behind an HTTP API.
- Building `/predict` and `/healthz` endpoints with FastAPI.
- Defining request/response schemas with pydantic.
- Supporting batched inference for throughput.

## Workflow

1. Load the trained model and preprocessing artifacts (tokenizer, scaler) once at startup.
2. Resolve device once and call `model.to(device)` and `model.eval()`.
3. Define pydantic request and response schemas.
4. Implement `/predict` POST endpoint that validates input, preprocesses, runs the forward pass, and post-processes.
5. Wrap the forward pass in `torch.no_grad()`.
6. Implement `/healthz` GET endpoint for liveness probes.
7. Support batched inputs for throughput.
8. Run with `uvicorn` and document the OpenAPI schema automatically.

## Inputs

- A trained model checkpoint.
- Preprocessing artifacts (tokenizer, scaler) persisted via `joblib`.
- `Configs/Config.yaml` with `Host`, `Port`, `BatchSize`.

## Outputs

- A runnable FastAPI app file.
- `/predict` and `/healthz` endpoints.
- Auto-generated OpenAPI schema.

## Key Rules

- Call `model.eval()` and use `torch.no_grad()` for inference.
- Validate inputs with pydantic schemas.
- Load the model ONCE at startup, not per request.
- Resolve device once; do not call `torch.device(...)` per request.
- Reference real FastAPI docs at https://fastapi.tiangolo.com.

## Examples

```python
# FastAPI inference endpoint with batch support.
from typing import List
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Resolve device once at import time.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class PredictionRequest(BaseModel):
  """Schema for a single prediction request."""
  # CamelCase dict keys for consistency.
  Features: List[float]


class BatchPredictionRequest(BaseModel):
  """Schema for a batched prediction request."""
  FeaturesList: List[List[float]]


class PredictionResponse(BaseModel):
  """Schema for the prediction response."""
  Probabilities: List[float]
  PredictedClass: int


app = FastAPI(title="InferenceService")


def LoadModel(CheckpointPath):
  """Load the model once at startup."""
  # Load with map_location for safety.
  Model = torch.load(CheckpointPath, map_location=device)
  Model.to(device)
  Model.eval()
  return Model


@app.get("/healthz")
def Health():
  """Liveness probe."""
  return {"Status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def Predict(Request: PredictionRequest):
  """Run a single prediction."""
  # Convert the request to a tensor.
  tensor = torch.tensor([Request.Features], dtype=torch.float32, device=device)
  with torch.no_grad():
    # Forward pass under no-grad context.
    logits = Model(tensor)
    # Softmax post-processing.
    probs = torch.softmax(logits, dim=-1).squeeze(0).tolist()
  predictedClass = int(torch.argmax(logits, dim=-1).item())
  return PredictionResponse(Probabilities=probs, PredictedClass=predictedClass)


@app.post("/predict/batch", response_model=List[PredictionResponse])
def PredictBatch(Request: BatchPredictionRequest):
  """Run a batched prediction."""
  # Guard against empty batches.
  if (len(Request.FeaturesList) == 0):
    raise HTTPException(status_code=400, detail="Empty batch.")
  tensor = torch.tensor(Request.FeaturesList, dtype=torch.float32, device=device)
  with torch.no_grad():
    # Forward pass under no-grad context.
    logits = Model(tensor)
    # Softmax post-processing.
    probs = torch.softmax(logits, dim=-1).tolist()
  predictedClasses = torch.argmax(logits, dim=-1).tolist()
  return [
    PredictionResponse(Probabilities=p, PredictedClass=c)
    for p, c in zip(probs, predictedClasses)
  ]


# Model loaded at import time; replace path with configured value.
Model = LoadModel("Aggregated/BestModel.pt")
```

## References

- FastAPI documentation: https://fastapi.tiangolo.com
- pydantic v2: https://docs.pydantic.dev/latest/
- uvicorn deployment: https://www.uvicorn.org/
