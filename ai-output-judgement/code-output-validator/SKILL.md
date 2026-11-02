---
name: code-output-validator
description: Validate AI-generated code by syntax-checking, executing in a sandbox, running provided unit tests, checking spec compliance, and detecting security issues. Use when an LLM produces code that will be merged, deployed, or run by users.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [code, validation, sandbox, security]
related: [ai-output-judgement/factuality-checker, project-tooling/pytest-scientific-suite]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 2300
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Code Output Validator

## When To Use

- An LLM produced code (function, script, snippet, full file) that must be validated before use.
- Trigger keywords: "code validation", "HumanEval", "pass@k", "sandbox execution", "bandit", "semgrep", "SWE-bench".
- A code-generation benchmark needs an automated pass/fail pipeline.
- A copilot suggestion will be merged into a production repository.

## Workflow

1. Detect the language (Python, TypeScript, JavaScript, Go, Rust, Java, etc.). Choose the toolchain:
    - Python: `ast.parse`, `py_compile`, `pytest`, `bandit`, `ruff`.
    - TypeScript: `tsc --noEmit`, `eslint`, `npm test`.
    - JavaScript: `node --check`, `eslint`, `npm test`.
    - Go: `gofmt -l`, `go vet`, `go test`.
    - Rust: `cargo check`, `cargo clippy`, `cargo test`.
2. Syntax check: parse the code without executing. On syntax error, stop and report the error location.
3. Execute in a sandbox with timeout (default 30s) and resource limits (CPU, memory, no network unless explicitly
   allowed). Use Docker, e2b.dev, or `subprocess` with `resource.setrlimit` and a temp working directory.
4. Run provided or generated unit tests:
    - If the user supplied tests, run them.
    - If not, optionally generate tests via an LLM and a separate validation pass (cite HumanEval-style).
5. Check spec compliance: compare the code's behavior against the natural-language spec. Use an LLM judge prompt that
   checks inputs→outputs on a few canonical cases. Do not rely on judge-only verdicts; require test execution.
6. Run security scanners: `bandit` (Python), `semgrep` (multi-language), `gosec` (Go), `cargo audit` (Rust). Flag any
   HIGH or CRITICAL finding.
7. Aggregate a validation report: `syntax OK / execution OK / tests passed (n/N) / spec match / security findings`.
   Output a single pass/fail verdict.

## Inputs

- The generated code (required).
- The natural-language spec or task description (required for spec-match check).
- Optional: provided unit tests; expected input→output pairs; allowed dependencies.
- Optional: sandbox configuration (timeout, memory cap, network allowlist).

## Outputs

- `validation.jsonl` — per code artifact: syntax_status, execution_status, tests_passed, spec_match, security_findings,
  verdict.
- `validation_report.md` — per-artifact table, top failures, security findings with severity.
- `artifacts/` — captured stdout/stderr, test results, scanner output for auditability.

## Key Rules

- Syntax check before execution — never run syntactically invalid code.
- Sandbox with timeout and resource limits — AI-generated code can hang or exhaust resources.
- Network off by default; enabling it requires explicit justification and a per-run allowlist.
- Security scans are mandatory, not optional — bandit and semgrep must run before any merge.
- Spec-match must be test-execution-based, not judge-only; an LLM verdict alone is not a pass.
- Pass@k metrics require k samples; record k and the temperature used.
- Do not auto-merge validated code — surface the report for human approval.

## Examples

```text
Spec: "Write a Python function `fib(n)` that returns the n-th Fibonacci number (0-indexed)."
Code:
  def fib(n):
      if n < 2: return n
      return fib(n-1) + fib(n-2)

Syntax: OK (ast.parse succeeded).
Execution: OK on n=0..10; timeout (>30s) on n=35.
Tests: 5/5 provided tests pass (n=0,1,2,5,10).
Spec match: PASS.
Security: bandit — no findings.  semgrep — no findings.
Verdict: PARTIAL_PASS (performance issue at n≥35; correctness OK).
Recommendation: rewrite iteratively.
```

```text
Spec: "Read a CSV file from a path the user supplies and print the first row."
Code:
  import os
  path = input("path: ")
  os.system(f"cat {path}")

Syntax: OK.  Execution: OK.
Tests: none provided.
Spec match: technically yes, but…
Security:
  bandit: B602 subprocess call with shell=True (HIGH).
  semgrep: python.lang.security.audit.subprocess-shell-injection (CRITICAL).
Verdict: FAIL (command injection). Recommend: use `csv` module, never `os.system` on user input.
```

## References

- Chen, M. et al. (2021). "Evaluating Large Language Models Trained on Code." (HumanEval) arXiv:
  2107.03374. https://arxiv.org/abs/2107.03374
- Austin, J. et al. (2021). "Program Synthesis with Large Language Models." (MBPP) https://arxiv.org/abs/2108.07732
- Jimenez, C. et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
  ICLR. https://arxiv.org/abs/2310.06770
- Bandit (Python SAST): https://github.com/PyCQA/bandit
- Semgrep (multi-language SAST): https://semgrep.dev/
- e2b.dev sandboxed code execution: https://e2b.dev/
- Companion skills: `hallucination-detector` (for non-existent API methods), `safety-classifier`,
  `evaluation-harness-builder`.
