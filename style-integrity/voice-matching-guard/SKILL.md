---
name: voice-matching-guard
description: When the user provides a writing sample, match its style exactly and override generic style rules. Use when an author's distinctive voice, idiosyncratic references, mixed feelings, dated slang, or genuine asides must be preserved even if they resemble AI tells.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [voice-matching, style, idiosyncratic, writing-sample, override]
related: [style-integrity/academic-prose-polisher, style-integrity/banned-vocabulary-filter, style-integrity/meta-commentary-stripper]
prerequisites: []
outputs: [markdown, latex]
difficulty: advanced
estimated_tokens: 870
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Voice Matching Guard

## When To Use

- The user supplies a writing sample and asks for new content "in my voice".
- An author's idiosyncratic phrasing, mixed feelings, or self-corrections must be preserved.
- Generic academic polish would erase the writer's distinctive style.
- An agent is tempted to "fix" stylistic quirks that are actually the writer's voice.

## Workflow

1. Read the user-provided writing sample end-to-end. Do not skim.
2. Catalogue the author's voice fingerprint:
    - Sentence-length rhythm (short punchy + long flowing, or uniform).
    - Vocabulary tier and preferred synonyms.
    - Rhetorical patterns (anaphora, parenthetical asides, rhetorical questions).
    - Idiosyncratic references (specific unusual citations, niche books, dated slang).
    - Stance markers (mixed feelings, self-corrections, hedging, contrarian asides).
3. Mark this fingerprint as the highest-priority style authority — it overrides every generic rule in this skill theme.
4. When generating new content, draft each sentence to match the fingerprint:
    - Reproduce the author's preferred sentence shapes.
    - Borrow the author's preferred synonyms and connectors.
    - Preserve idiosyncratic references and dated slang the author uses.
    - Keep genuine asides and self-corrections, even if they mimic AI tells.
5. Where the fingerprint conflicts with a generic rule (e.g., the author uses em-dashes deliberately), the fingerprint
   wins. Document the override.
6. After drafting, re-read against the sample to confirm the voice carries.
7. Flag any sentence that drifts toward generic "AI polish" and rewrite it back toward the fingerprint.
8. Deliver the content with a brief "Voice Notes" appendix documenting which fingerprint traits were reproduced and
   which generic rules were overridden.

## Inputs

- One or more writing samples from the target author.
- The new content brief or topic to be written.
- Optional clarification on which traits are most important to preserve.

## Outputs

- New content drafted in the author's voice.
- A "Voice Notes" appendix listing the fingerprint traits reproduced and any generic rules overridden.

## Key Rules

- The user's writing sample is the highest-priority style authority.
- Voice overrides every generic rule in the `style-integrity` theme.
- Idiosyncratic references, dated slang, mixed feelings, and genuine self-corrections are PRESERVED, even if they
  resemble AI tells.
- Generic "polish" must not flatten the author's distinct rhythm or vocabulary.
- Document overrides explicitly so the choice is auditable.
- When in doubt, prefer fidelity to the sample over conformity to generic rules.

## Examples

Sample (author's voice):

```
I keep coming back to Smith's 1987 paper — not because it's right (it
isn't, really), but because the man had the decency to admit he was
guessing. Half the field has forgotten that. The newer work, frankly,
is too clever by half.
```

New content (matching voice):

```
I keep coming back to the original transformer paper — not because
it's the last word (it isn't, not by a long shot), but because the
authors had the honesty to flag what they did not understand. Half
the field has forgotten that. The newer "efficient" variants,
frankly, are too clever by half.
```

Voice Notes (appended):

```
Voice Notes:
- Preserved: em-dash parentheticals (overrides em-dash-eliminator).
- Preserved: self-correction in parentheses ("it isn't, really").
- Preserved: dated idiom ("too clever by half").
- Preserved: first-person hedging stance ("I keep coming back to").
- Overridden: academic-prose-polisher rule on em-dashes.
- Overridden: meta-commentary-stripper on conversational asides.
```
