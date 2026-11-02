---
name: voice-profile-matcher
description: Extract an author's voice profile (vocabulary distribution, sentence-length distribution, rhetorical patterns, idiosyncratic phrases) from a writing sample and use it to override generic AI-tell rules during humanization. Use when humanizing text attributed to a specific author whose voice must survive the rewrite.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [voice-profiling, humanization, style, ai-text]
related: [ai-text/ai-text-humanizer, ai-text/ai-text-detector]
prerequisites: []
outputs: [markdown, json]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Voice Profile Matcher

## When To Use

- `ai-text-humanizer` is about to rewrite text attributed to a known author.
- You need to preserve an author's recognizable voice while removing AI tells.
- A reviewer complains that humanized output "doesn't sound like the author".
- You are auditing whether a passage plausibly matches an author's prior work.
- You want to keep genuine author quirks (dated slang, mixed feelings, self-corrections) that mimic AI tells.

## Workflow

1. Collect at least 1,000 words of confirmed-human writing by the target author (more is better).
2. Extract the voice profile:
    - Vocabulary distribution: top 50 content words, signature verbs, avoided words.
    - Sentence-length distribution: mean, median, standard deviation, skew.
    - Punctuation habits: em-dash frequency, semicolon use, parenthetical frequency.
    - Rhetorical patterns: does the author open with anecdote? Define terms first? Use questions?
    - Idiosyncratic phrases: any repeated turns of phrase, dated slang, regional markers.
    - Self-correction / mixed-feeling markers: "or rather", "well, almost", "I keep coming back to".
3. Store the profile as a structured object so it can be reused across runs.
4. During humanization, before applying a generic tell fix, check whether the tell pattern falls within the author's
   normal range.
    - If the author's em-dash frequency is ≥3× the population baseline, an em-dash is not an AI tell for this author —
      keep it.
    - If the author genuinely opens with "Look," keep it.
5. Keep idiosyncratic detail: unusual references, mixed feelings, dated slang, genuine asides and self-corrections, even
   when they superficially resemble AI tells.
6. Remove only tells that fall outside the author's profile. A "delve" is never a voice match unless the author's sample
   uses it ≥2× per 1,000 words.
7. After the rewrite, score the output against the profile (sentence-length z-score, vocabulary overlap, punctuation
   match). Aim for a profile match ≥ 0.8.
8. Emit a voice-match report alongside the rewritten text.

## Inputs

- A confirmed-human writing sample by the target author (≥1,000 words).
- The text to humanize (and optionally, the detection evidence).
- Optional: prior voice profile (re-use across sessions).

## Outputs

- The voice profile object (vocabulary, sentence-length stats, punctuation, rhetorical patterns, idiosyncrasies).
- The humanized text.
- A voice-match report: profile-overlap score, deviations, tells kept vs. removed with justification.
- An explicit list of "kept despite tell-match" with the author baseline that justified keeping.

## Key Rules

- Voice overrides generic rules. If the author does it, keep it — even if it superficially matches an AI tell.
- 1,000 words is the minimum sample. Below that, mark the profile as low-confidence.
- Dated slang, regional markers, mixed feelings, self-corrections, and genuine asides are almost always voice — preserve
  them.
- A profile is per-author, not per-genre. Do not borrow one author's profile for another.
- If a tell cannot be confirmed as in-author-voice, fall back to the generic fix.
- Voice overrides can downgrade severity by at most one level and never below S2 (see `severity-classifier`).
- Keep the voice-match report so reviewers can see why a tell was preserved.

## Examples

**Voice profile (excerpt):**

```
Author: J. M. (essayist)
Sentence length: mean 22.3 words, σ 14.1 (high burstiness — keep variation)
Em-dash frequency: 4.2 per 1,000 words (baseline 1.1) → keep em-dashes
Signature verbs: "skewers", "circles back to", "lands on"
Idiosyncrasy: opens paragraphs with "Look," or "Here's the thing —"
Avoids: "moreover", "furthermore", "in conclusion"
```

**Humanization with voice override:**

```
Original AI-flavored draft:
"In conclusion, the policy underscores the importance of robust frameworks,
ultimately leaving an indelible mark on the broader landscape of regulation."

Humanized (with voice):
"Here's the thing — the policy lands on one idea: frameworks matter. The
rest of the regulation circles back to that, more or less, every time.

[Voice-match report]
Kept: em-dash (author baseline 4.2/1k), opening "Here's the thing —"
Removed: "in conclusion" (author avoids it), "indelible mark" (inflation tell)
Profile overlap: 0.87 (acceptable)
```

**Voice-preservation case (mixed feelings):**

```
Original (mimics a tell but is genuine voice):
"Or rather — and I keep coming back to this — the framework matters less
than the people inside it."

Verdict: keep verbatim. The mixed-feeling marker ("or rather", "I keep
coming back to this") is idiosyncratic voice, not an AI tell.
```

## References

- Companion skills: `ai-text-humanizer`, `ai-tell-catalogue`, `severity-classifier`.
- Authorship attribution background: Grieve, J. (2007). "Quantitative authorship attribution: A history and evaluation
  of methods."
- Stamatatos, E. (2009). "A survey of modern authorship attribution methods." *JASIST* 60(3).
