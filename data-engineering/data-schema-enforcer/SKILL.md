---
name: data-schema-enforcer
description: Enforce schemas on incoming rows using pydantic BaseModel type annotations and validators or pandera DataFrameSchema. Use this skill when rejecting invalid rows, quarantining soft failures, or producing a validation report with passed/failed counts and sample failures.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [schema, pydantic, pandera, validation, quarantine]
related: [data-engineering/data-quality-validator, data-engineering/etl-pipeline-builder]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Data Schema Enforcer

## When To Use

- A pipeline ingests user-uploaded or partner-supplied rows of unknown quality.
- Hard rejection and soft quarantine must be distinguishable per column rule.
- A validation report must accompany every batch (counts, samples, reasons).
- Schemas evolve and old batches must still validate against their original schema.
- You are using pydantic models or pandera schemas as the contract.

## Workflow

1. Author a pydantic `BaseModel` (row-level) or pandera `DataFrameSchema` (batch-level).
2. Tag each field with type, nullability, and a validator where needed.
3. Configure severity per rule: `fail` halts the row, `warn` quarantines it.
4. Iterate the batch row by row, attempting validation against the model.
5. On success, append to the clean list; on failure, append to quarantine with the reason.
6. Build a validation report with passed count, failed count, and sample failures.
7. Write clean rows, quarantine rows, and the report atomically.
8. Surface the report to the orchestrator so downstream tasks can branch on status.

## Inputs

- The incoming batch (list of dicts, DataFrame, or file).
- The schema definition (pydantic model or pandera schema).
- The severity map (column to fail/warn/quarantine).

## Outputs

- A clean rows artifact that passed every fail-level rule.
- A quarantined rows artifact with one reason column per row.
- A validation report (JSON) with passed count, failed count, and samples.
- An exit code the orchestrator can branch on.

## Key Rules

- Schemas are versioned; a batch records the schema version it was validated against.
- Fail-level rules reject the row entirely; warn-level rules quarantine but keep going.
- Reports include sample failures, not the entire bad batch.
- Validators must be deterministic; no random checks, no time-of-day checks.
- Quarantined rows keep the original payload plus a `ValidationError` column.
- Re-running enforcement on the same batch yields the same partition split.

## Examples

```python
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRow(BaseModel):
  # Pydantic model that enforces the row-level contract.
  UserId: int = Field(gt=0)
  Email: EmailStr
  DateOfBirth: date
  Country: str

  @field_validator("Country")
  @classmethod
  def CountryMustBeIsoAlpha2(cls, value):
    # Reject anything that is not a 2-letter country code.
    if (len(value) != 2 or not value.isalpha()):
      raise ValueError("Country must be ISO Alpha-2")
    return value.upper()


def EnforceSchema(rows, model, severityMap):
  # Split rows into clean and quarantined partitions.
  cleanRows = []
  quarantinedRows = []
  for row in rows:
    try:
      validated = model(**row)
      cleanRows.append(validated.model_dump())
    except Exception as error:
      # Attach the reason so reviewers can triage.
      row["ValidationError"] = str(error)
      quarantinedRows.append(row)
  return cleanRows, quarantinedRows


def BuildReport(cleanRows, quarantinedRows, schemaVersion):
  # Produce a machine-readable validation report.
  return {
    "SchemaVersion": schemaVersion,
    "Passed": len(cleanRows),
    "Failed": len(quarantinedRows),
    "SampleFailures": quarantinedRows[:10],
  }
```
