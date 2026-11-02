# 🔬 Data Engineering — ETL, Schemas & Lineage

> Build ETL pipelines, enforce schemas, anonymize datasets, and track lineage from raw input to model-ready features.
> Covers tabular, image, text, and time-series data, plus the quality, drift, and dataset-card tooling required to ship
> data that is auditable and reproducible. Every pipeline ends with a dataset card describing provenance and license.

<div align="center">

[![Skills](https://img.shields.io/badge/Skills-18-blue)]()
[![Theme](https://img.shields.io/badge/Theme-data-engineering-green)]()

</div>

## Theme Overview

This folder contains **18 skills** in the `data-engineering/` theme. Each subfolder holds a `SKILL.md` whose YAML
frontmatter declares `name`, `description`, `difficulty`, `tags`, and `related` — the table below is generated from that
frontmatter, not hand-maintained.

Skills are independent modules: load any one of them on demand. The `related` column lists the canonical next skills to
chain with, and the chains section at the bottom shows the most common sequences observed across the SkillStack repo.

## Quick Start

1. Open the table below and locate the skill that matches your task.
2. Click the skill name to open its `SKILL.md`.
3. Read the YAML frontmatter to confirm `description`, `difficulty`, and `prerequisites`.
4. Read the body of `SKILL.md` in full, then any referenced `references/*.md`.
5. If the skill emits Python, also load `style-integrity/coding-conventions-enforcer`.
6. When the skill finishes, follow the `related` column to the next skill in the chain.

## Skills

| #  | Skill                                                                 | Description                                                                                                                                                                                                                                                                                                              | Difficulty   | Tags                                                                       | Related                                                                                                                            |
|----|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 1  | [`categorical-encoder`](categorical-encoder/SKILL.md)                 | Encode categorical columns using one-hot (low cardinality), ordinal (meaningful order), target/mean encoding with k-fold CV, frequency encoding, hash encoding (fixed dim for high cardinality), or entity embeddings learned via NN.                                                                                    | intermediate | `categorical`, `encoding`, `one-hot`, `target-encoding`, `embeddings`      | `data-engineering/feature-engineering-toolkit`, `data-engineering/data-quality-validator`, `data-engineering/data-schema-enforcer` |
| 2  | [`csv-json-converter`](csv-json-converter/SKILL.md)                   | Convert between CSV, JSON, Parquet, and Arrow formats while preserving types (dates, ints, floats, nulls) and streaming large files in chunks.                                                                                                                                                                           | beginner     | `csv`, `json`, `parquet`, `arrow`, `format-conversion`                     | `data-engineering/incremental-loader`, `data-engineering/data-schema-enforcer`                                                     |
| 3  | [`data-anonymizer`](data-anonymizer/SKILL.md)                         | Anonymize PII by hashing or removing direct identifiers, applying k-anonymity via generalization/suppression to quasi-identifiers, enforcing l-diversity and t-closeness on sensitive attributes, and adding calibrated noise for differential privacy.                                                                  | intermediate | `pii`, `gdpr`, `hipaa`, `anonymization`, `privacy`                         | `ai-output-judgement/pii-leak-detector`, `data-engineering/data-quality-validator`                                                 |
| 4  | [`data-drift-monitor`](data-drift-monitor/SKILL.md)                   | Monitor data drift between TRAIN and production data using Population Stability Index (PSI), Kolmogorov-Smirnov test, and Wasserstein distance per feature.                                                                                                                                                              | intermediate | `drift`, `psi`, `monitoring`, `mlops`                                      | `data-engineering/data-quality-validator`, `ml-engineering/metrics-computation-suite`                                              |
| 5  | [`data-lineage-tracker`](data-lineage-tracker/SKILL.md)               | Track data lineage as a provenance graph from source through transforms to sink, where each dataset carries a unique ID, version, source URI, transform function reference, parent dataset IDs, and a content hash (md5/sha256).                                                                                         | advanced     | `lineage`, `provenance`, `openlineage`, `atlas`, `dag`                     | `data-engineering/etl-pipeline-builder`, `data-engineering/incremental-loader`                                                     |
| 6  | [`data-quality-validator`](data-quality-validator/SKILL.md)           | Validate datasets against declarative schemas using pandera DataFrameSchemas and Great Expectations suites.                                                                                                                                                                                                              | intermediate | `data-quality`, `pandera`, `great-expectations`, `validation`, `schema`    | `data-engineering/data-schema-enforcer`, `data-engineering/data-drift-monitor`, `data-engineering/etl-pipeline-builder`            |
| 7  | [`data-schema-enforcer`](data-schema-enforcer/SKILL.md)               | Enforce schemas on incoming rows using pydantic BaseModel type annotations and validators or pandera DataFrameSchema.                                                                                                                                                                                                    | intermediate | `schema`, `pydantic`, `pandera`, `validation`, `quarantine`                | `data-engineering/data-quality-validator`, `data-engineering/etl-pipeline-builder`                                                 |
| 8  | [`dataset-card-generator`](dataset-card-generator/SKILL.md)           | Generate dataset cards in the model-card style documenting provenance, license, composition, intended use, out-of-scope use, limitations, and ethical considerations.                                                                                                                                                    | beginner     | `dataset-card`, `documentation`, `ethics`, `provenance`, `model-card`      | `data-engineering/data-lineage-tracker`, `data-engineering/data-quality-validator`                                                 |
| 9  | [`etl-pipeline-builder`](etl-pipeline-builder/SKILL.md)               | Design and implement idempotent ETL pipelines that Extract from APIs/DBs/files, Validate schemas, Transform clean data, and Load to warehouses or lakes.                                                                                                                                                                 | advanced     | `etl`, `pipeline`, `airflow`, `dbt`                                        | `data-engineering/data-quality-validator`, `data-engineering/data-lineage-tracker`                                                 |
| 10 | [`feature-engineering-toolkit`](feature-engineering-toolkit/SKILL.md) | Build numeric features (polynomial, log, sqrt, binning), categorical features (one-hot, ordinal, target/mean encoding with CV, frequency), interaction features, datetime features, and lag/rolling window features with closed='right' to prevent leakage.                                                              | intermediate | `feature-engineering`, `polynomial`, `binning`, `lag-features`, `datetime` | `data-engineering/categorical-encoder`, `data-engineering/missing-data-imputer`                                                    |
| 11 | [`feature-store-recipe`](feature-store-recipe/SKILL.md)               | Build feature engineering pipelines with point-in-time correctness, versioned feature definitions, and synced offline (training) and online (inference) stores.                                                                                                                                                          | advanced     | `feature-store`, `feast`, `hopsworks`, `point-in-time`, `online-features`  | `data-engineering/feature-engineering-toolkit`, `data-engineering/etl-pipeline-builder`                                            |
| 12 | [`image-dataset-loader`](image-dataset-loader/SKILL.md)               | Load image datasets from directory structures (`train/cat/`, `train/dog/`) using torchvision ImageFolder, apply augmentations (RandomResizedCrop, HorizontalFlip, ColorJitter, Normalize with ImageNet stats), and batch with DataLoader (num_workers, pin_memory, prefetch_factor) to overlap data loading and compute. | intermediate | `images`, `torchvision`, `augmentation`, `dataloader`, `cnn`               | `data-engineering/tabular-data-sampler`, `data-engineering/text-preprocessor`                                                      |
| 13 | [`incremental-loader`](incremental-loader/SKILL.md)                   | Load data incrementally using stateful checkpoints (last-modified or watermark columns), idempotent re-runs deduplicated by primary key, and a JSON state file.                                                                                                                                                          | intermediate | `cdc`, `incremental`, `watermark`, `upsert`, `idempotent`                  | `data-engineering/etl-pipeline-builder`, `data-engineering/data-lineage-tracker`                                                   |
| 14 | [`missing-data-imputer`](missing-data-imputer/SKILL.md)               | Impute missing values with simple strategies (mean, median, mode), KNN imputation, iterative imputation modeling each feature as a function of the others, or MICE for multiple imputation.                                                                                                                              | intermediate | `imputation`, `knn`, `mice`, `missing-data`, `leakage-prevention`          | `data-engineering/feature-engineering-toolkit`, `data-engineering/outlier-detector`                                                |
| 15 | [`outlier-detector`](outlier-detector/SKILL.md)                       | Detect outliers using statistical methods (IQR and z-score), distance-based methods (DBSCAN), tree-based methods (Isolation Forest), and local methods (Local Outlier Factor).                                                                                                                                           | intermediate | `outliers`, `iqr`, `isolation-forest`, `dbscan`, `lof`                     | `data-engineering/data-quality-validator`, `data-engineering/missing-data-imputer`                                                 |
| 16 | [`tabular-data-sampler`](tabular-data-sampler/SKILL.md)               | Sample tabular data using random, stratified (preserve class proportions), weighted (oversample minority via WeightedRandomSampler), or reservoir sampling for streaming data.                                                                                                                                           | beginner     | `sampling`, `stratified`, `weighted`, `reservoir`, `random-seed`           | `data-engineering/data-quality-validator`, `data-engineering/feature-engineering-toolkit`                                          |
| 17 | [`text-preprocessor`](text-preprocessor/SKILL.md)                     | Preprocess raw text by lowercasing, tokenizing (word or subword via BPE/SentencePiece), removing punctuation and numbers, lemmatizing with spaCy or stemming with Porter/Snowball, removing stopwords via NLTK, and extracting n-grams.                                                                                  | intermediate | `nlp`, `tokenization`, `lemmatization`, `stopwords`, `bpe`                 | `data-engineering/image-dataset-loader`, `data-engineering/tabular-data-sampler`                                                   |
| 18 | [`time-series-resampler`](time-series-resampler/SKILL.md)             | Resample time series to a new frequency (minute to hourly mean), apply forward fill, backward fill, and interpolation (linear, spline), align multiple series to a common index, and handle irregular timestamps.                                                                                                        | intermediate | `time-series`, `resampling`, `interpolation`, `forward-fill`, `alignment`  | `data-engineering/missing-data-imputer`, `data-engineering/data-quality-validator`                                                 |

## Difficulty Breakdown

Across **18** skills in this theme, the difficulty distribution is:

- **Beginner** — 3 skill(s)
- **Intermediate** — 12 skill(s)
- **Advanced** — 3 skill(s)

Beginner skills are safe to load cold. Intermediate skills assume familiarity with the theme's domain. Advanced skills
expect the operator to have read the prerequisites first.

## Tag Index

Tags below are extracted from each `SKILL.md` frontmatter. Use them to filter skills within this theme.

`pandera` (2), `provenance` (2), `schema` (2), `validation` (2), `airflow` (1), `alignment` (1), `anonymization` (1),
`arrow` (1), `atlas` (1), `augmentation` (1), `binning` (1), `bpe` (1), `categorical` (1), `cdc` (1), `cnn` (1), `csv`
(1), `dag` (1), `data-quality` (1), `dataloader` (1), `dataset-card` (1), `datetime` (1), `dbscan` (1), `dbt` (1),
`documentation` (1), `drift` (1), `embeddings` (1), `encoding` (1), `ethics` (1), `etl` (1), `feast` (1),
`feature-engineering` (1), `feature-store` (1), `format-conversion` (1), `forward-fill` (1), `gdpr` (1),
`great-expectations` (1), `hipaa` (1), `hopsworks` (1), `idempotent` (1), `images` (1), `imputation` (1), `incremental`
(1), `interpolation` (1), `iqr` (1), `isolation-forest` (1), `json` (1), `knn` (1), `lag-features` (1),
`leakage-prevention` (1), `lemmatization` (1), `lineage` (1), `lof` (1), `mice` (1), `missing-data` (1), `mlops` (1),
`model-card` (1), `monitoring` (1), `nlp` (1), `one-hot` (1), `online-features` (1), `openlineage` (1), `outliers` (1),
`parquet` (1), `pii` (1), `pipeline` (1), `point-in-time` (1), `polynomial` (1), `privacy` (1), `psi` (1), `pydantic`
(1), `quarantine` (1), `random-seed` (1), `resampling` (1), `reservoir` (1), `sampling` (1), `stopwords` (1),
`stratified` (1), `target-encoding` (1), `time-series` (1), `tokenization` (1), `torchvision` (1), `upsert` (1),
`watermark` (1), `weighted` (1)

## Skill Chains in This Theme

Skills rarely run in isolation. Load the first skill, finish its output, then load the next. The chains below are the
most common sequences observed across the SkillStack repo.

- **`etl-pipeline-builder` → `data-quality-validator` → `data-schema-enforcer` → `data-lineage-tracker`** — ETL →
  validate → enforce → lineage.
- **`feature-engineering-toolkit` → `categorical-encoder` → `missing-data-imputer` → `outlier-detector` →
  `data-drift-monitor`** — Features → encode → impute → outlier → drift.
- **`csv-json-converter` → `data-schema-enforcer` → `data-anonymizer` → `dataset-card-generator`** — Convert → schema →
  anonymize → card.
- **`incremental-loader` → `time-series-resampler` → `missing-data-imputer` → `data-drift-monitor`** — Incremental →
  resample → impute → drift.

## Cross-Theme Connections

Skills in `data-engineering/` declare `related` pointers to skills in other themes. The most common destinations are:

- `../ai-output-judgement/` — 1 related pointer(s)
- `../ml-engineering/` — 1 related pointer(s)

Themes that commonly chain with this one:

- [`../ml-engineering/README.md`](ml-engineering/README.md) — feature pipelines feed train/val/test splitters.
- [`../visualization/README.md`](visualization/README.md) — data drift and distributions are visualized as figures.
- [`../project-tooling/README.md`](project-tooling/README.md) — ETL pipelines are packaged into Docker containers.
- [`../ai-output-judgement/README.md`](ai-output-judgement/README.md) — dataset cards are audited for PII and bias.

## Back to Master

← [Back to SkillStack README](../README.md)
