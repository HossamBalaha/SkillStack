# ⚖️ Ethics & Compliance — IRB, Privacy, AI Accountability

> Draft IRB protocols, write informed consent, assess GDPR/HIPAA/CCPA compliance, review dual-use research, conduct AI
> impact assessments, select fairness metrics, audit algorithms, and author research ethics checklists. This theme
> covers
> every ethics and compliance artifact a research or product team produces — from human-subjects protocols through
> privacy-by-design pipelines and algorithmic audit reports. Use this theme whenever the deliverable is an ethics,
> privacy, or accountability document rather than raw code.

## Theme Overview

This folder contains **12 skills** in the `ethics-compliance/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                           | Description                                                                                                                                                                                                                                                                                                                        | Difficulty   | Tags                                                                                               | Related                                                                                                                                           |
|----|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`ai-impact-assessment`](ai-impact-assessment/SKILL.md)                         | Conduct an AI impact assessment identifying stakeholders, benefits and harms, fairness concerns, transparency measures, human oversight requirements, and a mitigation plan, aligned with the EU AI Act, NIST AI RMF, and Canada's AIA.                                                                                            | advanced     | `ai-impact`, `ai-act`, `nist-airmf`, `fairness`, `oversight`                                       | `ethics-compliance/fairness-metric-selector`, `ethics-compliance/algorithmic-audit-reporter`, `ethics-compliance/dual-use-research-reviewer`      |
| 2  | [`algorithmic-audit-reporter`](algorithmic-audit-reporter/SKILL.md)             | Produce algorithmic audit reports containing a model card summary, a dataset card, performance by subgroup, fairness metrics, robustness tests, and prioritized recommendations.                                                                                                                                                   | advanced     | `algorithmic-audit`, `model-card`, `dataset-card`, `robustness`, `accountability`                  | `ethics-compliance/fairness-metric-selector`, `ethics-compliance/ai-impact-assessment`, `ethics-compliance/data-minimization-designer`            |
| 3  | [`ccpa-compliance-auditor`](ccpa-compliance-auditor/SKILL.md)                   | Audit compliance with the California Consumer Privacy Act (CCPA) as amended by the CPRA, covering consumer rights (know, delete, correct, opt-out of sale/share), privacy policy requirements, the "Do Not Sell or Share My Personal Information" link, service provider and contractor contracts, and sensitive-data limitations. | advanced     | `ccpa`, `cpra`, `california-privacy`, `consumer-rights`, `privacy-policy`                          | `ethics-compliance/gdpr-data-protection-assessor`, `ethics-compliance/data-minimization-designer`, `ethics-compliance/hipaa-compliance-checker`   |
| 4  | [`consent-form-translator`](consent-form-translator/SKILL.md)                   | Translate informed consent forms across reading levels, targeting Flesch-Kincaid grade 6-8 for general adults and grade 4-6 for assent, with plain-language rewrites, multilingual considerations, and low-literacy adaptations aligned with NIH Plain Language guidelines.                                                        | intermediate | `consent-translation`, `plain-language`, `flesch-kincaid`, `readability`, `low-literacy`           | `ethics-compliance/informed-consent-writer`, `ethics-compliance/irb-protocol-drafter`, `ethics-compliance/research-ethics-checklist-author`       |
| 5  | [`data-minimization-designer`](data-minimization-designer/SKILL.md)             | Design data-minimized pipelines that collect only necessary fields, enforce purpose limitation, set storage limits, and apply privacy-by-design principles from the earliest stage.                                                                                                                                                | intermediate | `data-minimization`, `privacy-by-design`, `purpose-limitation`, `storage-limitation`, `gdpr-art-5` | `ethics-compliance/gdpr-data-protection-assessor`, `ethics-compliance/hipaa-compliance-checker`, `ethics-compliance/data-minimization-designer`   |
| 6  | [`dual-use-research-reviewer`](dual-use-research-reviewer/SKILL.md)             | Review dual-use research of concern (DURC) for potential misuse in biological, chemical, nuclear, or cyber domains, identify risk mitigation strategies, and document institutional oversight requirements under NSPM-33 and the USG DURC policy.                                                                                  | advanced     | `dual-use`, `durc`, `biosecurity`, `nspm-33`, `oversight`                                          | `ethics-compliance/irb-protocol-drafter`, `ethics-compliance/ai-impact-assessment`, `ethics-compliance/research-ethics-checklist-author`          |
| 7  | [`fairness-metric-selector`](fairness-metric-selector/SKILL.md)                 | Select fairness metrics appropriate to the task (demographic parity, equalized odds, predictive parity, calibration within groups) and conduct trade-off analysis so that the chosen metric aligns with the application context.                                                                                                   | advanced     | `fairness-metrics`, `demographic-parity`, `equalized-odds`, `calibration`, `trade-off`             | `ethics-compliance/algorithmic-audit-reporter`, `ethics-compliance/ai-impact-assessment`, `ethics-compliance/data-minimization-designer`          |
| 8  | [`gdpr-data-protection-assessor`](gdpr-data-protection-assessor/SKILL.md)       | Assess GDPR compliance by identifying a lawful basis under Article 6, mapping data subject rights, performing a Data Protection Impact Assessment (DPIA) under Article 35, and drafting Records of Processing Activities (ROPA) under Article 30.                                                                                  | advanced     | `gdpr`, `dpia`, `ropa`, `lawful-basis`, `data-protection`                                          | `ethics-compliance/data-minimization-designer`, `ethics-compliance/hipaa-compliance-checker`, `ethics-compliance/ccpa-compliance-auditor`         |
| 9  | [`hipaa-compliance-checker`](hipaa-compliance-checker/SKILL.md)                 | Check HIPAA compliance for health data by identifying Protected Health Information (PHI), validating Safe Harbor de-identification against the 18 identifiers, documenting Expert Determination, reviewing Business Associate Agreements, and verifying the minimum necessary standard.                                            | advanced     | `hipaa`, `phi`, `safe-harbor`, `baa`, `minimum-necessary`                                          | `ethics-compliance/irb-protocol-drafter`, `ethics-compliance/data-minimization-designer`, `ethics-compliance/gdpr-data-protection-assessor`       |
| 10 | [`informed-consent-writer`](informed-consent-writer/SKILL.md)                   | Write informed consent forms covering plain-language summary, study procedures, risks, benefits, confidentiality protections, voluntary participation, withdrawal rights, and contacts.                                                                                                                                            | beginner     | `informed-consent`, `belmont-report`, `plain-language`, `human-subjects`, `21-cfr-50`              | `ethics-compliance/irb-protocol-drafter`, `ethics-compliance/consent-form-translator`, `ethics-compliance/research-ethics-checklist-author`       |
| 11 | [`irb-protocol-drafter`](irb-protocol-drafter/SKILL.md)                         | Draft Institutional Review Board (IRB) protocols covering background, research design, participant recruitment, informed consent procedures, risk/benefit analysis, and a data management plan aligned with 45 CFR 46.                                                                                                             | intermediate | `irb`, `human-subjects`, `common-rule`, `protocol`, `ethics-review`                                | `ethics-compliance/informed-consent-writer`, `ethics-compliance/research-ethics-checklist-author`, `ethics-compliance/data-minimization-designer` |
| 12 | [`research-ethics-checklist-author`](research-ethics-checklist-author/SKILL.md) | Author research ethics checklists covering conflicts of interest disclosure, funding sources, data sharing commitments, animal welfare compliance, and human subjects approval status, aligned with COPE guidelines and ICMJE recommendations.                                                                                     | intermediate | `research-ethics`, `checklist`, `conflict-of-interest`, `cope`, `icmje`                            | `ethics-compliance/irb-protocol-drafter`, `ethics-compliance/informed-consent-writer`, `ethics-compliance/dual-use-research-reviewer`             |

## Difficulty Breakdown

Across **12** skills in this theme, the difficulty distribution is:

- **Beginner** — 1 skill(s)
- **Intermediate** — 4 skill(s)
- **Advanced** — 7 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`human-subjects` (2), `oversight` (2), `plain-language` (2), `21-cfr-50` (1), `accountability` (1), `ai-act` (1),
`ai-impact` (1), `algorithmic-audit` (1), `baa` (1), `belmont-report` (1), `biosecurity` (1), `california-privacy`
(1), `calibration` (1), `ccpa` (1), `checklist` (1), `common-rule` (1), `conflict-of-interest` (1),
`consent-translation`
(1), `consumer-rights` (1), `cope` (1), `cpra` (1), `data-minimization` (1), `data-protection` (1), `dataset-card`
(1), `demographic-parity` (1), `dpia` (1), `dual-use` (1), `durc` (1), `equalized-odds` (1), `ethics-review` (1),
`fairness` (1), `fairness-metrics` (1), `flesch-kincaid` (1), `gdpr` (1), `gdpr-art-5` (1), `hipaa` (1), `icmje` (1),
`informed-consent` (1), `irb` (1), `lawful-basis` (1), `low-literacy` (1), `minimum-necessary` (1), `model-card`
(1), `nist-airmf` (1), `nspm-33` (1), `phi` (1), `privacy-by-design` (1), `privacy-policy` (1), `protocol` (1),
`purpose-limitation` (1), `readability` (1), `research-ethics` (1), `robustness` (1), `ropa` (1), `safe-harbor` (1),
`storage-limitation` (1), `trade-off` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`irb-protocol-drafter` → `informed-consent-writer` → `consent-form-translator` →
  `research-ethics-checklist-author`**
  — Human-subjects chain: protocol → consent → readability → submission package.
- **`gdpr-data-protection-assessor` → `data-minimization-designer` → `hipaa-compliance-checker` →
  `ccpa-compliance-auditor`** — Multi-jurisdiction privacy chain: GDPR → minimisation → HIPAA → CCPA.
- **`ai-impact-assessment` → `fairness-metric-selector` → `algorithmic-audit-reporter` →
  `research-ethics-checklist-author`** — AI accountability chain: AIA → metrics → audit report → ethics annex.
- **`dual-use-research-reviewer` → `irb-protocol-drafter` → `research-ethics-checklist-author`** — Biosecurity chain:
  DURC review → IRB protocol → ethics annex.

## Cross-Theme Connections

Skills in `ethics-compliance/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../academic-research/` — IRB protocols and ethics annexes attach to manuscripts and grant proposals.
- `../data-engineering/` — `data-minimization-designer` pairs with the data-anonymizer and dataset-card-generator.
- `../ml-engineering/` — algorithmic audits consume model artefacts from reproducible experiment runners.
- `../ai-output-judgement/` — `bias-auditor` and `safety-classifier` feed into `algorithmic-audit-reporter`.

Themes that commonly chain with this one:

- [`../academic-research/README.md`](../academic-research/README.md) — IRB protocols and ethics checklists accompany
  manuscripts, theses, and grant proposals.
- [`../data-engineering/README.md`](../data-engineering/README.md) — de-identification and dataset cards feed into
  HIPAA,
  GDPR, and minimisation reviews.
- [`../ml-engineering/README.md`](../ml-engineering/README.md) — model artefacts from reproducible experiment runners
  feed
  into algorithmic audits.
- [`../ai-output-judgement/README.md`](../ai-output-judgement/README.md) — bias and safety classifiers complement the
  fairness and audit skills here.

## Back to Master

← [Back to SkillStack README](../README.md)
