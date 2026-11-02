---
name: narrative-arc-designer
description: Design narrative arcs for data stories by mapping evidence onto a setup-conflict-resolution spine and choosing between author-driven and reader-driven structures. Use when the user needs to shape raw analysis into a story, choose a martini-glass or drill-down arc, or decide between story-first and data-first sequencing.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [narrative-arc, story-design, martini-glass, drill-down, sequencing]
related: [data-storytelling/data-story-storyboarder, data-storytelling/audience-tailor, data-storytelling/data-annotation-writer]
prerequisites: []
outputs: [markdown, yaml]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Narrative Arc Designer

## When To Use

- The user says "turn this analysis into a story" or "give my report a narrative".
- A deck, dashboard, or article lacks a clear through-line and the audience loses the point.
- The user must choose between a guided story and a free-form exploration.
- Trigger keywords: narrative arc, story spine, martini glass, drill-down, story-first, data-first.

## Workflow

1. Collect the evidence stack: headline finding, supporting figures, secondary findings, and known caveats.
2. State the single-sentence takeaway the audience should leave with; everything else supports it.
3. Pick a genre from the Segel and Heer taxonomy: martini-glass, slide show, drill-down, or free-form.
4. Map the evidence onto a three-beat spine:
    - Setup — establish context, units, time frame, and the question being answered.
    - Conflict — surface the surprise, gap, or tension the data reveals.
    - Resolution — deliver the takeaway, the "so what", and any recommended action.
5. Decide on ordering: story-first (lead with the punchline, then justify) or data-first (build the case, then reveal).
6. Annotate each beat with the chart, table, or annotation it depends on; flag missing evidence.
7. Record pacing notes: where to slow down, where to pause for emphasis, where to invite interaction.
8. Emit a YAML arc spec (beats, evidence pointers, ordering, genre) plus a Markdown narrative brief.

## Inputs

- A headline finding and the dataset or analysis behind it.
- Audience profile and reading context (live talk, scrolled article, exported PDF).
- Optional: existing charts, captions, or quotes to reuse.

## Outputs

- `arc_spec.yaml` — machine-readable beats, genre, ordering, evidence pointers.
- `narrative_brief.md` — prose walkthrough of setup, conflict, and resolution.
- `evidence_gap_list.md` — missing charts or quotes that the arc still needs.

## Key Rules

- Every arc states its single takeaway in one sentence before any beat is written.
- Genre choice is justified by audience attention budget, not by author preference alone.
- Story-first ordering is the default for time-pressed executives; data-first for technical reviewers.
- The conflict beat must carry genuine tension; "things improved" is not a conflict.
- Resolution names an action or a decision, not just a summary.
- Annotated beats link to evidence by file or figure number so downstream skills can verify.

## Examples

```text
Arc: "Martini glass, story-first"
Takeaway: "District 4 readmission rate is 2.3x the system average, driven by
a single discharge protocol we can replace in 90 days."
Beat 1 (Setup): Readmissions 2020-2024 system-wide, define "readmission".
Beat 2 (Conflict): District 4 outliers in scatter; annotate the cluster.
Beat 3 (Resolution): Protocol swap, projected 31% reduction, board ask.
Genre justification: 8-minute board slot, decision needed today.
```

```yaml
# arc_spec.yaml (excerpt)
genre: martini-glass
ordering: story-first
takeaway: "District 4 readmission rate is 2.3x the system average..."
beats:
  - id: setup
    role: setup
    evidence: [figures/readmissions_trend.png, tables/defs.md]
  - id: conflict
    role: conflict
    evidence: [figures/district_scatter.png, annotations/d4_callout.md]
  - id: resolution
    role: resolution
    evidence: [tables/protocol_swap.md]
```

## References

- Segel, E., and Heer, J. (2010). Narrative Visualization: Telling Stories with Data. IEEE TVCG 16
  (6). https://ieeexplore.ieee.org/document/5506124
- Kosara, R. (2016). Narrative Tableau. https://eagereyes.org/
- Lee, B. et al. (2015). More Than Telling a Story: Transforming Data into Visually Shared Stories. IEEE CG&A 35
  (5). https://ieeexplore.ieee.org/document/7241862
- Hullman, J., and Diakopoulos, N. (2011). Visualization Rhetoric: Framing Effects in Dynamic Data
  Visualization. https://idl.cs.washington.edu/papers/visualization-rhetoric/
