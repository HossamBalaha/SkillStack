---
name: ai-tell-catalogue
description: Reference catalogue of 26 AI tells organized into six categories, each with a name, what to watch for, why it is a problem, and a before/after pair. Use this as the lookup table when running `ai-text-detector` or `ai-text-humanizer`; do not invent new tells on the fly.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [reference, ai-tells, catalogue, ai-text]
related: [ai-text/ai-text-detector, ai-text/ai-text-humanizer, ai-text/severity-classifier]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: en
---

# AI Tell Catalogue

## When To Use

- `ai-text-detector` needs to confirm whether a flagged phrase matches a known tell.
- `ai-text-humanizer` needs the canonical fix for a given tell.
- A reviewer asks "what are the known patterns?" and wants a single source of truth.
- You want to extend detection to a new domain and need to know which tells already exist.

## Workflow

1. Receive a candidate phrase or pattern from the detector or humanizer.
2. Look up the phrase against the catalogue, scanning each of the six categories.
3. If matched, return the tell's canonical name, severity, and the recommended fix.
4. If not matched, do NOT invent a new tell ad hoc. Return `unknown-tell` and let the caller treat it as S1 at most.
5. When extending the catalogue (rare), add the tell through a versioned update to this file, with before/after examples
   you have written yourself.

## Inputs

- A phrase, sentence, or structural pattern suspected of being an AI tell.
- Optional: which category to search first (lexical, structural, thematic, tonal, statistical, citation).

## Outputs

- The matched tell's canonical record: name, category, what to watch for, why it is a problem, before, after, default
  severity.
- Or `unknown-tell` if no match.

## Key Rules

- This catalogue is the single source of truth. Detector and humanizer MUST consult it; they do not invent tells.
- 26 tells total: 5 staging, 7 rhythm-by-rule, 5 inflation, 4 formatting-by-rule, 4 leftovers, 1 wrong-reader.
- Severity labels in this catalogue are defaults; `severity-classifier` may upgrade or downgrade based on context.
- Before/after examples here are illustrative, not prescriptive. The humanizer may produce different fixes if voice
  demands it.
- Never copy catalogue text verbatim into user-facing output. Use paraphrase.
- Adding a new tell requires a version bump (e.g. 1.0 → 1.1).

## The 26 Tells

### Staging (5)

1. **Not X but Y** — "It's not merely a report, it's a manifesto." Signalling importance instead of stating a fact.
   *After:* "The report doubles as a manifesto."
2. **One-line closers** — "And that is the real win." / "That's the heart of it." Delete; the prior sentence already
   carries the point.
3. **Sayings that sound deep** — "Symmetry is the language of trust." Replace with a concrete claim: "Symmetric layouts
   feel more predictable to readers."
4. **Staged run-ups** — "Let's dive in.", "Here's what you need to know." Delete.
5. **Arguing with no one** — "A tempting approach would be to X, but Y." State the choice: "We chose Y because Z."

### Rhythm-by-rule (7)

6. **Forced triads** — "fast, reliable, and scalable." Replace with the actual items, even if there are two or four.
7. **Repeated sentence openings** — three sentences starting with "The". Vary them.
8. **Em-dash as universal connector** — "X — Y — Z." Replace with commas, colons, or periods as appropriate.
9. **Stacked qualifiers** — "could potentially possibly lead to". Collapse: "may lead to".
10. **Hyphenated pairs after the noun** — "a solution, high-quality," when predicative. Use "high quality".
11. **Passive voice with missing actor** — "Mistakes were made." Restore the actor or rewrite.
12. **Uniform sentence length** — every sentence 16-19 words. Vary length; allow a 4-word sentence next to a 30-word
    one.

### Inflation (5)

13. **Overused lexical choices** — delve, tapestry, underscore, pivotal, seamless, navigate, robust. Replace with
    concrete verbs.
14. **Inflated significance** — "marks a pivotal moment", "leaves an indelible mark", "stands as a testament". Replace
    with the actual fact.
15. **Vague connections** — "in the broader landscape of", "within the realm of". Delete or specify.
16. **"-ing" riders** — "X, paving the way for Y." Cut the rider or make it a separate sentence.
17. **Sales language / borrowed authority** — "trusted by", "industry-leading", "as experts note". Remove or source it.

### Formatting-by-rule (4)

18. **Bold as decoration** — bolding words for emphasis inside flowing prose. Remove unless structural.
19. **Title-case or decorated headings** — "The Future Of Caching". Use sentence case: "The future of caching".
20. **Emojis / arrows in headings** — "🚀 Performance →". Strip decorations.
21. **Curly quotes in plain text/code** — "smart quotes" inside code blocks or plain text. Use straight quotes.

### Leftovers (4)

22. **Chatbot residue** — "I hope this helps", "Let me know if you'd like me to expand". Delete (see
    `chatbot-residue-cleaner`).
23. **Knowledge-limit disclaimers** — "As an AI language model", "As of my last update". Delete.
24. **Heading repeated in first sentence** — "## Conclusion. In conclusion, …" Cut the repetition.
25. **Writing about the document** — "This section explores", "We will examine". Get to the content.

### Wrong-reader (1)

26. **Wrong-reader addressing** — "Whether you're a beginner or a seasoned pro" in technical writing. Address the actual
    reader.

## Examples

**Lookup request:**

```
Phrase: "leaves an indelible mark on the field"
```

**Catalogue response:**

```
Tell #14: Inflated significance
Category: inflation
Watch for: phrases that inflate the importance of an event beyond the cited facts.
Why it's a problem: signals significance rather than stating it; classic LLM tic.
Before: The 2023 paper leaves an indelible mark on the field.
After:  The 2023 paper introduced a 38% latency reduction in federated test clusters.
Default severity: S2
```

## References

- Companion skills: `ai-text-detector`, `ai-text-humanizer`, `severity-classifier`, `chatbot-residue-cleaner`,
  `inflation-stripper`, `staging-tell-remover`, `rhythm-by-rule-fixer`, `formatting-by-rule-cleaner`.
- Principles paraphrased from widely documented observations on AI-generated prose; no external text reproduced.
