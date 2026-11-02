---
name: thesis-chapter-planner
description: Plan thesis and dissertation chapters with strict cross-chapter non-redundancy enforcement. If a concept was defined in Chapter 2, Chapter 5 must reference "As detailed in Section 2.3..." instead of re-explaining. Produces a cumulative concept map and per-chapter scope. Use when the user is outlining a master's thesis, PhD dissertation, or any multi-chapter academic monograph.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [thesis, dissertation, chapter, monograph, concept-map]
related: [academic-research/academic-book-author, academic-research/scope-and-aims-writer, style-integrity/cross-reference-validator]
prerequisites: []
outputs: [markdown, latex]
difficulty: advanced
estimated_tokens: 820
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Thesis Chapter Planner

## When To Use

- The user is writing a master's thesis or PhD dissertation.
- The user wants a chapter outline that avoids redundancy across chapters.
- The user asks for a concept map showing where each concept is introduced and reused.
- Trigger keywords: thesis, dissertation, chapter plan, cross-referencing, concept map, monograph.

## Workflow

1. Capture the thesis title, central research question, and degree (MSc, PhD).
2. List the canonical chapter set: Introduction, Background, Related Work, Methodology, Experiments, Discussion,
   Conclusion. Add appendices if needed.
3. For each chapter, write a 2-3 sentence scope statement and a list of sections (e.g., 2.1, 2.2, 2.3).
4. Build a concept inventory: every key term, notation symbol, dataset, and method gets a unique ID and a "defined-in"
   section reference.
5. For every later chapter, scan for each concept and replace any re-explanation with "As defined in Section X.Y, ..."
   cross-references.
6. Produce a cumulative concept map (graphviz DOT or Markdown adjacency list) showing introduction → reuse edges.
7. Identify forward references where a concept is used before being defined; either reorder or insert a placeholder (
   "defined later in Section Z").
8. Draft a per-chapter milestone calendar aligned with the defense date.
9. Validate against institutional formatting requirements (page limits, margins, citation style).
10. Output the chapter plan and the non-redundancy audit log.

## Inputs

- Thesis title and degree.
- Central research question(s) and hypothesis.
- Institution's thesis formatting guide.
- Defense target date and committee feedback (if any).

## Outputs

- `chapter_plan.md` — chapter list with scope and section headings.
- `concept_inventory.csv` — concept ID, name, defined-in section, reused-in sections.
- `concept_map.dot` — graphviz source for the concept map.
- `nonredundancy_audit.md` — list of redundancies removed with replacement cross-references.
- `milestone_calendar.md` — chapter drafts vs. defense date.

## Key Rules

- Every concept has exactly one "defined-in" section; all other mentions must cross-reference.
- Re-explaining a concept is forbidden; use "As defined in Section X.Y, ..." instead.
- Forward references are allowed only if a placeholder is inserted.
- Concept map nodes are stable IDs (e.g., C12 = "federated aggregation").
- Chapter scope statement must fit in 2-3 sentences; if longer, split the chapter.
- Plan validated against the institution's thesis format guide.

## Examples

```text
Chapter plan excerpt:
  Ch 2 Background
    Scope: Establish notation, formalize the federated learning problem,
           and define topological descriptors.
    Sections: 2.1 Notation; 2.2 Federated Learning; 2.3 Persistent Homology.

  Ch 5 Discussion
    Scope: Interpret results, link to the topology regularizer (Section 2.3),
           and discuss limitations.
    Sections: 5.1 Findings; 5.2 Topology Revisited; 5.3 Limitations.
```

```text
Non-redundancy audit log:
  Found: Section 5.2 redefines persistent homology (1 paragraph).
  Action: Replaced with "As defined in Section 2.3, persistent homology
          quantifies topological features across scales; here we revisit
          its role in our results."
  Forward reference inserted at Section 1.4 ("defined later in Section 2.3").
```

## References

- "How to Write a Thesis" (Umberto Eco) structural guidance.
- LaTeX thesis classes: https://ctan.org/topic/thesis
- Graphviz DOT language: https://graphviz.org/doc/info/lang.html
- MIT thesis specifications: https://libraries.mit.edu/dist/ams/thesis-specs/

## Notes

- Treat the concept inventory as the canonical truth; if a concept is missing from the inventory, it has not been
  formally defined.
- Each time a chapter is drafted, run the non-redundancy audit before sending to the advisor.
- Update the concept map whenever a new section is added so forward references stay valid.
