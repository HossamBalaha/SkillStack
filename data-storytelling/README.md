# 📖 Data Storytelling — Narratives, Dashboards & Decks

> Turn analysis into stories that move a decision. Skills cover narrative arc design,
> executive dashboards, assertion-evidence slides, data-journalism pieces, infographics, chart annotations,
> audience tailoring, scrollytelling, storyboarding, metric translation, and pitch decks. Use this theme
> whenever the deliverable is a story a human reads, watches, or clicks through — not a raw chart or a notebook.

## Theme Overview

This folder contains **11 skills** in the `data-storytelling/` theme. Each subfolder holds a `SKILL.md` whose YAML
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

| #  | Skill                                                                     | Description                                                                                                                                                                                               | Difficulty   | Tags                                                                            | Related                                                                                                                                       |
|----|---------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`narrative-arc-designer`](narrative-arc-designer/SKILL.md)               | Design narrative arcs for data stories by mapping evidence onto a setup-conflict-resolution spine and choosing between author-driven and reader-driven structures.                                        | intermediate | `narrative-arc`, `story-design`, `martini-glass`, `drill-down`, `sequencing`    | `data-storytelling/data-story-storyboarder`, `data-storytelling/audience-tailor`, `data-storytelling/data-annotation-writer`                  |
| 2  | [`executive-dashboard-designer`](executive-dashboard-designer/SKILL.md)   | Design executive dashboards that surface the right KPI hierarchy, encode state with restrained color, annotate thresholds, and offer drill-down paths that hold up on mobile.                             | intermediate | `dashboard`, `kpi`, `executive`, `drill-down`, `mobile-responsive`              | `data-storytelling/data-annotation-writer`, `data-storytelling/audience-tailor`, `visualization/dashboard-builder`                            |
| 3  | [`presentation-slide-builder`](presentation-slide-builder/SKILL.md)       | Build presentation slides that lead with an assertion, keep text sparse, let full-bleed charts carry the evidence, and chain into a narrative flow with planned transitions.                              | intermediate | `slides`, `assertion-evidence`, `full-bleed`, `narrative-flow`, `readability`   | `data-storytelling/data-story-storyboarder`, `data-storytelling/audience-tailor`, `academic-research/conference-talk-prep`                    |
| 4  | [`data-journalism-writer`](data-journalism-writer/SKILL.md)               | Write data-journalism pieces with a finding-first lede, a methodology paragraph, an interactive chart, sourced quotes, and honest caveats.                                                                | intermediate | `data-journalism`, `lede`, `methodology`, `sourcing`, `caveats`                 | `data-storytelling/metric-translation-writer`, `data-storytelling/data-annotation-writer`, `data-storytelling/interactive-narrative-builder`  |
| 5  | [`infographic-crafter`](infographic-crafter/SKILL.md)                     | Craft single-takeaway infographics with deliberate visual hierarchy, a curated icon set, statistics callouts at display size, and a restrained color palette.                                             | intermediate | `infographic`, `visual-hierarchy`, `icons`, `callouts`, `single-takeaway`       | `data-storytelling/metric-translation-writer`, `data-storytelling/audience-tailor`, `visualization/infographic-summarizer`                    |
| 6  | [`data-annotation-writer`](data-annotation-writer/SKILL.md)               | Write chart annotations that highlight the right data points, add contextual labels, draw narrative arrows, and place callouts so a reader lands the finding without the prose.                           | beginner     | `annotation`, `callout`, `contextual-label`, `narrative-arrow`, `chart-craft`   | `data-storytelling/narrative-arc-designer`, `visualization/figure-caption-writer`, `visualization/publication-figure-maker`                   |
| 7  | [`audience-tailor`](audience-tailor/SKILL.md)                             | Tailor a data story for a named audience by reshaping the lead, depth, analogy, and caveats to match what each reader expects.                                                                            | intermediate | `audience`, `tailoring`, `analogy`, `framing`, `caveats`                        | `data-storytelling/narrative-arc-designer`, `data-storytelling/metric-translation-writer`, `data-storytelling/presentation-slide-builder`     |
| 8  | [`interactive-narrative-builder`](interactive-narrative-builder/SKILL.md) | Build interactive scrollytelling narratives using D3.js and IntersectionObserver, with step-by-step chart reveals and branch choices for reader-driven exploration.                                       | advanced     | `scrollytelling`, `d3`, `intersection-observer`, `branch-choice`, `interactive` | `data-storytelling/narrative-arc-designer`, `data-storytelling/data-story-storyboarder`, `visualization/interactive-plot-builder`             |
| 9  | [`data-story-storyboarder`](data-story-storyboarder/SKILL.md)             | Storyboard a data story into panels with transitions, emotional beats, planned surprises, and a conclusion that lands the takeaway.                                                                       | intermediate | `storyboard`, `panels`, `emotional-beats`, `surprise`, `conclusion`             | `data-storytelling/narrative-arc-designer`, `data-storytelling/presentation-slide-builder`, `data-storytelling/interactive-narrative-builder` |
| 10 | [`metric-translation-writer`](metric-translation-writer/SKILL.md)         | Translate technical metrics into human-scaled outcomes for non-technical readers, converting dollars into scholarships saved, percentages into absolute counts, and accuracy gains into prevented errors. | beginner     | `metric-translation`, `human-scale`, `framing`, `analogies`, `made-to-stick`    | `data-storytelling/audience-tailor`, `data-storytelling/infographic-crafter`, `data-storytelling/data-journalism-writer`                      |
| 11 | [`data-pitch-deck-builder`](data-pitch-deck-builder/SKILL.md)             | Build data-driven pitch decks with a problem slide anchored by evidence, a solution slide backed by data, a market slide sized as TAM/SAM/SOM, and a traction slide that proves momentum.                 | intermediate | `pitch-deck`, `problem-solution`, `tam-sam-som`, `traction`, `demo-day`         | `data-storytelling/audience-tailor`, `data-storytelling/presentation-slide-builder`, `data-storytelling/data-annotation-writer`               |

