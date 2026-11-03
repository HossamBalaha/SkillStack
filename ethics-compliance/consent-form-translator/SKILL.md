---
name: consent-form-translator
description: Translate informed consent forms across reading levels, targeting Flesch-Kincaid grade 6-8 for general adults and grade 4-6 for assent, with plain-language rewrites, multilingual considerations, and low-literacy adaptations aligned with NIH Plain Language guidelines. Use when consent text is too dense for the intended participant population.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [consent-translation, plain-language, flesch-kincaid, readability, low-literacy]
related: [ethics-compliance/informed-consent-writer, ethics-compliance/irb-protocol-drafter, ethics-compliance/research-ethics-checklist-author]
prerequisites: []
outputs: [markdown, python]
difficulty: intermediate
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Consent Form Translator

## When To Use

- The user says "this consent is too dense", "rewrite for an 8th-grade reading level", or "make this assent form
  child-friendly".
- A consent form scored above Flesch-Kincaid grade 10 and needs rewriting to grade 6-8 (adult) or grade 4-6 (child
  assent).
- A study recruits low-literacy participants or speakers of a language not yet covered by the existing consent.
- An IRB reviewer flagged readability as a barrier to informed consent.
- Trigger keywords: readability, Flesch-Kincaid, plain language, assent, low-literacy, translation, NIH plain language.

## Workflow

1. Read the source consent form and confirm the IRB-approved content (purpose, procedures, risks, benefits, withdrawal,
   contacts) is intact.
2. Choose the target reading level: adult general (grade 6-8), adult low-literacy (grade 4-5), child assent 7-12 (grade
   4-5), child assent 13-17 (grade 6-7).
3. Compute the current Flesch-Kincaid grade and readability statistics on the source; record them as the baseline.
4. Apply plain-language rewrites: short sentences (target <= 15 words), active voice, second-person ("you"), one idea
   per sentence, common vocabulary, and acronyms defined on first use.
5. Replace technical terms with plain equivalents; when a term has no plain equivalent, define it immediately in
   parentheses.
6. Use concrete examples and analogies for abstract procedures (e.g., "two teaspoons of blood" instead of "10 mL").
7. Reproduce the regulatory content unchanged (voluntary participation, withdrawal rights, contact information) and
   verify nothing material is lost.
8. Recompute the readability statistics on the rewrite; iterate until the target grade is met on every section, not only
   the overall.
9. Produce a readability report card with per-section scores and the revisions made.
10. Address multilingual adaptations: list target languages, identify certified translator requirements, and note that
    back-translation is recommended for non-English consent.
11. Address low-literacy adaptations: pictograms for key procedures, teach-back prompts, and an audio version where
    applicable.
12. Re-submit the rewritten consent to the IRB for approval before use; readability rewrites are an amendment, not a
    casual edit.

## Inputs

- Source consent form (IRB-approved version).
- Target reading level and audience.
- Target languages if multilingual adaptation is required.
- Any institutional plain-language style guide.
- Sample pictograms or low-literacy resources available.

## Outputs

- `consent_adult_plain.md` — adult consent rewritten to grade 6-8.
- `consent_assent_child_plain.md` — child assent rewritten to grade 4-5.
- `consent_low_literacy.md` — low-literacy adaptation with pictograms.
- `readability_report.md` — baseline vs. revised scores per section.
- `multilingual_plan.md` — target languages, translators, back-translation plan.
- `teach_back_script.md` — script for the consent conversation with low-literacy participants.
- `compute_readability.py` — Python snippet that scores a consent file.
- `irb_amendment_cover.md` — cover letter for the IRB amendment.

## Key Rules

- Plain-language rewrites must not omit, soften, or reframe any risk; risk magnitude must remain equivalent.
- The target grade must be met on every section, not only the overall; a long dense section invalidates the rewrite.
- Acronyms must be defined on first use and reused only after the definition; new acronyms in the rewrite must be added
  to the glossary.
- Multilingual translations require certified translators; machine translation alone is non-compliant for IRB consent.
- Back-translation is recommended for languages where mis-translation could affect risk comprehension.
- Teach-back is not a substitute for written consent; it is a verification step and must be documented.
- Pictograms must be reviewed for cultural appropriateness for the target population; a pictogram in one culture may be
  unclear in another.
- The rewritten consent must be re-approved by the IRB before deployment; readability edits are amendments.

## Examples

```text
Plain-language rewrite (excerpt):
  Source (grade 12): "The investigator will perform phlebotomy to obtain
    a 10 mL specimen of venous blood for haematological analysis."
  Rewrite (grade 6): "A trained staff member will take about two teaspoons
    of blood from a vein in your arm. We will test your blood in the lab."
  Score: 12.1 -> 6.3. Risk magnitude preserved: physical, minimal.
```

```python
# compute_readability.py (excerpt)
import textstat
def score(text: str) -> dict:
    return {
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "smog_index": textstat.smog_index(text),
    }
```
