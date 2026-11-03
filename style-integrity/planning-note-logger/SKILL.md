---
name: planning-note-logger
description: Append a concise "Planning Note" section at the end of any deliverable summarizing what data was missing, what assumptions were made, and what the user must provide. Use when shipping a partial deliverable, when silent omissions occurred, or when the agent must surface residual unknowns without polluting the body.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [planning-note, deliverable, assumptions, unknowns, transparency]
related: [style-integrity/silent-omission-protocol, style-integrity/execution-protocol, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 810
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Planning Note Logger

## When To Use

- A deliverable is being shipped with known gaps in data or assumptions.
- Silent omissions have occurred in the body and the user must be informed.
- A task is partially complete pending user input (paths, parameters, citations, files).
- The agent must surface residual unknowns without breaking the body's narrative.

## Workflow

1. While completing the deliverable, maintain an internal list of every missing input and every assumption made.
2. Once the body is finalized, draft a "Planning Note" section.
3. For each missing item, state: (a) what specifically is missing, (b) what assumption (if any) was made in its place,
   (c) what the user must provide to complete the work.
4. Order the items by priority: blocking items first, optional refinements second.
5. Keep each entry to one or two sentences. Use a flat list, not nested prose.
6. Append the Planning Note at the very end of the deliverable, after the conclusion or final section.
7. Use the heading `## Planning Note` (or `Planning Note —` if Markdown is not supported).
8. Re-read the body to confirm no Planning-Note content leaked into the body itself.
9. Deliver the full document with the appended note.

## Inputs

- The deliverable body.
- The internal log of missing data and assumptions accumulated during execution.
- Optional priority labels (blocking / optional).

## Outputs

- A "Planning Note" section appended at the very end of the deliverable, with three columns of information per item:
  missing, assumption, requested user input.

## Key Rules

- The Planning Note is ALWAYS at the very end of the deliverable.
- Each entry states what is missing, what was assumed, and what the user must provide.
- Tone is professional and concise — no apologies, no filler.
- The body never references the Planning Note directly.
- If nothing is missing, the Planning Note reads: "No missing data. No assumptions beyond those stated inline."
- Blocking items are listed before optional refinements.
- Each entry is at most two sentences; no nested sub-bullets.

## Examples

Planning Note appended to a deliverable:

```
## Planning Note

Missing data and assumptions:
- Missing: the production dataset path. Assumed: `data/production.csv`
  matches the schema of `data/sample.csv`. Provide the canonical path
  to finalize the data-loading code.
- Missing: the target top-1 accuracy value. Assumed: the qualitative
  comparison in Section 4 holds; a numerical value is not yet supplied.
  Provide the evaluation protocol and the value to restore the claim.
- Missing: the BibTeX key for the Smith et al. 2024 reference. Assumed:
  the citation will be added manually before submission. Provide the
  DOI or canonical citation to finalize.

Requested user input (in priority order):
1. Production dataset path.
2. Target accuracy value and evaluation protocol.
3. BibTeX entry for Smith et al. 2024.
```

Empty Planning Note (when nothing is missing):

```
## Planning Note

No missing data. No assumptions beyond those stated inline.
```
