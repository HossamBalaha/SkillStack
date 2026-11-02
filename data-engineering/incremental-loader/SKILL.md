---
name: incremental-loader
description: Load data incrementally using stateful checkpoints (last-modified or watermark columns), idempotent re-runs deduplicated by primary key, and a JSON state file. Use this skill for CDC pipelines, MERGE/UPSERT loads, and handling late-arriving records without full reprocessing.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: data-engineering
tags: [cdc, incremental, watermark, upsert, idempotent]
related: [data-engineering/etl-pipeline-builder, data-engineering/data-lineage-tracker]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Incremental Loader

## When To Use
- Source tables are large and a full snapshot per run is too expensive.
- Late-arriving records must be merged into the target without duplicating rows.
- The pipeline must be re-runnable: a retry must converge to the same final state.
- A watermark column (updated_at, event_at, scn) is available on the source.
- You are implementing CDC (Change Data Capture) or warehouse MERGE/UPSERT.

## Workflow
1. Pick the watermark column: monotonic, populated on every update, indexed on source.
2. Read the previous watermark from the JSON state file (default to epoch on first run).
3. Query the source for rows with `watermark > previousWatermark` and `<= runWindowEnd`.
4. Deduplicate in-batch rows by primary key, keeping the latest version per key.
5. MERGE into the target by primary key: insert new, update changed, optionally soft-delete.
6. Recompute the new watermark as `max(watermark)` of the loaded rows.
7. Persist the new watermark only after the MERGE commits.
8. Handle late arrivals: rows older than the previous watermark are merged regardless.
9. Emit a load report (rows inserted, updated, late, skipped) keyed by run_id.
10. Backfill by overriding the watermark window and running the same code.

## Inputs
- Source connection spec plus watermark column and primary key.
- Target connection spec plus the MERGE/UPSERT capability check.
- State file path storing the last successful watermark per table.
- Run window: start, end, and batch size for chunked reads.

## Outputs
- Updated target table with new and changed rows merged.
- Updated JSON state file with the new high-watermark.
- A load report (JSON) summarising inserts, updates, late arrivals, and skips.

## Key Rules
- The watermark is only advanced after the MERGE transaction commits.
- Re-running the same window is idempotent: target converges to the same final state.
- Late-arriving rows are merged by primary key, never dropped.
- The state file is the single source of truth; concurrent writers are rejected.
- Soft deletes are explicit: a tombstone column marks the row, not a hard delete.
- Every load records the source hash and run_id for downstream lineage.

## Examples

```python
import json
from pathlib import Path


def ReadWatermark(statePath, defaultValue):
  # Return the last persisted watermark or the default on first run.
  if (not Path(statePath).exists()):
    return defaultValue
  with open(statePath, "r", encoding="utf-8") as handle:
    state = json.load(handle)
  return state.get("Watermark", defaultValue)


def WriteWatermark(statePath, watermark, runId):
  # Persist the new watermark only after the merge has committed.
  state = {"Watermark": watermark, "RunId": runId}
  tmpPath = statePath + ".tmp"
  with open(tmpPath, "w", encoding="utf-8") as handle:
    json.dump(state, handle)
  Path(tmpPath).rename(statePath)


def IncrementalLoad(sourceConn, targetConn, primaryKey, watermarkCol, runWindow, statePath):
  # Pull changed rows from the source and merge them into the target.
  previousWatermark = ReadWatermark(statePath, runWindow["Start"])
  rows = sourceConn.Fetch(f"WHERE {watermarkCol} > %s AND {watermarkCol} <= %s",
                          (previousWatermark, runWindow["End"]))
  # Keep only the latest version per primary key.
  dedupedRows = DedupByKey(rows, primaryKey)
  inserted, updated = targetConn.Merge(dedupedRows, primaryKey)
  newWatermark = max(row[watermarkCol] for row in dedupedRows)
  WriteWatermark(statePath, newWatermark, runWindow["RunId"])
  return {"Inserted": inserted, "Updated": updated, "Watermark": newWatermark}


def DedupByKey(rows, primaryKey):
  # When the same key appears multiple times in a batch, keep the newest.
  latest = {}
  for row in rows:
    key = row[primaryKey]
    if (key not in latest or row["updated_at"] > latest[key]["updated_at"]):
      latest[key] = row
  return list(latest.values())
```

## References
- Change Data Capture patterns: https://en.wikipedia.org/wiki/Change_data_capture
- Snowflake MERGE: https://docs.snowflake.com/en/sql-reference/sql/merge
- BigQuery MERGE: https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#merge
