---
name: formatting-by-rule-cleaner
description: Clean formatting-by-rule tells — decorative bold, title-case headings, emojis and arrows in headings, horizontal rules between every section, curly quotation marks in plain-text or code contexts. Use when `ai-text-detector` flags formatting-category tells, or when a document has LLM-default visual chrome that obscures content.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [humanization, formatting, prose, ai-text]
related: [ai-text/ai-text-humanizer, ai-text/ai-text-detector, ai-text/chatbot-residue-cleaner, ai-text/ai-tell-catalog]
prerequisites: [ai-text/ai-tell-catalog]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 2400
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Formatting-by-Rule Cleaner

## When To Use

- `ai-text-detector` flagged formatting-by-rule tells (catalog #18-#21).
- A document bolds random words for emphasis inside flowing prose.
- Headings are in Title Case, decorated with emojis, or followed by horizontal rules between every section.
- Code or plain-text contains curly ("smart") quotation marks that break tools.
- You are converting chatbot-formatted Markdown into a clean deliverable.

## Workflow

1. Identify formatting tells using the catalog (#18-#21).
2. Apply the canonical fixes:
    - **Bold as decoration**: remove bold unless it carries structural meaning (a defined term on first use, a column
      header, a UI label the user must click). Emphasis in flowing prose is removed.
    - **Title-case headings**: convert to sentence case. "The Future Of Caching" → "The future of caching". Proper nouns
      retain capitalization.
    - **Emojis and arrows in headings**: remove. "🚀 Performance →" → "Performance". Arrows in body text are kept only if
      they indicate a literal direction or flow.
    - **Horizontal rules between every section**: remove. Keep a rule only where it separates genuinely distinct
      document parts (e.g., appendix from body).
    - **Curly quotes in plain text/code**: replace with straight quotes (`'` and `"`) inside code blocks, plain-text
      files, JSON, YAML, and configuration. Curly quotes in narrative prose may stay.
3. After removal, re-check structural coherence. Headings that lost their emoji may need a slight rewording for clarity,
   but never invent new content.
4. Verify code blocks render with straight quotes and that no smart-quote artifacts remain in identifiers.
5. Voice override: if the author's style genuinely uses emojis as section markers (rare, usually in informal
   newsletters), keep them but log the override.
6. Emit the cleaned text plus a formatting log: `Tell (#) | Span | Fix`.

## Inputs

- The text or Markdown containing formatting tells.
- Optional: target format (Markdown, plain text, HTML) — affects quote handling.
- Optional: voice profile (for emoji overrides).

## Outputs

- The cleaned text with formatting tells removed.
- A formatting log: `Tell (#) | Span | Fix`.
- A note on any structural changes (e.g., a heading was kept because it carried a UI label).

## Key Rules

- Bold is structural or it is removed. No decorative bold survives.
- Headings are sentence case. Proper nouns stay capitalized.
- Emojis in headings are removed unless a voice override is logged.
- Horizontal rules between every section are removed; keep only genuinely structural separators.
- Curly quotes are straightened in code, plain text, JSON, YAML, and configuration. Narrative prose may keep them.
- Do not introduce new formatting while cleaning. No new bold, no new emojis, no new rules.
- Structural meaning (UI labels, defined terms on first use, column headers) is preserved.

## Examples

**Bold as decoration:**

```
Before: The cache is **critical** for performance, and **every** miss costs us.
After:  The cache is critical for performance, and every miss costs us.
[Formatting log] bold-as-decoration (#18) | "**critical**", "**every**" | removed
```

**Title-case heading:**

```
Before: ## The Future Of Caching In Modern Web Architecture
After:  ## The future of caching in modern web architecture
[Formatting log] title-case heading (#19) | heading | sentence-cased (proper nouns kept)
```

**Emoji and arrow in heading:**

```
Before: ## 🚀 Performance → Latency Reduction
After:  ## Performance and latency reduction
[Formatting log] emoji/arrow in heading (#20) | "🚀", "→" | removed
```

**Horizontal rules between every section:**

```
Before:
## Section one
text
---
## Section two
text
---
## Section three
text

After:
## Section one
text

## Section two
text

## Section three
text
[Formatting log] decorative hr (#21) | two "---" separators | removed
```

**Curly quotes in code:**

```
Before (in a YAML file):
  greeting: “Hello, world”

After:
  greeting: "Hello, world"
[Formatting log] curly quotes (#21) | “ ” | straightened to " "
```

**Mixed (multiple formatting tells):**

```
Before:
## 🚀 **Key Takeaways**

The system is **fast**, **reliable**, and **scalable** — a true *game-changer*.

---

## **What’s Next?**

After:
## Key takeaways

The system is fast, reliable, and scalable.

## What's next?

[Formatting log]
- emoji in heading (#20)        | "🚀"               | removed
- bold as decoration (#18)      | "**Key Takeaways**" | heading un-bolded, sentence-cased
- bold as decoration (#18)      | "**fast**", "**reliable**", "**scalable**" | removed
- italic as decoration          | "*game-changer*"   | removed (no catalog entry; treated as bold sibling)
- decorative hr (#21)           | "---"              | removed
- bold as decoration (#18)      | "**What's Next?**" | un-bolded, sentence-cased
- curly quote (#21)             | "What's"           | straightened
```
