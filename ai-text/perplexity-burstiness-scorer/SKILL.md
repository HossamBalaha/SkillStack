---
name: perplexity-burstiness-scorer
description: Compute statistical measures of how predictable and how uniform a text is, using per-token log-probabilities from a small language model and the coefficient of variation of sentence lengths. Use when you need numeric evidence to support an `ai-text-detector` verdict or to track humanization progress.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ai-text
tags: [perplexity, burstiness, statistics, ai-detection]
related: [ai-text/ai-text-detector, ai-text/ai-text-humanizer, ai-text/ai-watermark-detector]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 1900
cost_warning: "Optional: requires a small LM for token log-probabilities; OpenAI API calls may incur costs."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: true
language: en
---

# Perplexity and Burstiness Scorer

## When To Use
- An `ai-text-detector` verdict needs numeric corroboration, not just pattern matching.
- You want a before/after metric for a `ai-text-humanizer` rewrite.
- A reviewer asks "how machine-like is this text, quantitatively?"
- You are benchmarking a corpus and need a comparable score across samples.
- You want to compare a draft against a known-human baseline by the same author.

## Workflow
1. Load or receive the input text. Confirm the encoding is plain UTF-8.
2. Choose a small reference language model (GPT-2 small is a reasonable default; ~124M parameters, runs locally).
3. Tokenize the input using the model's tokenizer.
4. For each token, compute the log-probability the model assigns to that token given the prior context.
5. Compute average negative log-likelihood per token, then exponentiate: `PPL = exp(-1/N * Σ log p(x_i | x_<i))`.
6. Sentence-split the text (spaCy or a simple regex). For each sentence compute word count and average token length.
7. Compute burstiness as the coefficient of variation of sentence lengths: `B = σ(L) / μ(L)`.
8. Optionally compute a second burstiness axis on per-sentence average log-probability variance.
9. Compare both metrics against a baseline distribution (human prose, AI prose) you maintain.
10. Classify severity: very low PPL + low B → S3; very low PPL + normal B → S2; normal PPL + low B → S1.
11. Emit a numeric scorecard with the raw values, the normalized z-scores against baseline, and a severity label.
12. If token-level probabilities reveal long runs of highly-predictable tokens, note the longest such run — long low-surprise runs are a strong AI signal.

## Inputs
- The text to score (at least 100 words for a stable estimate; 300+ preferred).
- Reference model name (default: `gpt2`).
- Optional: a human-prose baseline corpus to compute z-scores.
- Optional: per-sentence output flag.

## Outputs
- A scorecard with: token count, perplexity, burstiness (CV of sentence length), longest low-surprise run, z-scores against baseline, severity label (S1-S3).
- Optional: per-sentence table (length, log-prob, contribution to burstiness).
- A short interpretation paragraph: "Perplexity in the bottom 5% of human prose; burstiness below the 10th percentile; pattern consistent with LLM output."

## Key Rules
- Perplexity is model-relative. Always state which model computed it. Never compare PPL across models without re-baselining.
- A single short paragraph produces unstable PPL. Require a minimum sample size or mark the result as low-confidence.
- Burstiness alone is weak — pair it with perplexity. R1 (cumulative evidence) still applies.
- Do not present a numeric score as proof of authorship. These are signals, not verdicts.
- Treat the small reference model as a fixed yardstick; switching models invalidates historical comparisons.
- If the text contains code, math, or quoted material, mark those spans and exclude from sentence-length statistics.
- Long low-surprise runs (e.g. 30+ consecutive tokens with low surprise) are stronger evidence than the average PPL.

## Examples

**Scorecard output:**
```
Sample: 412 tokens, 23 sentences
Reference model: gpt2
Perplexity:           14.2   (z = -2.1 vs human baseline → 2nd percentile)
Burstiness (CV):      0.41   (z = -1.6 → 6th percentile)
Longest low-surprise run: 47 tokens
Severity: S3 (statistical)

Interpretation: Perplexity and burstiness both sit in the bottom decile of the
human-prose baseline. Combined with the 47-token low-surprise run, this is
consistent with LLM output. Pair with lexical/citation tells before concluding.
```

**Before/after (humanizer progress):**
```
Before: PPL 14.2, B 0.41, severity S3
After:  PPL 31.7, B 0.78, severity S1  → mixed, acceptable.
```

**Edge case (mixed signals):**
```
Sample: 220 tokens
Perplexity: 28.4  (z = -0.4 → 35th percentile, unremarkable)
Burstiness: 0.31  (z = -2.3 → 1st percentile, very uniform)
Longest low-surprise run: 12 tokens
Severity: S2 (statistical)

Interpretation: Perplexity is in normal range, but burstiness is in the bottom
1%. Uniform sentence length is the only red flag here. Do not conclude AI on
burstiness alone — pair with lexical and citation tells before concluding.
```

## References
- GPT-2 reference model: Radford, A. et al. (2019). "Language Models are Unsupervised Multitask Learners." OpenAI.
- Concept of burstiness in authorship attribution: Grieve, J. (2007). "Quantitative authorship attribution: A history and evaluation of methods."
- Weber-Wulff et al. (2023) caution that statistical scores alone misclassify at non-trivial rates — combine with manual tell analysis.
