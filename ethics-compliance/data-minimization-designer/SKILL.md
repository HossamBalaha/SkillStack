---
name: data-minimization-designer
description: Design data-minimized pipelines that collect only necessary fields, enforce purpose limitation, set storage limits, and apply privacy-by-design principles from the earliest stage. Use when scoping a new data collection, an ML training set, or an analytics pipeline that touches personal or sensitive data.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [data-minimization, privacy-by-design, purpose-limitation, storage-limitation, gdpr-art-5]
related: [ethics-compliance/gdpr-data-protection-assessor, ethics-compliance/hipaa-compliance-checker, ethics-compliance/data-minimization-designer]
prerequisites: []
outputs: [markdown, yaml, python]
difficulty: intermediate
estimated_tokens: 1300
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Data Minimization Designer

## When To Use

- The user says "what data do we actually need?", "design a privacy-by-default schema", or "minimise our data
  collection".
- A new form, sensor, or analytics event is being added and there is no field-level justification.
- A model is being trained and the team wants to know which features are necessary versus merely available.
- A regulator or privacy office has flagged over-collection in a prior audit.
- Trigger keywords: data minimization, privacy by design, purpose limitation, storage limitation, GDPR Article 5,
  need-to-know.

## Workflow

1. State the primary purpose for which data is being collected; if there is no clearly stated purpose, collection is
   premature.
2. List every candidate field and ask three questions: does it serve the stated purpose? is there a less identifying
   alternative? is the precision justified?
3. Apply the necessity test: each retained field must be necessary, adequate, relevant, and limited to what is necessary
   (GDPR Article 5(1)(c)).
4. Replace identifying fields with pseudonymous or aggregate alternatives: email → opaque ID, exact date of birth → age
   band, exact geolocation → city.
5. Apply precision reduction: truncate timestamps to day, coarsen GPS to city block, aggregate small cells, bin ages.
6. Define the storage limitation: per data category, the retention period, the trigger for deletion, and the destruction
   method.
7. Define the access limitation: per data category, the roles allowed, the purpose bound at access time, and the audit
   logging.
8. Where aggregation is used, verify the minimum cell size (typically k >= 5 to k >= 11 depending on context).
9. Document the data flow: collection → processing → storage → sharing → destruction, with minimisation applied at each
   hop.
10. Add privacy-by-design controls: default opt-out, default off for sensitive toggles, encryption at rest and in
    transit, and access reviews on a fixed cadence.
11. Provide a code-level minimisation snippet showing how to enforce the reduced schema in an ingestion pipeline.
12. Produce a minimisation report card with the original count of fields, the minimised count, and the per-field
    rationale.

## Inputs

- Stated purpose of data collection.
- Candidate data dictionary with proposed fields and types.
- Roles in the system and their access needs.
- Retention policy and legal basis for each field.
- Any prior minimisation analyses or audits.

## Outputs

- `purpose_statement.md` — primary and secondary purposes explicitly listed.
- `field_necessity_matrix.md` — field × purpose × necessity × alternative × retained precision.
- `minimised_schema.yaml` — the reduced schema enforced by the pipeline.
- `retention_schedule.md` — category × retention period × trigger × destruction method.
- `access_matrix.md` — role × data category × purpose × audit logging.
- `data_flow_diagram.md` — collection → processing → storage → sharing → destruction.
- `minimisation_snippet.py` — Python ingestion code enforcing the reduced schema.
- `minimisation_report_card.md` — before/after field counts and per-field rationale.

## Key Rules

- Each retained field must map to at least one stated purpose; orphan fields must be removed.
- Pseudonymisation does not equal anonymisation; the linking key still requires protection.
- Aggregated data with cells smaller than the minimum cell size must be suppressed or merged with a neighbour.
- Retention periods must be enforced automatically; "we will delete when we remember" is non-compliant.
- Access must be purpose-bound at the time of access; broad "read-all" roles are non-compliant.
- Encryption is necessary but not sufficient; minimisation reduces risk before encryption applies.
- Collection of "nice-to-have" data for future unspecified purposes violates purpose limitation.
- Logs and telemetry must be subject to the same minimisation rules as primary data.

## Examples

```text
Field necessity matrix (excerpt):
  Field            Purpose          Necessary?  Alternative        Decision
  email            account login   yes         opaque login ID    RETAIN (hashed)
  email            marketing       no          consent-gated flag REMOVE
  date_of_birth    age verification yes        age band           COARSEN to age band
  ip_address       security audit  yes         truncated /24      COARSEN
  gender           analytics       optional    suppressed         SUPPRESS if cell <11
```

```python
# minimisation_snippet.py (excerpt)
ALLOWED_FIELDS = {"user_id", "age_band", "city", "device_class"}
def minimise(record: dict) -> dict:
    return {k: v for k, v in record.items() if k in ALLOWED_FIELDS}
```
