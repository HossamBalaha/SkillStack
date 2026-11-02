---
name: structured-abstract-writer
description: Drafts structured abstracts with explicit bold inline headings (Background, Methods, Results, Conclusion) tuned to journal word limits, then appends 4-6 SEO-optimized keywords separated by semicolons. Use when a journal mandates a structured abstract or when preparing a manuscript for biomedical, public-health, or NIH-funded venues.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: writing-citation
tags: [abstract, structured, imrad, keywords, biomedical]
related: [writing-citation/imrad-thesis-writer, writing-citation/english-academic-editor]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Structured Abstract Writer

## When To Use
- The journal's author guide requires a structured abstract with bold headings (e.g., JAMA, Lancet, PLOS ONE).
- You must hit a strict word ceiling (commonly 250-350 words) without dropping required sections.
- You need to generate the post-abstract keyword line for indexing (MeSH-style or SEO-oriented).
- A reviewer asked the abstract to mirror the IMRaD body of the paper.

## Workflow
1. Read the target journal's abstract policy: word limit, mandatory headings, whether tables are allowed.
2. Collect source material: study question, design, sample, primary outcome, key effect size, and bottom-line conclusion.
3. Draft each labeled section in order: **Background:**, **Methods:**, **Results:**, **Conclusion:** (add **Objective:**, **Trial Registration:** only if the journal mandates).
4. Allocate word budget roughly 15/30/35/20 percent across the four sections; trim the longest section first.
5. Strip hedging from Results (report numbers); keep one cautious sentence in Conclusion.
6. Generate the keyword line: 4-6 terms, semicolon-separated, none duplicating title words, ordered by specificity descending.
7. Run a word-count check and a heading-presence check; iterate until both pass.
8. Produce a plain-text version (for the submission portal) and a LaTeX version (with `\textbf`).

## Inputs
- Manuscript draft or bulleted facts covering objective, methods, results, conclusion.
- Journal name and abstract policy (word limit, required headings).
- Paper title (so keywords can avoid duplicating it).

## Outputs
- `abstract_structured.md` — the structured abstract with bold inline headings.
- `keywords.txt` — single line of 4-6 semicolon-separated keywords.
- `abstract_check.md` — word count per section and pass/fail on each policy rule.

## Key Rules
- Every mandated heading must appear, in the order the journal specifies.
- Keywords may not duplicate any word in the title (case-insensitive, stemming ignored).
- Results must contain at least one numeric effect estimate with units and confidence interval when applicable.
- Conclusion must not overclaim — use "may," "suggests," or "is associated with" rather than "proves."
- Total word count (including headings) must not exceed the journal limit.
- Do not cite references inside the structured abstract unless the journal explicitly permits it.

## Examples
```text
Before (free-form, 412 words, no headings):
This study looked at whether a new drug lowers blood pressure. We enrolled
a bunch of patients and gave them the drug or placebo. The drug worked
really well, reducing systolic BP by about 15 points. Patients tolerated
it. We think this drug could be a game changer for hypertension care...

After (structured, 248 words, headings present):
**Background:** Hypertension remains the leading modifiable risk factor for
cardiovascular mortality, yet first-line monotherapy fails in roughly 30%
of patients. This trial evaluated the efficacy and safety of compound XR-217,
a novel dual-acting renin inhibitor, as add-on therapy.

**Methods:** In a multi-center, double-blind, randomized controlled trial,
612 adults with uncontrolled hypertension (systolic BP ≥ 140 mmHg despite
angiotensin-receptor-blocker monotherapy) were assigned 1:1 to XR-217 50 mg
daily or placebo for 12 weeks. The primary endpoint was change in mean
24-hour ambulatory systolic BP from baseline.

**Results:** XR-217 reduced 24-hour systolic BP by 14.2 mmHg (95% CI 12.1,
16.3) versus 5.1 mmHg (95% CI 3.4, 6.8) for placebo (difference -9.1 mmHg,
p < 0.001). Adverse-event rates were comparable between arms (11.3% vs 10.9%).

**Conclusion:** XR-217, as add-on therapy, produces clinically meaningful BP
reductions with an acceptable safety profile and may benefit patients whose
hypertension is uncontrolled on standard monotherapy.

Keywords: renin inhibitor; ambulatory blood pressure; resistant hypertension; add-on therapy; randomized controlled trial
```

## References
- NIH structured abstract guidance for grant applications and reports.
- ICMJE Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals (abstract section).
- MeSH Browser for keyword normalization: https://meshb.nlm.nih.gov/.
