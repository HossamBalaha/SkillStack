---
name: coding-conventions-enforcer-lite
description: Enforce five strict Python coding rules across an entire repository — camelCase variables, CamelCase functions/classes/files/dict-keys, parenthesized if-conditions, period-terminated comments above every statement, and double-quoted strings. Use when auditing Python code, preparing ML/DL repos for review, or onboarding contributors to a strict-style codebase.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity

lite: true
full_version: coding-conventions-enforcer/SKILL.md
language: en
---

# Coding Conventions Enforcer (Lite)

> Condensed version. Load `coding-conventions-enforcer/SKILL.md` for the full workflow.

Enforces five strict non-standard Python style rules across a repository, plus 2-space indentation and centralized
`Configs/Config.yaml` infrastructure.

## Top 3 Workflow Steps

1. Enumerate every `.py` file (excluding `__pycache__`, `.venv`, `node_modules`); scan declarations and statements
   against the five rules.
2. Apply rules in order: rename variables to `camelCase`; rename functions/classes/files/dict-keys to `CamelCase`; wrap
   `if`/`elif`/`while` conditions in parentheses; insert a period-terminated comment above every statement; convert all
   strings to double quotes (except inside docstrings).
3. Enforce infrastructure (centralized `Configs/Config.yaml`,
   `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")`, `.to(device)` on every `nn.Module`) and
   2-space indentation; re-run scanner to confirm zero violations, then emit a per-file change report.

## Top 3 Key Rules

1. **Variables = `camelCase`** (`dataSourceUrl`); **functions/classes/file names/dict keys = `CamelCase`**
   (`ProcessData`, `DataProcessor`, `DataUtils.py`, `"ValidationStatus"`). Functions must NOT be `camelCase`.
2. **Every `if`/`elif`/`while` condition wrapped in parentheses** (`if (condition):`); **2-space indentation** (no tabs,
   no 4-space).
3. **Comment above every statement ending with a period** (`# Initialize the data source URL.`); **double-quoted
   strings** (`"hello"`) everywhere except inside docstrings. Framework-mandated lowercase names (`forward`,
   `training_step`, `setUp`) are exempt — their internals still follow all rules.
