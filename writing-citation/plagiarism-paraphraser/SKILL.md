---
name: plagiarism-paraphraser
description: Rewrites source text to reduce similarity scores below 15% on iThenticate/Turnitin while preserving meaning, structural integrity, and technical vocabulary. Use when a draft flags high similarity on a plagiarism checker, or when incorporating source material without falling into patchwriting.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [paraphrase, plagiarism, similarity, ithenticate, patchwriting]
related: [writing-citation/english-academic-editor, writing-citation/cohesive-device-checker]
prerequisites: []
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Plagiarism Paraphraser

## When To Use
- A similarity report flags passages over 15% with a single source.
- You need to incorporate dense technical source material without quoting it directly.
- A reviewer suspects patchwriting (synonym-swapping that retains original sentence structure).
- A grant or thesis office requires a sub-threshold iThenticate score before submission.

## Workflow
1. Read the flagged passage and its source side-by-side; identify the core claim and any technical terms that must be preserved verbatim.
2. Decide whether paraphrase is even appropriate — direct quotation is preferred for definitions, laws, or verbatim policy language.
3. Reorganize structure: change sentence order, merge adjacent sentences, or split long sentences.
4. Substitute non-technical vocabulary; preserve domain terms, species names, model names, and unit abbreviations.
5. Switch voice (active ↔ passive) only when it does not distort agency.
6. Add or strengthen the in-text citation crediting the original source.
7. Re-read to confirm the paraphrase preserves meaning, scope, and stance of the original.
8. Estimate similarity against the source using n-gram overlap; iterate until overlap falls below 15%.
9. Never invent citations to lend authority to the paraphrase.

## Inputs
- The flagged text passage and its matching source.
- The intended in-text citation (author, year).
- A list of technical terms that must be preserved.

## Outputs
- `paraphrased.md` — the rewritten passage with citation in place.
- `similarity_report.md` — estimated overlap with source before and after paraphrasing.
- `preserved_terms.txt` — list of technical terms kept verbatim, with rationale.

## Key Rules
- Never fabricate citations — if the paraphrase needs support, mark `[CITATION NEEDED]`.
- Preserve technical terms, proper nouns, units, and species names verbatim.
- Patchwriting (synonym-swap only) is not acceptable paraphrase — the structure must change.
- Meaning must be preserved; do not soften or strengthen claims during paraphrase.
- Direct quotations over 40 words must be set as block quotes with page number citation.
- A paraphrase without a citation is still plagiarism.

## Examples
```text
Source (Smith et al., 2022):
"The rapid expansion of urban green spaces has been linked to measurable
reductions in ambient summer temperatures, particularly in dense
residential neighborhoods where canopy cover exceeds 20 percent."

Before (patchwrite, 38% similarity):
"The fast growth of city green spaces is connected to measurable drops in
summer air temperatures, especially in dense housing areas where tree cover
is more than 20 percent."

After (paraphrase, <10% similarity):
"Smith et al. (2022) observe that urban green-space expansion cools summer
air temperatures most visibly in densely built residential blocks once tree
canopy exceeds 20% — an effect attributable to evapotranspiration and
shading rather than albedo change."
```

```text
Preserved terms log:
  - "green spaces" (domain term, kept)
  - "canopy cover" (technical term, kept)
  - "20 percent" -> "20%" (unit-equivalent, allowed)
```

## Common Pitfalls
- Swapping synonyms without restructuring — patchwriting still trips similarity checkers and is still plagiarism.
- Preserving the original sentence's clause order even after synonym swaps.
- Paraphrasing without citing — a citation-free paraphrase is still plagiarism.
- Inventing a citation to lend authority to a paraphrased claim — fabricate never; insert `[CITATION NEEDED]` instead.
- Softening or strengthening the original claim during paraphrase — preserve meaning exactly.

## References
- Howard, R. M. (1992). A Plagiarism Pentimento. *Journal of Teaching Writing*, 11(2), 233-245 — on patchwriting.
- iThenticate similarity scoring documentation: https://www.turnitin.com/products/similarity.
- Purdue OWL on paraphrasing: https://owl.purdue.edu/owl/research_and_citation/using_research/quoting_paraphrasing_and_summarizing/paraphrasing.html.
