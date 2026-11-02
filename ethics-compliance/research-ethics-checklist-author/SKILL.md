---
name: research-ethics-checklist-author
description: Author research ethics checklists covering conflicts of interest disclosure, funding sources, data sharing commitments, animal welfare compliance, and human subjects approval status, aligned with COPE guidelines and ICMJE recommendations. Use when finalising a manuscript submission package or an institutional ethics file.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [research-ethics, checklist, conflict-of-interest, cope, icmje]
related: [ethics-compliance/irb-protocol-drafter, ethics-compliance/informed-consent-writer, ethics-compliance/dual-use-research-reviewer]
prerequisites: []
outputs: [markdown, yaml]
difficulty: intermediate
estimated_tokens: 1200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Research Ethics Checklist Author

## When To Use

- The user says "prepare our ethics checklist", "what COPE items do we need?", or "ready our submission package".
- A manuscript is being finalised and the journal requires a research ethics disclosure section.
- A grant proposal needs an ethics annex covering human subjects, animals, conflicts, and data sharing.
- An institutional review is auditing past submissions for ethics compliance.
- Trigger keywords: research ethics, COPE, ICMJE, conflict of interest, funding, data sharing, animal welfare, IRB
  approval.

## Workflow

1. Identify the applicable guidelines: COPE core practices for journals and authors, ICMJE recommendations for medical
   journals, and any venue-specific ethics requirements.
2. Build the human-subjects section: IRB or ethics committee approval number, approval date, jurisdiction, and any
   amendments.
3. Confirm informed consent: written or verbal, language, reading level, and any waivers with justification.
4. Build the animal-welfare section (if applicable): IACUC approval number, species, numbers, 3Rs
   replacement/refinement/reduction statement, and any ARRIVE 2.0 reporting notes.
5. Compile conflicts of interest: financial (employment, consultancies, equity, patents), personal (relationships,
   competition), and intellectual (deeply held beliefs). State "none declared" only when truly none.
6. Compile funding sources: funder name, grant number, funder role (if any), and a statement if the funder had no role.
7. Compile data sharing commitments: what will be shared, where (repository with DOI), when (immediately or embargo),
   under what licence, and any access conditions.
8. Author contributions: CRediT taxonomy per author, with explicit statements on conceptualisation, methodology,
   software, validation, analysis, writing, visualisation, supervision, and administration.
9. Address authorship criteria: ICMJE four criteria (substantial contribution, drafting or revising, final approval,
   accountability) — flag any author failing any criterion.
10. Address registration: clinical trial registration number (if applicable) per ICMJE requirement and pre-registration
    of analyses.
11. Address dual-use and biosafety (if applicable): refer to the dual-use-research-reviewer skill outputs.
12. Produce the checklist as a Markdown table and as a YAML file for downstream tooling, with each item assigned an
    owner and a status.

## Inputs

- Manuscript metadata (title, authors, venue, version).
- IRB/IACUC approval documents.
- Funding and conflict-of-interest declarations per author.
- Data sharing plan and repository DOI.
- CRediT contribution matrix.

## Outputs

- `ethics_checklist.md` — table with item, status, evidence, and owner.
- `human_subjects_section.md` — IRB approval, consent, amendments.
- `animal_welfare_section.md` — IACUC approval, 3Rs, ARRIVE 2.0.
- `conflict_of_interest.md` — COI declarations per author.
- `funding_statement.md` — funders, grant numbers, funder role.
- `data_sharing_statement.md` — what, where, when, licence, access.
- `credit_contributions.md` — CRediT taxonomy per author.
- `ethics_checklist.yaml` — machine-readable items with status and owner.

## Key Rules

- "No conflict of interest" is only valid when the author has reviewed the full COI definition; default to disclosure.
- ICMJE requires all four authorship criteria to be met; honorary and ghost authorship are non-compliant.
- IRB approval numbers must be verifiable; placeholder values are non-conformances.
- Data sharing statements must specify the repository, DOI, licence, and access conditions; "available upon request" is
  non-compliant under most modern policies.
- Animal research must report on the 3Rs and follow ARRIVE 2.0; absence of reporting is a non-conformance.
- Funding sources must include the funder's role; "no role" must be stated explicitly, not implied.
- The checklist must be signed off by the corresponding author before submission; an unsigned checklist is incomplete.
- Changes after submission require versioned amendments with dates and reasons.

## Examples

```text
Checklist excerpt:
  Item: IRB approval number.
  Status: COMPLETE.
  Evidence: Protocol 2024-038, approved 2024-02-15 by University X IRB.
  Owner: Corresponding author.
  Notes: Amendment 1 (recruitment) approved 2024-04-10.
```

```text
CRediT matrix excerpt:
  A. Researcher: Conceptualization, Methodology, Writing - original draft.
  B. Researcher: Software, Validation, Visualization.
  C. Researcher: Investigation, Data curation.
  D. Researcher: Supervision, Writing - review & editing, Funding acquisition.
  All authors meet ICMJE four criteria: yes.
```

## References

- COPE core practices: https://publicationethics.org/core-practices
- ICMJE recommendations: https://www.icmje.org/recommendations/
- ICMJE conflict of interest form: https://www.icmje.org/disclosure-of-conflicts-of-interest/
- CRediT taxonomy: https://credit.niso.org/
- ARRIVE 2.0 guidelines: https://arriveguidelines.org/
- ICMJE clinical trial
  registration: https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/clinical-trial-registration.html
