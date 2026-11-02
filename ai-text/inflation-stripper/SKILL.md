---
name: inflation-stripper
description: Remove inflated-significance phrasing ("stands as a testament", "marking a pivotal moment", "left an indelible mark", "broader landscape") and replace with concrete facts drawn from the source. Use when `ai-text-detector` flags inflation-category tells, or when a draft overstates the importance of events beyond what the evidence supports.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-text
tags: [humanization, inflation, prose, ai-text]
related: [ai-text/ai-text-humanizer, ai-text/ai-text-detector, ai-text/grace-degradation-protocol, ai-text/ai-tell-catalogue]
prerequisites: [ai-text/ai-tell-catalogue]
outputs: [markdown]
difficulty: intermediate
estimated_tokens: 2000
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Inflation Stripper

## When To Use

- `ai-text-detector` flagged inflation-category tells (catalogue #13-#17).
- A passage reads as marketing copy or grand narrative rather than reporting.
- A reviewer says "this overstates things; what actually happened?"
- A draft contains a "Future Outlook" or "What This Means" section that inflates rather than informs.
- You are converting chatbot-generated summaries into factual prose.

## Workflow

1. Identify inflation phrases using the catalogue list (overused lexical choices, inflated significance, vague
   connections, "-ing" riders, sales language, borrowed authority).
2. For each match, locate the underlying factual claim. If the source material contains the fact, retrieve it. If not,
   mark the spot for `grace-degradation-protocol`.
3. Replace the inflation with the concrete fact. If no fact is available, either omit the sentence or insert
   `[Verify Source]`.
4. Delete or rewrite "Future Outlook" sections that speculate without evidence. If the section contains genuine
   predictions, label them as such and attribute them.
5. Remove vague-connective phrases ("in the broader landscape of", "within the realm of", "at the intersection of")
   unless they name a specific domain.
6. Strip "-ing" riders ("X, paving the way for Y") unless the rider states a concrete outcome.
7. Remove sales language ("industry-leading", "trusted by", "best-in-class") unless backed by a citation.
8. Re-read for cohesion. Ensure each remaining sentence states a fact, a defined opinion, or a clearly labelled
   speculation.
9. Emit the rewritten text plus an inflation log: `Phrase removed | Replacement | Source for the fact`.

## Inputs

- The text containing inflation tells.
- Optional: source material to verify and supply concrete facts.
- Optional: voice profile (some authors use grand rhetoric intentionally — keep if in-voice).

## Outputs

- The rewritten text with inflation removed and concrete facts inserted.
- An inflation log: `Span removed | Replacement | Fact source (or [Verify Source])`.
- A note on any "Future Outlook" sections: kept, removed, or converted to labelled speculation.

## Key Rules

- Replace inflation with facts. Never swap one grand phrase for another.
- If no fact is available, omit the sentence or insert `[Verify Source]`. Never invent a fact.
- "Future Outlook" sections without evidence are removed by default.
- Sales language is removed unless cited. Borrowed authority ("as experts note") is removed unless the expert is named
  and the source verifiable.
- Voice override: an author known for grand rhetoric may keep some inflation. Note this in the log.
- Vague connectives are deleted unless they name a specific domain ("in the broader landscape of X" → "in X" or delete).
- Do not introduce new inflation while removing old. Watch for the rewrite slipping back into "marks a significant
  step".

## Replacement Patterns

| Inflation phrase                 | Replace with                                |
|----------------------------------|---------------------------------------------|
| "stands as a testament to"       | the actual fact: "X reduced latency by 38%" |
| "marking a pivotal moment"       | the date or the metric                      |
| "setting the stage for"          | the specific subsequent event, or delete    |
| "left an indelible mark"         | the measurable outcome                      |
| "in the broader landscape of"    | "in" + the domain, or delete                |
| "paving the way for"             | the concrete follow-up, or delete           |
| "underscores the importance of"  | the importance statement itself, or delete  |
| "a testament to"                 | the fact that justifies it                  |
| "at the intersection of X and Y" | "in both X and Y" or specify the overlap    |
| "Future Outlook" heading         | "Open questions" or delete                  |

## Examples

**Before:**

```
Established in 1989, marking a pivotal moment in the evolution of the field,
the institute stands as a testament to how visionary leadership can leave an
indelible mark on the broader landscape of research.
```

**After:**

```
Established in 1989, the institute was among the first in the region to focus
on distributed computing. It now hosts 14 active research groups.

[Inflation log]
- "marking a pivotal moment in the evolution of the field" → replaced with "among the first in the region to focus on distributed computing" (source: institute history page, verified)
- "stands as a testament to how visionary leadership can leave an indelible mark" → removed; no measurable claim supported it
- "on the broader landscape of research" → removed (vague connective)
```

**Before (Future Outlook):**

```
Future Outlook: As we look ahead, the framework stands poised to reshape the
industry, leaving an indelible mark on generations to come.
```

**After:**

```
Open questions: Whether the framework's 38% latency reduction will hold at
10× the test load remains unmeasured. A second trial is planned for Q4.

[Inflation log]
- "Future Outlook" heading → renamed "Open questions"
- "stands poised to reshape the industry" → replaced with the open measurable question
- "leaving an indelible mark on generations to come" → removed (no evidence)
```

## References

- Companion skills: `ai-text-detector`, `ai-tell-catalogue` (tells #13-#17), `grace-degradation-protocol`.
- Principles paraphrased from widely documented observations on inflated LLM prose; no external text reproduced.
