---
name: literature-review-synthesizer
description: Build systematic literature reviews using PICO or SPIDER framing, Boolean search strings, a PRISMA 2020 flow diagram, thematic synthesis matrix, and quality appraisal with CASP, AMSTAR-2, or ROBIS. Use when the user asks to perform a systematic review, scoping review, or meta-analysis-ready literature synthesis.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [systematic-review, prisma, pico, synthesis, casp]
related: [academic-research/related-work-surveyor, academic-research/citation-network-mapper, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [markdown, latex]
difficulty: advanced
estimated_tokens: 840
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Literature Review Synthesizer

## When To Use

- The user asks for a "systematic review", "scoping review", or "PRISMA diagram".
- The user wants a Boolean search string for PubMed, Scopus, Web of Science, or IEEE Xplore.
- The user needs a thematic synthesis matrix or quality appraisal using CASP, AMSTAR-2, or ROBIS.
- Trigger keywords: PRISMA, PICO, SPIDER, systematic review, Boolean search, CASP, AMSTAR-2, ROBIS, synthesis matrix.

## Workflow

1. Decide review type: systematic, scoping, or rapid. Choose framework: PICO (intervention studies), SPIDER
   (qualitative/mixed), or PCC (scoping).
2. Define Population, Intervention/Exposure, Comparator, Outcome (or equivalents).
3. Construct a Boolean search string with synonyms, MeSH terms, truncation, and field tags. Run it on at least two
   databases plus a grey-literature source.
4. Document PRISMA 2020 flow: Identification → Screening → Eligibility → Included. Report counts at every gate.
5. Set inclusion/exclusion criteria: date range, language, study design, publication type.
6. Deduplicate results; pilot screening on a 5% sample with two reviewers and compute Cohen's kappa.
7. Extract data into a structured matrix: rows = studies, columns = methodology dimensions (not chronology).
8. Perform thematic synthesis: code findings, group into descriptive themes, generate analytical themes.
9. Run quality appraisal with the matched tool: CASP (qualitative/cohort), AMSTAR-2 (systematic reviews of RCTs), ROBIS
   (bias in systematic reviews).
10. Generate a risk-of-bias summary figure (e.g., robvis-style traffic light).
11. Draft the synthesis narrative under thematic headings; cite each study by its row ID.
12. Document limitations: search date, language bias, single-reviewer risk.

## Inputs

- Review question in PICO/SPIDER/PCC form.
- Target databases (PubMed, Scopus, Web of Science, IEEE Xplore, Embase).
- Date range and language filter.
- Reviewer count (single vs. dual).
- Optional: prior protocol registration (PROSPERO ID).

## Outputs

- `protocol.docx` — review protocol (PROSPERO-ready).
- `search_strings.md` — Boolean strings per database with hit counts.
- `prisma_flow.tex` — PRISMA 2020 flow diagram.
- `extraction_matrix.csv` — studies × dimensions.
- `quality_appraisal.csv` — CASP/AMSTAR-2/ROBIS scores.
- `synthesis_narrative.md` — thematic write-up.
- `risk_of_bias.pdf` — robvis-style figure.

## Key Rules

- Never invent counts; every number in the PRISMA diagram must come from the executed search.
- Use PICO for interventions, SPIDER for qualitative/mixed, PCC for scoping reviews.
- Report Cohen's kappa on the pilot screening sample; if kappa < 0.6, revise the criteria.
- Quality appraisal tool must match study design; do not apply AMSTAR-2 to qualitative studies.
- Themes are grouped by methodology, not by year.
- Every included study appears in the extraction matrix with a stable row ID.
- Protocol must be registered or registration-ready before screening begins.

## Examples

```text
PICO: Population = adult stroke survivors; Intervention = robot-assisted gait
training; Comparator = conventional physiotherapy; Outcome = 6-minute walk
distance at 12 weeks.

Search string (PubMed):
("stroke"[MeSH] OR "cerebrovascular accident"[tiab]) AND
("robot*"[tiab] OR "exoskeleton"[tiab]) AND
("gait"[tiab] OR "walking"[tiab]) AND
("random*"[tiab]) Filters: Humans, English, 2015:2025
```

```text
PRISMA counts sample:
Identification: 1,284 records (PubMed 612, Scopus 410, WoS 262)
  After deduplication: 891
Screening (title/abstract): 891 → 142 included for full-text
Eligibility (full-text): 142 → 38 excluded (reasons logged)
Included: 104 studies
```

## References

- PRISMA 2020 statement: https://www.prisma-statement.org/
- CASP checklists: https://casp-uk.net/casp-tools-checklists/
- AMSTAR-2: https://amstar.ca/
- ROBIS: http://www.robis-tool.info/
- PROSPERO registration: https://www.crd.york.ac.uk/prospero/
- robvis visualization tool: https://www.riskofbias.info/welcome/robvis-visualization-tool
