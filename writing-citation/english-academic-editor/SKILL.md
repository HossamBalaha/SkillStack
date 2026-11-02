---
name: english-academic-editor
description: Edits non-native English academic prose to improve article usage, tense consistency, register, and hedging, while preserving the author's meaning. Use when polishing a manuscript by a non-native English speaker before journal submission, or when a reviewer has flagged language issues.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [editing, english, academic, grammar, tense]
related: [writing-citation/tense-consistency-fixer, writing-citation/hedging-language-balancer, writing-citation/cohesive-device-checker]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# English Academic Editor

## When To Use
- A non-native English author has asked for a language polish before submission.
- A reviewer comment says "the English needs improvement" without specifics.
- The draft shows inconsistent articles (a/an/the), tense drift, or informal register.
- A bilingual author wants a parallel glossary of technical terms in English and their L1.

## Workflow
1. Read the full draft once for comprehension; note the author's apparent L1 from recurring error patterns.
2. Fix article usage: "the" for specific/known referents; "a/an" for first-mention countable nouns; zero article for generics where idiomatic.
3. Unify tense: past for completed methods/results, present for established facts and statements about the paper itself, present perfect for prior work leading to the current study.
4. Adjust register: replace informal verbs ("get," "show," "find out") with formal equivalents ("obtain," "demonstrate," "ascertain"); remove contractions and colloquialisms.
5. Balance hedging: insert "may," "might," "could," "arguably," "potentially" where claims outrun the evidence; remove excess hedging that weakens well-supported claims.
6. Build a bilingual term glossary mapping each technical term to the author's L1 equivalent (if identifiable).
7. Track every change in a diff view; produce a clean version and a change-log with rationale.

## Inputs
- The manuscript file (DOCX, LaTeX, or Markdown).
- Author's native language (optional, but improves glossary and L1-typified fixes).
- Target journal style guide (American vs. British English, Oxford comma preference).

## Outputs
- `manuscript_edited.md` — polished version with track-changes preserved.
- `change_log.md` — list of edits categorized by type (articles, tense, register, hedging).
- `glossary_bilingual.csv` — English term ↔ L1 term ↔ short definition.

## Key Rules
- Preserve the author's meaning and voice; do not rewrite for style alone.
- Do not introduce factual claims or citations the author did not make.
- American and British English must not be mixed within a single manuscript.
- Hedging changes must reflect evidence strength, not authorial timidity.
- All changes must be auditable — never silently alter technical content.
- Contractions, slang, and second-person address ("you") are out of scope for formal academic prose.

## Examples
```text
Before:
"The experiment was showed interesting result. We get the data from 30
participant and analyze it. It is maybe because of the temperature.
This findings is very important."

After:
"The experiment produced notable results. We obtained data from 30
participants and analyzed them. This outcome may be attributable to
temperature variation. These findings are significant."
```

```text
Glossary excerpt (English ↔ Spanish):
  outcome         | resultado       | measured effect of an intervention
  attributable to | atribuible a    | traceable to a cause
  significant     | significativo  | statistically meaningful (p < 0.05)
```

## Common Pitfalls
- Over-correcting articles by inserting "the" before every generic noun — this is wrong for generics ("Patience is a virtue").
- Forcing past tense into the Discussion when interpreting a general truth (should be present).
- Removing all hedging to "sound more confident" — this overclaims low-evidence results.
- Mixing American and British spelling ("-ize" vs. "-ise") within the same manuscript.
- Treating contractions as the only register defect — colloquial verbs ("get," "find out") matter equally.
- Inventing L1 glossary entries where the author's L1 is unknown — leave the L1 column blank instead.

## References
- Hyland, K. (2005). Metadiscourse: Exploring Interaction in Writing. Continuum.
- Hedging techniques in academic writing: https://www.ref-n-write.com/blog/hedging-techniques-in-academic-writing-with-examples.
- Swales, J. M., & Feak, C. B. *Academic Writing for Graduate Students*. University of Michigan Press.
- Caplan, N. A. (2019). *Grammar Choices for Graduate and Professional Writers*. University of Michigan Press.
- Chicago Manual of Style, 17th ed., sections on article usage and tense in scholarly prose.
- Pinker, S. (2014). *The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century*. Viking.
- ISO 690:2021 — Information and documentation — Guidelines for bibliographic references and citations to information resources.
