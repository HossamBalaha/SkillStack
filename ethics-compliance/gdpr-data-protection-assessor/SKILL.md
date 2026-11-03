---
name: gdpr-data-protection-assessor
description: Assess GDPR compliance by identifying a lawful basis under Article 6, mapping data subject rights, performing a Data Protection Impact Assessment (DPIA) under Article 35, and drafting Records of Processing Activities (ROPA) under Article 30. Use when processing personal data of EU residents or preparing for a supervisory authority review.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [gdpr, dpia, ropa, lawful-basis, data-protection]
related: [ethics-compliance/data-minimization-designer, ethics-compliance/hipaa-compliance-checker, ethics-compliance/ccpa-compliance-auditor]
prerequisites: []
outputs: [markdown, yaml]
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

# GDPR Data Protection Assessor

## When To Use

- The user says "we need a DPIA", "check our GDPR compliance", or "draft our ROPA".
- A new processing activity begins that involves systematic monitoring, large-scale special-category data, or new
  technologies.
- A data subject has exercised rights (access, erasure, portability) and the response workflow is unclear.
- A vendor outside the EU will process personal data and Article 28 data processor terms are needed.
- Trigger keywords: GDPR, DPIA, ROPA, lawful basis, data subject rights, supervisory authority.

## Workflow

1. Inventory processing activities: for each, record purpose, categories of data subjects and personal data, recipients,
   third-country transfers, and retention.
2. Identify the lawful basis under Article 6 (consent, contract, legal obligation, vital interests, public task,
   legitimate interests). For special-category data add an Article 9 condition.
3. Document data subject rights mapping: access (15), rectification (16), erasure (17), restriction (18), portability
   (20), objection (21), and automated decision-making (22). For each right, specify the response workflow and the
   one-month deadline.
4. Screen for DPIA triggers under Article 35(3) and the WP29 criteria: systematic monitoring, large scale, special
   category data, vulnerable subjects, or innovative technology.
5. If DPIA is triggered, perform the assessment: describe processing, assess necessity and proportionality, identify
   risks to rights and freedoms, and define mitigation measures with a residual-risk rating.
6. Consult the supervisory authority under Article 36 if residual high risk remains after mitigation.
7. Draft the Records of Processing Activities under Article 30: controller identity, DPO contact, purposes, categories,
   recipients, transfers, retention, and security measures.
8. Specify technical and organisational measures (Article 32): encryption, pseudonymisation, access control, backups,
   incident response, and staff training.
9. Define data breach response under Articles 33-34: 72-hour notification to the supervisory authority and communication
   to data subjects when high risk.
10. Map cross-border transfers and select a mechanism: adequacy decision, Standard Contractual Clauses, or derogations
    under Article 49.
11. Identify whether a Data Protection Officer is mandatory under Article 37, and whether legitimate-interest balancing
    is required.
12. Produce a gap report with severity, owner, and remediation deadline for every non-conformance.

## Inputs

- Inventory of processing activities (purposes, data fields, systems, vendors).
- Data flow diagrams including any cross-border transfers.
- Existing privacy notices and consent mechanisms.
- Vendor list with their role (controller, processor, sub-processor).
- Risk appetite statement from the controller.

## Outputs

- `lawful_basis_register.md` — basis per processing activity with justification.
- `data_subject_rights_matrix.md` — rights × workflow × deadline.
- `dpia_report.md` — Article 35 assessment with residual risk.
- `ropa.yaml` — Article 30 records in structured form.
- `tom_list.md` — technical and organisational measures under Article 32.
- `breach_response_plan.md` — Articles 33-34 workflow.
- `transfer_mechanism_map.md` — per-transfer adequacy/SCC/derogation.
- `gap_report.md` — non-conformances with severity and remediation.

## Key Rules

- A processing activity cannot run without a documented lawful basis; "we will figure it out later" is a
  non-conformance.
- Special-category data (health, biometric, genetic, etc.) requires both an Article 6 basis and an Article 9 condition.
- Consent under Article 7 must be freely given, specific, informed, unambiguous, and as easy to withdraw as to give.
- DPIA is mandatory for large-scale systematic monitoring, regardless of risk level after mitigation.
- Legitimate interests require a documented balancing test against data subject interests, rights, and freedoms.
- The 72-hour breach notification clock starts when the controller becomes aware, not when investigation completes.
- Records of Processing Activities must be available to the supervisory authority on request; they are not optional.
- Cross-border transfers without a valid mechanism are a non-conformance regardless of encryption.

## Examples

```text
Lawful basis decision (e-commerce analytics):
  Basis: Article 6(1)(f) legitimate interests.
  Balancing test: analytics necessary to improve service; data minimised; opt-out available.
  Special category: none.
  Retention: 13 months then aggregated.
  Documented in LIA dated 2024-03-12.
```

```text
DPIA residual risk (hospital ML triage):
  Initial risk: HIGH (large-scale health data, automated decision-making).
  Mitigations: pseudonymisation, human-in-the-loop, bias audit, opt-out.
  Residual risk: MEDIUM — proceed without Article 36 consultation,
  but review every 12 months.
```
