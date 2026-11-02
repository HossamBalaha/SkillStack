---
name: prompt-template-library
description: Curate a reusable library of prompt templates organized by task family — summarization, translation, code generation, classification, extraction, and rewriting. Each template ships a name, description, template string, variables list, and a worked example. Use when you need an off-the-shelf, peer-reviewed prompt for a common task rather than rewriting one from scratch.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [templates, library, summarization, translation, code-generation, classification]
related: [prompt-engineering/few-shot-template-builder, prompt-engineering/system-prompt-architect, prompt-engineering/prompt-versioning-system]
prerequisites: []
outputs: [markdown, json, yaml]
difficulty: beginner
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Prompt Template Library

## When To Use

- You need a prompt for a common task (summarize, translate, classify, extract, rewrite) and want a vetted starting
  point.
- Your team keeps re-inventing the same prompts with subtle drift; you want a single canonical library.
- A new teammate asks "what prompt should I use for X?" and you want to point at one file.
- Trigger keywords: prompt library, template catalog, summarization prompt, translation prompt, extraction prompt.
- You want to A/B test variant templates on the same task.

## Workflow

1. Pick the task family from the six supported: `summarization`, `translation`, `code-generation`, `classification`,
   `extraction`, `rewriting`.
2. Open the corresponding template entry in `templates.json`.
3. Read the description, the variables list, and the worked example.
4. Substitute your concrete values for each variable.
5. (Optional) Append few-shot exemplars using the `few-shot-template-builder` skill — the templates are written to
   accept an `{{Examples}}` block.
6. Send the rendered prompt to the LLM.
7. Log which template id and version you used, so a regression later is traceable.
8. If the template underperforms, file a diff against the library rather than editing it in place.

## Inputs

- Task family name.
- The concrete values for the template's variables.
- (Optional) Few-shot exemplars rendered into the `{{Examples}}` block.

## Outputs

- `templates.json` — the library: one object per template with `Id`, `Family`, `Description`, `Variables`, `Template`,
  `Example`.
- `rendered_prompt.txt` — the prompt after variable substitution, ready to send.
- `usage_log.jsonl` — per call: template id, version, variables, model, tokens, latency.

## Key Rules

- Every template must declare its variables explicitly — no implicit placeholders.
- Every template must ship one worked example with concrete variable values.
- Templates must be versioned; edits create a new version, never overwrite.
- Templates must not hard-code provider-specific tokens (e.g., `<|im_start|>`) — those go in the compiler layer.
- One template per task family is the minimum; additional variants go under a `Variant` field.
- The library is read-only at runtime; edits happen via pull request.

## Examples

```json
{
  "Id": "summarization.abstract.v1",
  "Family": "summarization",
  "Description": "Summarize a document into a 3-sentence abstract suitable for a research index.",
  "Variables": ["Document", "MaxLength"],
  "Template": "Summarize the following document in at most {{MaxLength}} words as a 3-sentence abstract.\n\nDocument:\n{{Document}}\n\nAbstract:",
  "Example": {
    "Document": "Transformer models have revolutionized NLP...",
    "MaxLength": "60"
  }
}
```

```text
Library excerpt — extraction template:

Id: extraction.keyterms.v1
Family: extraction
Description: Extract the top-N key terms from a document, returned as a JSON array.
Variables: ["Document", "TopN"]
Template:
  Extract the top {{TopN}} key terms from the document below.
  Return a JSON array of strings, no other text.
  Document: {{Document}}
  Key terms:
Example:
  Document: "Batch normalization stabilizes training of deep networks."
  TopN: "3"
  Output: ["batch normalization", "training stability", "deep networks"]
```

```python
def RenderTemplate(TemplateEntry, VariableValues):
  # Start from the template string declared in the entry.
  Rendered = TemplateEntry["Template"]
  # Substitute each declared variable with its concrete value.
  for Variable in TemplateEntry["Variables"]:
    # Look up the value provided by the caller.
    Value = VariableValues[Variable]
    # Replace the placeholder with the value.
    Rendered = Rendered.replace("{{" + Variable + "}}", str(Value))
  # Return the final prompt string.
  return Rendered
```

## References

- OpenAI Prompt Examples: https://platform.openai.com/docs/examples
- LangChain PromptHub: https://smith.langchain.com/hub
- PromptingGuide.ai templates: https://www.promptingguide.ai/
- Companion skills: `few-shot-template-builder`, `system-prompt-architect`, `prompt-versioning-system`.
