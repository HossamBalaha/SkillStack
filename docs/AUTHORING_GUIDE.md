# SkillStack Authoring Guide — How to Write a New Skill

> Canonical template, schema, and rules for contributing a skill to SkillStack.
> Every skill in the stack follows this guide. Follow it exactly so the maestro can route to your skill and the linter
> can validate it.
>
> 168 skills · 9 themes · MIT License · by Hossam Magdy Balaha

---

## 1. Skill folder structure

Every skill lives in its own folder, named in **lowercase-kebab-case**, inside one of the 9 theme folders. The folder
must contain a `SKILL.md` and may contain an optional `references/` subfolder for deeper rule files.

```
<theme>/<skill-name>/
├── SKILL.md                  ← required, the skill itself
└── references/               ← optional, deeper rule files
    ├── api-reference.md
    └── edge-cases.md
```

Rules:

- The **folder name** is the skill's canonical identifier. It must match the YAML `name` field. Use lowercase-kebab-case
  (e.g., `hyperparameter-tuner`, not `HyperparameterTuner` or `hyperparameter_tuner`).
- The **theme folder** must be one of the 9 existing themes (`academic-research`, `style-integrity`, `ml-engineering`,
  `data-engineering`, `visualization`, `writing-citation`, `ai-text`, `ai-output-judgement`, `project-tooling`) or a new
  lowercase-kebab-case theme you register in `maestro/SKILL.md`.
- **`SKILL.md` is the only required file.** Do not ship scripts, notebooks, or binaries inside a skill folder unless the
  skill explicitly generates them at runtime. Skills are instructions, not executables.
- The optional **`references/`** subfolder holds longer reference material the agent reads on demand (e.g., an API
  cheat-sheet, an edge-case catalogue). Reference it from the `References` section of `SKILL.md`.

---

## 2. YAML frontmatter schema

Every `SKILL.md` begins with a YAML frontmatter block delimited by `---`. The required fields are `name`, `description`,
and `metadata.{author, version, theme}`. The remaining fields are recommended; include them whenever they apply.

```yaml
---
name: my-new-skill                       # required, lowercase-kebab-case, matches folder name
description: One-sentence purpose with trigger keywords.   # required
metadata:
  author: Hossam Magdy Balaha            # required
  version: "1.0"                         # required, quoted string, semver
  theme: ml-engineering                   # required, must match the parent theme folder
tags: [pytorch, training, reproducibility]               # recommended, 3–8 lowercase tags
related: [hyperparameter-tuner, reproducible-experiment-runner]  # recommended, sibling skill names
prerequisites: [Configs/Config.yaml, Requirements.txt]    # recommended, files/state the skill expects
outputs: [Aggregated/Metrics.csv, Checkpoints/Best.pt]    # recommended, artifacts the skill produces
# Allowed `outputs:` values: latex, python, pdf, json, csv, bash, svg, html, markdown, yaml, dockerfile.
difficulty: intermediate                # recommended, one of: beginner | intermediate | advanced
estimated_tokens: 2400                   # recommended, integer, rough token size of SKILL.md
cost_warning: "Calls the Crossref API; rate-limited without a polite-mail header."  # optional
permissions: [network:read, filesystem:write]             # recommended, capability flags
language: en                             # recommended, ISO 639-1 code of the skill's prose language
---
```

Field rules:

- **`name`** — must equal the folder name. No spaces, no CamelCase, no underscores.
- **`description`** — one sentence stating *when* to use the skill and *what* it does. Include 2–4 trigger keywords the
  maestro can match on (e.g., "Optuna", "TPE sampler", "Bayesian optimization").
- **`metadata.author`** — use `Hossam Magdy Balaha` for canonical skills, or your own name for contributed skills.
- **`metadata.version`** — quoted string, semantic versioning. Start at `"1.0"`.
- **`metadata.theme`** — must exactly match the parent theme folder name.
- **`tags`** — 3 to 8 lowercase tags for searchability.
- **`related`** — sibling skill *names* (not paths) that chain naturally before or after this one.
- **`prerequisites`** — files, configs, or state the skill assumes exist. Be concrete: `Configs/Config.yaml`, not "a
  config file".
