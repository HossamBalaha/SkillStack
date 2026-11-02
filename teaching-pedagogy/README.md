# 🎓 Teaching Pedagogy — Course Design, Assessment & Learning Analytics

> Design courses, write measurable objectives, build assessments and rubrics, scaffold lessons and curricula, embed
> accessibility and Universal Design for Learning, run active-learning activities, deliver formative feedback, and
> instrument learning analytics. Skills span the full teaching cycle — from syllabus design through microlearning
> delivery — and each is grounded in a named pedagogical framework (backward design, Bloom's taxonomy, Hunter's lesson
> design, CAST UDL Guidelines, Hattie & Timperley's feedback model). Use this theme whenever the deliverable is a
> teaching artifact rather than raw code or data.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-13-blue)]()
[![Theme](https://img.shields.io/badge/Theme-teaching-pedagogy-green)]()

</div>

## Theme Overview

This folder contains **13 skills** in the `teaching-pedagogy/` theme. Each subfolder holds a `SKILL.md` whose YAML
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

| #  | Skill                                                                   | Description                                                                                                                                                                                                                                                                  | Difficulty   | Tags                                                                                     | Related                                                                                                                                    |
|----|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`course-syllabus-designer`](course-syllabus-designer/SKILL.md)         | Design course syllabi that align learning outcomes, weekly schedule, assessment plan, required materials, and policies using backward design. Use when the user asks to build a syllabus, plan a multi-week course, or align outcomes with assessments and policies.         | intermediate | `syllabus`, `backward-design`, `course-planning`, `outcomes`, `assessment`               | `teaching-pedagogy/learning-objective-writer`, `teaching-pedagogy/assessment-designer`, `teaching-pedagogy/curriculum-mapper`              |
| 2  | [`learning-objective-writer`](learning-objective-writer/SKILL.md)       | Write measurable learning objectives using Bloom's revised taxonomy with observable action verbs (analyze, evaluate, create), conditions, and criteria. Use when the user asks to draft learning outcomes, ABCD objectives, or align objectives with assessments.            | beginner     | `learning-objectives`, `bloom`, `abcd`, `measurable`, `outcomes`                         | `teaching-pedagogy/course-syllabus-designer`, `teaching-pedagogy/lesson-plan-builder`, `teaching-pedagogy/exam-question-author`            |
| 3  | [`assessment-designer`](assessment-designer/SKILL.md)                   | Design formative and summative assessments including MCQs with distractor analysis, short-answer rubrics, project rubrics, and peer-review forms. Use when the user asks to build quizzes, write assessment plans, or design peer-review forms.                              | intermediate | `assessment`, `mcq`, `rubric`, `formative`, `summative`, `peer-review`                   | `teaching-pedagogy/rubric-builder`, `teaching-pedagogy/learning-objective-writer`, `teaching-pedagogy/formative-feedback-writer`           |
| 4  | [`rubric-builder`](rubric-builder/SKILL.md)                             | Build analytic and holistic rubrics with criteria, performance levels, descriptors, and point allocation. Use when the user asks to create grading rubrics, score essays or projects, or design consistent scoring guides.                                                   | intermediate | `rubric`, `analytic`, `holistic`, `grading`, `descriptors`                               | `teaching-pedagogy/assessment-designer`, `teaching-pedagogy/formative-feedback-writer`, `teaching-pedagogy/exam-question-author`           |
| 5  | [`lesson-plan-builder`](lesson-plan-builder/SKILL.md)                   | Build lesson plans using the Hunter lesson design with anticipatory hook, direct instruction, guided practice, independent practice, closure, and formative check. Use when the user asks to draft a single-class lesson plan or sequence daily lessons.                     | intermediate | `lesson-plan`, `hunter-model`, `direct-instruction`, `formative-check`, `closure`        | `teaching-pedagogy/learning-objective-writer`, `teaching-pedagogy/active-learning-designer`, `teaching-pedagogy/formative-feedback-writer` |
| 6  | [`accessible-content-designer`](accessible-content-designer/SKILL.md)   | Design accessible content meeting WCAG 2.2 AA: alt text, captioning, screen-reader friendly structure, color contrast, and keyboard navigation. Use when the user asks to make slides, documents, LMS pages, or videos accessible.                                           | intermediate | `accessibility`, `wcag`, `alt-text`, `captions`, `screen-reader`, `color-contrast`       | `teaching-pedagogy/universal-design-builder`, `teaching-pedagogy/lesson-plan-builder`, `teaching-pedagogy/microlearning-designer`          |
| 7  | [`universal-design-builder`](universal-design-builder/SKILL.md)         | Apply Universal Design for Learning (UDL) by providing multiple means of engagement, representation, and action/expression. Use when the user asks to design inclusive lessons, scaffold options, or build UDL-aligned activities.                                           | intermediate | `udl`, `universal-design`, `inclusion`, `engagement`, `representation`, `expression`     | `teaching-pedagogy/accessible-content-designer`, `teaching-pedagogy/lesson-plan-builder`, `teaching-pedagogy/assessment-designer`          |
| 8  | [`active-learning-designer`](active-learning-designer/SKILL.md)         | Design active-learning activities including think-pair-share, jigsaw, case-based learning, and peer instruction with ConcepTests. Use when the user asks to convert a lecture to active learning, build ConcepTests, or design small-group structures.                       | intermediate | `active-learning`, `think-pair-share`, `jigsaw`, `peer-instruction`, `case-based`        | `teaching-pedagogy/lesson-plan-builder`, `teaching-pedagogy/formative-feedback-writer`, `teaching-pedagogy/universal-design-builder`       |
| 9  | [`formative-feedback-writer`](formative-feedback-writer/SKILL.md)       | Write formative feedback that is specific, actionable, timely, and growth-oriented using the Hattie and Timperley feedback model. Use when the user asks to draft feedback on student work, peer-review comments, or coaching notes.                                         | intermediate | `feedback`, `formative`, `hattie-timperley`, `growth-oriented`, `actionable`             | `teaching-pedagogy/assessment-designer`, `teaching-pedagogy/rubric-builder`, `teaching-pedagogy/active-learning-designer`                  |
| 10 | [`learning-analytics-dashboard`](learning-analytics-dashboard/SKILL.md) | Build learning-analytics dashboards that extract LMS data, compute engagement metrics, predict at-risk students, and track interventions. Use when the user asks to monitor cohort engagement, predict dropout, or design early-alert systems.                               | advanced     | `learning-analytics`, `dashboard`, `lms`, `at-risk-prediction`, `early-alert`            | `teaching-pedagogy/formative-feedback-writer`, `teaching-pedagogy/assessment-designer`, `teaching-pedagogy/curriculum-mapper`              |
| 11 | [`curriculum-mapper`](curriculum-mapper/SKILL.md)                       | Map curriculum to program outcomes via a course × outcome matrix, gap analysis, and scaffold planning. Use when the user asks to align a degree program, audit coverage, or plan prerequisite scaffolds.                                                                     | intermediate | `curriculum`, `mapping`, `outcomes`, `gap-analysis`, `scaffold`                          | `teaching-pedagogy/course-syllabus-designer`, `teaching-pedagogy/learning-objective-writer`, `teaching-pedagogy/assessment-designer`       |
| 12 | [`exam-question-author`](exam-question-author/SKILL.md)                 | Author exam questions targeting higher-order thinking (Bloom's analyze, evaluate, create) with scenario-based stems, blueprints, and psychometric review. Use when the user asks to write midterm or final exam questions, build test blueprints, or review item statistics. | advanced     | `exam-questions`, `higher-order-thinking`, `blueprint`, `psychometrics`, `item-analysis` | `teaching-pedagogy/learning-objective-writer`, `teaching-pedagogy/assessment-designer`, `teaching-pedagogy/rubric-builder`                 |
| 13 | [`microlearning-designer`](microlearning-designer/SKILL.md)             | Design microlearning modules of 3-5 minute units, each with a single learning objective, spaced-repetition hooks, and mobile-first delivery. Use when the user asks to build short learning bites, mobile study cards, or spaced-repetition decks.                           | intermediate | `microlearning`, `spaced-repetition`, `mobile-first`, `learning-bites`, `microcontent`   | `teaching-pedagogy/lesson-plan-builder`, `teaching-pedagogy/accessible-content-designer`, `teaching-pedagogy/active-learning-designer`     |

## Difficulty Breakdown

Across **13** skills in this theme, the difficulty distribution is:

- **Beginner** — 1 skill(s)
- **Intermediate** — 10 skill(s)
- **Advanced** — 2 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`outcomes` (3), `assessment` (2), `formative` (2), `rubric` (2), `abcd` (1), `accessibility` (1), `actionable` (1),
`active-learning` (1), `alt-text` (1), `analytic` (1), `at-risk-prediction` (1), `backward-design` (1), `bloom` (1),
`blueprint` (1), `captions` (1), `case-based` (1), `closure` (1), `color-contrast` (1), `course-planning` (1),
`curriculum` (1), `dashboard` (1), `descriptors` (1), `direct-instruction` (1), `early-alert` (1), `engagement` (1),
`exam-questions` (1), `expression` (1), `feedback` (1), `formative-check` (1), `gap-analysis` (1), `grading` (1),
`growth-oriented` (1), `hattie-timperley` (1), `higher-order-thinking` (1), `holistic` (1), `hunter-model` (1),
`inclusion` (1), `item-analysis` (1), `jigsaw` (1), `learning-analytics` (1), `learning-bites` (1),
`learning-objectives` (1), `lesson-plan` (1), `lms` (1), `mapping` (1), `measurable` (1), `mcq` (1), `microcontent`
(1), `microlearning` (1), `mobile-first` (1), `peer-instruction` (1), `peer-review` (1), `psychometrics` (1),
`representation` (1), `scaffold` (1), `screen-reader` (1), `spaced-repetition` (1), `summative` (1), `syllabus` (1),
`think-pair-share` (1), `udl` (1), `universal-design` (1), `wcag` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`learning-objective-writer` → `course-syllabus-designer` → `curriculum-mapper` → `assessment-designer`** —
  Objectives → syllabus → program map → assessment.
- **`course-syllabus-designer` → `lesson-plan-builder` → `active-learning-designer` → `formative-feedback-writer`** —
  Syllabus → lesson → activity → feedback.
- **`learning-objective-writer` → `assessment-designer` → `rubric-builder` → `exam-question-author`** — Objectives →
  assessment → rubric → exam.
- **`lesson-plan-builder` → `microlearning-designer` → `accessible-content-designer` → `universal-design-builder`** —
  Lesson → micro → access → UDL.
- **`assessment-designer` → `learning-analytics-dashboard` → `formative-feedback-writer`** — Assess → analytics →
  feedback.

## Cross-Theme Connections

Skills in `teaching-pedagogy/` declare `related` pointers to skills in other themes. The most common destinations are:

- No cross-theme related pointers found in this theme.

Themes that commonly chain with this one:

- [`../visualization/README.md`](../visualization/README.md) — learning-analytics dashboards reuse visualization
  patterns; rubric heatmaps and curriculum maps render as figures.
- [`../writing-citation/README.md`](../writing-citation/README.md) — syllabi, rubrics, and feedback narratives benefit
  from prose editing and structured-abstract tooling.
- [`../academic-research/README.md`](../academic-research/README.md) — peer-review simulators and conference-talk prep
  share structures with assessment-designer and lesson-plan-builder.
- [`../project-tooling/README.md`](../project-tooling/README.md) — learning-analytics dashboards ship as Docker
  containers with `requirements.txt` pinned by the packaging skills.

## Back to Master

← [Back to SkillStack README](../README.md)
