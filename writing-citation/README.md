# 📝 Writing & Citation — BibTeX, Editing & Paraphrasing

> Draft, edit, paraphrase, and cite academic prose with strict consistency. Skills cover outline expansion, paragraph
> transitions, tense/hedging balance, IMRaD thesis writing, BibTeX management, DOI verification, citation-style
> conversion, and plagiarism-safe paraphrasing. Every skill respects author voice and preserves every fact, citation,
> and
> number verbatim.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-18-blue)]()
[![Theme](https://img.shields.io/badge/Theme-writing-citation-green)]()

</div>

## Theme Overview

This folder contains **18 skills** in the `writing-citation/` theme. Each subfolder holds a `SKILL.md` whose YAML
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

| #  | Skill                                                                       | Description                                                                                                                                                                                                                                          | Difficulty   | Tags                                                                    | Related                                                                                                                                                                |
|----|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`annotated-bibliography-builder`](annotated-bibliography-builder/SKILL.md) | Builds annotated bibliographies where each entry combines a full citation, a 2-4 sentence summary (what the paper did, its method, and key finding), and an assessment of strengths, limitations, and relevance to the user's work.                  | intermediate | `bibliography`, `annotated`, `summary`, `literature-review`, `citation` | `writing-citation/literature-matrix-builder`, `writing-citation/bibtex-citation-manager`, `writing-citation/reference-list-formatter`                                  |
| 2  | [`bibtex-citation-manager`](bibtex-citation-manager/SKILL.md)               | Manages BibTeX bibliography databases by generating stable citekeys, deduplicating entries, validating required fields, and enforcing IEEE citation style.                                                                                           | intermediate | `bibtex`, `citations`, `latex`, `ieee`                                  | `writing-citation/doi-verifier`, `writing-citation/citation-style-converter`, `writing-citation/reference-list-formatter`, `style-integrity/cross-reference-validator` |
| 3  | [`citation-style-converter`](citation-style-converter/SKILL.md)             | Converts bibliographies and inline citations between IEEE, APA, Chicago, Vancouver, and MLA styles while keeping citekeys and the bibliography in sync.                                                                                              | intermediate | `citation`, `ieee`, `apa`, `chicago`, `vancouver`                       | `writing-citation/bibtex-citation-manager`, `writing-citation/reference-list-formatter`                                                                                |
| 4  | [`cohesive-device-checker`](cohesive-device-checker/SKILL.md)               | Checks cohesive devices in academic prose — reference (this/that/these/those/it), conjunction (however, therefore, moreover), lexical (repetition, synonyms, superordinates), and ellipsis — to ensure cohesion without overusing any single device. | intermediate | `cohesion`, `reference`, `conjunction`, `lexical`, `ellipsis`           | `writing-citation/english-academic-editor`, `writing-citation/paragraph-transition-smoother`                                                                           |
| 5  | [`doi-verifier`](doi-verifier/SKILL.md)                                     | Verifies that each DOI in a bibliography resolves to the paper claimed by the entry, by querying the Crossref REST API and matching title, first author, and journal.                                                                                | intermediate | `doi`, `crossref`, `verification`, `citations`                          | `ai-output-judgement/reference-accuracy-checker`, `style-integrity/zero-fabrication-guard`                                                                             |
| 6  | [`english-academic-editor`](english-academic-editor/SKILL.md)               | Edits non-native English academic prose to improve article usage, tense consistency, register, and hedging, while preserving the author's meaning.                                                                                                   | intermediate | `editing`, `english`, `academic`, `grammar`, `tense`                    | `writing-citation/tense-consistency-fixer`, `writing-citation/hedging-language-balancer`, `writing-citation/cohesive-device-checker`                                   |
| 7  | [`hedging-language-balancer`](hedging-language-balancer/SKILL.md)           | Balances hedging (cautious language) to match evidence strength, deploying modal verbs, epistemic adverbs, and tentative reporting verbs where claims outrun the data, and removing excess hedging where claims are well-supported.                  | intermediate | `hedging`, `modals`, `epistemic`, `calibrated`, `claims`                | `writing-citation/english-academic-editor`, `writing-citation/tense-consistency-fixer`                                                                                 |
| 8  | [`imrad-thesis-writer`](imrad-thesis-writer/SKILL.md)                       | Drafts full IMRaD theses and dissertations with strict cross-chapter non-redundancy, keeping contributions only in the Introduction, technical detail only in Methods, neutral reporting in Results, and interpretation in Discussion.               | advanced     | `imrad`, `thesis`, `dissertation`, `structure`, `non-redundancy`        | `writing-citation/outline-to-prose-expander`, `writing-citation/structured-abstract-writer`                                                                            |
| 9  | [`literature-matrix-builder`](literature-matrix-builder/SKILL.md)           | Builds a paper-by-dimension literature matrix (rows = papers, columns = year, methodology, dataset, sample size, key findings, limitations, relevance) as a Markdown table or CSV, sorted by year or theme.                                          | beginner     | `literature-review`, `matrix`, `synthesis`, `csv`, `gaps`               | `writing-citation/annotated-bibliography-builder`, `writing-citation/research-methodology-designer`                                                                    |
| 10 | [`outline-to-prose-expander`](outline-to-prose-expander/SKILL.md)           | Expands a bullet outline into flowing academic prose where each bullet becomes a 3-5 sentence paragraph with topic sentence, evidence, and transition.                                                                                               | intermediate | `outline`, `prose`, `paragraphs`, `topic-sentence`, `transition`        | `writing-citation/imrad-thesis-writer`, `writing-citation/paragraph-transition-smoother`                                                                               |
| 11 | [`paragraph-transition-smoother`](paragraph-transition-smoother/SKILL.md)   | Smooths paragraph transitions using conceptual bridges and appropriate logical connectors (addition, contrast, cause-effect, sequence), while avoiding formulaic openers like "Furthermore" and "In conclusion.                                      | beginner     | `transitions`, `cohesion`, `connectors`, `flow`, `academic`             | `writing-citation/cohesive-device-checker`, `writing-citation/outline-to-prose-expander`                                                                               |
| 12 | [`plagiarism-paraphraser`](plagiarism-paraphraser/SKILL.md)                 | Rewrites source text to reduce similarity scores below 15% on iThenticate/Turnitin while preserving meaning, structural integrity, and technical vocabulary.                                                                                         | intermediate | `paraphrase`, `plagiarism`, `similarity`, `ithenticate`, `patchwriting` | `writing-citation/english-academic-editor`, `writing-citation/cohesive-device-checker`                                                                                 |
| 13 | [`reading-level-adjuster`](reading-level-adjuster/SKILL.md)                 | Adjusts the reading level of academic prose to a target grade using Flesch-Kincaid Grade Level, Gunning Fog Index, and SMOG metrics, by simplifying long sentences, reducing jargon, and defining abbreviations.                                     | beginner     | `reading-level`, `flesch-kincaid`, `gunning-fog`, `smog`, `lay-summary` | `writing-citation/english-academic-editor`, `writing-citation/structured-abstract-writer`                                                                              |
| 14 | [`reference-list-formatter`](reference-list-formatter/SKILL.md)             | Formats reference lists in any citation style from a `.bib` source, applying author-name order, italics, punctuation, and abbreviated-vs-full journal-name rules.                                                                                    | intermediate | `bibliography`, `reference-list`, `citation-style`, `italics`, `bibtex` | `writing-citation/bibtex-citation-manager`, `writing-citation/citation-style-converter`                                                                                |
| 15 | [`research-methodology-designer`](research-methodology-designer/SKILL.md)   | Designs complete research methodologies covering study design, sampling strategy, sample-size calculation, data-collection methods, and ethical considerations.                                                                                      | advanced     | `methodology`, `rct`, `sampling`, `sample-size`, `irb`                  | `writing-citation/imrad-thesis-writer`, `writing-citation/annotated-bibliography-builder`                                                                              |
| 16 | [`structured-abstract-writer`](structured-abstract-writer/SKILL.md)         | Drafts structured abstracts with explicit bold inline headings (Background, Methods, Results, Conclusion) tuned to journal word limits, then appends 4-6 SEO-optimized keywords separated by semicolons.                                             | beginner     | `abstract`, `structured`, `imrad`, `keywords`, `biomedical`             | `writing-citation/imrad-thesis-writer`, `writing-citation/english-academic-editor`                                                                                     |
| 17 | [`tense-consistency-fixer`](tense-consistency-fixer/SKILL.md)               | Fixes tense drift in academic prose by enforcing PAST for Methods and Results, PRESENT for established facts and the Discussion, and PRESENT PERFECT for prior work leading to the current study.                                                    | intermediate | `tense`, `grammar`, `methods`, `results`, `discussion`                  | `writing-citation/english-academic-editor`, `writing-citation/hedging-language-balancer`                                                                               |
| 18 | [`zotero-better-bibtex-bridge`](zotero-better-bibtex-bridge/SKILL.md)       | Bridges Zotero reference libraries into LaTeX workflows via the BetterBibTeX plugin, configuring stable citekeys, exporting auto-updating `.bib` files, and wiring cite-as-you-write into editors such as vim, Atom, and Scrivener.                  | intermediate | `zotero`, `betterbibtex`, `citekeys`, `latex`, `bibtex`                 | `writing-citation/bibtex-citation-manager`, `writing-citation/reference-list-formatter`                                                                                |

## Difficulty Breakdown

Across **18** skills in this theme, the difficulty distribution is:

- **Beginner** — 4 skill(s)
- **Intermediate** — 12 skill(s)
- **Advanced** — 2 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`bibtex` (3), `academic` (2), `bibliography` (2), `citation` (2), `citations` (2), `cohesion` (2), `grammar` (2), `ieee`
(2), `imrad` (2), `latex` (2), `literature-review` (2), `tense` (2), `abstract` (1), `annotated` (1), `apa` (1),
`betterbibtex` (1), `biomedical` (1), `calibrated` (1), `chicago` (1), `citation-style` (1), `citekeys` (1), `claims`
(1), `conjunction` (1), `connectors` (1), `crossref` (1), `csv` (1), `discussion` (1), `dissertation` (1), `doi` (1),
`editing` (1), `ellipsis` (1), `english` (1), `epistemic` (1), `flesch-kincaid` (1), `flow` (1), `gaps` (1),
`gunning-fog` (1), `hedging` (1), `irb` (1), `italics` (1), `ithenticate` (1), `keywords` (1), `lay-summary` (1),
`lexical` (1), `matrix` (1), `methodology` (1), `methods` (1), `modals` (1), `non-redundancy` (1), `outline` (1),
`paragraphs` (1), `paraphrase` (1), `patchwriting` (1), `plagiarism` (1), `prose` (1), `rct` (1), `reading-level` (1),
`reference` (1), `reference-list` (1), `results` (1), `sample-size` (1), `sampling` (1), `similarity` (1), `smog` (1),
`structure` (1), `structured` (1), `summary` (1), `synthesis` (1), `thesis` (1), `topic-sentence` (1), `transition` (1),
`transitions` (1), `vancouver` (1), `verification` (1), `zotero` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`outline-to-prose-expander` → `paragraph-transition-smoother` → `tense-consistency-fixer` →
  `hedging-language-balancer` → `cohesive-device-checker`** — Outline → flow → tense → hedge → cohesion.
- **`structured-abstract-writer` → `imrad-thesis-writer` → `tense-consistency-fixer` → `english-academic-editor` →
  `reading-level-adjuster`** — Abstract → IMRaD → tense → edit → readability.
- **`zotero-better-bibtex-bridge` → `bibtex-citation-manager` → `doi-verifier` → `citation-style-converter` →
  `reference-list-formatter`** — Zotero → BibTeX → verify → convert → format.
- **`plagiarism-paraphraser` → `english-academic-editor` → `tense-consistency-fixer` → `cohesive-device-checker`** —
  Paraphrase → edit → tense → cohesion.

## Cross-Theme Connections

Skills in `writing-citation/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../style-integrity/` — 2 related pointer(s)
- `../ai-output-judgement/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../academic-research/README.md`](academic-research/README.md) — literature reviews and theses are written here.
- [`../style-integrity/README.md`](style-integrity/README.md) — prose polish, tense, and banned-vocabulary rules are
  shared.
- [`../ai-text/README.md`](ai-text/README.md) — paraphrasing skills pair with AI-text humanization.
- [`../ai-output-judgement/README.md`](ai-output-judgement/README.md) — citation verifiers overlap with
  reference-accuracy checks.

## Back to Master

← [Back to SkillStack README](../README.md)
