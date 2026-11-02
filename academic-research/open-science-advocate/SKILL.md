---
name: open-science-advocate
description: 'Apply open-science practices across the research lifecycle: open data (Zenodo, Figshare, Dryad), open code (GitHub with DOI via Zenodo), preprints (arXiv, bioRxiv, medRxiv), pre-registration (OSF, AsPredicted), and Registered Reports. Use when the user asks to make their workflow open, FAIR, or reproducible, or when a venue requires open-science compliance.'
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: academic-research
tags: [open-science, fair, preprints, osf, zenodo]
related: [academic-research/pre-registration-drafter, academic-research/reproducibility-checklist-author, academic-research/research-repo-builder]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 830
cost_warning: "Optional: Zenodo / Figshare / OSF API uploads may incur storage costs on paid tiers."
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: false
language: en
---

# Open Science Advocate

## When To Use
- The user asks "how do I make this open science", "where should I archive my data/code", or "should I preprint".
- The user wants to comply with an open-science mandate (e.g., NIH DMSP, Horizon Europe, Plan S).
- The user is choosing between OSF, AsPredicted, and Registered Reports.
- Trigger keywords: open science, FAIR, preprint, Zenodo, Figshare, Dryad, OSF, AsPredicted, Registered Report, Plan S.

## Workflow
1. Identify the artifact needing open-science treatment (data, code, paper, protocol).
2. Map each artifact to a repository: data → Zenodo/Figshare/Dryad; code → GitHub + Zenodo DOI; preprints → arXiv/bioRxiv/medRxiv.
3. Choose a license per artifact: code MIT/Apache-2.0, data CC-BY 4.0/CC0, content CC-BY 4.0.
4. Generate FAIR metadata: title, creators, ORCID, keywords, related identifiers, funding.
5. For empirical studies, draft a pre-registration: AsPredicted (7 questions) for low-risk, OSF registration for full protocols.
6. Where the venue supports Registered Reports, recommend Stage 1 submission before data collection.
7. For publications, choose a preprint server matching the field (arXiv for CS/physics, bioRxiv for biology, medRxiv for medicine).
8. Mint a DOI for code by linking the GitHub repo to Zenodo (archive on every release).
9. For Plan S compliance, confirm publication route (gold, green, hybrid) and CC-BY license.
10. Output an open-science plan with links, DOIs, and license statements.

## Inputs
- Artifact type (data, code, paper, protocol).
- Field and target venue.
- Funding agency open-science policy (e.g., NIH DMSP, Horizon Europe, Plan S).
- Existing repositories or preprints (if any).

## Outputs
- `open_science_plan.md` — per-artifact repository, DOI, license.
- `fair_metadata.json` — FAIR-aligned metadata block.
- `preregistration_choice.md` — AsPredicted vs. OSF vs. Registered Report.
- `preprint_recommendation.md` — server choice and licensing.
- `plan_s_compliance.md` — route and license check.

## Key Rules
- Every data artifact gets a DOI and a license (CC-BY 4.0 default; CC0 if mandate).
- Code is on GitHub with a Zenodo DOI archived at each release.
- Preprints are posted BEFORE or at submission, never after publication unless venue forbids.
- Pre-registration must occur BEFORE data collection; post-hoc registrations are flagged as such.
- Registered Reports are preferred where the venue supports them.
- FAIR metadata must include ORCID for every creator.

## Examples
```text
Open-science plan (excerpt):
  Artifact        | Repository     | License   | DOI
  Code            | GitHub + Zenodo| MIT       | 10.5281/zenodo.1234567
  Dataset (MRI)   | Zenodo         | CC-BY 4.0 | 10.5281/zenodo.7654321
  Preprint        | arXiv          | arXiv     | 2025.12345
  Protocol        | OSF            | CC-BY 4.0 | 10.17605/OSF.IO/xxxx
```
```text
Plan S compliance check:
  Venue: Nature Communications (Plan S compliant).
  Route: Gold OA.
  License: CC-BY 4.0 — required.
  Preprint: Allowed (green route also available).
  APC: covered by institutional transform agreement.
```

## References
- Zenodo: https://zenodo.org/
- Figshare: https://figshare.com/
- Dryad: https://datadryad.org/
- Open Science Framework (OSF): https://osf.io/
- AsPredicted: https://aspredicted.org/
- Center for Open Science Registered Reports: https://www.cos.io/initiatives/registered-reports
- arXiv / bioRxiv / medRxiv: https://arxiv.org/, https://www.biorxiv.org/, https://www.medrxiv.org/
- Plan S: https://www.coalition-s.org/
- NIH Data Management and Sharing Policy: https://grants.nih.gov/policy/data-sharing/

## Notes
- Persistent identifiers (DOI, ORCID, ROR) are required for FAIR compliance; do not substitute bare URLs.
- For sensitive data, prefer restricted-access archives with a data-access committee instead of public repositories.
- Confirm funder data-sharing timelines (e.g., NIH DMSP requires data at acceptance, not just at publication).
