---
name: learning-analytics-dashboard
description: Build learning-analytics dashboards that extract LMS data, compute engagement metrics, predict at-risk students, and track interventions. Use when the user asks to monitor cohort engagement, predict dropout, or design early-alert systems.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [learning-analytics, dashboard, lms, at-risk-prediction, early-alert]
related: [teaching-pedagogy/formative-feedback-writer, teaching-pedagogy/assessment-designer, teaching-pedagogy/curriculum-mapper]
prerequisites: []
outputs: [python, html, csv, json]
difficulty: advanced
estimated_tokens: 2400
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Learning Analytics Dashboard

## When To Use

- The user asks for "an early-alert system", "at-risk dashboard", or "cohort engagement report".
- A course instructor wants to see who has disengaged before the midterm.
- A program needs to track intervention outcomes across multiple sections.
- An LMS data extract needs to be turned into actionable weekly alerts.
- Trigger keywords: learning analytics, LMS data, at-risk prediction, early alert, intervention log, SoLAR.

## Workflow

1. Pull raw event logs from the LMS via its REST API (Canvas, Moodle, Brightspace) or via a database export.
2. Normalize events into a long-format table: student_id, course_id, event_type, timestamp, page_id.
3. Compute engagement metrics: login frequency, page views per week, time-on-task, submission timeliness, discussion
   posts.
4. Derive behavioral signals: attendance proxy, late submission rate, quiz attempt count, video watch completion.
5. Define at-risk using a combination of: missing two consecutive weeks of activity, late submission rate above 50%,
   quiz score below 60% on formative.
6. Train a simple interpretable model (logistic regression with feature importance) rather than a black box —
   explainability is required for educational decisions.
7. Validate the model on a held-out term; report precision, recall, F1, and the false-positive rate (the cost of a wrong
   alert).
8. Build the dashboard: cohort overview, per-student drill-down, and an intervention log.
9. Add an intervention log where the instructor records what was done and the student's response within 48 hours.
10. Schedule a weekly refresh; daily predictions add noise without adding insight.
11. Surface "why at-risk" reasons, not just the score; instructors need a reason to act.
12. Document data governance: FERPA compliance, retention window, and who is authorized to see the dashboard.

## Inputs

- LMS event logs (CSV, JSON, or API token with read scope).
- Course roster and enrollment status.
- Assessment scores and submission timestamps.
- Prior term data for model training and validation.

## Outputs

- `dashboard.py` — Streamlit or Dash app loading the metrics table and the prediction table.
- `metrics.csv` — student × engagement metric matrix per week.
- `at_risk_predictions.csv` — student × probability × top reasons × recommended action.
- `intervention_log.csv` — student × intervention × date × outcome.
- `data_governance.md` — FERPA, retention, access policy, and audit trail.

## Key Rules

- At-risk predictions must come with explanations, not raw scores — instructors need a reason to act.
- Models must be interpretable (logistic regression, decision tree); black boxes are unacceptable for educational
  decisions.
- False-positive rate must be reported alongside recall; a high false-positive rate erodes instructor trust.
- Weekly refresh cadence; daily predictions add noise without adding insight.
- All data access must be FERPA-compliant; minimize who sees the dashboard and log every view.
- The intervention log is mandatory — predictions without follow-up have no value.
- Engagement metrics must adjust for course structure (a 3-week module has different baselines than a 15-week course).

## Examples

```python
# Engagement metric: weekly login streak (consecutive ISO
# weeks with at least one login event).
import pandas as pd

def LoginStreak(events: pd.DataFrame, studentId: int) -> int:
  # Filter to this student's login events.
  logins = events[(events.student_id == studentId)
                  & (events.event_type == "login")]
  if (logins.empty):
    return 0
  # Collect the ISO week of each login as a sorted unique list.
  weeks = sorted({ts.isocalendar()[1] for ts in logins.timestamp})
  streak, maxStreak = 1, 1
  for i in range(1, len(weeks)):
    if (weeks[i] == weeks[i - 1] + 1):
      streak += 1
      maxStreak = max(maxStreak, streak)
    else:
      streak = 1
  return maxStreak
```

```text
At-risk alert (dashboard sample):
Student 012345 — Probability 0.78
Top reasons (SHAP-style, ranked):
  - No login in 9 days (last: Mar 14)
  - Missed submission: Quiz 4 (due Mar 12)
  - Discussion posts: 0 this week (cohort median: 2)
Recommended action: send personalized email within 48 hours
  offering office hours.
Logged intervention on Mar 16: email sent.
Follow-up on Mar 23: student logged in, submitted Quiz 5 on
  time. Outcome: resolved.
```

```text
Model report (held-out term):
Precision: 0.71   Recall: 0.83   F1: 0.76
False-positive rate: 0.18
Top features by absolute weight:
  1. login_streak (negative, strongest)
  2. late_submission_rate (positive)
  3. quiz_score_formative (negative)
  4. discussion_posts_week (negative)
Action: model accepted for weekly use; revisit at end of term.
```

## References

- Society for Learning Analytics Research (SoLAR) — https://www.solaresearch.org/
- Sclater, Peasgood & Mullan (2017), "Learning Analytics in Higher Education" — JISC. SOLES framework.
- Siemens & Long (2011), "Penetrating the Fog: Analytics in Learning and Education" — EDUCAUSE Review, 46(5), 30-32.
- Canvas LMS REST API — https://canvas.instructure.com/doc/api/
