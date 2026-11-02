---
name: etl-pipeline-builder
description: Design and implement idempotent ETL pipelines that Extract from APIs/DBs/files, Validate schemas, Transform clean data, and Load to warehouses or lakes. Use this skill when building batch pipelines, wiring Airflow/Prefect/Dagster DAGs, defining dbt models, or wiring row-level audit trails and provenance for every record.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [etl, pipeline, airflow, dbt]
related: [data-engineering/data-quality-validator, data-engineering/data-lineage-tracker]
prerequisites: []
outputs: [python, yaml]
difficulty: advanced
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# ETL Pipeline Builder

## When To Use

- A user asks to "build an ETL pipeline", "wire a DAG", or "move data from source X to warehouse Y".
- Reproducibility matters: re-running the same job must produce identical output (idempotency).
- Sources include REST APIs, OLTP databases, files (CSV/Parquet/JSON), or message queues.
- The target is a warehouse (BigQuery, Snowflake, Redshift), lake (S3/GCS/Azure), or file sink.
- Row-level governance is required: every row must carry provenance and audit metadata.
- You are using orchestrators such as Airflow, Prefect, Dagster, or dbt models.

## Workflow

1. Profile the source: schema, primary keys, update cadence, expected row volume.
2. Pick the extraction mode: full snapshot vs incremental watermark (CDC).
3. Define a `DataFrameSchema` (pandera) or pydantic models that describe valid rows.
4. Implement Extract, Validate, Transform, and Load as separate, pure functions.
5. Decorate each transform with row-level governance (source uri, ingested_at, batch_id).
6. Make Load idempotent: MERGE/UPSERT on the natural key, or overwrite partition.
7. Write an audit record per batch: counts in/out/quarantined, hashes, run_id.
8. Wrap the four steps in a single orchestrator task so a retry replays cleanly.
9. Add data tests (not-null, unique, referential) at the boundary after Transform.
10. Emit a run report (JSON) summarising timings, row counts, and failed checks.
11. Backfill safely by parameterising the run window and stamping the batch_id.

## Inputs

- Source connection spec (URI, credentials reference, table or endpoint name).
- Target connection spec (warehouse table or lake path, partition columns).
- Schema definition file (YAML/JSON or pandera/pydantic module).
- Run configuration: start/end time, batch_id, mode (full or incremental).

## Outputs

- A runnable pipeline module with `Extract`, `Validate`, `Transform`, `Load` functions.
- An audit log table/file with one row per source row plus batch metadata.
- A run report (JSON) capturing counts, durations, and validation failures.
- A quarantine sink for rows that failed validation.

## Key Rules

- Idempotency is non-negotiable: same input window plus run_id yields identical output.
- Never mutate the source during Extract; always read with a snapshot or as-of timestamp.
- Reject silent drops: every filtered row must land in the quarantine sink with a reason.
- Each transform function is pure: deterministic input to deterministic output.
- Partition the target by event date so backfills overwrite only the affected slice.
- Emit a content hash (sha256) for every loaded row to enable downstream lineage.
- Secrets live in the orchestrator's secret store, never in code or config files.
- Validate before Transform; Transform never sees invalid rows.

## Examples

```python
import hashlib
import json
from datetime import datetime, timezone


def ExtractFromApi(endpoint, runConfig):
  # Fetch a page of records from the source API.
  rawRows = ApiClient.Get(endpoint, params=runConfig)
  return rawRows


def ValidateRows(rawRows, schema):
  # Run pandera checks and split clean vs quarantined rows.
  cleanRows = []
  quarantinedRows = []
  for row in rawRows:
    try:
      schema.validate(row)
      cleanRows.append(row)
    except Exception as error:
      row["ValidationError"] = str(error)
      quarantinedRows.append(row)
  return cleanRows, quarantinedRows


def TransformRows(cleanRows, runConfig):
  # Normalise types, derive columns, stamp provenance on every row.
  transformedRows = []
  for row in cleanRows:
    record = {
      "UserId": row["user_id"],
      "EventAt": datetime.fromisoformat(row["event_at"]),
      "SourceUri": runConfig["SourceUri"],
      "IngestedAt": datetime.now(timezone.utc),
      "BatchId": runConfig["BatchId"],
      "ContentHash": hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest(),
    }
    transformedRows.append(record)
  return transformedRows


def LoadToWarehouse(rows, targetTable, runConfig):
  # Upsert by primary key so re-runs are idempotent.
  warehouse.Merge(targetTable, rows, primaryKey="UserId")
  return {"Loaded": len(rows), "BatchId": runConfig["BatchId"]}
```

## References

- dbt ETL best practices: https://www.getdbt.com/blog/etl-pipeline-best-practices
- Databricks SQL ETL: https://www.databricks.com/blog/sql-etl-pipeline
- Airflow: https://airflow.apache.org
- Prefect: https://www.prefect.io
- Dagster: https://dagster.io
- dbt: https://www.getdbt.com
