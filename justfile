# SkillStack justfile.
#
# A modern alternative to the Makefile with the same targets. Each recipe
# invokes the corresponding CamelCase Python helper script under scripts/.
#
# Install `just`:
#   cargo install just      # via cargo
#   brew install just       # via Homebrew
#
# List available recipes:
#   just --list
#
# Run one recipe:
#   just lint
#   just smoke-test
#
# Unlike Makefile, just recipes use plain indentation (spaces are fine — no
# tab requirement). This file therefore fully complies with the repo's
# 2-space-indent convention.

# Default recipe lists the available targets.
default:
    @just --list

# Lint every SKILL.md (frontmatter, sections, line count, banned markers).
lint:
    python scripts/LintSkills.py

# Regenerate the skills.yaml manifest from the live skills tree.
manifest:
    python scripts/GenerateManifest.py

# Run the per-skill health report (line count, examples, references).
health:
    python scripts/SkillHealth.py

# Generate docs/Coverage.md from every skill's metrics.
coverage:
    python scripts/CoverageReport.py

# Render the skill dependency graph as SVG (themes -> skills -> related).
graph:
    python scripts/GraphvizChains.py

# HEAD-check every external URL referenced by any SKILL.md.
links:
    python scripts/CheckLinks.py

# Verify every arXiv ID and DOI cited by any SKILL.md.
citations:
    python scripts/VerifyCitations.py

# Print the last 50 entries from the .audit-log.jsonl audit trail.
audit-show:
    python scripts/Audit.py show

# Cache every skill (SKILL.md + references/*.md) under .cache/<name>.md.
cache-all:
    python scripts/CacheSkill.py --all

# Export every skill to export/anthropic/<theme>/<name>.md.
export-anthropic:
    python scripts/ExportAnthropic.py

# Run the smoke test harness (parse + section check + fenced-code exec).
smoke-test:
    python scripts/SmokeTest.py

# Run the 50-prompt maestro routing regression suite.
test-maestro:
    python scripts/TestMaestro.py

# Build a release zip excluding node_modules and __pycache__.
zip:
    python scripts/Skill.py list > /dev/null
    zip -r skillstack.zip . -x "*/node_modules/*" "*/__pycache__/*"

# Run the full local CI gate (lint, smoke, maestro) before pushing.
ci-local: lint smoke-test test-maestro
    @echo "Local CI gate passed."