- **`outputs`** — concrete artifact paths the skill writes. List every file the agent should expect.
- **`difficulty`** — `beginner`, `intermediate`, or `advanced`.
- **`estimated_tokens`** — rough token count of the `SKILL.md` body, so the maestro can budget context.
- **`cost_warning`** — required if the skill calls paid APIs, runs long jobs, or writes irrevocably. State the cost in
  plain language.
- **`permissions`** — capability flags: `network:read`, `network:write`, `filesystem:read`, `filesystem:write`,
  `shell:exec`, `model:call`. Helps the agent runtime gate dangerous skills.
- **`language`** — ISO 639-1 code of the skill's prose. Default `en`.

---

## 3. Body sections (all mandatory)

After the frontmatter, the body has exactly these sections, in this order. Each is a `##` heading. Do not skip, merge,
or rename sections.

### When To Use

A bulleted list of situations and trigger keywords that tell the maestro and the agent *when* this skill applies.
Include 3–6 bullets. Match on what the user *says* and what the *inputs* look like.

### Workflow

A numbered, ordered list of the steps the agent executes. Number every step (`1.`, `2.`, ...). Be concrete: name the
libraries, the file paths, the API calls. This is the heart of the skill — a reader should be able to execute it without
further guidance.

### Inputs

A bulleted list of what the skill expects as input — files, configs, data shapes, model checkpoints. Mark which are
required vs. optional.

### Outputs

A bulleted list of the concrete artifacts the skill produces — file paths, formats, and what each contains. The next
skill in a chain reads these.

### Key Rules

A bulleted list of invariants, guardrails, and "never do X" rules. This is where you encode the discipline that
distinguishes a good skill from a sloppy one (e.g., "Never fabricate a citation", "Always seed the sampler for
reproducibility").

### Examples

One or more fenced code blocks showing a realistic input → output pair. Use ```` ```text ````, ```` ```python ````, or
```` ```latex ```` as appropriate. Examples must be runnable or at least syntactically valid. Show the *before* and
*after* where relevant.

### References

A bulleted list of authoritative sources the skill paraphrases. Every entry must be a real URL that resolves with
HTTP 200. Cite foundational papers with author, year, title, venue, and link. No fabricated citations — the
`zero-fabrication-guard` skill will catch them.

---

## 4. Style rules

- **Be concrete.** Name the library, the function, the file path. "Use `optuna.samplers.TPESampler(seed=42)`" beats "use
  a sampler".
- **Paraphrase from verified sources only.** Read the official docs or the paper, then write the rule in your own words.
  Never copy-paste a paragraph from a third party.
- **No fabricated citations.** Every reference must resolve. If you are unsure a paper exists, do not cite it. The
  `ai-output-judgement/citation-hallucination-detector` skill exists precisely because LLMs fabricate citations — do not
  add to that problem.
- **Real URLs only.** Verify each link returns HTTP 200 before committing. Prefer canonical URLs (`https://optuna.org`,
  `https://docs.pytest.org`) over deep links that rot.
- **Length: 80–250 lines (linter hard cap).** A typical `SKILL.md` should fit in one screen of context (target 80–180
  lines). If yours exceeds 180 lines, consider splitting the overflow into `references/` files and link to them. If it
  is under 80 lines, you are probably missing a section or an example. The linter (`LintSkills.py`) rejects files
  shorter than 80 or longer than 250. The `coding-conventions-enforcer` skill is intentionally at the 250-line cap
  because it is the canonical reference for the repo's strict style rules. **LITE.md variants are exempt** from the
  80-line minimum (target 25–35 lines).
- **Match the repo's Python style** in any code blocks: `camelCase` variables, `CamelCase` functions/classes,
  parenthesized `if`, period-ended comments above statements, double-quoted strings, 2-space indent. Framework-mandated
  lowercase methods (`forward`, `training_step`, `configure_optimizers`) are exempt.
- **No emojis in skill bodies** unless the user explicitly requests them. The maestro and theme badges use them; the
  skills do not.
