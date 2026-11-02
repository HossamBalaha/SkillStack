---
name: curriculum-mapper
description: Map curriculum to program outcomes via a course × outcome matrix, gap analysis, and scaffold planning. Use when the user asks to align a degree program, audit coverage, or plan prerequisite scaffolds.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: teaching-pedagogy
tags: [curriculum, mapping, outcomes, gap-analysis, scaffold]
related: [teaching-pedagogy/course-syllabus-designer, teaching-pedagogy/learning-objective-writer, teaching-pedagogy/assessment-designer]
prerequisites: []
outputs: [markdown, csv]
difficulty: intermediate
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

# Curriculum Mapper

## When To Use

- The user asks to "map the curriculum", "audit coverage", or "where do we teach outcome X?".
- A program is preparing for accreditation (ABET, AACSB, regional body) and needs an outcomes map.
- A new course is being proposed and its place in the scaffold must be justified.
- A program is being revised and gaps or redundancies must be identified.
- Trigger keywords: curriculum mapping, program outcomes, gap analysis, scaffold, accreditation.

## Workflow

1. List the program outcomes (5-8 statements) and every course in the program with its course-level outcomes.
2. For each course × outcome cell, mark coverage level: I (Introduced), R (Reinforced), M (Mastered), or blank.
3. Build the curriculum map matrix; verify each program outcome has I → R → M somewhere in the sequence.
4. Run a gap analysis: any program outcome with no M, or with no I in the first half of the program, is a gap.
5. Run a redundancy check: any program outcome over-covered in more than 70% of courses is a candidate for trimming.
6. Build the scaffold plan: list which courses introduce, reinforce, and master each outcome in chronological order.
7. Verify prerequisite chains support the scaffold — the mastering course must list the reinforcing course as a
   prerequisite.
8. Flag outcomes taught by a single course — single-thread outcomes are fragile to staffing changes.
9. Document assessment evidence per outcome: where will students demonstrate mastery, and with what artifact.
10. Propose revisions: introduce earlier, reinforce across more courses, or add a capstone to master.
11. Schedule a review cycle (every 2-3 years) and assign an owner per outcome so orphan outcomes do not survive a
    staffing change.
12. Publish the map to faculty and students as part of the program handbook.

## Inputs

- Program outcomes (5-8 statements, ideally measurable).
- Course catalog with course-level outcomes.
- Course prerequisite chain (from the registrar).
- Assessment inventory per course (what artifacts demonstrate each outcome).

## Outputs

- `curriculum_map.csv` — course × program outcome × I / R / M cell.
- `gap_analysis.md` — outcomes with insufficient coverage and the proposed fix.
- `scaffold_plan.md` — outcome × introducing / reinforcing / mastering courses, in chronological order.
- `assessment_evidence.csv` — outcome × course × assessment item that elicits it.

## Key Rules

- Every program outcome must have at least one Introduce, one Reinforce, and one Master in the sequence.
- Outcomes taught by a single course are fragile — distribute to at least two courses where possible.
- The scaffold must respect prerequisites: the mastering course must list the reinforcing course as a prerequisite.
- Coverage labels must be backed by assessment evidence, not just syllabus claims — audit the syllabus against the
  artifact.
- A gap is any outcome with no M, or with I only in the final third of the program (too late to reinforce).
- The map is reviewed every 2-3 years; ownership per outcome prevents orphan outcomes.

## Examples

```text
Program outcome O2: "Apply statistical reasoning to data."
Course × O2 coverage:
  Year 1 STAT 101 — I (intro to distributions)
  Year 2 STAT 201 — R (hypothesis testing)
  Year 3 DATA 310 — R (regression)
  Year 4 CAP 401 — M (capstone analysis)
Status: well scaffolded. Gap: none.
Assessment evidence: STAT 201 midterm Q4-Q6; CAP 401 final
  report section 3.
```

```text
Gap example:
Program outcome O5: "Communicate technical findings in writing."
Coverage:
  Year 1 ENGL 101 — I
  Year 4 CAP 401 — M
Status: GAP — no Reinforce between Year 1 and Year 4 (3-year
  gap erodes the skill).
Recommended fix: add R coverage in a Year 2 or Year 3 core
  course (e.g., DATA 310 lab report). Owner: program chair.
```

```text
Redundancy example:
Program outcome O1: "Identify major data structures."
Coverage: O1 marked in 9 of 12 courses (75%) — over-covered.
Recommended fix: trim O1 coverage from elective courses;
  keep I/R/M chain in the 3-course core.
```

```text
Curriculum map cell sample (CSV row):
course_id,outcome_id,level,assessment_evidence,owner
CS101,O1,I,Quiz 3 Q1-Q5,Smith J.
CS201,O1,R,Lab 2,Smith J.
CS401,O1,M,Capstone deliverable 1,Patel A.
```

## References

- Nicholls (1978), "Developing a Curriculum: A Practical Guide" — Routledge. Curriculum design framework.
- Biggs & Tang (2011), "Teaching for Quality Learning at University" (4th ed.) — Open University Press. Constructive
  alignment.
- Harden (2001), "Outcome-based education — the future is today" — Medical Teacher, 24(2), 125-138. Outcome mapping.
- ABET criteria for accrediting programs — https://www.abet.org/accreditation/
