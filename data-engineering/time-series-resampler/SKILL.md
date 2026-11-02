---
name: time-series-resampler
description: Resample time series to a new frequency (minute to hourly mean), apply forward fill, backward fill, and interpolation (linear, spline), align multiple series to a common index, and handle irregular timestamps. Use this skill when preparing sensor, log, or financial series for downstream models.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [time-series, resampling, interpolation, forward-fill, alignment]
related: [data-engineering/missing-data-imputer, data-engineering/data-quality-validator]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1100
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Time Series Resampler

## When To Use

- A series arrives at an irregular cadence and must be aligned to a fixed grid.
- Multiple series must share a common index before being joined or stacked.
- Forward fill, backward fill, or interpolation is needed to fill gaps.
- Aggregation rules differ per column (mean for prices, sum for counts, last for flags).
- The series is large enough that resampling must happen in chunks.

## Workflow

1. Parse the timestamp column into a datetime with explicit timezone.
2. Sort by timestamp; drop duplicate timestamps keeping the latest observation.
3. Set the timestamp as the index.
4. Pick the target frequency (e.g., `1H`, `5min`, `1D`).
5. Apply `resample` with a per-column aggregation map.
6. Fill gaps with the chosen strategy: ffill, bfill, linear, spline, or none.
7. Align multiple series by reindexing onto the union of timestamps.
8. Validate: no NaT in the index, no gaps beyond the chosen fill window.
9. Emit metadata: original cadence, target cadence, rows in/out, fill counts.

## Inputs

- The time series (DataFrame with a datetime column or index).
- Target frequency string (pandas offset alias).
- Per-column aggregation map (sum, mean, last, max, min, count).
- Fill strategy (ffill, bfill, linear, spline, none) and max gap to fill.

## Outputs

- A resampled DataFrame on the target frequency grid.
- A metadata JSON capturing original and target cadence plus fill counts.
- Optional alignment report when multiple series are joined.

## Key Rules

- Timestamps are parsed with explicit timezone; never naive unless source is naive.
- Duplicate timestamps are collapsed keeping the latest observation.
- Fill strategies cap the max gap; longer gaps stay as NaN.
- Aggregation is per column; mixed rules in one call are supported via a dict.
- The output index is monotonic increasing with no duplicates.
- Metadata accompanies the resampled output for downstream audit.

## Examples

```python
import pandas as pd


def ParseTimestamps(df, tsColumn, timezone="UTC"):
  # Coerce the timestamp column into tz-aware datetimes.
  df[tsColumn] = pd.to_datetime(df[tsColumn], utc=True).dt.tz_convert(timezone)
  df = df.drop_duplicates(subset=tsColumn, keep="last").sort_values(tsColumn)
  return df.set_index(tsColumn)


def ResampleSeries(df, targetFreq, aggMap, fillStrategy="ffill", maxGap=3):
  # Aggregate per column to the target frequency and fill gaps.
  resampled = df.resample(targetFreq).agg(aggMap)
  if (fillStrategy == "ffill"):
    resampled = resampled.ffill(limit=maxGap)
  elif (fillStrategy == "bfill"):
    resampled = resampled.bfill(limit=maxGap)
  elif (fillStrategy == "linear"):
    resampled = resampled.interpolate(method="linear", limit=maxGap)
  elif (fillStrategy == "spline"):
    resampled = resampled.interpolate(method="spline", order=3, limit=maxGap)
  return resampled


def AlignSeries(seriesList, targetFreq):
  # Reindex every series onto a common grid defined by the union of timestamps.
  unionIndex = None
  for series in seriesList:
    if (unionIndex is None):
      unionIndex = series.index
    else:
      unionIndex = unionIndex.union(series.index)
  aligned = []
  for series in seriesList:
    aligned.append(series.reindex(unionIndex).ffill(limit=3))
  return aligned


def EmitMetadata(originalDf, resampledDf, targetFreq):
  return {
    "OriginalRows": len(originalDf),
    "ResampledRows": len(resampledDf),
    "TargetFrequency": targetFreq,
    "FillCount": int(resampledDf.isna().sum().sum()),
  }
```

## References

- pandas resample: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html
- pandas asfreq: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.asfreq.html
- pandas reindex: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reindex.html
