---
name: reading-level-adjuster
description: Adjusts the reading level of academic prose to a target grade using Flesch-Kincaid Grade Level, Gunning Fog Index, and SMOG metrics, by simplifying long sentences, reducing jargon, and defining abbreviations. Use when producing lay summaries, press releases, patient-facing consent forms, or broader-impacts sections in grant proposals.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: writing-citation
tags: [reading-level, flesch-kincaid, gunning-fog, smog, lay-summary]
related: [writing-citation/english-academic-editor, writing-citation/structured-abstract-writer]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 900
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: en
---

# Reading Level Adjuster

## When To Use
- A grant proposal requires a broader-impacts section readable by non-specialists.
- A patient-facing consent form must score at grade 8 or below.
- A press release summarizing a paper must be accessible to a general audience.
- A reviewer says the methods section is "too dense" for the target audience.

## Workflow
1. Compute baseline readability metrics on the source text: Flesch-Kincaid Grade Level, Gunning Fog Index, SMOG.
2. Determine the target grade from the venue (academic paper: 12-16; lay summary: 8-10; patient-facing: ≤ 8; press release: 10-12).
3. Identify the levers available: sentence length (target ≤ 20 words), word length (multi-syllable), jargon density, passive-voice frequency, and undefined abbreviations.
4. Split long sentences at natural breaks; preserve meaning and citation anchors.
5. Replace jargon with plain-language equivalents where the technical term is not load-bearing; when it is load-bearing, define it inline on first use.
6. Spell out every abbreviation on first use; consider dropping abbreviations entirely for lay audiences.
7. Convert passive voice to active where agency is clear ("the model was trained" → "we trained the model") only if the style guide permits first person.
8. Re-compute readability; iterate until the target grade is met or the simplification begins to distort meaning.
9. Emit the adjusted text plus a before/after metric table.

## Inputs
- The source text (Markdown, LaTeX, or plain text).
- Target grade (or venue category: lay / patient / press / academic).
- Style guide constraints (e.g., journal prohibits first person; consent form must avoid "you" in some legal contexts).

## Outputs
- `adjusted_text.md` — the simplified prose.
- `readability_metrics.csv` — metric, source value, target value, adjusted value.
- `glossary.md` — list of jargon terms replaced or defined inline.
- `simplification_log.md` — list of sentences split, with before/after.

## Key Rules
- Never distort meaning to meet a readability target — if a sentence cannot be simplified without changing meaning, leave it and flag it.
- Every abbreviation must be spelled out on first use.
- Technical terms that are load-bearing must be defined inline, not deleted.
- Sentence length should average ≤ 20 words; long sentences (> 30 words) are candidates for splitting.
- Passive voice is acceptable in Methods where agency is irrelevant (e.g., "samples were stored at -80°C"); do not force active voice there.
- Citations and effect sizes (numbers, CIs) must be preserved verbatim during simplification.

## Examples
```text
Before (grade 17, Gunning Fog):
"The investigators leveraged a multi-tiered convolutional architecture
to ameliorate the deleterious effects of distributional heterogeneity
on federated convergence dynamics."

Metrics: Flesch-Kincaid 17.2 | Gunning Fog 19.4 | SMOG 16.8

After (lay summary, grade 10):
"The research team used a step-by-step neural network design to reduce
the problems that arise when devices in a federated learning system
have very different data."

Metrics: Flesch-Kincaid 10.1 | Gunning Fog 11.8 | SMOG 10.4

Glossary entry:
  "convolutional architecture" → "step-by-step neural network design"
  (plain-language equivalent; technical term defined inline elsewhere)
```

```text
Consent form fix (target grade ≤ 8):
Before: "Your participation is contingent upon the provision of
informed consent, which must be executed prior to the commencement of
the study protocol." (grade 14)

After: "You must sign a consent form before the study begins." (grade 6)
```

## References
- Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, 32(3), 221-233.
- Gunning, R. (1952). *The Technique of Clear Writing*. McGraw-Hill.
- McLaughlin, G. H. (1969). SMOG grading — a new readability formula. *Journal of Reading*, 12(8), 639-646.
- NIH Plain Language guidelines: https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/clear-communication/plain-language.
