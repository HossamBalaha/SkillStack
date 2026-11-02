---
name: execution-protocol
description: Apply a 10-stage meta-discipline wrapper around any complex multi-step task to guarantee comprehension, surgical edits, fact verification, and clean delivery. Use when the task spans multiple files, requires behavioral changes, or carries high risk of placeholder output and fabrication.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [meta-discipline, workflow, verification, multi-step, protocol]
related: [style-integrity/planning-note-logger, style-integrity/silent-omission-protocol, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [markdown]
difficulty: advanced
estimated_tokens: 830
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Execution Protocol

## When To Use
- User issues a complex task with multiple sub-objectives.
- Task modifies existing code or documents where preservation of style matters.
- A task carries high risk of fabricated references, broken signatures, or placeholder output.
- Agent must deliver concrete edits rather than suggestions.
- User explicitly invokes "execution protocol" or "10-stage" workflow.

## Workflow
1. **Comprehend.** Read every relevant file in full. Do not skim. Note structure, conventions, dependencies, and existing patterns.
2. **Clarify.** If critical context is missing, ask ONE targeted question. Otherwise, state explicit assumptions in the delivery note.
3. **Define Success.** Translate the request into a concrete, verifiable success criterion. Each criterion must be checkable (e.g., "all tests pass", "no `\textit{}` remains").
4. **Plan.** Write a step → verification plan: for each planned edit, state how it will be checked afterward.
5. **Preserve.** Make surgical changes only. Match existing code style, naming, indentation, and idioms. Never refactor tangential code.
6. **Implement.** Apply edits directly to files. Never return placeholders like `// TODO` or `[INSERT HERE]`.
7. **Verify Facts.** Re-check every file path, function signature, API endpoint, and citation against the actual source — not memory.
8. **Self-Judge.** Attack the solution for edge cases. Ask: what breaks under empty input? Under concurrent access? Under missing dependencies?
9. **Refine.** Fix discovered flaws quietly without narrating each fix.
10. **Deliver.** Output exact file paths changed. State residual risks in ONE line. No preamble, no summary, no recap.

## Inputs
- The user's task description.
- All referenced files and repositories.
- Existing project conventions (style guides, config files, test suites).

## Outputs
- Concrete file edits in place.
- A delivery block listing exact paths changed.
- A one-line residual-risk statement.
- An optional "Planning Note" when assumptions were made or data was missing.

## Key Rules
- Read every relevant file before editing — no skimming.
- Ask at most ONE clarifying question; otherwise state assumptions.
- Apply surgical edits only. Match existing style exactly.
- Never return placeholders. Every edit must be real and complete.
- Re-verify paths, signatures, APIs against actual source.
- Deliver without preamble: paths, then one-line residual risk.
- The 10 stages are executed in order; do not skip or merge stages.
- Self-judgment must consider edge cases: empty input, missing dependencies, concurrent access.

## Examples

Input task:
```
Add a CLI option `--output-format` to scripts/Run.py that accepts
"json" or "csv".
```

Delivery block:
```
Files changed:
- /home/z/my-project/scripts/Run.py  (added --output-format argument)

Residual risk: existing callers that do not pass --output-format
default to "csv", matching prior behavior. No breaking change.

Planning Note:
- Assumed default "csv" because existing tests expect CSV output.
- If JSON should be the default, confirm and re-run.
```

Anti-example (forbidden output):
```
Updated scripts/Run.py. The changes look good! Let me know if you need
anything else. [TODO: implement the JSON path].
```
This output violates stages 6 (placeholder) and 10 (preamble, no residual-risk line).

## References
- The clean-code and "boy-scout rule" traditions (Robert C. Martin).
- Software engineering best practices on surgical edits and regression safety.
- Academic writing traditions on factual verification and reproducible audit trails.
