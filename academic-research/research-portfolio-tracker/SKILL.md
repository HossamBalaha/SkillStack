---
name: research-portfolio-tracker
description: Track research outputs (papers submitted/under-review/accepted, code repos, datasets, presentations) and produce a status dashboard as a Markdown table with deadlines and next actions. Use when the user wants to monitor the status of multiple research artifacts across a research group or solo portfolio.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [portfolio, dashboard, tracking, status, deadlines]
related: [academic-research/research-repo-builder, academic-research/conference-talk-prep, academic-research/journal-manuscript-writer]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Research Portfolio Tracker

## When To Use
- The user asks to "track my papers", "build a research dashboard", or "what is the status of my submission".
- The user manages multiple artifacts (papers, repos, datasets, talks).
- The user wants a single status view with deadlines and next actions.
- Trigger keywords: portfolio, dashboard, status, deadline, next action, submission tracker.

## Workflow
1. Collect all active artifacts: papers, preprints, code repos, datasets, presentations, posters.
2. For each artifact, capture: title, type, venue, status, submission date, expected decision date, DOI/URL, lead author, next action.
3. Normalize status values: Drafted, Submitted, Under Review, Revise-and-Resubmit, Accepted, Published, Rejected, Withdrawn.
4. Build a unified Markdown dashboard table with one row per artifact.
5. Sort by urgency: deadline-ascending, with overdue items pinned to the top.
6. For each artifact, derive the next action: e.g., "Draft response to Reviewer 2 by 2025-11-15".
7. Compute summary counts: active submissions, under-review, accepted this year, preprints.
8. Flag missing artifacts (e.g., "code repo not yet public for accepted paper") for open-science compliance.
9. Optionally emit an iCalendar (.ics) for each deadline.
10. Output the dashboard and a CSV snapshot for spreadsheet import.

## Inputs
- List of artifacts with current status (or a CSV/portfolio file).
- Today's date and target review period.
- Per-artifact deadlines and action items.
- Optional: group members and roles.

## Outputs
- `dashboard.md` — Markdown status table sorted by deadline.
- `portfolio.csv` — same data in CSV form.
- `next_actions.md` — derived next action per artifact.
- `summary_counts.md` — counts by status and by type.
- `deadlines.ics` — optional calendar file.

## Key Rules
- Status values are normalized to the eight allowed values.
- Dashboard is sorted by deadline ascending; overdue items pinned to top.
- Every artifact row must include a next action with an explicit date.
- Open-science flags raised when an accepted paper has no public code/data.
- CSV columns are stable across snapshots for trend analysis.
- No fabricated DOIs; leave blank if not yet issued.

## Examples
```text
Dashboard excerpt (sorted by deadline):

| Artifact                  | Type  | Venue           | Status        | Deadline   | Next Action                       |
|---------------------------|-------|-----------------|---------------|------------|-----------------------------------|
| FedTopo segmentation       | Paper | MedIA           | Revise/R&R    | 2025-11-20 | Respond to Reviewer 2 by 11-15   |
| Topology toolkit            | Repo  | GitHub          | Public        | 2025-11-05 | Tag v1.0 and archive to Zenodo    |
| MRI benchmark               | Data  | Zenodo          | Drafted       | 2025-11-30 | Upload curated dataset            |
| NeurIPS workshop talk       | Talk  | NeurIPS-W       | Accepted      | 2025-12-06 | Finalize slides by 12-01          |
```
```text
Summary counts:
  Active submissions: 2
  Under Review: 1
  Accepted (2025): 3
  Preprints: 4
  Open-science flags: 1 (MedIA paper accepted, no public code yet).
```

## References
- ORCID for researcher identifiers: https://orcid.org/
- Zenodo for DOI minting: https://zenodo.org/
- GitHub Actions for deadline reminders: https://docs.github.com/en/actions
- Pandoc for Markdown-to-CSV conversion: https://pandoc.org/

## Notes
- Refresh the dashboard at least weekly during submission-heavy periods.
- Pin the snapshot date in the CSV header so trend reports stay auditable.
- Track both personal and shared artifacts separately to avoid double-counting.
