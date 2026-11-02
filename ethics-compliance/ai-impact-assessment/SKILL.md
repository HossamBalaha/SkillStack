---
name: ai-impact-assessment
description: Conduct an AI impact assessment identifying stakeholders, benefits and harms, fairness concerns, transparency measures, human oversight requirements, and a mitigation plan, aligned with the EU AI Act, NIST AI RMF, and Canada's AIA. Use when deploying a new AI system or re-evaluating an existing one that affects people.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [ai-impact, ai-act, nist-airmf, fairness, oversight]
related: [ethics-compliance/fairness-metric-selector, ethics-compliance/algorithmic-audit-reporter, ethics-compliance/dual-use-research-reviewer]
prerequisites: []
outputs: [markdown, yaml]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# AI Impact Assessment

## When To Use

- The user says "do we need an AI impact assessment?", "evaluate our AI for EU AI Act risk", or "what are the harms of
  this model?".
- A new AI system is being deployed that affects individuals in employment, education, credit, healthcare, justice, or
  essential services.
- An existing system is being substantially modified, retrained, or extended to a new population.
- A regulator or procurement office has requested a risk classification and mitigation plan.
- Trigger keywords: AI impact assessment, AIA, EU AI Act, NIST AI RMF, high-risk AI, fundamental rights, human
  oversight.

## Workflow

1. Describe the system: intended purpose, provider, deployer, model type, training data summary, and intended users.
2. Classify the risk level under the EU AI Act: prohibited, high-risk, limited-risk (transparency), or minimal-risk.
3. Identify stakeholders: directly affected individuals, indirectly affected groups, deployers, regulators, and society
   at large.
4. Conduct a benefit/harm analysis: enumerate potential benefits, then potential harms (physical, psychological,
   financial, reputational, autonomy, dignity, and discrimination).
5. Assess fairness by mapping protected or sensitive attributes in scope; flag any disparate impact pathway.
6. Apply the NIST AI RMF functions: Govern, Map, Measure, Manage — and document evidence under each.
7. Define transparency measures: information to deployers and end users, model card availability, decision explanation,
   and right to human review.
8. Specify human oversight requirements: who can override, how override is logged, what training is required, and the
   conditions for suspension.
9. Address data governance: training data provenance, lawful basis, representativeness, bias mitigation, and data
   minimisation.
10. Set accuracy, robustness, and cybersecurity targets with validation methods; document acceptable failure modes.
11. Document the mitigation plan: for each harm, list mitigation, owner, deadline, and verification method; rate
    residual risk.
12. Define monitoring and post-market surveillance: drift detection, incident reporting, periodic review cadence, and
    trigger for re-assessment.
13. Append the regulatory crosswalk: EU AI Act articles, NIST AI RMF functions, and (where applicable) Canada AIA
    elements.

## Inputs

- System description and intended use.
- Model documentation (model card, dataset card, evaluation report).
- Stakeholder list and deployment context.
- Existing risk assessments, privacy notices, and consent mechanisms.
- Risk appetite statement from the deploying organisation.

## Outputs

- `system_description.md` — purpose, scope, and deployment context.
- `risk_classification.md` — EU AI Act level with article citations.
- `stakeholder_map.md` — stakeholders × affected interests × power.
- `benefit_harm_analysis.md` — benefits and harms with magnitude and likelihood.
- `fairness_assessment.md` — sensitive attributes × impact pathway × metric target.
- `transparency_plan.md` — information to users and deployers.
- `human_oversight_plan.md` — override, logging, training, suspension.
- `mitigation_plan.md` — harm × mitigation × owner × deadline × residual risk.
- `monitoring_plan.md` — drift, incidents, periodic review, re-assessment triggers.
- `regulatory_crosswalk.yaml` — EU AI Act × NIST AI RMF × Canada AIA.

## Key Rules

- The risk classification must cite the specific EU AI Act article; "high risk" without an article citation is
  non-conforming.
- Stakeholder mapping must include indirectly affected groups (e.g., family members of healthcare patients), not only
  direct users.
- Every identified harm must have at least one mitigation; harms without mitigations are unacceptable.
- Human oversight must be effective: the human must have authority, competence, and time to override;
  "human-in-the-loop" without override authority is theatre.
- Transparency measures must include information for deployers (Article 4) and information for affected individuals
  (Article 86, where high-risk).
- Data governance must address representativeness and bias, not only lawful basis.
- Mitigation plans must specify residual risk after mitigation; a plan that does not change the risk rating has failed.
- Monitoring must include incident reporting and post-market surveillance; deployment without monitoring is
  non-conforming.

## Examples

```text
EU AI Act classification (recruitment screening):
  System: AI shortlisting CVs for technical roles.
  Classification: HIGH-RISK — Annex III, point 4 (employment).
  Articles applicable: 8-17 (high-risk requirements).
  Transparency: candidates informed of AI use; right to human review.
  Oversight: recruiter may override; override logged with reason.
```

```text
Benefit/harm analysis excerpt:
  Benefit: faster screening; wider applicant pool reach.
  Harm: disparate rejection of older candidates (psychological + financial).
  Likelihood: MEDIUM. Magnitude: HIGH.
  Mitigation: age-band fairness constraint in top-k; manual review
  for applicants over 50 flagged low-confidence.
  Residual: LOW after second-review safeguard.
```

## References

- EU Artificial Intelligence Act (Regulation 2024/1689): https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- NIST AI Risk Management Framework (AI RMF 1.0): https://www.nist.gov/itl/ai-risk-management-framework
- Treasury Board of Canada Directive on Automated
  Decision-Making: https://www.canada.ca/en/treasury-board-secretariat/services/innovation/directive-automated-decision-making.html
- OECD AI Principles: https://oecd.ai/en/ai-principles
- AlgorithmWatch AI ethics guidelines global inventory: https://algorithmwatch.org/en/ai-ethics-guidelines-inventory/
- Assessment List for Trustworthy AI
  (ALTAI): https://digital-strategy.ec.europa.eu/en/library/assessment-list-trustworthy-artificial-intelligence-altai-self-assessment
