---
name: figure-caption-writer
description: Write publication-ready figure captions explaining what the figure shows, how the methodology produced it, and why it validates the framework. Trigger when finalising manuscript figures, theses, or technical reports.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: visualization
tags: [caption, manuscript, figure, publication, writing]
related: [visualization/publication-figure-maker, visualization/multi-panel-figure-composer]
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

# Figure Caption Writer

## When To Use
- Drafting captions for manuscript figures during revision.
- Tightening a thesis chapter's figure captions to a house style.
- Adding captions to a technical report's figures.
- Ensuring each figure stands alone without the surrounding text.
- Standardising caption voice and length across a multi-author paper.

## Workflow
1. Inspect the figure and list its visual elements.
2. State WHAT the figure shows in one or two sentences.
3. State HOW the methodology produced the visualization.
4. State WHY it supports the framework's claim or utility.
5. Reference methods and equations via `\ref{}` and `\eqref{}`.
6. Define every abbreviation on first use within the caption.
7. Keep length consistent across figures in the same paper.
8. Cross-check every reference resolves after the final compile.
9. Log every caption in a central file so revisions stay in sync.

## Inputs
- The figure file or its description.
- The methods section to reference for HOW and WHY.
- A list of abbreviations and their expansions.

## Outputs
- A LaTeX caption block ready to paste into the figure environment.
- A plain-text caption for the supplementary README.
- A checklist of references used in the caption for verification.

## Key Rules
- Each caption covers WHAT, HOW, and WHY.
- Reference methods and equations via `\ref{}` and `\eqref{}`.
- Define every abbreviation on first use.
- Keep the caption self-contained; readers skip the body.
- Match caption length across figures in the same paper.
- Avoid restating the title in the caption.

## Examples
```python
# Assemble a caption from structured fields.
def BuildCaption(fields):
  # WHAT the figure shows.
  what = fields["What"]
  # HOW the methodology produced the visualization.
  how = f"Method: {fields['Method']} (Sec.~\\ref{{sec:method}})."
  # WHY it validates the framework's claim.
  why = f"This confirms {fields['Claim']} (Eq.~\\eqref{{eq:{fields['Equation']}}})."
  # Define abbreviations on first use.
  abbr = ", ".join([f"{a} ({full})" for (a, full) in fields["Abbreviations"].items()])
  caption = f"{what} {how} {why} Abbreviations: {abbr}."
  return caption

fields = {
  "What": "Training and validation loss over 200 epochs for the proposed model.",
  "Method": "stochastic gradient descent with cosine annealing",
  "Claim": "convergence within the first 100 epochs",
  "Equation": "loss",
  "Abbreviations": {"SGD": "stochastic gradient descent"}
}
print(BuildCaption(fields))

# Verify that every \ref target actually resolves in the manuscript.
def CheckReferences(caption, labelSet):
  # Extract every \ref{...} and \eqref{...} target from the caption.
  import re
  targets = re.findall(r"\\(?:eq)?ref\{([^}]+)\}", caption)
  missing = [t for t in targets if t not in labelSet]
  # Fail loudly so broken captions never reach the publisher.
  if (missing):
    raise ValueError(f"Unresolved references: {missing}")
  return True
```

## References
- Nature author guide on figure captions: https://www.nature.com/nature/for-authors/final-submission
