---
name: output-format-enforcer
description: Enforce structured output from LLMs using JSON schema prompting, function calling, regex-constrained decoding, or Pydantic model prompting so downstream parsers never see malformed output. Use when the model's output feeds another program, when you need typed fields and not free text, or when a single malformed response breaks the pipeline.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [json-schema, function-calling, structured-output, pydantic, llm]
related: [prompt-engineering/system-prompt-architect, prompt-engineering/few-shot-template-builder, prompt-engineering/prompt-testing-harness]
prerequisites: []
outputs: [python, json, yaml]
difficulty: intermediate
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Output Format Enforcer

## When To Use

- The model's output feeds another program that needs typed fields, not free text.
- A single malformed response (trailing comma, missing key) breaks the pipeline.
- You are calling a tool-using model and need function-call arguments validated against a schema.
- Trigger keywords: JSON schema, function calling, structured output, regex decoding, Pydantic, Outlines, Guidance.
- You want a single enforcement strategy that works across providers.

## Workflow

1. Define the output schema as a JSON Schema (or a Pydantic model compiled to JSON Schema).
2. Pick the enforcement mechanism, in descending order of strictness:
   (a) **Regex-constrained decoding** — the sampler only emits tokens matching a grammar (Outlines, Guidance, llama.cpp
   GBNF). Strictest; works for open-weight models. (b) **Function/tool calling** — pass the schema as a tool definition;
   the model returns structured arguments (OpenAI, Anthropic, Gemini). Works for hosted models. (c) **Schema
   prompting** — paste the JSON Schema into the prompt and demand valid JSON. Weakest; needs a fallback parser.
3. If using (c), add a **repair step**: on JSON parse failure, send the broken output back to the model with the parse
   error and ask for a corrected version. Cap repair attempts at 2.
4. Always validate the parsed object against the schema with `jsonschema.validate` or Pydantic — never trust the model's
   claim of validity.
5. For lists and nested objects, prefer function calling over schema prompting — nesting is where prompting breaks.
6. Log every parse failure with the raw output and the parse error so failure modes are visible.
7. Add a unit test that feeds a known-bad output through the repair step and confirms it produces a valid object.

## Inputs

- The output schema (JSON Schema file or Pydantic model class).
- The prompt template that asks for the structured output.
- The enforcement mechanism choice (regex / function calling / schema prompting).
- (Optional) The model provider's function-calling config.

## Outputs

- `schema.json` — the JSON Schema the model must satisfy.
- `enforcer.py` — the function that calls the model, parses, validates, and (if needed) repairs.
- `parse_failures.jsonl` — per failure: raw output, parse error, repair attempts, final outcome.
- `test_enforcer.py` — unit tests with known-good and known-bad outputs.

## Key Rules

- Always validate against the schema after parsing — never trust the model's claim of validity.
- Cap repair attempts at 2 — a model that cannot produce valid JSON in 2 tries is broken; surface the failure.
- Prefer regex-constrained decoding for open-weight models; it is the only mechanism that guarantees validity.
- Prefer function calling over schema prompting for hosted models — nesting breaks prompting.
- Log every parse failure with the raw output — failure modes are invisible without this log.
- The schema must declare required fields explicitly; optional fields must be marked `required: false` or omitted from
  `required`.

## Examples

```text
JSON Schema (event extraction):
{
  "type": "object",
  "properties": {
    "Events": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Date": {"type": "string", "format": "date"},
          "Title": {"type": "string"},
          "Location": {"type": "string"}
        },
        "required": ["Date", "Title"]
      }
    }
  },
  "required": ["Events"]
}
```

```python
import json
import jsonschema

def EnforceStructuredOutput(RawOutput, Schema, MaxRepairAttempts=2):
  # Try to parse and validate the raw output, repairing up to MaxRepairAttempts times.
  for Attempt in range(MaxRepairAttempts + 1):
    # Parse the raw output as JSON.
    try:
      Parsed = json.loads(RawOutput)
      # Validate the parsed object against the schema.
      jsonschema.validate(Parsed, Schema)
      # Return the validated object on success.
      return Parsed
    except (json.JSONDecodeError, jsonschema.ValidationError) as Error:
      # If we have retries left, ask the model to repair the output.
      if (Attempt < MaxRepairAttempts):
        RawOutput = CallModelForRepair(RawOutput, str(Error), Schema)
      else:
        # Surface the failure after exhausting repair attempts.
        raise
```

## References

- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- Anthropic Tool Use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Outlines — structured generation: https://github.com/outlines-dev/outlines
- Guidance — constrained generation: https://github.com/guidance-ai/guidance
- Pydantic: https://docs.pydantic.dev/
- JSON Schema specification: https://json-schema.org/
- Companion skills: `system-prompt-architect`, `few-shot-template-builder`, `prompt-testing-harness`.
