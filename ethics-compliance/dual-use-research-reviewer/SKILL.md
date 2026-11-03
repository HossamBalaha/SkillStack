---
name: dual-use-research-reviewer
description: Review dual-use research of concern (DURC) for potential misuse in biological, chemical, nuclear, or cyber domains, identify risk mitigation strategies, and document institutional oversight requirements under NSPM-33 and the USG DURC policy. Use when life-sciences or emerging-technology research could plausibly be misused to cause harm.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [dual-use, durc, biosecurity, nspm-33, oversight]
related: [ethics-compliance/irb-protocol-drafter, ethics-compliance/ai-impact-assessment, ethics-compliance/research-ethics-checklist-author]
prerequisites: []
outputs: [markdown, yaml]
difficulty: advanced
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

# Dual-Use Research Reviewer

## When To Use

- The user says "is my research dual-use?", "review for biosecurity concerns", or "do we need DURC review?".
- A life-sciences project involves enhanced potential pandemic pathogens (ePPPs), gain-of-function studies, toxin
  production, or antimicrobial resistance work.
- A chemistry project produces, purifies, or stabilizes scheduled chemicals.
- A cyber or AI project could plausibly enable offensive operations, surveillance, or weaponisation.
- A funder or institution requests a DURC review before releasing funds or accepting a manuscript.
- Trigger keywords: dual-use, DURC, ePPP, gain-of-function, biosecurity, NSPM-33, institutional review entity (IRE).

## Workflow

1. Screen the research against the seven categories of USG DURC (avian influenza, SARS/MERS, foot-and-mouth, Rift Valley
   fever, Japanese encephalitis, botulinum neurotoxin, and any pathogen or toxin on the Select Agent list).
2. Extend the screen to broader dual-use domains: chemical (CWC scheduled chemicals), nuclear (uranium enrichment,
   weaponisation), cyber (offensive tools, surveillance), and emerging tech (AI, synthetic biology).
3. Apply the NSPM-33 criteria: research involving a listed pathogen or toxin, or research that is reasonably anticipated
   to produce one of the listed experimental outcomes (enhanced transmissibility, pathogenicity, or host range).
4. Identify the Institutional Review Entity (IRE) responsible for the institution; submit the research for review if any
   criterion is met.
5. For each identified risk, classify by likelihood (low/medium/high) and consequence (low/medium/high).
6. Draft mitigation options: redaction of methods, modification of experimental design, heightened biosafety (BSL-3 or
   BSL-4), pre-publication review, training requirements, and access controls.
7. Document the responsible conduct decisions: who can access materials, who is trained, and how chain of custody is
   maintained.
8. Specify communication plans: communication with funders, the IRE, the funding agency's program officer, and (where
   required) the USG funding agency review.
9. Address international considerations: export control, the Australia Group, and any dual-use export license
   requirements.
10. Set up ongoing monitoring: annual review, deviation reporting, and a re-review trigger if protocols or personnel
    change.
11. Append a clear statement of whether the research is DURC, DURC-exempt, or outside scope, with the reviewer's
    signature and date.
12. File the review with the IRE and link it to the protocol record for audit.

## Inputs

- Research protocol summary and aims.
- List of pathogens, toxins, or technologies involved.
- Experimental outcomes reasonably anticipated (transmissibility, host range, etc.).
- Institutional biosafety level and risk assessment.
- Personnel list with training status and access.
- Funder identity and any export-control determinations.

## Outputs

- `durc_screening.md` — categories checked, evidence, and outcome.
- `nspm33_criteria_check.md` — each NSPM-33 criterion with a yes/no and rationale.
- `risk_register.md` — risk × likelihood × consequence × mitigation.
- `mitigation_plan.md` — mitigation strategy, owner, deadline, and verification.
- `communication_plan.md` — internal and external communications and timelines.
- `export_control_review.md` — Australia Group, EAR, and license requirements.
- `monitoring_plan.md` — annual review, deviation reporting, re-review triggers.
- `durc_review_record.yaml` — machine-readable determination for the IRE.

## Key Rules

- A research project may fall outside the seven USG DURC categories but still be dual-use in another domain (chemical,
  nuclear, cyber, AI); a single-domain screen is insufficient.
- Enhanced potential pandemic pathogen (ePPP) research requires institutional review even when not on the Select Agent
  list.
- Mitigations must reduce risk to a level acceptable to the IRE; if residual risk remains high, the research should not
  proceed without an explicit approval.
- Communication of methods that enable misuse must be subject to pre-publication review, not just the data.
- Export-control screening is independent of biosafety review; both must be completed.
- The review must be revisited whenever the protocol, personnel, or materials change; stale reviews are
  non-conformances.
- Personnel training records must be current at the time of work commencement; expired training blocks access.
- DURC review records are auditable by funders and oversight bodies; they must be retained for the institutional
  retention period.

## Examples

```text
Screening sample (virology):
  Pathogen: H5N1 influenza (avian).
  USG category 1: yes — avian influenza with enhanced transmissibility.
  NSPM-33 trigger: research anticipated to enhance transmissibility in mammals.
  Risk: HIGH likelihood of misuse if methods published in full.
  Mitigation: redaction of detailed protocols; pre-publication review by IRE
  and USG funding agency; BSL-3 enhancements; restricted-access lab.
```

```text
Cyber dual-use finding:
  Outcome: proof-of-concept exploit for zero-day in widely deployed SCADA system.
  Domain: cyber.
  Risk: HIGH consequence (critical infrastructure), MEDIUM likelihood of misuse.
  Mitigation: coordinated disclosure with vendor; 90-day embargo;
  redaction of full exploit code; responsible-disclosure plan documented.
```
