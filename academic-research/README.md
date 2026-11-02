# 🎓 Academic Research — Research Planning & Writing

> Plan studies, draft manuscripts, write theses, design grants, peer-review papers, and prepare conference talks. Skills
> cover the full research lifecycle — from formulating a research question and hypothesis, through experimental design
> and
> pre-registration, to journal articles, academic books, and reproducibility checklists. Use this theme whenever the
> deliverable is a research artifact rather than raw code or data.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-20-blue)]()
[![Theme](https://img.shields.io/badge/Theme-academic-research-green)]()

</div>

## Theme Overview

This folder contains **20 skills** in the `academic-research/` theme. Each subfolder holds a `SKILL.md` whose YAML
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

| #  | Skill                                                                             | Description                                                                                                                                                                                                                                                                                                      | Difficulty   | Tags                                                                               | Related                                                                                                                                          |
|----|-----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`academic-book-author`](academic-book-author/SKILL.md)                           | Draft academic book chapters in LaTeX with learning objectives, narrative hooks, progressive disclosure, mandatory code-walkthrough sequences, A-Z numerical examples, chapter summaries, Q&A, exercises, nomenclature glossary, and summary slides via tcolorbox.                                               | advanced     | `latex`, `textbook`, `book-chapter`, `exercises`, `nomenclature`                   | `academic-research/journal-manuscript-writer`, `academic-research/thesis-chapter-planner`, `style-integrity/latex-style-guard`                   |
| 2  | [`citation-network-mapper`](citation-network-mapper/SKILL.md)                     | Map citation networks using tools like Connected Papers, Semantic Scholar, and Inciteful to identify influential/bridge papers, research lineages, and emerging trends, and output a citation graph (nodes = papers, edges = citations).                                                                         | intermediate | `citations`, `literature`, `network-graph`, `semantic-scholar`, `connected-papers` | `academic-research/literature-review-synthesizer`, `academic-research/related-work-surveyor`, `style-integrity/zero-fabrication-guard`           |
| 3  | [`conference-talk-prep`](conference-talk-prep/SKILL.md)                           | Draft conference talks with slide-by-slide outline, speaker notes per slide, transition sentences, time-boxing per slide, anticipated Q&A with prepared answers, and accessibility checks (contrast, font size, alt text).                                                                                       | intermediate | `conference`, `slides`, `talk`, `presentation`, `qa-prep`                          | `academic-research/journal-manuscript-writer`, `academic-research/research-portfolio-tracker`, `academic-research/peer-review-simulator`         |
| 4  | [`experimental-design-planner`](experimental-design-planner/SKILL.md)             | Plan experimental designs (RCT, factorial, crossover, repeated-measures, quasi-experimental) with sample-size calculation via power analysis (alpha=0.05, power=0.80), randomization scheme, blinding, and control conditions.                                                                                   | advanced     | `experimental-design`, `rct`, `power-analysis`, `sample-size`, `randomization`     | `academic-research/hypothesis-designer`, `academic-research/research-question-formulator`, `academic-research/pre-registration-drafter`          |
| 5  | [`grant-proposal-writer`](grant-proposal-writer/SKILL.md)                         | Draft competitive grant proposals with Specific Aims (1 page), Background and Significance, Innovation, Approach (preliminary data, methodology, pitfalls, alternatives), Budget Justification, and Biosketch narrative.                                                                                         | advanced     | `grant`, `nsf`, `nih`, `proposal`, `specific-aims`                                 | `academic-research/scope-and-aims-writer`, `academic-research/research-ideation-planner`, `academic-research/journal-manuscript-writer`          |
| 6  | [`hypothesis-designer`](hypothesis-designer/SKILL.md)                             | Design testable hypotheses with explicit null (H0) and alternative (H1) statements, effect-size framing, expected direction, and the statistical test that will evaluate each hypothesis.                                                                                                                        | intermediate | `hypothesis`, `h0-h1`, `effect-size`, `statistical-test`, `finer`                  | `academic-research/research-question-formulator`, `academic-research/experimental-design-planner`, `academic-research/pre-registration-drafter`  |
| 7  | [`journal-manuscript-writer`](journal-manuscript-writer/SKILL.md)                 | Draft publication-ready journal sections in LaTeX with strict structural style: only \section and \subsection (no \subsubsection), separator comments around floats, IEEE citation style, and mandatory back-matter sections.                                                                                    | advanced     | `latex`, `manuscript`, `journal`, `imrad`, `writing`                               | `style-integrity/latex-style-guard`, `academic-research/related-work-surveyor`, `academic-research/supplementary-materials-organizer`            |
| 8  | [`literature-review-synthesizer`](literature-review-synthesizer/SKILL.md)         | Build systematic literature reviews using PICO or SPIDER framing, Boolean search strings, a PRISMA 2020 flow diagram, thematic synthesis matrix, and quality appraisal with CASP, AMSTAR-2, or ROBIS.                                                                                                            | advanced     | `systematic-review`, `prisma`, `pico`, `synthesis`, `casp`                         | `academic-research/related-work-surveyor`, `academic-research/citation-network-mapper`, `style-integrity/zero-fabrication-guard`                 |
| 9  | [`open-science-advocate`](open-science-advocate/SKILL.md)                         | Apply open-science practices across the research lifecycle: open data (Zenodo, Figshare, Dryad), open code (GitHub with DOI via Zenodo), preprints (arXiv, bioRxiv, medRxiv), pre-registration (OSF, AsPredicted), and Registered Reports.                                                                       | intermediate | `open-science`, `fair`, `preprints`, `osf`, `zenodo`                               | `academic-research/pre-registration-drafter`, `academic-research/reproducibility-checklist-author`, `academic-research/research-repo-builder`    |
| 10 | [`peer-review-simulator`](peer-review-simulator/SKILL.md)                         | Generate rigorous peer-review reports structured as Summary, Strengths, Major Revisions, Minor Revisions, Specific Comments by Section, and Decision Letter, plus draft author rebuttal letters responding point-by-point.                                                                                       | advanced     | `peer-review`, `rebuttal`, `reviewer`, `decision-letter`, `revision`               | `academic-research/journal-manuscript-writer`, `style-integrity/zero-fabrication-guard`, `style-integrity/claim-source-tracer`                   |
| 11 | [`pre-registration-drafter`](pre-registration-drafter/SKILL.md)                   | Draft pre-registration documents: AsPredicted (7 questions), OSF registrations, and Registered Report Stage 1 protocols.                                                                                                                                                                                         | intermediate | `pre-registration`, `aspredicted`, `osf`, `registered-report`, `hypotheses`        | `academic-research/hypothesis-designer`, `academic-research/experimental-design-planner`, `academic-research/open-science-advocate`              |
| 12 | [`related-work-surveyor`](related-work-surveyor/SKILL.md)                         | Survey related work and build thematic comparison tables (paper x dimension matrix) grouped by methodology, not chronology, and identify the gap your work fills.                                                                                                                                                | intermediate | `related-work`, `comparison-table`, `novelty`, `gap-analysis`, `literature`        | `academic-research/literature-review-synthesizer`, `academic-research/citation-network-mapper`, `academic-research/journal-manuscript-writer`    |
| 13 | [`reproducibility-checklist-author`](reproducibility-checklist-author/SKILL.md)   | Author a reproducibility checklist for a submitted manuscript covering code on GitHub with DOI, data on Zenodo with DOI, environment lockfile (requirements.txt or environment.yml), seeds fixed, random partitions documented, hardware and software stated, compute time reported, and a license file present. | intermediate | `reproducibility`, `checklist`, `zenodo`, `doi`, `environment-lock`                | `academic-research/research-repo-builder`, `academic-research/open-science-advocate`, `ml-engineering/reproducible-experiment-runner`            |
| 14 | [`research-ideation-planner`](research-ideation-planner/SKILL.md)                 | Propose three or more novel research ideas aligned to a target venue's scope, then convert the user-selected idea into an end-to-end research blueprint.                                                                                                                                                         | intermediate | `ideation`, `brainstorm`, `venue`, `novelty`, `research-plan`                      | `academic-research/research-question-formulator`, `academic-research/scope-and-aims-writer`, `academic-research/grant-proposal-writer`           |
| 15 | [`research-portfolio-tracker`](research-portfolio-tracker/SKILL.md)               | Track research outputs (papers submitted/under-review/accepted, code repos, datasets, presentations) and produce a status dashboard as a Markdown table with deadlines and next actions.                                                                                                                         | beginner     | `portfolio`, `dashboard`, `tracking`, `status`, `deadlines`                        | `academic-research/research-repo-builder`, `academic-research/conference-talk-prep`, `academic-research/journal-manuscript-writer`               |
| 16 | [`research-question-formulator`](research-question-formulator/SKILL.md)           | Formulate research questions using the FINER criteria (Feasible, Interesting, Novel, Ethical, Relevant) and PICO/SPIDER/PCC frameworks.                                                                                                                                                                          | intermediate | `research-question`, `finer`, `pico`, `spider`, `pcc`                              | `academic-research/hypothesis-designer`, `academic-research/research-ideation-planner`, `academic-research/scope-and-aims-writer`                |
| 17 | [`research-repo-builder`](research-repo-builder/SKILL.md)                         | Scaffold a complete modular research repository from an approved plan, including src/data, src/models, src/utils, Configs/Config.yaml, manual/ chapters, Datasets.md, unversioned Requirements.txt, CreateProjectZip.py, and Main.py entry point.                                                                | intermediate | `scaffolding`, `repository`, `project-structure`                                   | `style-integrity/coding-conventions-enforcer`, `ml-engineering/modular-ml-architect`, `academic-research/reproducibility-checklist-author`       |
| 18 | [`scope-and-aims-writer`](scope-and-aims-writer/SKILL.md)                         | Draft scope statements, three to four numbered specific aims, and contribution statements, with contributions reserved for the Introduction only and the Methodology focused on technical "how" and domain "why".                                                                                                | intermediate | `scope`, `specific-aims`, `contributions`, `introduction`, `thesis`                | `academic-research/research-ideation-planner`, `academic-research/grant-proposal-writer`, `academic-research/thesis-chapter-planner`             |
| 19 | [`supplementary-materials-organizer`](supplementary-materials-organizer/SKILL.md) | Organize supplementary materials (math derivations, additional figures, full tables, code release, dataset, model weights, video demos) and cross-reference every supplementary item from the main text.                                                                                                         | intermediate | `supplementary`, `appendix`, `cross-reference`, `multimedia`, `code-release`       | `academic-research/journal-manuscript-writer`, `style-integrity/cross-reference-validator`, `academic-research/reproducibility-checklist-author` |
| 20 | [`thesis-chapter-planner`](thesis-chapter-planner/SKILL.md)                       | Plan thesis and dissertation chapters with strict cross-chapter non-redundancy enforcement.                                                                                                                                                                                                                      | advanced     | `thesis`, `dissertation`, `chapter`, `monograph`, `concept-map`                    | `academic-research/academic-book-author`, `academic-research/scope-and-aims-writer`, `style-integrity/cross-reference-validator`                 |

## Difficulty Breakdown

Across **20** skills in this theme, the difficulty distribution is:

- **Beginner** — 1 skill(s)
- **Intermediate** — 12 skill(s)
- **Advanced** — 7 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`finer` (2), `latex` (2), `literature` (2), `novelty` (2), `osf` (2), `pico` (2), `specific-aims` (2), `thesis` (2),
`zenodo` (2), `appendix` (1), `aspredicted` (1), `book-chapter` (1), `brainstorm` (1), `casp` (1), `chapter` (1),
`checklist` (1), `citations` (1), `code-release` (1), `comparison-table` (1), `concept-map` (1), `conference` (1),
`connected-papers` (1), `contributions` (1), `cross-reference` (1), `dashboard` (1), `deadlines` (1), `decision-letter`
(1), `dissertation` (1), `doi` (1), `effect-size` (1), `environment-lock` (1), `exercises` (1), `experimental-design`
(1), `fair` (1), `gap-analysis` (1), `grant` (1), `h0-h1` (1), `hypotheses` (1), `hypothesis` (1), `ideation` (1),
`imrad` (1), `introduction` (1), `journal` (1), `manuscript` (1), `monograph` (1), `multimedia` (1), `network-graph`
(1), `nih` (1), `nomenclature` (1), `nsf` (1), `open-science` (1), `pcc` (1), `peer-review` (1), `portfolio` (1),
`power-analysis` (1), `pre-registration` (1), `preprints` (1), `presentation` (1), `prisma` (1), `project-structure`
(1), `proposal` (1), `qa-prep` (1), `randomization` (1), `rct` (1), `rebuttal` (1), `registered-report` (1),
`related-work` (1), `repository` (1), `reproducibility` (1), `research-plan` (1), `research-question` (1), `reviewer`
(1), `revision` (1), `sample-size` (1), `scaffolding` (1), `scope` (1), `semantic-scholar` (1), `slides` (1), `spider`
(1), `statistical-test` (1), `status` (1), `supplementary` (1), `synthesis` (1), `systematic-review` (1), `talk` (1),
`textbook` (1), `tracking` (1), `venue` (1), `writing` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`scope-and-aims-writer` → `research-question-formulator` → `hypothesis-designer` → `experimental-design-planner`** —
  Scope → question → hypothesis → study design.
- **`research-ideation-planner` → `research-repo-builder` → `modular-ml-architect` →
  `reproducible-experiment-runner`** — Idea → repo → code style → experiments.
- **`literature-review-synthesizer` → `literature-matrix-builder` → `related-work-surveyor` →
  `citation-network-mapper`** — Survey → matrix → gap → influential papers.
- **`grant-proposal-writer` → `research-methodology-designer` → `pre-registration-drafter` →
  `reproducibility-checklist-author`** — Grant → methods → pre-reg → repro.

## Cross-Theme Connections

Skills in `academic-research/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../style-integrity/` — 9 related pointer(s)
- `../ml-engineering/` — 2 related pointer(s)

Themes that commonly chain with this one:

- [`../style-integrity/README.md`](style-integrity/README.md) — manuscript and LaTeX style guards run on every drafted
  article.
- [`../writing-citation/README.md`](writing-citation/README.md) — literature reviews feed into the BibTeX pipeline.
- [`../visualization/README.md`](visualization/README.md) — conference talks and posters need figures and slides.
- [`../project-tooling/README.md`](project-tooling/README.md) — research repos are scaffolded by repo and CI skills.

## Back to Master

← [Back to SkillStack README](../README.md)
