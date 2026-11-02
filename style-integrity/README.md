# 🛡️ Style & Integrity — LaTeX, Prose & Coding Conventions

> Enforce strict style rules across LaTeX, prose, and Python code; verify every citation, DOI, and claim against its
> source; audit math notation; and execute multi-step tasks with discipline. These skills act as the quality gates that
> keep a research artifact honest, consistent, and submission-ready. Load them before submission, not after.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-18-blue)]()
[![Theme](https://img.shields.io/badge/Theme-style-integrity-green)]()

</div>

## Theme Overview

This folder contains **18 skills** in the `style-integrity/` theme. Each subfolder holds a `SKILL.md` whose YAML
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

| #  | Skill                                                                           | Description                                                                                                                                                                                                                                       | Difficulty   | Tags                                                                      | Related                                                                                                                                                                          |
|----|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`abbreviation-consistency-checker`](abbreviation-consistency-checker/SKILL.md) | Verify every abbreviation in a manuscript is defined exactly once at first appearance, used consistently thereafter, and aggregated in a final abbreviations table when the count exceeds ten.                                                    | intermediate | `abbreviations`, `acronyms`, `consistency`, `manuscript`, `glossary`      | `style-integrity/notation-consistency-checker`, `style-integrity/latex-style-guard`, `style-integrity/cross-reference-validator`                                                 |
| 2  | [`academic-prose-polisher`](academic-prose-polisher/SKILL.md)                   | Rewrite informal or AI-flavored prose into formal academic register suitable for peer-reviewed venues.                                                                                                                                            | intermediate | `prose`, `academic-register`, `editing`, `revision`, `formal`             | `style-integrity/banned-vocabulary-filter`, `style-integrity/em-dash-eliminator`, `style-integrity/meta-commentary-stripper`, `style-integrity/passive-voice-detector`           |
| 3  | [`banned-vocabulary-filter`](banned-vocabulary-filter/SKILL.md)                 | Strip banned AI-tell vocabulary and cliché phrases from academic or technical prose and replace each with a precise synonym.                                                                                                                      | beginner     | `vocabulary`, `banned-words`, `ai-tells`, `synonyms`, `prose`             | `style-integrity/academic-prose-polisher`, `style-integrity/meta-commentary-stripper`, `style-integrity/voice-matching-guard`                                                    |
| 4  | [`claim-source-tracer`](claim-source-tracer/SKILL.md)                           | Map every factual claim in a manuscript to its originating binder, page, line, and citation, producing a verification table and a separate unverified-sources list.                                                                               | advanced     | `verification`, `claims`, `citations`, `binder`, `traceability`           | `style-integrity/zero-fabrication-guard`, `style-integrity/cross-reference-validator`, `academic-research/supplementary-materials-organizer`                                     |
| 5  | [`coding-conventions-enforcer`](coding-conventions-enforcer/SKILL.md)           | Enforce five strict Python coding rules across an entire repository — camelCase variables, CamelCase functions/classes/files/dict-keys, parenthesized if-conditions, period-terminated comments above every statement, and double-quoted strings. | intermediate | `python`, `style`, `lint`, `camelcase`, `conventions`                     | `ml-engineering/modular-ml-architect`, `style-integrity/latex-style-guard`, `ml-engineering/reproducible-experiment-runner`                                                      |
| 6  | [`cross-reference-validator`](cross-reference-validator/SKILL.md)               | Verify that every `\label{}` in a LaTeX manuscript has a corresponding `\ref{}`, and vice versa, that every float and equation is cross-referenced, and that punctuation sits outside the closing brace.                                          | intermediate | `latex`, `cross-reference`, `label`, `ref`, `floats`                      | `style-integrity/latex-style-guard`, `style-integrity/notation-consistency-checker`, `academic-research/supplementary-materials-organizer`                                       |
| 7  | [`em-dash-eliminator`](em-dash-eliminator/SKILL.md)                             | Find em-dashes (`—`) and en-dashes used as parenthetical separators in academic prose and replace them with commas, parentheses, or en-dashes for numerical ranges.                                                                               | beginner     | `em-dash`, `en-dash`, `punctuation`, `prose`, `typography`                | `style-integrity/academic-prose-polisher`, `style-integrity/banned-vocabulary-filter`, `style-integrity/numerical-value-formatter`                                               |
| 8  | [`execution-protocol`](execution-protocol/SKILL.md)                             | Apply a 10-stage meta-discipline wrapper around any complex multi-step task to guarantee comprehension, surgical edits, fact verification, and clean delivery.                                                                                    | advanced     | `meta-discipline`, `workflow`, `verification`, `multi-step`, `protocol`   | `style-integrity/planning-note-logger`, `style-integrity/silent-omission-protocol`, `style-integrity/zero-fabrication-guard`                                                     |
| 9  | [`latex-style-guard`](latex-style-guard/SKILL.md)                               | Enforce strict LaTeX typography and structural formatting rules on manuscripts before submission.                                                                                                                                                 | advanced     | `latex`, `typography`, `manuscript`, `formatting`, `camera-ready`         | `style-integrity/cross-reference-validator`, `style-integrity/notation-consistency-checker`, `academic-research/journal-manuscript-writer`                                       |
| 10 | [`math-symbol-auditor`](math-symbol-auditor/SKILL.md)                           | Audit a math-heavy manuscript for one-to-one symbol-to-concept mapping, immediate textual definition after first equation use, and standard calligraphic-font conventions for sets and spaces.                                                    | advanced     | `math`, `symbols`, `nomenclature`, `latex`, `audit`                       | `style-integrity/notation-consistency-checker`, `style-integrity/latex-style-guard`, `style-integrity/abbreviation-consistency-checker`                                          |
| 11 | [`meta-commentary-stripper`](meta-commentary-stripper/SKILL.md)                 | Remove pedagogical, conversational, and meta phrases from academic prose so the text delivers direct, dense scientific exposition.                                                                                                                | intermediate | `meta-commentary`, `prose`, `editing`, `exposition`, `density`            | `style-integrity/academic-prose-polisher`, `style-integrity/banned-vocabulary-filter`, `style-integrity/passive-voice-detector`                                                  |
| 12 | [`notation-consistency-checker`](notation-consistency-checker/SKILL.md)         | Audit a mathematical manuscript for one-to-one symbol-to-concept mapping and enforce a Nomenclature table when symbol count exceeds fifteen.                                                                                                      | advanced     | `notation`, `symbols`, `nomenclature`, `latex`, `math`                    | `style-integrity/math-symbol-auditor`, `style-integrity/abbreviation-consistency-checker`, `style-integrity/latex-style-guard`                                                   |
| 13 | [`numerical-value-formatter`](numerical-value-formatter/SKILL.md)               | Wrap every standalone numerical value in body text with the `\ineq{}` LaTeX macro, replace the `PIP` token with `\ineq{pip}`, normalize en-dash-minus variants to hyphen, and fix `etc.etc.` duplicates.                                          | intermediate | `latex`, `numerical`, `ineq-macro`, `typography`, `formatting`            | `style-integrity/latex-style-guard`, `style-integrity/math-symbol-auditor`, `style-integrity/notation-consistency-checker`                                                       |
| 14 | [`passive-voice-detector`](passive-voice-detector/SKILL.md)                     | Detect passive-voice constructions in prose ("is done", "was performed", "are preserved automatically") and rewrite them as active-voice sentences with a clear subject.                                                                          | intermediate | `passive-voice`, `active-voice`, `prose`, `editing`, `grammar`            | `style-integrity/academic-prose-polisher`, `style-integrity/meta-commentary-stripper`, `style-integrity/banned-vocabulary-filter`                                                |
| 15 | [`planning-note-logger`](planning-note-logger/SKILL.md)                         | Append a concise "Planning Note" section at the end of any deliverable summarizing what data was missing, what assumptions were made, and what the user must provide.                                                                             | beginner     | `planning-note`, `deliverable`, `assumptions`, `unknowns`, `transparency` | `style-integrity/silent-omission-protocol`, `style-integrity/execution-protocol`, `style-integrity/zero-fabrication-guard`                                                       |
| 16 | [`silent-omission-protocol`](silent-omission-protocol/SKILL.md)                 | Silently omit data the user has not provided, instead of inserting jarring declaration markers in the body.                                                                                                                                       | intermediate | `silent-omission`, `missing-data`, `prose`, `narrative`, `cohesion`       | `style-integrity/planning-note-logger`, `style-integrity/execution-protocol`, `style-integrity/zero-fabrication-guard`                                                           |
| 17 | [`voice-matching-guard`](voice-matching-guard/SKILL.md)                         | When the user provides a writing sample, match its style exactly and override generic style rules.                                                                                                                                                | advanced     | `voice-matching`, `style`, `idiosyncratic`, `writing-sample`, `override`  | `style-integrity/academic-prose-polisher`, `style-integrity/banned-vocabulary-filter`, `style-integrity/meta-commentary-stripper`                                                |
| 18 | [`zero-fabrication-guard`](zero-fabrication-guard/SKILL.md)                     | Verify every citation, DOI, URL, dataset name, author name, paper title, and numerical claim in a manuscript against authoritative external sources before submission.                                                                            | advanced     | `verification`, `citations`, `fabrication`, `doi`                         | `style-integrity/claim-source-tracer`, `academic-research/literature-review-synthesizer`, `style-integrity/cross-reference-validator`, `academic-research/peer-review-simulator` |

## Difficulty Breakdown

Across **18** skills in this theme, the difficulty distribution is:

- **Beginner** — 3 skill(s)
- **Intermediate** — 8 skill(s)
- **Advanced** — 7 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`prose` (6), `latex` (5), `editing` (3), `typography` (3), `verification` (3), `citations` (2), `formatting` (2),
`manuscript` (2), `math` (2), `nomenclature` (2), `style` (2), `symbols` (2), `abbreviations` (1), `academic-register`
(1), `acronyms` (1), `active-voice` (1), `ai-tells` (1), `assumptions` (1), `audit` (1), `banned-words` (1), `binder`
(1), `camelcase` (1), `camera-ready` (1), `claims` (1), `cohesion` (1), `consistency` (1), `conventions` (1),
`cross-reference` (1), `deliverable` (1), `density` (1), `doi` (1), `em-dash` (1), `en-dash` (1), `exposition` (1),
`fabrication` (1), `floats` (1), `formal` (1), `glossary` (1), `grammar` (1), `idiosyncratic` (1), `ineq-macro` (1),
`label` (1), `lint` (1), `meta-commentary` (1), `meta-discipline` (1), `missing-data` (1), `multi-step` (1), `narrative`
(1), `notation` (1), `numerical` (1), `override` (1), `passive-voice` (1), `planning-note` (1), `protocol` (1),
`punctuation` (1), `python` (1), `ref` (1), `revision` (1), `silent-omission` (1), `synonyms` (1), `traceability` (1),
`transparency` (1), `unknowns` (1), `vocabulary` (1), `voice-matching` (1), `workflow` (1), `writing-sample` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`coding-conventions-enforcer` → `latex-style-guard` → `academic-prose-polisher` → `banned-vocabulary-filter`** —
  Code + prose style enforcement before submission.
- **`bibtex-citation-manager` → `doi-verifier` → `citation-style-converter` → `reference-list-formatter` →
  `cross-reference-validator` → `zero-fabrication-guard`** — Full citation integrity pass.
- **`claim-source-tracer` → `zero-fabrication-guard` → `silent-omission-protocol` → `planning-note-logger`** — Verify
  claims → omit silently → log gaps.
- **`notation-consistency-checker` → `math-symbol-auditor` → `numerical-value-formatter` →
  `abbreviation-consistency-checker`** — Math notation audit.

## Cross-Theme Connections

Skills in `style-integrity/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../academic-research/` — 5 related pointer(s)
- `../ml-engineering/` — 2 related pointer(s)

Themes that commonly chain with this one:

- [`../academic-research/README.md`](academic-research/README.md) — style guards are applied to drafted manuscripts and
  theses.
- [`../writing-citation/README.md`](writing-citation/README.md) — citation verification and prose polish share
  vocabulary rules.
- [`../ai-output-judgement/README.md`](ai-output-judgement/README.md) — zero-fabrication guard pairs with hallucination
  detectors.
- [`../ml-engineering/README.md`](ml-engineering/README.md) — coding-conventions-enforcer styles every Python file.

## Back to Master

← [Back to SkillStack README](../README.md)