- **Write in second person imperative** ("Load the config", "Persist the trials dataframe"), not first person ("I will
  load...").

---

## 5. Submission checklist

Before opening a pull request, confirm every item:

- [ ] Folder is lowercase-kebab-case and matches the YAML `name` field.
- [ ] Folder is inside one of the 9 registered theme folders (or you have registered a new theme in `maestro/SKILL.md`).
- [ ] `SKILL.md` exists and begins with a valid YAML frontmatter block.
- [ ] All required frontmatter fields are present: `name`, `description`, `metadata.author`, `metadata.version`,
  `metadata.theme`.
- [ ] `metadata.theme` exactly matches the parent theme folder name.
- [ ] All seven body sections are present in order: When To Use, Workflow, Inputs, Outputs, Key Rules, Examples,
  References.
- [ ] The `Workflow` section is a numbered list; every step is concrete.
- [ ] The `Examples` section uses fenced code blocks.
- [ ] Every URL in `References` resolves with HTTP 200.
- [ ] No fabricated citations. Every cited paper or tool has been verified to exist.
- [ ] Body is 80–250 lines long (target 80–180; `coding-conventions-enforcer` and LITE variants excepted).
- [ ] Python code blocks follow the repo's strict style (camelCase/CamelCase, parenthesized `if`, period-ended comments,
  double quotes, 2-space indent).
- [ ] The linter passes: `python scripts/LintSkills.py <theme>/<skill-name>/SKILL.md`.
- [ ] You have updated the theme's skill count in `maestro/SKILL.md` and `README.md` if you added a new skill.
- [ ] No files outside `docs/`, `maestro/`, or the skill's own folder were modified.

---

## 6. Complete `SKILL.md` template

Copy this template, fill in every field, and delete the inline comments (the `< ... >` placeholders).

````markdown
---
name: <lowercase-kebab-case-skill-name>
description: <One sentence: when to use this skill and what it does, with 2–4 trigger keywords.>
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: <one-of-the-9-themes>
tags: [<tag1>, <tag2>, <tag3>]
related: [<sibling-skill-name-1>, <sibling-skill-name-2>]
prerequisites: [<Configs/Config.yaml>, <Requirements.txt>]
outputs: [<Aggregated/Output.csv>, <Checkpoints/Best.pt>]
difficulty: <beginner|intermediate|advanced>
estimated_tokens: <integer>
cost_warning: "<Plain-language description of any paid API, long job, or irrevocable write. Omit if none.>"
permissions: [<network:read>, <filesystem:write>]
language: en
---

# <Skill Title in Title Case>

## When To Use
- <Situation 1 that triggers this skill.>
- <Situation 2.>
- <Situation 3.>
- Trigger keywords: "<keyword1>", "<keyword2>", "<keyword3>".

## Workflow
1. <First concrete step, naming the library, function, or file path.>
2. <Second step.>
3. <Third step.>
4. <...continue for every step the agent must execute.>
5. <Final step that produces the declared Outputs.>

## Inputs
- <Required input 1 with format.>
- <Required input 2.>
- Optional: <optional input and what it improves.>

## Outputs
- `<path/to/file1>` — <what it contains, one line.>
- `<path/to/file2>` — <what it contains.>

## Key Rules
- <Invariant or guardrail 1.>
- <Invariant 2 — often a "never do X" rule.>
- <Reference only the real <tool> API at <real URL>.>
- <Never fabricate / never skip verification.>

## Examples

```python
# <One-line description of the example.>
import <library>

# <Step comment ending with a period.>
def ProcessData(DataSource):
  """<Docstring describing the function.>"""
  # <Comment above each statement, ending with a period.>
  if (len(DataSource) == 0):
    return None
  result = DoSomething(DataSource)
  return result
```

## References
- [<Tool/library official docs>] (<real URL>)
- <Author et al. Year> — <Paper title>. <Venue>. <real URL>
- <Standard or spec name> — <real URL>

````

---

## 7. After submission

Once merged, the maestro can route to your skill immediately — no registry, no build step. Add the skill to relevant
chains in `docs/COOKBOOK.md` if it participates in a multi-skill pipeline, and bump the theme's skill count in the
badges in `README.md` and in `maestro/SKILL.md`.

Keep your skill's `metadata.version` incremented on any material change to the `Workflow` or `Key Rules` sections;
cosmetic edits need not bump the version.

---

<div align="center">

**SkillStack** — *Drop themes. Chain skills. Ship work.*

Built with rigor by **Hossam Magdy Balaha** · MIT License · 2026

</div>
