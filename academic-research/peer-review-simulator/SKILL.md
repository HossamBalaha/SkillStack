---
name: peer-review-simulator
description: Generate rigorous peer-review reports structured as Summary, Strengths, Major Revisions, Minor Revisions, Specific Comments by Section, and Decision Letter, plus draft author rebuttal letters responding point-by-point. Use when the user asks to peer review a manuscript, simulate reviewer feedback, or write a rebuttal letter for a journal or conference revision.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [peer-review, rebuttal, reviewer, decision-letter, revision]
related: [academic-research/journal-manuscript-writer, style-integrity/zero-fabrication-guard, style-integrity/claim-source-tracer]
prerequisites: []
outputs: [markdown]
difficulty: advanced
estimated_tokens: 810
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Peer Review Simulator

## When To Use

- The user asks to "review this paper", "play the role of reviewer", or "generate reviewer comments".
- The user needs a decision letter for an editorial role.
- The user has received reviewer comments and needs a rebuttal letter.
- Trigger keywords: peer review, reviewer report, decision letter, rebuttal, response to reviewers, COPE.

## Workflow

1. Read the manuscript end-to-end. Confirm scope fit for the target venue.
2. Draft a 150-200 word Summary that paraphrases the contribution in your own words; never quote the abstract.
3. List Strengths (3-6 bullets) tied to methodological soundness, novelty, and clarity.
4. List Major Revisions (numbered M1, M2, ...). Each item must specify the issue, why it matters, and a concrete fix.
5. List Minor Revisions (numbered m1, m2, ...). Each item is a localized, actionable edit.
6. Write Specific Comments by Section: Introduction, Related Work, Methodology, Experiments, Discussion, Conclusion. Use
   line numbers from the manuscript.
7. Assign a recommendation: Accept, Minor Revision, Major Revision, Reject, or Reject and Resubmit.
8. Draft the Decision Letter: salutation, recommendation, summary of key points, deadline, and signature block.
9. For rebuttal mode: read each reviewer comment, draft a point-by-point response in a two-column table (Reviewer
   Comment → Author Response), cite manuscript edits with new line numbers.
10. Verify COPE compliance: comments are courteous, evidence-based, free of personal criticism, and disclose any
    conflicts of interest.
11. Output the review and (when applicable) the rebuttal as separate files.

## Inputs

- Manuscript file (PDF, LaTeX source, or Markdown).
- Target venue scope and review criteria.
- Mode: reviewer-report or rebuttal-letter.
- For rebuttal: original reviewer comments and the revised manuscript diff.

## Outputs

- `reviewer_report.md` — structured review with all six sections.
- `decision_letter.md` — editor-style decision letter.
- `rebuttal_letter.md` — point-by-point response table (when in rebuttal mode).
- `cope_compliance_check.md` — short statement of COPE adherence.

## Key Rules

- Every Major Revision item names the issue, explains the impact, and proposes a fix.
- Use line numbers when commenting on specific text.
- Recommendation must be one of: Accept, Minor Revision, Major Revision, Reject, Reject and Resubmit.
- Rebuttal responses are point-by-point; no narrative essays.
- Comments are courteous and evidence-based; no personal tone.
- Disclose any conflict of interest at the top of the review.
- Follow COPE ethical guidelines for peer reviewers verbatim.

## Examples

```text
Major Revision M2:
Issue: The ablation study removes only one component at a time.
Impact: Interactions between components (e.g., topology regularizer and
aggregator) are invisible, weakening the causal claim in Section 4.3.
Fix: Add a factorial ablation (2^3 design) reporting Dice for all
combinations; include a brief interaction analysis paragraph.
```

```text
Rebuttal row sample:
| Reviewer 2, M3: "Sample size of 30 seems underpowered." |
| We agree. A post-hoc power analysis (G*Power 3.1, alpha=0.05,
| power=0.80, effect size d=0.5) yields n=64 per arm. We have rerun
| the experiment with n=64 per arm (now reported in revised Table 2,
| lines 312-318) and the effect remains significant (p=0.012). |
```

## Notes

- Keep reviewer and rebuttal tone strictly professional; no sarcasm or speculation about authorship.
- For rebuttal mode, always include the page or line number the reviewer can verify.
- When uncertain about scope fit, recommend "Reject and Resubmit" rather than outright reject.
- Disclose any competing interest at the top of the review; if a conflict is material, recuse the review.
- Avoid requesting new experiments unless they are essential to the central claims of the paper.
