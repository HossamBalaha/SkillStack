---
name: hipaa-compliance-checker
description: Check HIPAA compliance for health data by identifying Protected Health Information (PHI), validating Safe Harbor de-identification against the 18 identifiers, documenting Expert Determination, reviewing Business Associate Agreements, and verifying the minimum necessary standard. Use when handling US health data for research, analytics, or product development.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [hipaa, phi, safe-harbor, baa, minimum-necessary]
related: [ethics-compliance/irb-protocol-drafter, ethics-compliance/data-minimization-designer, ethics-compliance/gdpr-data-protection-assessor]
prerequisites: []
outputs: [markdown, yaml]
difficulty: advanced
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# HIPAA Compliance Checker

## When To Use

- The user says "is this HIPAA compliant?", "de-identify our dataset", or "do we need a BAA with this vendor?".
- A research team is about to receive a limited dataset from a covered entity.
- A health-tech product wants to confirm that analytics data is properly de-identified.
- A vendor processes PHI on behalf of a covered entity and a Business Associate Agreement is being drafted.
- Trigger keywords: HIPAA, PHI, Safe Harbor, Expert Determination, BAA, minimum necessary, covered entity, business
  associate.

## Workflow

1. Determine whether the organisation is a covered entity, business associate, or neither under 45 CFR 160.103.
2. Inventory the data fields and identify which constitute Protected Health Information (PHI) — any health information
   tied to an identifiable individual.
3. Choose a de-identification method: Safe Harbor (45 CFR 164.514(b)(2)) or Expert Determination (164.514(b)(1)).
4. For Safe Harbor, remove all 18 enumerated identifiers: names, geographic subdivisions smaller than state (with
   exceptions for first three ZIP digits if >20,000), dates (except year), phone, fax, email, SSN, MRN, health plan
   beneficiary numbers, account numbers, certificate/license numbers, vehicle identifiers, device identifiers, URLs, IP
   addresses, biometric identifiers, full-face photos, and any other unique identifying number.
5. Confirm no actual knowledge remains that the remaining data could identify an individual.
6. For Expert Determination, document the expert's qualifications, the method used, the analysis, and the resulting risk
   determination that re-identification is very small.
7. Build a Limited Data Set where direct identifiers are removed but dates and geographic city/state/township are
   retained; this requires a Data Use Agreement (45 CFR 164.514(e)).
8. Review each vendor relationship: if PHI is created, received, maintained, or transmitted on behalf of a covered
   entity, a Business Associate Agreement is mandatory.
9. Verify the BAA contains the required safeguards: subcontractor flow-down, breach notification, access by the covered
   entity, return or destruction at termination, and audit rights.
10. Apply the minimum necessary standard (164.502(b) and 164.514(d)) to every PHI request; document the role-based
    access matrix.
11. Map the breach notification workflow under 45 CFR 164.400-414: 60-day individual notice, 60-day HHS notice, and
    annual summary for breaches under 500 individuals.
12. Produce a compliance report with non-conformances, severity, owner, and remediation deadline.

## Inputs

- Data dictionary of the dataset or system under review.
- Vendor list with their roles and the data they access.
- Existing BAAs and DUAs as applicable.
- Role-based access matrix or system permissions export.
- Risk appetite and any institutional policy overrides.

## Outputs

- `phi_inventory.md` — every field flagged as PHI or non-PHI with rationale.
- `safe_harbor_checklist.md` — the 18 identifiers checked off field by field.
- `expert_determination_record.md` — qualifications, method, analysis, risk result.
- `limited_data_set_dua.md` — Data Use Agreement template for 164.514(e).
- `baa_review.md` — per-vendor BAA sufficiency with missing-clause list.
- `minimum_necessary_matrix.md` — role × data element access matrix.
- `breach_response_plan.md` — notification workflow and timelines.
- `compliance_report.yaml` — machine-readable findings with severity.

## Key Rules

- Safe Harbor requires removal of all 18 enumerated identifiers; partial removal is non-compliant.
- A ZIP code's first three digits may be retained only if the corresponding geographic area has more than 20,000 people;
  otherwise the first three digits change to 000.
- Dates related to an individual (birth, admission, discharge, death) must be reduced to year, except ages over 89 which
  must be aggregated to "90 or older".
- Expert Determination requires an expert with appropriate qualifications; the determination has no fixed expiration but
  must be re-validated when data or context change.
- A Business Associate Agreement is required even if the vendor only stores encrypted PHI; encryption alone does not
  remove the vendor's status.
- The minimum necessary standard does not apply to disclosures to or requests by a healthcare provider for treatment
  purposes.
- Breach notification to HHS is required within 60 days for breaches affecting 500 or more; smaller breaches are logged
  and reported annually.
- De-identified data is no longer PHI and is not subject to HIPAA; this must be documented.

## Examples

```text
Safe Harbor field review (excerpt):
  Field "date_of_birth" → REMOVE (date more specific than year).
  Field "admission_year" → KEEP (year only).
  Field "ZIP" → 91711 → population 53,000 → KEEP first 3 digits (917).
  Field "ZIP" → 03600 → population <20,000 → CHANGE first 3 to 000.
  Field "age" → 92 → CHANGE to "90+".
```

```text
BAA sufficiency finding:
  Vendor: CloudAnalytics Inc.
  PHI access: yes (database hosting).
  BAA on file: yes, dated 2024-01-15.
  Missing clause: subcontractor flow-down (no explicit obligation).
  Finding: NON-CONFORMANCE, severity HIGH,
  remediation: amend BAA within 30 days.
```
