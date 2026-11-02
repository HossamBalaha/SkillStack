---
name: jupyter-to-script-converter
description: "Convert a `.ipynb` notebook into a clean `.py` module by stripping metadata, extracting code cells into named functions, removing `display()` calls and `!` shell escapes, preserving cell outputs as `# Output:` comments, adding a module docstring, and wrapping runnable code in `if __name__ == \"__main__\":`. Use this when promoting an exploratory notebook into production source. Triggers: nbconvert, ipynb to py, notebook to script, clean notebook export."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [jupyter, nbconvert, notebook, refactoring]
related: [project-tooling/pytest-scientific-suite, project-tooling/makefile-generator]
prerequisites: []
outputs: [python, bash]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Jupyter To Script Converter

## When To Use
- An exploratory notebook has matured and you want to promote it to a versioned `.py` module.
- You need to remove `display(...)`, `!pip install`, `!ls`, and other cell-magic noise before committing.
- You want cell outputs preserved as `# Output:` comments so reviewers see results without rerunning.
- You want a runnable `if __name__ == "__main__":` block at the bottom.

## Workflow
1. Parse the `.ipynb` JSON; ignore the `metadata`, `nbformat`, and `kernelspec` blocks.
2. Walk the `cells` list; for each code cell, collect its `source` lines.
3. Strip lines starting with `!` (shell escapes), `%` (magics), `display(`, `IPython.display`, and bare `!`.
4. Detect top-level function or class definitions; promote each to a top-level `def`/`class`.
5. Wrap any remaining free-standing code into a `def Main():` function.
6. Add an `if __name__ == "__main__": Main()` block at the bottom.
7. For each cell that has `outputs`, append `# Output:` followed by the captured text.
8. Add a module docstring at the top stating the notebook's origin and conversion date.
9. Optionally run `ruff` and `black` on the result to normalise formatting.
10. Save as `<NotebookName>.py` next to the original (or in `src/` if requested).

## Inputs
- The `.ipynb` file path.
- An optional output directory (default: same folder as the notebook).
- A flag to keep or drop `# Output:` comments (default: keep).

## Outputs
- A clean `<NotebookName>.py` module with docstring, functions, `Main`, and `__main__` guard.
- A small conversion report listing how many cells were merged, dropped, or wrapped.

## Key Rules
- Never commit the notebook's raw JSON metadata into the `.py` file.
- All `!shell` escapes and `%magics` are dropped silently — record them in the conversion report.
- `display(...)` calls are removed; if a return value matters, reassign it explicitly.
- Every function gets a docstring (even a one-liner) — no bare `def`.
- The `if __name__ == "__main__":` guard is mandatory at the bottom.
- Preserve the original cell order so the narrative flow survives.
- Run `ruff check --fix` and `black` on the output so it matches repo style.

## Examples
Using `nbconvert`:

```bash
# Convert notebook to a plain script, then hand-clean.
jupyter nbconvert --to script notebooks/Analysis.ipynb --output Analysis
```

Manual parser:

```python
# ConvertNotebook.py — turn an .ipynb into a clean .py module.
import json
import re
import sys


def ShouldDropLine(line):
  # Drop shell escapes, magics, display calls, and IPython imports.
  stripped = line.lstrip()
  if (stripped.startswith("!") or stripped.startswith("%")):
    return True
  if (stripped.startswith("display(") or "IPython.display" in stripped):
    return True
  return False


def CellToSource(cell):
  source = "".join(cell.get("source", []))
  cleaned = [line for line in source.splitlines() if (not ShouldDropLine(line))]
  return "\n".join(cleaned)


def Convert(notebookPath, outputPath):
  with open(notebookPath, "r", encoding="utf-8") as handle:
    nb = json.load(handle)
  cells = nb.get("cells", [])
  codeCells = [c for c in cells if (c.get("cell_type") == "code")]
  chunks = [CellToSource(c) for c in codeCells]
  body = "\n\n# ---\n\n".join(chunks)
  header = '"""Module converted from notebook: %s."""\n' % notebookPath
  mainWrap = "\n\n\ndef Main():\n%s\n\n\nif (__name__ == \"__main__\"):\n  Main()\n"
  indentedBody = "\n".join("  " + line if line else "" for line in body.splitlines())
  with open(outputPath, "w", encoding="utf-8") as handle:
    handle.write(header + mainWrap % indentedBody)
  print(f"Wrote {outputPath}")


if (__name__ == "__main__"):
  Convert(sys.argv[1], sys.argv[2])
```

Post-conversion cleanup:

```bash
# Normalise the converted module to repo style.
ruff check --fix Analysis.py
black Analysis.py
```

## References
- `nbconvert` script exporter — https://nbconvert.readthedocs.io
- `.ipynb` JSON schema — https://nbformat.readthedocs.io
- `ruff` — https://docs.astral.sh/ruff/
