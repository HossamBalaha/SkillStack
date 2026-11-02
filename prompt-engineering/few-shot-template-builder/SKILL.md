---
name: few-shot-template-builder
description: Construct few-shot prompt templates with consistent input/output formatting, deliberate delimiter choices, and principled example-selection strategies (random, diverse, hardest, or similarity-based). Use when you need reproducible few-shot prompts across a project, when exemplar selection matters more than the instruction text, or when the same task must run against multiple LLMs with stable formatting.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [few-shot, templates, exemplars, prompt-engineering, llm]
related: [prompt-engineering/system-prompt-architect, prompt-engineering/prompt-template-library, prompt-engineering/prompt-testing-harness]
prerequisites: []
outputs: [markdown, json, python]
difficulty: beginner
estimated_tokens: 1300
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Few-Shot Template Builder

## When To Use

- You have a task where 2-10 labelled exemplars noticeably improve accuracy over zero-shot.
- Exemplar formatting drifts between runs (different separators, different field orders) and breaks reproducibility.
- You need to compare exemplar selection strategies on the same task.
- Trigger keywords: few-shot, in-context learning, exemplar selection, k-shot, prompt template, ICL.
- The same task runs against multiple model providers and you want one template that compiles to each.

## Workflow

1. Define the task's input fields (e.g., `Question`, `Context`) and output fields (e.g., `Answer`, `Confidence`).
2. Pick a delimiter scheme that cannot collide with field content: triple quotes for text fields, JSON for structured
   fields, or XML tags for nested content.
3. Pick an exemplar selection strategy:
   (a) **Random** — sample K exemplars from the labelled pool per run; useful for variance estimation. (b) **Diverse** —
   cluster the labelled pool and pick one exemplar per cluster to cover the input space. (c) **Hardest** — pick
   exemplars the model most often gets wrong in isolation, to anchor on edge cases. (d) **Similarity** — pick exemplars
   whose embeddings are closest to the test input (kNN ICL).
4. Write the template as a string with `{{Input}}` and `{{Output}}` placeholders per exemplar.
5. Append a final `{{Input}}` (with no output) for the test question so the model completes it.
6. Enforce label balance across exemplars — a skewed label distribution biases the model toward the majority class.
7. Pin exemplar order (or shuffle it as an explicit ablation) — order shifts accuracy by several points.
8. Build a compile step that renders the template with the chosen exemplars and the test input into one string per
   provider.
9. Write a unit test that round-trips the template: render it, parse the model's completion, and verify the field
   structure.

## Inputs

- A labelled exemplar pool with at least 2K exemplars (K = number of exemplars per prompt).
- The test input(s) to answer.
- Template parameters: delimiter, number of exemplars, selection strategy, order policy.
- (Optional) Embedding model for similarity-based selection.

## Outputs

- `template.txt` — the prompt template with `{{Input}}`/`{{Output}}` placeholders.
- `exemplars.json` — the selected exemplars, with the selection strategy and seed.
- `compiled_prompt.txt` — the rendered prompt ready to send to the LLM.
- `compile.py` — the function that renders the template given exemplars and a test input.
- `test_compile.py` — round-trip unit tests for the template.

## Key Rules

- Use one delimiter scheme across all exemplars and the test input — mixing delimiters is the #1 source of template
  bugs.
- Append the test input as `{{Input}}` only (no `{{Output}}`) so the model completes it.
- Exemplar labels must be balanced — skewed distributions bias predictions.
- Pin exemplar order and the random seed; order shifts accuracy and you must be able to reproduce it.
- Hard-code the delimiter strings in one constant so they cannot drift across files.
- The template must render to a single string per provider, with provider-specific start/stop tokens handled outside the
  template.

## Examples

```text
Template (delimiter: triple quotes):

Example 1
Input: \"\"\"What is 2 + 2?\"\"\"
Output: \"\"\"4\"\"\"

Example 2
Input: \"\"\"What is 7 - 3?\"\"\"
Output: \"\"\"4\"\"\"

Example 3
Input: \"\"\"{{TestInput}}\"\"\"
Output:
```

```python
def CompileFewShotPrompt(Template, Exemplars, TestInput):
  # Build the exemplar block by rendering each exemplar through the template.
  Blocks = []
  # Iterate over the exemplars and render each one.
  for Exemplar in Exemplars:
    # Substitute the exemplar's input and output into the template.
    Block = Template.replace("{{Input}}", Exemplar["Input"]).replace("{{Output}}", Exemplar["Output"])
    # Append the rendered block to the list.
    Blocks.append(Block)
  # Append the test input with an empty output to elicit completion.
  TestBlock = Template.replace("{{Input}}", TestInput).replace("{{Output}}", "")
  # Join all blocks and return the compiled prompt.
  return "\n\n".join(Blocks) + "\n\n" + TestBlock
```

## References

- Brown, T. et al. (2020). "Language Models are Few-Shot Learners." (GPT-3 in-context learning)
  https://arxiv.org/abs/2005.14165
- Liu, J. et al. (2022). "What Makes Good In-Context Examples for Large Language Models?"
  https://arxiv.org/abs/2301.12785
- Zhao, T. et al. (2021). "Calibrate Before Use: Improving Few-Shot Performance of Language Models."
  https://arxiv.org/abs/2102.09690
- Companion skills: `prompt-template-library`, `prompt-testing-harness`, `system-prompt-architect`.