## Difficulty Breakdown

Across **11** skills in this theme, the difficulty distribution is:

- **Beginner** — 2 skill(s)
- **Intermediate** — 8 skill(s)
- **Advanced** — 1 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`caveats` (2), `drill-down` (2), `framing` (2), `analogy` (1), `analogies` (1), `annotation` (1), `assertion-evidence`
(1), `audience` (1), `branch-choice` (1), `callout` (1), `callouts` (1), `chart-craft` (1), `conclusion` (1),
`contextual-label` (1), `d3` (1), `dashboard` (1), `demo-day` (1), `emotional-beats` (1), `executive` (1),
`full-bleed` (1), `human-scale` (1), `icons` (1), `infographic` (1), `intersection-observer` (1), `interactive` (1),
`kpi` (1), `lede` (1), `made-to-stick` (1), `martini-glass` (1), `methodology` (1), `metric-translation` (1),
`mobile-responsive` (1), `narrative-arc` (1), `narrative-arrow` (1), `narrative-flow` (1), `panels` (1), `pitch-deck`
(1), `problem-solution` (1), `readability` (1), `scrollytelling` (1), `sequencing` (1), `single-takeaway` (1), `slides`
(1), `sourcing` (1), `story-design` (1), `storyboard` (1), `surprise` (1), `tailoring` (1), `tam-sam-som` (1),
`traction` (1), `visual-hierarchy` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`narrative-arc-designer` → `data-story-storyboarder` → `presentation-slide-builder` →
  `data-annotation-writer`** — Arc → storyboard → slides → annotation.
- **`narrative-arc-designer` → `interactive-narrative-builder` → `data-annotation-writer`** — Arc → scrolly →
  annotation.
- **`metric-translation-writer` → `audience-tailor` → `presentation-slide-builder`** — Translate → tailor → slide.
- **`data-journalism-writer` → `metric-translation-writer` → `data-annotation-writer`** — Article → translate →
  annotate.
- **`data-pitch-deck-builder` → `audience-tailor` → `presentation-slide-builder`** — Deck → tailor → slide.

## Cross-Theme Connections

Skills in `data-storytelling/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../visualization/` — 5 related pointer(s)
- `../academic-research/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../visualization/README.md`](../visualization/README.md) — dashboards, infographics, annotations, and scrolly
  narratives build on visualization outputs.
- [`../academic-research/README.md`](../academic-research/README.md) — conference talks and pitch decks reuse the
  assertion-evidence structure academic talks rely on.
- [`../writing-citation/README.md`](../writing-citation/README.md) — data-journalism pieces feed the citation and
  style-guard pipeline.
- [`../style-integrity/README.md`](../style-integrity/README.md) — claim-source tracers and zero-fabrication guards run
  on every published story and pitch.

## Back to Master

← [Back to SkillStack README](../README.md)
