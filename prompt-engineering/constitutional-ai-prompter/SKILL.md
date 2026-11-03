---
name: constitutional-ai-prompter
description: Build Constitutional AI prompts that define a constitution of principles, run a self-critique loop where the model rates its own draft against those principles, and apply revision prompts to fix violations. Use when you need aligned outputs without massive human-labelling of preferences, when your assistant must self-correct for harm, helpfulness, or honesty, or when red-team probes reveal recurrent failure patterns.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: prompt-engineering
tags: [constitutional-ai, alignment, self-critique, safety, llm]
related: [prompt-engineering/system-prompt-architect, prompt-engineering/prompt-injection-defense, ai-output-judgement/safety-classifier]
prerequisites: []
outputs: [markdown, json, python]
difficulty: advanced
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Constitutional AI Prompter

## When To Use

- You want aligned outputs without scaling human-labelling of preferences.
- Red-team probes reveal recurrent harm patterns the model keeps falling into.
- You need a self-critique step where the model rates its own draft and rewrites it.
- Trigger keywords: constitutional AI, CAI, self-critique, principles, revision, harmlessness, helpfulness, honesty.
- You can afford 2-3x the LLM calls per response in exchange for higher alignment quality.

## Workflow

1. Author the **constitution**: 5-15 numbered principles, each with a one-sentence rule and a short rationale. Cover
   harmlessness, helpfulness, honesty, and any task-specific principles (e.g., cite sources, refuse out-of-scope
   requests).
2. Write the **initial response prompt**: the user request plus the instruction to draft a first response.
3. Write the **critique prompt**: given the user request, the draft response, and the constitution, ask the model to
   identify which principles are violated, by which sentence, and to propose a revision.
4. Write the **revision prompt**: given the critique, produce a revised response that resolves every identified
   violation.
5. Optionally run a second critique pass on the revised response — a two-pass loop catches violations the first pass
   missed.
6. Define a per-principle scoring rubric (1-5) so the critique is structured and comparable across runs.
7. Log every (draft, critique, revision) triple per principle so the alignment improvement is auditable.
8. Evaluate on a red-team suite; report harm rate before and after the CAI loop.
9. Keep the constitution versioned — a principle change is a major version bump.

## Inputs

- The constitution (list of principles with rationales).
- The user request.
- (Optional) A red-team prompt suite for evaluation.
- Parameters: number of critique passes (1 or 2), per-principle scoring scale.

## Outputs

- `constitution.yaml` — the versioned list of principles.
- `prompt_initial.txt`, `prompt_critique.txt`, `prompt_revision.txt` — the three templates.
- `cai_trace.jsonl` — per request: draft, critique per principle, revised response, scores.
- `alignment_report.md` — harm rate before vs. after CAI on the red-team suite.
- `constitution_changelog.md` — per-version principle edits with rationale.

## Key Rules

- Principles must be specific enough to be enforceable — "be helpful" is not; "cite sources for factual claims" is.
- Every critique must name the violating sentence, not just assert a violation — vague critiques produce vague
  revisions.
- Cap the number of critique passes at 2 — more passes do not improve quality and multiply cost.
- The constitution is versioned; principle edits are major-version bumps and require a re-run of the red-team suite.
- CAI does not replace output filtering — it reduces, not eliminates, harm, and a downstream safety classifier is still
  needed.
- Score every principle per pass; aggregate scores reveal which principles the model violates most.

## Examples

```text
Constitution excerpt:
  P1 (Harmlessness): Do not provide instructions for synthesizing controlled substances.
      Rationale: Legal and health risk to the user and third parties.
  P2 (Honesty): Cite a source for every factual claim about named individuals or organisations.
      Rationale: Prevents fabrication and reputational harm.
  P3 (Helpfulness): If the request is in scope, answer it; do not refuse merely to be cautious.
      Rationale: Over-refusal reduces usefulness.

Critique pass output:
  Draft: "You can make X at home by mixing A and B..."
  P1 violation: sentence 1 provides synthesis instructions. Proposed revision: refuse with the exact phrasing from P1.
  P2 violation: no source cited for "A and B react to form X". Proposed revision: remove the unsupported claim.
  P3: not applicable (refusal is the correct behavior here).
```

```python
def RunConstitutionalLoop(UserRequest, Constitution, Passes=2):
  # Generate the initial draft response.
  Draft = CallModel(InitialPrompt(UserRequest))
  # Iterate critique-and-revision passes.
  for PassIndex in range(Passes):
    # Ask the model to critique the draft against every principle.
    Critique = CallModel(CritiquePrompt(UserRequest, Draft, Constitution))
    # Ask the model to revise the draft given the critique.
    Draft = CallModel(RevisionPrompt(UserRequest, Draft, Critique))
  # Return the final revised response and the critique trace.
  return Draft, Critique
```
