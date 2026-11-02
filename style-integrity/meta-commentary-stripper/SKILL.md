---
name: meta-commentary-stripper
description: Remove pedagogical, conversational, and meta phrases from academic prose so the text delivers direct, dense scientific exposition. Use when finalizing a manuscript for a top-tier journal, stripping phrases like "The reader will learn", "In this section we will show", or "Let us delve into".
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [meta-commentary, prose, editing, exposition, density]
related: [style-integrity/academic-prose-polisher, style-integrity/banned-vocabulary-filter, style-integrity/passive-voice-detector]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 860
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Meta-Commentary Stripper

## When To Use
- A manuscript addresses the reader directly ("The reader will learn…").
- Body prose narrates its own structure ("In this section, we will show…", "As we will discuss…").
- Top-tier journal submission requires dense scientific exposition without throat-clearing.
- A reviewer has flagged conversational tone or pedagogical asides.

## Workflow
1. Tokenize the manuscript into sentences.
2. Match each sentence against the trigger-phrase list (see Key Rules).
3. For each match, classify the action:
   - Delete entirely if the sentence adds no information beyond narration.
   - Rewrite if the sentence contains a substantive claim buried in meta-framing.
4. When rewriting, drop the meta prefix and keep the substantive clause.
5. Re-read the surrounding paragraph to confirm cohesion after deletion.
6. Log each transformation in a change report: line, original, action (delete/rewrite), result.
7. Re-scan to confirm no meta phrases remain.

## Inputs
- Manuscript source text (LaTeX, Markdown, or plain text).
- Optional project-specific extension list of meta phrases.

## Outputs
- Revised prose with all meta-commentary removed.
- A change report: line, original, action, result.

## Key Rules
- Trigger phrases (case-insensitive, whole-phrase match):
  - `The reader will learn`
  - `In this section, we will show`
  - `In this section we will show`
  - `As we will discuss`
  - `It is important to note that`
  - `This article will explore`
  - `Let us delve into`
  - `Here's what you need to know`
  - `We now turn to`
  - `Having discussed X, we now`
- Delete pure-narration sentences entirely.
- Rewrite sentences whose meta prefix buries a substantive claim.
- The remaining prose must stand alone without transitional narration.
- Cohesion is verified after each deletion.

## Examples

Before:
```
In this section, we will show that our method outperforms baselines.
The reader will learn that the convergence rate improves under warm
starting. It is important to note that the loss curve plateaus after
200 epochs. Let us delve into the ablation results.
```

After:
```
Our method outperforms baselines. The convergence rate improves under
warm starting. The loss curve plateaus after 200 epochs. The ablation
results follow.
```

Change report:
```
Line 1:  "In this section, we will show that" → deleted prefix.
         Result: "Our method outperforms baselines."
Line 2:  "The reader will learn that"        → deleted prefix.
         Result: "The convergence rate improves under warm starting."
Line 3:  "It is important to note that"      → deleted prefix.
         Result: "The loss curve plateaus after 200 epochs."
Line 4:  "Let us delve into the ablation results." → rewritten.
         Result: "The ablation results follow."
```

## References
- Stephen Pinker, *The Sense of Style*, on classic style and direct exposition.
- The Economist Style Guide, on concise journal prose.
- American Psychological Association (APA) Publication Manual, on authorial voice.
