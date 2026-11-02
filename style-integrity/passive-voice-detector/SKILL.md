---
name: passive-voice-detector
description: Detect passive-voice constructions in prose ("is done", "was performed", "are preserved automatically") and rewrite them as active-voice sentences with a clear subject. Use when tightening academic or technical prose, reducing word count, or matching journals that prefer active voice.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [passive-voice, active-voice, prose, editing, grammar]
related: [style-integrity/academic-prose-polisher, style-integrity/meta-commentary-stripper, style-integrity/banned-vocabulary-filter]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 830
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Passive Voice Detector

## When To Use
- A manuscript reads with excessive passive constructions that obscure agency.
- A reviewer or copy editor requests active voice.
- Word count must be reduced without losing information.
- A README or technical guide sounds bureaucratic ("files are saved automatically").

## Workflow
1. Tokenize the manuscript into sentences.
2. For each sentence, apply the detection patterns (see Key Rules).
3. For each match, identify the implied or explicit agent (subject).
4. Rewrite the sentence in active voice: `Agent + verb + object`. If the agent is unclear, decide whether to introduce a generic subject ("the system", "we", "you") or to flag the sentence for author review.
5. Preserve technical accuracy. Do not invent agents that imply false attribution.
6. Re-read each rewritten sentence for tense, agreement, and register.
7. Log each transformation in a change report: original, rewrite, agent introduced.
8. Re-scan to confirm passive density is below the target threshold (default: < 15% of sentences).

## Inputs
- Manuscript source text (LaTeX, Markdown, or plain text).
- Optional target passive-voice threshold (default 15%).
- Optional allow-list of acceptable passive constructions (e.g., "was discovered by" in historical narrative).

## Outputs
- Revised prose with passive constructions rewritten in active voice.
- A change report: line, original, rewrite, agent introduced.
- A passive-density statistic per section.

## Key Rules
- Detection pattern (regex-style):
  - `\b(is|are|was|were|be|been|being)\s+(\w+ed|(\w+en))\b` — auxiliary + past participle.
  - `\b(is|are|was|were)\s+\w+\s+by\b` — explicit "by" agent.
  - `\b(it|this|that)\s+(is|was)\s+\w+ed\b` — dummy subject passive.
- Every detected passive is either rewritten or flagged for author review.
- If no agent can be inferred, introduce a generic subject that is technically accurate (e.g., "the system", "the library") rather than fabricating a researcher's action.
- Preserve tense and aspect in the rewrite.
- Technical accuracy overrides stylistic preference: do not rewrite a passive that would distort attribution.
- Method-section passive ("the network was trained for 100 epochs") is permitted when the agent is the authors collectively and active voice would inflate the use of "we".

## Examples

Before:
```
The model is trained on ImageNet. Results are reported in Table 2.
It was observed that accuracy is improved by 3%. The configuration
file is read automatically.
```

After:
```
We trained the model on ImageNet. Table 2 reports the results. The
system improved accuracy by 3%. You do not need a configuration file;
the system preserves the results automatically.
```

Detection pattern matches (excerpt):
```
"is trained"           → "We trained"            (agent: we, the authors)
"are reported"          → "Table 2 reports"       (agent: Table 2)
"It was observed that"  → "" (delete dummy subject) (agent: the system)
"is improved by 3%"    → "improved accuracy by 3%" (agent: the system)
"is read automatically" → "the system preserves the results automatically"
```

Allow-list exception (kept as-is):
```
"The drug was discovered by Smith et al. (1982)."
```
This passive preserves historical attribution and is not rewritten.

## References
- Strunk & White, *The Elements of Style*, on active voice.
- Williams & Bizup, *Style: Lessons in Clarity and Grace*.
- The `passive` checker module from the `write-good` linter: https://github.com/btford/write-good
