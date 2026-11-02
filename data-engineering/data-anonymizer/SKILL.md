---
name: data-anonymizer
description: Anonymize PII by hashing or removing direct identifiers, applying k-anonymity via generalization/suppression to quasi-identifiers, enforcing l-diversity and t-closeness on sensitive attributes, and adding calibrated noise for differential privacy. Use this skill when releasing data under GDPR Article 5 or HIPAA Safe Harbor constraints.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [pii, gdpr, hipaa, anonymization, privacy]
related: [ai-output-judgement/pii-leak-detector, data-engineering/data-quality-validator]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Data Anonymizer

## When To Use

- A dataset containing PII must be shared internally or externally.
- Quasi-identifiers (ZIP, DOB, gender) could re-identify individuals in combination.
- Compliance with GDPR Article 5 (data minimisation) or HIPAA Safe Harbor is required.
- A privacy budget must be tracked for differential-privacy releases.
- Re-identification risk must be quantified before a release is approved.

## Workflow

1. Classify columns: direct identifiers, quasi-identifiers, sensitive attributes, others.
2. Direct identifiers: hash with a per-release salt or remove entirely.
3. Quasi-identifiers: generalise (e.g., ZIP → 3 digits, DOB → year) and suppress rare values.
4. Check k-anonymity: every quasi-identifier combination covers at least k records.
5. Check l-diversity on sensitive attributes within each k-group.
6. Check t-closeness: the distribution of a sensitive value within a group is close to global.
7. For numeric releases, add Laplace or Gaussian noise calibrated to the privacy budget.
8. Record the privacy parameters (k, l, t, epsilon) in a release manifest.
9. Run a re-identification risk test before signing off.

## Inputs

- The dataset containing direct, quasi, and sensitive attributes.
- Classification map: column to category (direct/quasi/sensitive/other).
- Privacy parameters: k, l, t, epsilon, delta.
- Salt value (rotated per release) for hashing direct identifiers.

## Outputs

- An anonymized dataset satisfying the declared privacy parameters.
- A release manifest recording parameters, hashes, and risk score.
- A re-identification risk report quantifying residual risk.

## Key Rules

- Direct identifiers are never shipped in cleartext; hash or remove.
- k-anonymity is enforced on the combination of all quasi-identifiers, not per column.
- The salt is rotated per release and never shared with the data recipient.
- The privacy budget (epsilon, delta) is consumed once per release and tracked.
- Generalisation rules are deterministic and versioned.
- Re-identification risk is reported with a numeric score, not a yes/no verdict.
- Sensitive attributes are never generalised away (l-diversity still needs them).

## Examples

```python
import hashlib
import numpy as np


class AnonymizationConfig:
  # Holds the privacy parameters that govern one release.
  def __init__(self, k, l, t, epsilon, salt):
    self.K = k
    self.L = l
    self.T = t
    self.Epsilon = epsilon
    self.Salt = salt


def HashIdentifier(value, salt):
  # Hash a direct identifier with a per-release salt.
  digest = hashlib.sha256((salt + str(value)).encode()).hexdigest()
  return digest[:16]


def GeneralizeZip(zipCode):
  # Reduce precision so quasi-identifiers form larger groups.
  return str(zipCode)[:3] + "**"


def CheckKAnonymity(df, quasiColumns, k):
  # Every combination of quasi-identifiers must cover at least k rows.
  groupSizes = df.groupby(quasiColumns).size()
  if (groupSizes.min() < k):
    raise ValueError(f"k-anonymity violated: smallest group is {groupSizes.min()}")
  return True


def AddLaplaceNoise(value, sensitivity, epsilon):
  # Apply calibrated noise for a differentially private numeric release.
  scale = sensitivity / epsilon
  noise = np.random.laplace(0.0, scale)
  return value + noise


def Anonymize(df, config):
  # Apply the full anonymization stack to a dataframe.
  df = df.copy()
  df["email_hash"] = df["email"].apply(lambda v: HashIdentifier(v, config.Salt))
  df = df.drop(columns=["email"])
  df["zip3"] = df["zip"].apply(GeneralizeZip)
  df = df.drop(columns=["zip"])
  CheckKAnonymity(df, ["zip3", "gender", "birth_year"], config.K)
  return df
```

## References

- GDPR Article 5: https://gdpr-info.eu/art-5-gdpr/
- HIPAA Safe Harbor: https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/
- k-anonymity (Sweeney 2002): https://epic.org/privacy/reidentification/Sweeney_Article.pdf
- Differential privacy (Dwork 2006): https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/dwork.pdf
