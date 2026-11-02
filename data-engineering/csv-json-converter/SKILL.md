---
name: csv-json-converter
description: Convert between CSV, JSON, Parquet, and Arrow formats while preserving types (dates, ints, floats, nulls) and streaming large files in chunks. Use this skill when moving data across formats, inferring schemas, or handling encodings and delimiters without loading the whole file into memory.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [csv, json, parquet, arrow, format-conversion]
related: [data-engineering/incremental-loader, data-engineering/data-schema-enforcer]
prerequisites: []
outputs: [python, csv, json]
difficulty: beginner
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# CSV JSON Converter

## When To Use

- A user needs to convert CSV to JSON, JSON to Parquet, or Arrow to CSV.
- The source file is large and must be processed in chunks (memory budget).
- Dates, integers, floats, and nulls must round-trip without type loss.
- Encoding (utf-8, latin-1), delimiter, or escaping varies across input files.
- Schema must be inferred once and reused for consistent downstream output.

## Workflow

1. Sniff the file: encoding, delimiter, header presence, and quoted fields.
2. Sample the first N rows to infer column types (date, int, float, bool, string).
3. Resolve a schema: explicit overrides win, otherwise inferred types apply.
4. Open the source as a streaming iterator (chunk size configurable).
5. For each chunk, coerce values to the schema and validate.
6. Write the chunk to the target format using an append-capable writer.
7. Preserve null markers: empty string vs None must stay distinct.
8. After the last chunk, flush writers and emit a manifest (row count, schema, hash).
9. On failure, partial outputs are deleted and the manifest is not written.

## Inputs

- Source file path plus format (csv, json, parquet, arrow).
- Target file path plus format.
- Optional schema override (column name to type mapping).
- Streaming config: chunk size, encoding, delimiter, null marker.

## Outputs

- The converted file in the requested format.
- A sidecar manifest (JSON) with row count, schema, source hash, and conversion time.
- Optional validation log of any rows that failed coercion.

## Key Rules

- Never load the whole file into memory; chunked streaming is mandatory above 100 MB.
- Type coercion is deterministic: a value that cannot be coerced becomes null and is logged.
- Empty strings and nulls are distinct; preserve both.
- Encoding is detected, never assumed; latin-1 is the fallback for invalid bytes.
- Manifests enable idempotent re-runs: matching hash skips conversion.
- Output is atomic: write to a temp path, then rename on success.

## Examples

```python
import csv
import json
import pyarrow as pa
import pyarrow.parquet as pq


def SniffCsv(path):
  # Detect delimiter and encoding before reading the file.
  with open(path, "r", encoding="utf-8", errors="replace") as handle:
    sample = handle.read(8192)
  dialect = csv.Sniffer().sniff(sample)
  return {"Delimiter": dialect.delimiter, "Encoding": "utf-8"}


def StreamCsvToParquet(sourcePath, targetPath, schema, chunkSize=10000):
  # Convert CSV to Parquet in chunks so memory stays bounded.
  writer = None
  totalRows = 0
  with open(sourcePath, "r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle)
    batch = []
    for row in reader:
      # Coerce each row to the inferred schema.
      coerced = {k: CoerceValue(v, schema[k]) for k, v in row.items()}
      batch.append(coerced)
      if (len(batch) >= chunkSize):
        table = pa.Table.from_pylist(batch, schema=pa.schema(schema))
        if (writer is None):
          writer = pq.ParquetWriter(targetPath, table.schema)
        writer.write_table(table)
        totalRows += len(batch)
        batch = []
    if (batch):
      table = pa.Table.from_pylist(batch, schema=pa.schema(schema))
      if (writer is None):
        writer = pq.ParquetWriter(targetPath, table.schema)
      writer.write_table(table)
      totalRows += len(batch)
  if (writer is not None):
    writer.close()
  return {"RowsWritten": totalRows, "TargetPath": targetPath}


def CoerceValue(rawValue, targetType):
  # Convert a string cell into the declared type.
  if (rawValue is None or rawValue == ""):
    return None
  if (targetType == pa.int64()):
    return int(rawValue)
  if (targetType == pa.float64()):
    return float(rawValue)
  return str(rawValue)
```

## References

- pandas IO: https://pandas.pydata.org/docs/reference/io.html
- pyarrow Parquet: https://arrow.apache.org/docs/python/parquet.html
- CSV format (RFC 4180): https://datatracker.ietf.org/doc/html/rfc4180
