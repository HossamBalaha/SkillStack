---
name: algorithmic-audit-reporter
description: Produce algorithmic audit reports containing a model card summary, a dataset card, performance by subgroup, fairness metrics, robustness tests, and prioritized recommendations. Use when an internal or external auditor needs a structured accountability document for an AI system.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [algorithmic-audit, model-card, dataset-card, robustness, accountability]
related: [ethics-compliance/fairness-metric-selector, ethics-compliance/ai-impact-assessment, ethics-compliance/data-minimization-designer]
prerequisites: []
outputs: [markdown, yaml, svg]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Algorithmic Audit Reporter

## When To Use

- The user says "audit our algorithm", "produce a model card", or "write an algorithmic audit report".
- A regulator, procurement office, or civil-society group has requested an accountability document.
- A model is being released externally and the team needs to disclose its capabilities and limitations.
- A prior fairness audit flagged gaps and a structured follow-up is required.
- Trigger keywords: algorithmic audit, model card, dataset card, subgroup analysis, robustness test, accountability gap,
  Raji.

## Workflow

1. Scope the audit: model under test, version, intended use, deployer, scope of evaluation, and out-of-scope items.
2. Produce the model card summary: model details, intended use and users, out-of-scope uses, ethical considerations, and
   caveats.
3. Produce the dataset card: motivation, composition, collection process, preprocessing, intended use, distribution, and
   maintenance plan.
4. Document the evaluation setup: dataset, splits, subgroups, protected attributes, sample sizes per subgroup, and
   metric definitions.
5. Compute performance by subgroup: accuracy, precision, recall, F1, calibration error, and confidence intervals.
6. Compute fairness metrics chosen by the fairness-metric-selector; present per-subgroup and disparity ratios.
7. Run robustness tests: input perturbation (typo, paraphrase, brightness, jitter), distribution shift, adversarial
   examples (PGD where relevant), and abstention behavior.
8. Run stress tests on edge cases: rare subgroups, out-of-distribution inputs, and minimum cell sizes.
9. Document the human-in-the-loop setup: who reviews, override rates, and observed override patterns.
10. Compile recommendations: prioritize by severity (critical, high, medium, low), owner, deadline, and verification
    method.
11. Produce a one-page executive summary, a full audit report, and structured findings in YAML for downstream tooling.
12. Define the re-audit cadence and the trigger conditions: retraining, distribution shift, incident, or regulatory
    change.

## Inputs

- Model artefact and version identifier.
- Evaluation dataset with subgroup annotations.
- Model card and dataset card source documents (if any).
- Existing fairness, robustness, and incident reports.
- Risk appetite and acceptance thresholds from prior AIA.

## Outputs

- `audit_scope.md` — model, version, use, scope, out-of-scope.
- `model_card.md` — standard model card sections.
- `dataset_card.md` — standard dataset card sections.
- `evaluation_setup.md` — splits, subgroups, metrics, sample sizes.
- `performance_by_subgroup.md` — metric × subgroup table with CIs.
- `fairness_results.md` — chosen metrics with disparity ratios.
- `robustness_tests.md` — perturbation, shift, adversarial, abstention.
- `recommendations.md` — prioritized actions with owner and deadline.
- `executive_summary.md` — one-page plain-language summary.
- `findings.yaml` — machine-readable findings for downstream tooling.
- `subgroup_chart.svg` — visual performance by subgroup.

## Key Rules

- The audit must be reproducible: dataset versions, model versions, seeds, code, and hyperparameters must be recorded.
- Performance must be reported with confidence intervals, not point estimates alone; small subgroups need bootstrap CIs.
- Out-of-scope items must be explicitly listed; "everything else" is not acceptable.
- Recommendations must be actionable; "improve fairness" without specifying the intervention is non-compliant.
- Recommendations must be prioritized by severity and tied to a verification method.
- Human-in-the-loop findings must report observed override rates, not only nominal authority.
- Robustness tests must include distribution shift, not only adversarial inputs; both are common failure modes.
- The re-audit cadence must be specified; an audit without a refresh plan goes stale.

## Examples

```text
Finding structure:
  ID: F-007
  Severity: HIGH
  Title: Subgroup recall gap on users aged 65+.
  Evidence: recall 0.71 (65+) vs. 0.86 (overall), 95% CI [0.65, 0.76].
  Recommendation: oversample older users in training; re-evaluate within 60 days.
  Owner: ML team; deadline: 2024-08-30; verification: re-run audit.
```

```text
Robustness test excerpt (NLP classifier):
  Perturbation: 1% character-level typos.
  Accuracy drop: 4.2 percentage points (overall), 7.1 pp (Group B).
  Threshold: 3 pp overall.
  Status: FAIL — recommendations to fine-tune on augmented data.
```
