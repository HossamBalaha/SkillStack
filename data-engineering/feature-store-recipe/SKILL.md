---
name: feature-store-recipe
description: Build feature engineering pipelines with point-in-time correctness, versioned feature definitions, and synced offline (training) and online (inference) stores. Use this skill when joining features to labels without leakage, syncing low-latency online stores, or operationalising Feast/Hopsworks/Tecton feature views.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [feature-store, feast, hopsworks, point-in-time, online-features]
related: [data-engineering/feature-engineering-toolkit, data-engineering/etl-pipeline-builder]
prerequisites: []
outputs: [python]
difficulty: advanced
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Feature Store Recipe

## When To Use

- Training data must join historical features at a specific event timestamp (no future leakage).
- The same feature definition must serve both batch training and low-latency online inference.
- Features are versioned, reviewed, and reused across teams.
- Freshness matters: a model served at inference time needs features newer than the request.
- You are adopting Feast, Hopsworks, Tecton, or a homegrown offline/online pair.

## Workflow

1. Define feature views as code: entities, features, source, TTL, and aggregation windows.
2. Stamp every feature row with an `event_timestamp` and an entity key.
3. Materialise the offline store (Parquet/BigQuery) for historical joins.
4. Build point-in-time joins: for each label row, take the latest feature as-of the label time.
5. Materialise the online store (Redis/DynamoDB) with the latest value per entity.
6. Schedule a sync job that pushes fresh offline rows into the online store.
7. Emit freshness metrics: `max(event_timestamp)` per feature view, sampled every few minutes.
8. Alert when freshness exceeds the feature's declared TTL.
9. Version feature definitions in git and tag them per training run.

## Inputs

- Raw event tables or streams with entity id and event timestamp.
- Feature view definitions (Python module declaring entities and feature specs).
- Label table with entity id and event timestamp for point-in-time joins.
- Online store connection spec (Redis/DynamoDB/feature-store server).

## Outputs

- A versioned feature definition module checked into git.
- An offline materialised dataset (Parquet/warehouse table) for training.
- A populated online store keyed by entity for inference.
- A freshness dashboard plus alerting rules.

## Key Rules

- Point-in-time correctness: never let a feature row's `event_timestamp` exceed the label's.
- One feature definition drives both stores; duplication causes skew.
- Entities must be stable identifiers; never use mutable columns as entity keys.
- Online features expire after TTL; stale reads must be rejected, not served.
- Feature definitions live in code, not notebooks.
- Every materialisation run records its feature view version and source hash.
- Train and serve use the same transformations; no offline-only post-processing.

## Examples

```python
from datetime import timedelta


class UserPurchaseFeatureView:
  # Declaration of a feature view consumed by Feast or an equivalent store.
  Name = "user_purchase_features"
  EntityKey = "user_id"
  EventTimestampColumn = "event_at"
  Features = ["total_purchases_30d", "avg_order_value_30d", "days_since_last_purchase"]
  Window = timedelta(days=30)
  OnlineTtl = timedelta(hours=24)


def BuildPointInTimeJoin(labelDf, featureDf, entityKey, eventTsCol):
  # For each label row, attach the latest feature strictly before the label time.
  labelDf = labelDf.sort_values(eventTsCol)
  featureDf = featureDf.sort_values(eventTsCol)
  mergedDf = labelDf.merge(
    featureDf,
    on=entityKey,
    suffixes=("", "_feature"),
    direction="backward",
  )
  # Drop feature rows that leaked into the future.
  leakedMask = mergedDf[f"{eventTsCol}_feature"] >= mergedDf[eventTsCol]
  if (leakedMask.any()):
    mergedDf.loc[leakedMask, Features.Features] = None
  return mergedDf


def CheckFreshness(featureView, onlineStore, now):
  # Fail loudly if the newest feature is older than the declared TTL.
  latestEvent = onlineStore.GetLatestEventTs(featureView.Name)
  age = now - latestEvent
  if (age > featureView.OnlineTtl):
    raise FreshnessError(f"{featureView.Name} stale by {age}")
```
