---
name: irb-protocol-drafter
description: Draft Institutional Review Board (IRB) protocols covering background, research design, participant recruitment, informed consent procedures, risk/benefit analysis, and a data management plan aligned with 45 CFR 46. Use when preparing a human-subjects submission for an IRB, ethics committee, or institutional review.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [irb, human-subjects, common-rule, protocol, ethics-review]
related: [ethics-compliance/informed-consent-writer, ethics-compliance/research-ethics-checklist-author, ethics-compliance/data-minimization-designer]
prerequisites: []
outputs: [markdown, yaml]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# IRB Protocol Drafter

## When To Use

- The user says "draft an IRB protocol", "prepare an ethics submission", or "write a human-subjects application".
- A study involving identifiable human participants is being prepared for institutional review.
- A protocol amendment is needed because recruitment, procedures, or data handling have changed.
- A multi-site study needs a master protocol plus site-specific addenda.
- Trigger keywords: IRB, ethics committee, human subjects, Common Rule, 45 CFR 46, exempt, expedited, full board.

## Workflow

1. Classify the review level: exempt (45 CFR 46.104), expedited (46.110), or full board (46.109). If unsure, default to
   full board.
2. Draft the Background section: gap, prior evidence, and why human participants are necessary.
3. State the Research Design: study type (observational, interventional, qualitative, or mixed), setting, and duration.
4. Define the Population: inclusion criteria, exclusion criteria, target sample size with justification, and
   vulnerable-population flags (pregnant, prisoners, children, cognitively impaired).
5. Detail Recruitment: channels, scripts, compensation, and any coercion or undue influence safeguards.
6. Specify Informed Consent procedures: written/verbal waiver rationale, language, timing, and re-consent triggers.
7. Enumerate Procedures step by step, including visit schedule, instruments, and any deception or debriefing.
8. Conduct Risk/Benefit analysis: physical, psychological, social, legal, and economic risks; probability and magnitude;
   mitigation plan.
9. Build the Data Management Plan: identifiers collected, de-identification method, storage, access controls, retention
   period, and destruction timeline.
10. Address Privacy and Confidentiality: data flow diagram, encryption, role-based access, and any certificate of
    confidentiality.
11. List Provisions for adverse events, unanticipated problems, and protocol deviations with reporting timelines.
12. Append the regulatory citations (45 CFR 46 subparts A-D) and any institutional addenda.

## Inputs

- Study title, principal investigator, and institutional affiliation.
- Research question and hypothesis table (from a prior planning skill).
- Participant-facing materials (recruitment script, consent draft).
- Data collection instruments and their storage format.
- Funding source and any conflicts of interest.

## Outputs

- `irb_protocol.md` — main protocol narrative with all sections above.
- `risk_benefit_table.md` — risks tabulated with probability, magnitude, and mitigation.
- `data_management_plan.md` — identifiers, retention, and destruction.
- `review_classification.md` — exempt/expedited/full-board rationale.
- `adverse_event_plan.md` — reporting workflow and timelines.
- `protocol_summary.yaml` — machine-readable metadata for the institutional system.

## Key Rules

- The review level must be justified against the regulatory category; "expedited because it is low risk" is not
  acceptable.
- Vulnerable populations require additional safeguards under subparts B-D; never omit this check.
- Risk magnitude must be rated as minimal, minor increase over minimal, or more than minimal.
- Identifiers must be enumerated field by field; "we will collect some demographics" is not acceptable.
- Retention periods must be specific (e.g., 7 years post-publication, then destroyed).
- Any waiver of consent must cite 46.116(f) criteria point by point.
- Compensation that could coerce withdrawal must be pro-rated in the protocol.

## Examples

```text
Review classification sample:
  Exempt category 2: anonymous educational surveys. No identifiers collected.
  Justification: data cannot be linked to participants; no sensitive topics.
  Reporting: only aggregate results published; raw data destroyed after 5 years.
```

```text
Risk/benefit excerpt:
  Risk: disclosure of mental-health diagnosis to employer (social, low probability, high magnitude).
  Mitigation: coded data only, separate linking file in PI's encrypted drive,
  certificate of confidentiality from NIH.
  Benefit: validated screening tool provided to participant at no cost.
```
