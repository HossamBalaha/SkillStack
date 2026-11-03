# 🤖 AI Text — Detect & Humanize AI Text

> Detect machine-written text using a six-category tell catalog, classify severity, and humanize flagged passages
> while preserving every fact, citation, and number verbatim. Covers perplexity/burstiness scoring, watermark detection,
> multi-engine verification, and voice-profile matching for author-attributed rewrites. Every humanization ends with a
> re-detection pass to confirm the rewrite held.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-15-blue)]()
[![Theme](https://img.shields.io/badge/Theme-ai-text-green)]()

</div>

## Theme Overview

This folder contains **15 skills** in the `ai-text/` theme. Each subfolder holds a `SKILL.md` whose YAML frontmatter
declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
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

| #  | Skill                                                                         | Description                                                                                                                                                                                                                                  | Difficulty   | Tags                                                                | Related                                                                                                                                                                                                                            |
|----|-------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`ai-tell-catalog`](ai-tell-catalog/SKILL.md)                                 | Reference catalog of 26 AI tells organized into six categories, each with a name, what to watch for, why it is a problem, and a before/after pair.                                                                                           | beginner     | `reference`, `ai-tells`, `catalog`, `ai-text`                       | `ai-text/ai-text-detector`, `ai-text/ai-text-humanizer`, `ai-text/severity-classifier`                                                                                                                                             |
| 2  | [`ai-text-detector`](ai-text-detector/SKILL.md)                               | Detect AI-generated text by scanning for a structured catalog of tells across lexical, structural, thematic, tonal, statistical, and citation categories.                                                                                    | intermediate | `ai-detection`, `tells`, `perplexity`, `burstiness`                 | `ai-text/ai-tell-catalog`, `ai-text/severity-classifier`, `ai-text/perplexity-burstiness-scorer`, `ai-text/citation-hallucination-detector`                                                                                        |
| 3  | [`ai-text-humanizer`](ai-text-humanizer/SKILL.md)                             | Rewrite AI-sounding text to restore natural voice and burstiness while preserving every fact, citation, date, name, and number verbatim.                                                                                                     | advanced     | `humanization`, `rewriting`, `voice`, `ai-text`                     | `ai-text/ai-text-detector`, `ai-text/voice-profile-matcher`, `ai-text/staging-tell-remover`, `ai-text/inflation-stripper`, `ai-text/rhythm-by-rule-fixer`, `ai-text/formatting-by-rule-cleaner`, `ai-text/chatbot-residue-cleaner` |
| 4  | [`ai-watermark-detector`](ai-watermark-detector/SKILL.md)                     | Detect statistical watermarks embedded by LLMs using the Kirchenbauer et al. (2023) green-list/red-list scheme — green-list token ratio above baseline, watermark strength parameter δ, and hash-based seeding keyed to the preceding token. | advanced     | `watermark`, `statistical-detection`, `green-list`, `ai-text`       | `ai-text/perplexity-burstiness-scorer`, `ai-text/ai-text-detector`, `ai-text/multi-engine-verification`                                                                                                                            |
| 5  | [`chatbot-residue-cleaner`](chatbot-residue-cleaner/SKILL.md)                 | Strip conversational chatbot wrappers ("I hope this helps", "Great question!", "As an AI language model") from text that must stand alone as prose.                                                                                          | beginner     | `humanization`, `chatbot-residue`, `prose`, `ai-text`               | `ai-text/ai-text-humanizer`, `ai-text/ai-text-detector`, `ai-text/formatting-by-rule-cleaner`, `ai-text/ai-tell-catalog`                                                                                                           |
| 6  | [`citation-hallucination-detector`](citation-hallucination-detector/SKILL.md) | Detect hallucinated citations by verifying DOIs via Crossref, paper titles via Google Scholar or publisher sites, author-journal-name matches, and "featured in regional trade publications" claims with no verifiable source.               | intermediate | `citations`, `hallucination`, `doi`, `verification`                 | `ai-text/ai-text-detector`, `ai-text/grace-degradation-protocol`, `ai-output-judgement/reference-accuracy-checker`                                                                                                                 |
| 7  | [`formatting-by-rule-cleaner`](formatting-by-rule-cleaner/SKILL.md)           | Clean formatting-by-rule tells — decorative bold, title-case headings, emojis and arrows in headings, horizontal rules between every section, curly quotation marks in plain-text or code contexts.                                          | intermediate | `humanization`, `formatting`, `prose`, `ai-text`                    | `ai-text/ai-text-humanizer`, `ai-text/ai-text-detector`, `ai-text/chatbot-residue-cleaner`, `ai-text/ai-tell-catalog`                                                                                                              |
| 8  | [`grace-degradation-protocol`](grace-degradation-protocol/SKILL.md)           | When a factual claim cannot be verified from the source text, either silently omit the claim or insert a `[Verify Source]` placeholder — never fabricate.                                                                                    | intermediate | `humanization`, `hallucination-prevention`, `citations`, `fallback` | `ai-text/ai-text-humanizer`, `ai-text/inflation-stripper`, `ai-text/citation-hallucination-detector`, `style-integrity/zero-fabrication-guard`                                                                                     |
| 9  | [`inflation-stripper`](inflation-stripper/SKILL.md)                           | Remove inflated-significance phrasing ("stands as a testament", "marking a pivotal moment", "left an indelible mark", "broader landscape") and replace with concrete facts drawn from the source.                                            | intermediate | `humanization`, `inflation`, `prose`, `ai-text`                     | `ai-text/ai-text-humanizer`, `ai-text/ai-text-detector`, `ai-text/grace-degradation-protocol`, `ai-text/ai-tell-catalog`                                                                                                           |
| 10 | [`multi-engine-verification`](multi-engine-verification/SKILL.md)             | Run text through two or more external AI-detection engines (GPTZero, Originality.ai, Turnitin AI detection, OpenAI's retired classifier — note OpenAI retired theirs in 2023) and cross-reference their verdicts.                            | intermediate | `ai-detection`, `multi-engine`, `triangulation`, `verification`     | `ai-text/ai-text-detector`, `ai-text/perplexity-burstiness-scorer`, `ai-text/ai-watermark-detector`                                                                                                                                |
| 11 | [`perplexity-burstiness-scorer`](perplexity-burstiness-scorer/SKILL.md)       | Compute statistical measures of how predictable and how uniform a text is, using per-token log-probabilities from a small language model and the coefficient of variation of sentence lengths.                                               | advanced     | `perplexity`, `burstiness`, `statistics`, `ai-detection`            | `ai-text/ai-text-detector`, `ai-text/ai-text-humanizer`, `ai-text/ai-watermark-detector`                                                                                                                                           |
| 12 | [`rhythm-by-rule-fixer`](rhythm-by-rule-fixer/SKILL.md)                       | Fix rhythm-by-rule tells — forced triads, repeated sentence openings, em-dashes used as universal connectors, stacked qualifiers, predicative hyphenated pairs, passive voice with missing actors, uniform sentence length.                  | intermediate | `humanization`, `rhythm`, `prose`, `ai-text`                        | `ai-text/ai-text-humanizer`, `ai-text/ai-text-detector`, `ai-text/ai-tell-catalog`                                                                                                                                                 |
| 13 | [`severity-classifier`](severity-classifier/SKILL.md)                         | Classify detected AI tells into four severity levels (S1 weak, S2 moderate, S3 strong, S4 critical) using specificity and how rarely the pattern occurs in human writing.                                                                    | intermediate | `severity`, `classification`, `tells`, `ai-detection`               | `ai-text/ai-text-detector`, `ai-text/ai-tell-catalog`                                                                                                                                                                              |
| 14 | [`staging-tell-remover`](staging-tell-remover/SKILL.md)                       | Remove staging tells that signal importance instead of adding a fact — "Not X but Y" constructions, one-line closers, sayings that sound deep, staged run-ups, and arguing with no one.                                                      | intermediate | `humanization`, `staging`, `rewriting`, `ai-text`                   | `ai-text/ai-text-humanizer`, `ai-text/ai-text-detector`, `ai-text/inflation-stripper`, `ai-text/ai-tell-catalog`                                                                                                                   |
| 15 | [`voice-profile-matcher`](voice-profile-matcher/SKILL.md)                     | Extract an author's voice profile (vocabulary distribution, sentence-length distribution, rhetorical patterns, idiosyncratic phrases) from a writing sample and use it to override generic AI-tell rules during humanization.                | advanced     | `voice-profiling`, `humanization`, `style`, `ai-text`               | `ai-text/ai-text-humanizer`, `ai-text/ai-text-detector`                                                                                                                                                                            |

## Difficulty Breakdown

Across **15** skills in this theme, the difficulty distribution is:

- **Beginner** — 2 skill(s)
- **Intermediate** — 9 skill(s)
- **Advanced** — 4 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`ai-text` (9), `humanization` (8), `ai-detection` (4), `prose` (4), `burstiness` (2), `citations` (2), `perplexity` (2),
`rewriting` (2), `tells` (2), `verification` (2), `ai-tells` (1), `catalog` (1), `chatbot-residue` (1),
`classification` (1), `doi` (1), `fallback` (1), `formatting` (1), `green-list` (1), `hallucination` (1),
`hallucination-prevention` (1), `inflation` (1), `multi-engine` (1), `reference` (1), `rhythm` (1), `severity` (1),
`staging` (1), `statistical-detection` (1), `statistics` (1), `style` (1), `triangulation` (1), `voice` (1),
`voice-profiling` (1), `watermark` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`ai-text-detector` → `severity-classifier` → `ai-tell-catalog` → `ai-text-humanizer` →
  `grace-degradation-protocol` → `multi-engine-verification`** — Detect → classify → catalog → humanize → degrade →
  re-verify.
- **`ai-text-detector` → `citation-hallucination-detector` → `ai-watermark-detector` → `perplexity-burstiness-scorer` →
  `multi-engine-verification`** — Multi-signal detection suite.
- **`ai-text-humanizer` → `chatbot-residue-cleaner` → `inflation-stripper` → `staging-tell-remover` →
  `rhythm-by-rule-fixer` → `formatting-by-rule-cleaner`** — Humanizer sub-skills in sequence.
- **`voice-profile-matcher` → `ai-text-humanizer` → `multi-engine-verification`** — Match voice → humanize → verify.

## Cross-Theme Connections

Skills in `ai-text/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../ai-output-judgement/` — 1 related pointer(s)
- `../style-integrity/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../ai-output-judgement/README.md`](ai-output-judgement/README.md) — detection verdicts trigger factuality and
  hallucination audits.
- [`../writing-citation/README.md`](writing-citation/README.md) — humanized prose flows through tense and cohesion
  fixers.
- [`../style-integrity/README.md`](style-integrity/README.md) — zero-fabrication guard backstops every humanization
  pass.
- [`../academic-research/README.md`](academic-research/README.md) — manuscripts and theses are scanned for AI tells.

## Back to Master

← [Back to SkillStack README](../README.md)
