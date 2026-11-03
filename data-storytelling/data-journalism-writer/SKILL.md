---
name: data-journalism-writer
description: Write data-journalism pieces with a finding-first lede, a methodology paragraph, an interactive chart, sourced quotes, and honest caveats. Use when the user is drafting an explainer, investigation, or news-graphic article for a public audience and must follow the ProPublica and FiveThirtyEight house style.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [data-journalism, lede, methodology, sourcing, caveats]
related: [data-storytelling/metric-translation-writer, data-storytelling/data-annotation-writer, data-storytelling/interactive-narrative-builder]
prerequisites: []
outputs: [markdown, html]
difficulty: intermediate
estimated_tokens: 1150
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Data Journalism Writer

## When To Use

- The user says "write this up as a news story" or "turn my analysis into a feature".
- The piece must read for a general public audience, not a peer reviewer.
- The story carries a single finding that should land in the first two sentences.
- Methodology must be visible but not dominate the narrative.
- Trigger keywords: lede, nut graf, methodology box, sourced quote, caveat, ProPublica, FiveThirtyEight.

## Workflow

1. State the headline finding in one sentence; that becomes the lede.
2. Write a nut graf in the second or third paragraph that names the finding, the data, and the stakes.
3. Draft a one-paragraph methodology note: source, time range, unit of analysis, known limits.
4. Embed the headline chart with an annotation that points to the finding without restating the lede.
5. Sourced quotes: at least one from a named expert, one from an affected stakeholder, both verbatim.
6. Add a caveats paragraph: what the data cannot say, alternative explanations, sample limitations.
7. Close with a forward-looking graf: what happens next, what the reader can do, or what the data will show.
8. Run a sourcing audit: every number, every quote, every chart has a named source and link.
9. Emit the article as Markdown plus an HTML wrapper that hosts the interactive chart.

## Inputs

- A finding plus the dataset, time range, and unit of analysis behind it.
- Source links for every number used in the piece.
- At least one expert contact and one affected-stakeholder contact for quotes.
- Optional: interactive chart asset from `interactive-narrative-builder`.

## Outputs

- `article.md` — the full piece, lede to kicker.
- `methodology_box.md` — standalone methodology paragraph.
- `source_list.yaml` — every claim mapped to a URL or document.
- `article.html` — wrapper that hosts the chart and the copy.
- `caveats.md` — limitations and alternative explanations.

## Key Rules

- The lede states the finding, not the topic; "readmissions rose" loses to "District 4 readmits 2.3 times more often".
- The methodology paragraph is short, plain, and present; never hidden in a footnote.
- Every number cites a source in the source list; uncited numbers are removed.
- Quotes are verbatim, attributed, and contextualised; paraphrased quotes are not quotes.
- Caveats appear before the kicker, not buried after it.
- Charts are annotated to land the finding on their own; the reader skims and still gets it.
- Avoid false balance: if the evidence points one way, the caveats name limits, not opposing claims.

## Examples

```text
Lede (excerpt):
"District 4 hospitals readmit nearly one in four patients within 30 days,
more than double the system average, and the gap has widened every year
since 2020, according to a system-wide analysis of 41,208 discharge records."

Methodology box (excerpt):
"Records cover every inpatient discharge from January 2020 through December
2024 across the 11-hospital network. Readmission is defined as any unplanned
inpatient return within 30 days of discharge; planned returns (chemotherapy,
transplant) are excluded. Names and identifiers were stripped before analysis."

Source list entry:
- claim: "2.3x the system average"
  source: tables/d4_readmissions.csv
  url: https://example.org/data/d4_readmissions.csv
  accessed: 2025-01-14
```
