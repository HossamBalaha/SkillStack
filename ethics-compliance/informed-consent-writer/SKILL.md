---
name: informed-consent-writer
description: Write informed consent forms covering plain-language summary, study procedures, risks, benefits, confidentiality protections, voluntary participation, withdrawal rights, and contacts. Use when preparing consent documents for any human-subjects research, including adult, pediatric, and low-literacy populations.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ethics-compliance
tags: [informed-consent, belmont-report, plain-language, human-subjects, 21-cfr-50]
related: [ethics-compliance/irb-protocol-drafter, ethics-compliance/consent-form-translator, ethics-compliance/research-ethics-checklist-author]
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Informed Consent Writer

## When To Use

- The user says "write a consent form", "draft an ICF", or "prepare a participant information sheet".
- An IRB protocol needs its companion consent documents in adult, parental permission, and child assent versions.
- A study involves vulnerable participants who need simplified wording or short-form consent.
- A waiver or alteration of consent is being requested and the justification narrative is needed.
- Trigger keywords: informed consent, ICF, assent, parental permission, Belmont Report, 21 CFR 50.

## Workflow

1. Pull the protocol summary (title, PI, purpose, procedures, risks, benefits) as the source of truth.
2. Choose the consent variant: adult full consent, parental permission, child assent (age-banded), short form, or waiver
   narrative.
3. Draft the plain-language summary at a Flesch-Kincaid grade 6-8 reading level for adult consent, grade 4-6 for assent.
4. Section the document in the regulatory order: purpose, eligibility, procedures, duration, risks, benefits,
   alternatives, confidentiality, compensation, voluntary participation, withdrawal, contacts.
5. Convert each technical procedure into a one-sentence plain-language step, preserving order.
6. Enumerate risks by category (physical, psychological, social, legal, economic) with probability and magnitude.
7. Describe confidentiality with the specific safeguards (encryption, coding, certificate of confidentiality) and any
   limits (subpoena, mandatory reporting).
8. State the voluntary participation clause and the right to withdraw without penalty, including how data already
   collected will be handled.
9. List contact information: PI, co-investigator, IRB office, and an independent participant-rights office where
   available.
10. Add the signature block: participant, parent/guardian, witness (for short form), and person obtaining consent, with
    date lines.
11. Add an IRB footer placeholder for protocol number, approval date, and expiration date.
12. Run a readability check; if the grade exceeds the target, rewrite the offending sentences.

## Inputs

- IRB protocol summary (title, procedures, risks, benefits).
- Study population and any vulnerable subgroups.
- Target reading level for each consent variant.
- Institutional contact details and IRB office information.
- Any compensation or reimbursement scheme.

## Outputs

- `consent_adult.md` — full adult informed consent document.
- `consent_parental_permission.md` — permission for parents/guardians.
- `consent_assent_child.md` — age-banded child assent (typically 7-12 and 13-17).
- `consent_short_form.md` — short-form consent with summary to be read aloud.
- `waiver_justification.md` — narrative for waiver or alteration under 45 CFR 46.116(f).
- `readability_report.md` — Flesch-Kincaid scores per section.

## Key Rules

- Consent language must avoid legalese, defined terms, and acronyms unless immediately explained.
- The phrase "you may withdraw at any time without penalty" must appear verbatim in adult consent.
- Risks must not be minimized; if a risk is unknown, state that explicitly.
- Benefits must distinguish direct benefit to the participant from benefit to society.
- Contact information must include the IRB office, not just the PI.
- The signature block must include the person obtaining consent and the date the consent was obtained.
- Short-form consent requires a witness signature and a written summary approved by the IRB.
- Waiver justification must address all six criteria of 45 CFR 46.116(f), not just some.

## Examples

```text
Plain-language procedure rewrite:
  Source: "Venipuncture will be performed by a certified phlebotomist to collect 10 mL of whole blood."
  Consent: "A trained staff member will take about two teaspoons of blood from a vein in your arm."
  Reading level: grade 6 (down from grade 12).
```

```text
Withdrawal clause:
  "You can stop being in this study at any time. You do not have to give a reason.
   If you stop, the data already collected about you will be kept and used for the study
   unless you tell us in writing to destroy it."
```

## References

- Belmont Report: https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html
- 21 CFR 50 (FDA informed consent): https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50
- 45 CFR 46.116 (general requirements for consent): https://www.ecfr.gov/current/title-45/part-46#46.116
- OHRP informed consent FAQs: https://www.hhs.gov/ohrp/regulations-and-policy/guidance/faq/informed-consent/index.html
- NIH Plain Language
  guidelines: https://www.nih.gov/institutes-nih/nih-office-communications-public-liaison/clear-communication/plain-language
