---
name: ccpa-compliance-auditor
description: Audit compliance with the California Consumer Privacy Act (CCPA) as amended by the CPRA, covering consumer rights (know, delete, correct, opt-out of sale/share), privacy policy requirements, the "Do Not Sell or Share My Personal Information" link, service provider and contractor contracts, and sensitive-data limitations. Use when a business processes personal information of California residents.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [ccpa, cpra, california-privacy, consumer-rights, privacy-policy]
related: [ethics-compliance/gdpr-data-protection-assessor, ethics-compliance/data-minimization-designer, ethics-compliance/hipaa-compliance-checker]
prerequisites: []
outputs: [markdown, yaml]
difficulty: advanced
estimated_tokens: 1600
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# CCPA Compliance Auditor

## When To Use

- The user says "are we CCPA compliant?", "audit our California privacy obligations", or "update our privacy policy for
  CPRA".
- A business meets any CCPA threshold: annual revenue over USD 25 million, personal information of 100,000+ consumers,
  or 50% of revenue from selling or sharing personal information.
- A consumer has submitted a request to know, delete, correct, or opt-out and the response workflow needs to be defined.
- A service provider, contractor, or third party is processing personal information and contracts must include
  CPRA-required clauses.
- Trigger keywords: CCPA, CPRA, California privacy, do not sell, opt-out, sensitive personal information, service
  provider.

## Workflow

1. Confirm the organisation is a "business" under CCPA/CPRA thresholds (revenue, volume, or sale/share of data).
2. Inventory personal information collected in the last 12 months by category: identifiers, commercial information,
   internet activity, geolocation, sensory, professional/employment, education, inferences, and sensitive personal
   information.
3. Map each category to a business purpose and a source; flag any collection not tied to a disclosed purpose.
4. Audit consumer rights coverage: know (1798.100, 1798.110, 1798.115), delete (1798.105), correct (1798.106), opt-out
   of sale/share (1798.120), limit use of sensitive personal information (1798.121), and non-discrimination (1798.125).
5. Verify the privacy policy includes all CPRA-required sections at 1798.135: categories collected, purposes,
   third-party recipients, consumer rights, opt-out mechanisms, financial-incentive notices, and the 12-month look-back
   disclosure.
6. Confirm the homepage displays a "Do Not Sell or Share My Personal Information" link if the business sells or shares;
   add "Limit the Use of My Sensitive Personal Information" link when applicable.
7. Validate the request-handling workflow: identity verification, 45-day response window (extendable by 45 days), and
   the methods to submit (toll-free number and at least one other designated method).
8. Review service provider and contractor agreements for required CPRA clauses: purpose limitation, confidentiality,
   deletion on termination, certification of compliance, and audit rights.
9. Check for "contractors" vs "third parties" classification: contractors may use data for business purposes on behalf
   of the business; third parties receive data for their own purposes and trigger sale/share analysis.
10. Verify training program for personnel handling consumer requests and document the audit trail for each request.
11. Conduct the annual cybersecurity audit required by CPRA regulations and verify risk assessment documentation.
12. Produce an audit report with findings, severity, owner, and remediation deadline; flag any unaddressed consumer
    requests.

## Inputs

- Data inventory and map of personal information flows.
- Existing privacy policy and any "just-in-time" notices.
- Vendor list with their classification (service provider, contractor, third party).
- Records of consumer requests received in the last 12 months.
- Cybersecurity policies and most recent risk assessment.

## Outputs

- `ccpa_applicability.md` — threshold analysis confirming business status.
- `data_inventory_by_category.md` — categories × purposes × sources × recipients.
- `consumer_rights_workflow.md` — request type × verification × response timeline.
- `privacy_policy_gap_report.md` — sections missing or non-compliant.
- `opt_out_link_audit.md` — homepage links and configuration check.
- `service_provider_contracts.md` — per-vendor classification and missing clauses.
- `cybersecurity_audit.md` — annual audit findings and risk assessment status.
- `compliance_report.yaml` — findings with severity, owner, and remediation.

## Key Rules

- "Sale" under CCPA includes any exchange of personal information for monetary or other valuable consideration; "share"
  includes cross-context behavioural advertising even without payment.
- Sensitive personal information includes precise geolocation, racial/ethnic origin, religious beliefs, biometric data
  for identification, health data, financial account credentials, and contents of mail/email/text unless for business
  purposes.
- The privacy policy must be updated at least every 12 months; changes must be summarised for consumers.
- A consumer's right to know covers the 12 months preceding the request; longer look-backs are optional but must be
  offered if technically feasible.
- The opt-out preference signals (Global Privacy Control) must be honoured as a valid opt-out request.
- Service provider contracts must explicitly prohibit using personal information for any purpose other than the business
  purposes specified.
- The 45-day response window may be extended once by 45 days with notice to the consumer.
- Children's data (under 13) requires opt-in consent; consumers aged 13-16 may consent themselves.

## Examples

```text
Consumer request workflow (delete):
  Day 0:   request received via web form.
  Day 1:   identity verification (email + ID match).
  Day 3:   confirmed; deletion cascaded to 4 service providers.
  Day 20:  deletion completed; confirmation sent.
  Day 21:  request closed in audit log with timestamps.
```

```text
Privacy policy gap finding:
  Missing: categories of third-party recipients in last 12 months.
  Missing: description of sensitive personal information collected.
  Missing: notice that GPC signals are honoured.
  Severity: HIGH. Remediation deadline: 30 days.
```

## References

- California Civil Code 1798.100-1798.199
  (CCPA/CPRA): https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5
- California Privacy Protection Agency regulations: https://cppa.ca.gov/regulations/
- CCPA FAQ (California AG): https://oag.ca.gov/privacy/ccpa
- CPPA enforcement actions: https://cppa.ca.gov/enforcement/
- "Do Not Sell My Personal Information" guidance: https://oag.ca.gov/privacy/ccpa#section6
