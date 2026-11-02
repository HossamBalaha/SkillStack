---
name: data-quality-validator
description: Validate datasets against declarative schemas using pandera DataFrameSchemas and Great Expectations suites. Use this skill when enforcing null/duplicate/outlier checks, detecting drift, or failing-fast pipelines with actionable error messages on tabular data.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: data-engineering
tags: [data-quality, pandera, great-expectations, validation, schema]
related: [data-engineering/data-schema-enforcer, data-engineering/data-drift-monitor, data-engineering/etl-pipeline-builder]
prerequisites: []
outputs: [python, json]
difficulty: intermediate
estimated_tokens: 1000
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
---

# Data Quality Validator

## When To Use
- A pipeline must fail fast on bad data instead of silently propagating garbage.
- You need declarative checks: null presence, uniqueness, value range, set membership.
- Drift between train and production data must be quantified and alerted on.
- A dataset is loaded for the first time and needs a contract before downstream use.
- Validation results must be tracked over time (run_id, suite version, pass rate).

## Workflow
1. Profile a sample of the dataset to learn column types and distributions.
2. Author a pandera `DataFrameSchema` (or Great Expectations suite) capturing the contract.
3. Encode column-level checks: not-null, unique, in-set, value range, regex format.
4. Encode dataset-level checks: row count bounds, primary key uniqueness, referential integrity.
5. Run validation against the full batch, capturing failed checks and sample failures.
6. Compute drift metrics (PSI, KS) against a reference snapshot for top features.
7. Decide fail vs warn: hard failures stop the pipeline; warnings quarantine and continue.
8. Emit a validation report (JSON) with counts, failed checks, and sample bad rows.
9. Register the report against the run_id so trends are queryable.
10. Re-run on a fixed window when fixes are deployed to confirm regression is gone.

## Inputs
- The dataset to validate (DataFrame, file, or warehouse table).
- The schema/suite definition (Python module or YAML).
- A reference snapshot for drift comparison (optional).
- Severity map per check: fail, warn, or quarantine.

## Outputs
- A validation report (JSON) with per-check status and sample failures.
- A quarantined rows artifact for warn-level failures.
- A drift report comparing current vs reference distributions.
- An exit code the orchestrator can branch on (0 pass, non-zero fail).

## Key Rules
- Validation is declarative and versioned alongside the dataset contract.
- Fail fast: a hard failure halts the pipeline before downstream consumers see bad data.
- Every failed check carries sample rows and the exact failing predicate.
- Reference snapshots for drift are immutable per training run.
- Schema changes require bumping the schema version and the suite version together.
- Validation runs on every batch, not only on schema-change events.
- Never mutate the dataset during validation; checks are read-only.

## Examples

```python
import pandera as pa
from pandera import Column, Check


UserSchema = pa.DataFrameSchema({
  "user_id": Column(int, checks=[Check.gt(0), Check.unique]),
  "email": Column(str, checks=[Check.str_matches(r"^[^@]+@[^@]+\.[^@]+$")], nullable=False),
  "age": Column(int, checks=[Check.ge(0), Check.le(130)], nullable=True),
  "country": Column(str, checks=[Check.isin(["US", "CA", "GB", "AU"])]),
})


def ValidateBatch(df, schema=UserSchema):
  # Run the schema and return a structured report.
  try:
    schema.validate(df, lazy=True)
    return {"Status": "Passed", "FailedChecks": [], "SampleFailures": []}
  except pa.errors.SchemaErrors as error:
    # Capture every failing check plus a sample of bad rows.
    return {
      "Status": "Failed",
      "FailedChecks": list(error.failure_cases.head(10).to_dict("records")),
      "SampleFailures": error.data.head(10).to_dict("records"),
    }


def AssertUniqueness(df, primaryKey):
  # Hard-fail when the natural key is not unique.
  duplicateCount = df.duplicated(subset=primaryKey).sum()
  if (duplicateCount > 0):
    raise ValueError(f"{duplicateCount} duplicate {primaryKey} rows")
```

## References
- pandera: https://pandera.readthedocs.io
- Great Expectations: https://greatexpectations.io
- Expectation gallery: https://greatexpectations.io/expectations
