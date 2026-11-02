---
name: results-table-formatter
description: Format experimental results tables in booktabs style with significance markers, confidence intervals, and bold best entries. Trigger when finalising a results section, ablation table, or benchmark comparison for a manuscript.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [table, booktabs, significance, ci, ablation]
related: [visualization/figure-caption-writer, visualization/publication-figure-maker]
prerequisites: []
outputs: [latex, markdown]
difficulty: intermediate
estimated_tokens: 900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Results Table Formatter

## When To Use
- Building a benchmark comparison table for a paper or report.
- Summarising ablation results across multiple model variants.
- Reporting metrics with statistical significance markers and 95% CIs.
- Exporting the same table to both LaTeX and CSV.

## Workflow
1. Collect raw metric rows from experiment logs.
2. Compute mean and 95% confidence interval per metric per model.
3. Determine the best result per column and mark it bold.
4. Attach significance markers based on a p-value threshold.
5. Round metrics to three decimals and p-values to four decimals.
6. Emit a LaTeX `booktabs` table block with multi-row headers.
7. Emit a parallel CSV with the same numbers for downstream tooling.
8. Verify that bold, CI, and significance glyphs survive the LaTeX compile.

## Inputs
- A dataframe of metric rows (model, dataset, metric, mean, std, n).
- A significance threshold and the reference model for paired tests.
- A list of metrics and the rounding policy (3 for metrics, 4 for p-values).

## Outputs
- A LaTeX `table` environment using `booktabs` macros.
- A CSV file mirroring every numeric cell.
- A short log noting the best model per metric.

## Key Rules
- Use `\toprule`, `\midrule`, `\bottomrule`; never `\hline`.
- Headers may use `\multirow` and `\multicolumn`; keep alignment consistent.
- Significance markers are `*` for p<0.05, `**` for p<0.01, `***` for p<0.001.
- 95% CI columns report `mean +/- CI`, not `mean +/- std`.
- Best result per column is bolded with `\textbf{}`.
- Metrics round to 3 decimals; p-values round to 4 decimals.

## Examples
```python
# Format a results row with CI, significance, and bold best.
def FormatCell(meanValue, ciValue, pValue, isBest):
  # Round metrics to three decimals per house style.
  text = f"{meanValue:.3f} \\pm {ciValue:.3f}"
  if (pValue < 0.001):
    text = text + "***"
  elif (pValue < 0.01):
    text = text + "**"
  elif (pValue < 0.05):
    text = text + "*"
  # Bold the best cell in the column.
  if (isBest):
    text = "\\textbf{" + text + "}"
  return text

def EmitLatexTable(rows, bestIndex):
  # Build a booktabs table from a list of metric rows.
  lines = []
  lines.append("\\begin{tabular}{lccc}")
  lines.append("\\toprule")
  lines.append("Model & Accuracy & F1 & p-value \\\\")
  lines.append("\\midrule")
  for (i, row) in enumerate(rows):
    cell = FormatCell(row["Accuracy"], row["Ci"], row["PValue"], (i == bestIndex))
    line = f"{row['Model']} & {cell} & {row['F1']:.3f} & {row['PValue']:.4f} \\\\"
    lines.append(line)
  lines.append("\\bottomrule")
  lines.append("\\end{tabular}")
  return "\n".join(lines)
```

## References
- booktabs LaTeX package: https://ctan.org/pkg/booktabs
- multirow LaTeX package: https://ctan.org/pkg/multirow
