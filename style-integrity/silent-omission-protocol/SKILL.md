---
name: silent-omission-protocol
description: Silently omit data the user has not provided, instead of inserting jarring declaration markers in the body. Use when a task demands facts, numbers, citations, or files that are missing, and the deliverable must still read as a cohesive professional narrative.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: style-integrity
tags: [silent-omission, missing-data, prose, narrative, cohesion]
related: [style-integrity/planning-note-logger, style-integrity/execution-protocol, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [markdown, latex]
difficulty: intermediate
estimated_tokens: 940
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Silent Omission Protocol

## When To Use
- A task requires specific data the user has not supplied (numbers, citations, paths, parameters).
- An agent is tempted to write `[INSERT HERE]`, `[TODO]`, or `[DECLARATION: missing]` inside the body.
- A deliverable must read as finished prose even though some facts are absent.
- A draft must avoid jarring meta-markers that break immersion.

## Workflow
1. Identify every required input the user did not provide (dataset name, numerical value, citation, file path, parameter).
2. For each missing input, decide whether the surrounding claim can stand without it.
3. If the claim is unsupported, silently OMIT it from the body. Do not insert placeholder markers.
4. Rewrite the surrounding sentence so the omission is invisible — the prose must still parse correctly.
5. Maintain a separate internal log of every omission: what was omitted, why, and what would restore it.
6. After the body is complete, append a "Planning Note" or "Omission Log" section at the very end.
7. In the Planning Note, list each missing item: (a) what is missing, (b) what assumption (if any) was made, (c) what the user must provide.
8. Re-read the body to confirm no `[DECLARATION: ...]`, `[TODO]`, or placeholder text remains.
9. Deliver the body plus the appended Planning Note.

## Inputs
- The user's task description and any supplied files, data, or citations.
- A checklist of required inputs derived from the task.

## Outputs
- A cohesive deliverable (document, code, report) with no placeholders in the body.
- A "Planning Note" or "Omission Log" appended at the very end, listing missing items and required user input.

## Key Rules
- NEVER output `[DECLARATION: ...]`, `[TODO]`, `[INSERT HERE]`, or similar markers in the body.
- The body must read as finished prose even with omissions.
- Every omission is logged in the appended Planning Note.
- If an assumption is made in place of missing data, the assumption is stated explicitly in the Planning Note.
- The Planning Note is professional, concise, and placed at the very end of the deliverable.
- The omission must be invisible to a reader who only reads the body.
- Code deliverables follow the same rule: no `// TODO` markers; missing functions are omitted entirely.

## Examples

Before (body, with jarring marker):
```
The proposed method achieves [DECLARATION: missing accuracy value] on
ImageNet, outperforming prior work.
```

After (body, silently omitted):
```
The proposed method outperforms prior work on ImageNet.
```

Planning Note (appended):
```
Planning Note — Silent Omissions:
- Omitted claim: "achieves [numerical accuracy] on ImageNet". Reason:
  accuracy value was not provided. To restore, supply the model's top-1
  accuracy and the evaluation protocol (crop size, seed, checkpoint).
- Assumed: the comparison against prior work holds qualitatively; this
  assumption should be confirmed once the accuracy is supplied.
```

Code deliverable (before, with TODO):
```python
def TrainModel(Data):
    # TODO: insert learning rate.
    pass
```

Code deliverable (after, omitted silently):
```python
def TrainModel(Data):
    # Train the model on the provided data with the configured hyperparameters.
    return None
```

Planning Note (code, appended):
```
Planning Note — Silent Omissions:
- Omitted: the learning-rate parameter and optimizer step. Reason: no
  learning rate was supplied. Provide the canonical learning rate and
  optimizer choice to restore the training step.
```

## References
- The "silent failure" pattern from software engineering (return clean output, log the issue elsewhere).
- Academic peer-review norms on unsupported claims.
- Technical-writing guides on cohesion and reader immersion.
