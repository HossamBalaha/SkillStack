---
name: rhythm-by-rule-fixer
description: Fix rhythm-by-rule tells — forced triads, repeated sentence openings, em-dashes used as universal connectors, stacked qualifiers, predicative hyphenated pairs, passive voice with missing actors, uniform sentence length. Use when `ai-text-detector` flags rhythm-category tells, or when prose has a mechanical, metronomic feel.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [humanization, rhythm, prose, ai-text]
related: [ai-text/ai-text-humanizer, ai-text/ai-text-detector, ai-text/ai-tell-catalogue]
prerequisites: [ai-text/ai-tell-catalogue]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Rhythm-by-Rule Fixer

## When To Use

- `ai-text-detector` flagged rhythm-by-rule tells (catalogue #6-#12).
- A passage reads in a metronomic, evenly-paced rhythm that suggests machine generation.
- Every sentence begins with "The" or "This".
- Em-dashes appear in nearly every sentence as the default connector.
- A draft stacks qualifiers ("could potentially possibly") or uses uniform sentence length.
- You want to restore natural burstiness without changing meaning.

## Workflow

1. Identify rhythm tells using the catalogue (#6-#12).
2. For each tell, apply the canonical fix:
    - **Forced triads**: replace 3-item lists with the actual items, even if there are two or four. "fast, reliable, and
      scalable" → list the real properties measured.
    - **Repeated sentence openings**: vary the openings. Two consecutive sentences must not start with the same word or
      structure. Three in a row is a definite tell.
    - **Em-dash as universal connector**: replace with commas, colons, or periods. Reserve em-dashes for genuine
      interruption (and only if the author's voice profile supports them).
    - **Stacked qualifiers**: collapse to a single qualifier. "could potentially possibly lead to" → "may lead to".
    - **Predicative hyphenated pairs**: "high-quality" after a copula becomes "high quality". Attributive use ("a
      high-quality build") keeps the hyphen; predicative use ("the build is high-quality") drops it.
    - **Passive voice with missing actor**: restore the actor or rewrite actively. "Mistakes were made" → "The team made
      mistakes" or "Errors entered via the import step."
    - **Uniform sentence length**: introduce variation. Pair a 5-word sentence with a 30-word one. Aim for a coefficient
      of variation in sentence length above ~0.5 (see `perplexity-burstiness-scorer`).
3. Re-read aloud to check rhythm. If it still feels metronomic, vary openings further and break one long sentence into
   two short ones.
4. Preserve every fact, citation, name, date, and number.
5. Voice override: if the author's profile genuinely uses em-dashes (≥3× baseline), keep em-dashes; fix only the
   over-use.
6. Emit the rewritten text plus a rhythm log: `Tell | Location | Fix applied`.

## Inputs

- The text containing rhythm tells.
- Optional: sentence-length baseline from `perplexity-burstiness-scorer` to target a burstiness goal.
- Optional: voice profile (em-dash-prone authors keep some).

## Outputs

- The rewritten text with varied rhythm.
- A rhythm log: `Tell (#) | Span | Fix`.
- A sentence-length distribution before/after, if a scorer is available.

## Key Rules

- Preserve meaning. Varying rhythm must not change what the text says.
- Two consecutive sentences must not begin identically. Three is a definite tell.
- Em-dashes are not forbidden, but the universal-connector pattern is. Keep em-dashes only where they mark genuine
  interruption and the voice profile supports them.
- Forced triads become real lists. If there are two items, write two. If four, write four.
- Predicative hyphens drop; attributive hyphens stay.
- Passive voice is restored with the actor or rewritten actively.
- Stacked qualifiers collapse to one. Never substitute "could potentially" for "may".

## Examples

**Forced triad:**

```
Before: The system is fast, reliable, and scalable.
After:  The system handles 18k requests per second with a 99.97% uptime SLO,
        and horizontal scaling is automatic above 70% CPU.
```

**Repeated openings:**

```
Before: The cache invalidates on write. The cache also evicts on TTL.
        The cache logs every miss.
After:  The cache invalidates on write and evicts on TTL. Every miss is logged.
```

**Em-dash as universal connector:**

```
Before: The API — which we rebuilt in March — now handles 3× the load — and
        latency is down 40% — mostly because of the new connection pool.
After:  The API, which we rebuilt in March, now handles 3× the load. Latency is
        down 40%, mostly because of the new connection pool.
```

**Stacked qualifiers:**

```
Before: This could potentially possibly lead to wider adoption.
After:  This may lead to wider adoption.
```

**Predicative hyphenated pair:**

```
Before: The build is high-quality.
After:  The build is high quality.
```

**Passive voice with missing actor:**

```
Before: Mistakes were made during the migration.
After:  The migration step introduced three indexing errors.
```

**Uniform sentence length:**

```
Before (all 17 words):
The deployment took twelve minutes. The rollback completed in eight minutes
total. The incident report was filed the same afternoon. The postmortem is
scheduled for Friday morning.

After (varied):
The deployment took twelve minutes; the rollback, eight. We filed the incident
report that afternoon. Friday's postmortem is on the calendar.

[Rhythm log]
- Uniform length (#12) | all four sentences ~17 words | varied to 8/9/10 words; CV 0.31 → 0.58
- Passive voice (#11)  | "was filed"                  | restored actor ("We filed")
```

## References

- Companion skills: `ai-text-detector`, `ai-tell-catalogue` (tells #6-#12), `perplexity-burstiness-scorer`,
  `voice-profile-matcher`.
- Burstiness concept: Grieve, J. (2007). "Quantitative authorship attribution."
