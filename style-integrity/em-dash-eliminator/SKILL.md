---
name: em-dash-eliminator
description: Find em-dashes (`—`) and en-dashes used as parenthetical separators in academic prose and replace them with commas, parentheses, or en-dashes for numerical ranges. Use when finalizing manuscript prose, enforcing a no-em-dash style rule, or normalizing dash usage across a document.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: style-integrity
tags: [em-dash, en-dash, punctuation, prose, typography]
related: [style-integrity/academic-prose-polisher, style-integrity/banned-vocabulary-filter, style-integrity/numerical-value-formatter]
prerequisites: []
outputs: [markdown, latex]
difficulty: beginner
estimated_tokens: 850
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Em-Dash Eliminator

## When To Use
- A manuscript uses em-dashes (`—`) as parenthetical separators in body prose.
- A style guide forbids `---` or `—` in academic text.
- En-dashes are misused as parenthetical separators rather than numerical-range indicators.
- A pre-submission pass must normalize all dash characters.

## Workflow
1. Scan the manuscript for em-dash characters: `—` (U+2014) and the LaTeX macro `---`.
2. Scan for en-dash characters: `–` (U+2013) and the LaTeX macro `--`.
3. Classify each dash by function:
   - Parenthetical separator (the typical em-dash use): rewrite as a comma or parenthesis pair.
   - Numerical range (e.g., "10–20"): rewrite as `10--20` (LaTeX en-dash) WITHOUT surrounding spaces.
   - Compound modifier (e.g., "non–linear"): rewrite with a hyphen `-`.
4. For each parenthetical em-dash, decide between a comma (mild interruption) or parentheses (stronger interruption).
5. Apply the substitution.
6. Re-scan to confirm no em-dash and no `---` remain.
7. Verify en-dashes appear ONLY in numerical ranges, with no surrounding spaces.
8. Produce a change report: location, original character, replacement, function classification.

## Inputs
- Manuscript source text (LaTeX, Markdown, or plain text).
- Optional style preference (commas preferred vs. parentheses preferred for interruptions).

## Outputs
- Revised manuscript with no em-dashes and no `---`.
- En-dashes (`--` in LaTeX) used only for numerical ranges without surrounding spaces.
- A change report listing each substitution and its function classification.

## Key Rules
- Em-dash (`—`, U+2014) is forbidden in body prose.
- The LaTeX macro `---` is forbidden in body prose.
- En-dash (`–`, U+2013, or `--` in LaTeX) is permitted ONLY for numerical ranges: `10--20`, `pp.~5--12`.
- En-dashes used for numerical ranges have NO surrounding spaces.
- Parenthetical separators are rewritten as commas or parentheses, never as dashes.
- Compound modifiers use the ASCII hyphen `-`, not an en-dash.

## Replacement Map (sed-style)

| Pattern | Replacement | Function |
|---------|-------------|----------|
| `---` | `,` or `(` `)` | Parenthetical separator (LaTeX em-dash macro) |
| `—` | `,` or `(` `)` | Parenthetical separator (Unicode em-dash) |
| `(\d+)\s*--\s*(\d+)` | `\1--\2` | Numerical range (strip surrounding spaces) |
| `(\d+)\s*–\s*(\d+)` | `\1--\2` | Numerical range (Unicode en-dash → LaTeX) |
| `(\w+)\s*–\s*(\w+)` | `\1-\2` | Compound modifier (en-dash → hyphen) |

## Examples

Before:
```
The proposed method—unlike prior work—handles edge cases. We evaluate
on datasets ranging from 10–20 thousand samples. The non–linear
activation improves results.
```

After:
```
The proposed method, unlike prior work, handles edge cases. We
evaluate on datasets ranging from 10--20 thousand samples. The
non-linear activation improves results.
```

Change report:
```
Line 1:  "---" (em-dash macro equivalent) → "," (parenthetical separator).
Line 1:  "—" → "," (parenthetical separator).
Line 2:  "10 – 20" → "10--20" (numerical range, no surrounding spaces).
Line 3:  "non–linear" → "non-linear" (compound modifier → ASCII hyphen).
```

## References
- Chicago Manual of Style, sections on dashes.
- The TeX FAQ on dashes: https://texfaq.org/FAQ-dashes
- `typogr` and `smartypants` libraries for dash normalization.
