---
name: issue-template-builder
description: "Build GitHub issue templates as YAML form schemas: `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, and a `question.md` config-based template. Use this when standardising how bugs, features, and questions are reported. Triggers: issue template, bug report form, feature request form, .github/ISSUE_TEMPLATE, config.yml."
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: project-tooling
tags: [issue-template, github, bug-report, feature-request]
related: [project-tooling/pr-template-builder, project-tooling/contribution-guide-builder]
prerequisites: []
outputs: [yaml]
difficulty: beginner
estimated_tokens: 2100
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Issue Template Builder

## When To Use

- You want every bug report to arrive with reproduction steps, expected/actual, environment, and logs.
- You want feature requests structured around problem, proposed solution, alternatives, and context.
- You want to disable the blank issue button and force users through templates.
- You are migrating from legacy `.md` templates to the newer YAML form schema.

## Workflow

1. Create `.github/ISSUE_TEMPLATE/bug_report.yml` with the GitHub form schema.
2. Add fields: description (textarea), reproduction steps (textarea), expected behavior (textarea), actual behavior
   (textarea), environment (input), logs (textarea).
3. Mark each required field with `validations: required: true`.
4. Create `.github/ISSUE_TEMPLATE/feature_request.yml` with fields: problem, proposed solution, alternatives, additional
   context.
5. Create `.github/ISSUE_TEMPLATE/question.md` for free-form questions that don't fit the other two.
6. Create `.github/ISSUE_TEMPLATE/config.yml` with `blank_issues_enabled: false` and a contact link.
7. Validate the YAML with `python -c "import yaml; yaml.safe_load(open('...'))"`.
8. Push to `main` and open a test issue on GitHub to confirm the form renders.

## Inputs

- The list of fields the maintainer wants on each form.
- The contact link (e.g. a Discussions URL or a support email).
- Whether blank issues are allowed (default: false).

## Outputs

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/question.md`
- `.github/ISSUE_TEMPLATE/config.yml`

## Key Rules

- Use the YAML form schema (keys: `name`, `description`, `title`, `labels`, `body`), not the legacy markdown-only
  templates.
- Every required field must have `validations: required: true`.
- Field `type` is one of `textarea`, `input`, `dropdown`, `checkboxes`, `markdown`.
- The `config.yml` must set `blank_issues_enabled` explicitly (false by default for this skill).
- Each form ends with a contact link in `config.yml` so users with questions go to Discussions, not issues.
- Labels referenced in templates must already exist in the repo, otherwise GitHub silently drops them.
- Keep forms short — long forms reduce response rates; cap at ~8 fields.

## Examples

`.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug Report
description: Report a reproducible bug in this repo.
title: "[bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to file a bug report.
        Please fill in every section below.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug.
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Reproduction steps
      description: Exact commands to reproduce.
      placeholder: "1. ...\n2. ...\n3. ..."
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
    validations:
      required: true
  - type: input
    id: environment
    attributes:
      label: Environment
      description: "OS, Python version, package version."
      placeholder: "Ubuntu 22.04, Python 3.11, researchkit 0.2.0"
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs
      description: Paste the full traceback between triple backticks.
      render: shell
```

`.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false
contact_links:
  - name: Questions & Discussions
    url: https://github.com/example/researchkit/discussions
    about: Please ask questions here instead of opening an issue.
```

Validate:

```bash
# Confirm the YAML parses cleanly before pushing.
python -c "import yaml, glob; [yaml.safe_load(open(p)) for p in glob.glob('.github/ISSUE_TEMPLATE/*.yml')]"
```
