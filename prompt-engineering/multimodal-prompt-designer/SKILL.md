---
name: multimodal-prompt-designer
description: Design multimodal prompts that fuse image and text inputs, interleave modalities, and frame vision-language tasks (VQA, captioning, document understanding, chart reading). Use when an LLM accepts images and the task requires reasoning over both pixels and prose, when the order of image vs. text tokens affects accuracy, or when you must instruct the model to ground claims in specific image regions.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [multimodal, vision-language, vqa, image-text, llm]
related: [prompt-engineering/rag-prompt-designer, prompt-engineering/system-prompt-architect, prompt-engineering/output-format-enforcer]
prerequisites: []
outputs: [markdown, json, python]
difficulty: advanced
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

# Multimodal Prompt Designer

## When To Use

- The model accepts images and the task needs reasoning over pixels and prose (VQA, chart reading, OCR, document QA).
- The order of image vs. text tokens in the prompt affects the answer.
- You need the model to ground a claim in a specific region of the image ("the red box on the left").
- Trigger keywords: multimodal, vision-language, VQA, image+text, GPT-4V, LLaVA, image grounding.
- You want a single prompt template that works across multimodal providers.

## Workflow

1. Confirm the model's image input limits: max number of images per turn, max resolution, supported formats (PNG, JPEG,
   WebP).
2. Decide the modality order: image-first (image tokens before the text instruction), text-first, or interleaved (text,
   image, text). Recent models are more accurate when the instruction comes after the image.
3. Write the instruction in three parts: (a) what the image shows in general, (b) the specific question or task, (c) the
   output format.
4. For grounding tasks, ask the model to reference image regions by ordinal ("the third object from the left") rather
   than coordinates — coordinate accuracy is unreliable without bounding-box tooling.
5. For multi-image tasks (e.g., compare two charts), label each image explicitly: "Image 1:", "Image 2:" and ask the
   model to reference the label.
6. Add a fallback clause: "If the image is too low-resolution to answer, reply exactly: `Image insufficient.`"
7. Cap image resolution at the model's native input size to avoid silent downsampling that drops fine detail.
8. Log the modality order, image count, and per-image resolution alongside the response so accuracy regressions are
   traceable.

## Inputs

- One or more images (file paths or URLs) within the model's limits.
- The instruction text (question, task, output format).
- The model's multimodal constraints (max images, max resolution, supported formats).
- (Optional) A gold answer for evaluation.

## Outputs

- `prompt_template.json` — variables: `Images`, `Instruction`, `ModalityOrder`, `OutputFormat`.
- `compiled_prompt.json` — the rendered multimodal prompt with image references and text.
- `eval_cases.jsonl` — per case: images, instruction, model response, gold, grounded flag.
- `modality_report.md` — accuracy by modality order and by image count.

## Key Rules

- Modality order affects accuracy — pin it and report it in every eval.
- For grounding, prefer ordinal references ("the leftmost object") over pixel coordinates — coordinates are unreliable
  without bounding-box tooling.
- Label multi-image inputs explicitly so the model can reference the right image.
- Cap image resolution at the model's native input size to avoid silent downsampling.
- Always include an "image insufficient" fallback so low-resolution inputs produce a known signal, not a hallucination.
- Log the image count and modality order per call — without them, multimodal regressions are unexplainable.

## Examples

```text
Multimodal prompt (image-first, grounding):

[Image: chart of monthly sales, Jan-Dec]

This image is a bar chart of monthly sales for 2024.
Question: Which month had the largest month-over-month drop, and by how much?
Output format: JSON {"Month": "<string>", "DropAmount": <number>, "PreviousMonthSales": <number>, "MonthSales": <number>}.
If the image is too low-resolution to read the values, reply exactly: Image insufficient.
```

```python
def CompileMultimodalPrompt(Images, Instruction, ModalityOrder="image-first"):
  # Build the content blocks in the requested modality order.
  Blocks = []
  # Place image blocks first when the order is image-first.
  if (ModalityOrder == "image-first"):
    # Iterate over the images and append each one as a block.
    for Index, Image in enumerate(Images):
      # Append the image with an explicit label.
      Blocks.append({"Type": "image", "Label": f"Image {Index + 1}", "Path": Image})
    # Append the instruction after the images.
    Blocks.append({"Type": "text", "Content": Instruction})
  else:
    # Place the instruction first and the images after.
    Blocks.append({"Type": "text", "Content": Instruction})
    for Index, Image in enumerate(Images):
      Blocks.append({"Type": "image", "Label": f"Image {Index + 1}", "Path": Image})
  # Return the compiled content blocks.
  return Blocks
```

## References

- OpenAI Vision guide (GPT-4V): https://platform.openai.com/docs/guides/vision
- Liu, H. et al. (2023). "Visual Instruction Tuning." (LLaVA) https://arxiv.org/abs/2304.08485
- Anthropic Claude — Vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- Google Gemini — Image understanding: https://ai.google.dev/gemini-api/docs/vision
- Companion skills: `rag-prompt-designer`, `system-prompt-architect`, `output-format-enforcer`.
