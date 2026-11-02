# SkillStack Makefile.
#
# Common developer entry points for linting, manifest generation, coverage,
# graphs, link/citation checks, audit, caching, exports, smoke tests, maestro
# routing tests, and packaging a release zip.
#
# Note: Makefile recipes MUST be indented with TAB characters, not spaces.
# This is the one file in the repo that is exempt from the 2-space-indent
# convention enforced by style-integrity/coding-conventions-enforcer.
#
# Usage:
#   make lint            # python scripts/LintSkills.py
#   make manifest        # python scripts/GenerateManifest.py
#   make health          # python scripts/SkillHealth.py
#   make coverage        # python scripts/CoverageReport.py
#   make graph           # python scripts/GraphvizChains.py
#   make links           # python scripts/CheckLinks.py
#   make citations       # python scripts/VerifyCitations.py
#   make audit-show      # python scripts/Audit.py show
#   make cache-all       # python scripts/CacheSkill.py --all
#   make export-anthropic  # python scripts/ExportAnthropic.py
#   make smoke-test      # python scripts/SmokeTest.py
#   make test-maestro    # python scripts/TestMaestro.py
#   make zip             # build skillstack.zip
#
# All targets are phony — no file artifacts are produced by the targets
# themselves except `zip`.

PYTHON ?= python

.PHONY: lint manifest health coverage graph links citations audit-show cache-all export-anthropic smoke-test test-maestro zip ci-local default

lint:
	$(PYTHON) scripts/LintSkills.py

manifest:
	$(PYTHON) scripts/GenerateManifest.py

health:
	$(PYTHON) scripts/SkillHealth.py

coverage:
	$(PYTHON) scripts/CoverageReport.py

graph:
	$(PYTHON) scripts/GraphvizChains.py

links:
	$(PYTHON) scripts/CheckLinks.py

citations:
	$(PYTHON) scripts/VerifyCitations.py

audit-show:
	$(PYTHON) scripts/Audit.py show

cache-all:
	$(PYTHON) scripts/CacheSkill.py --all

export-anthropic:
	$(PYTHON) scripts/ExportAnthropic.py

smoke-test:
	$(PYTHON) scripts/SmokeTest.py

test-maestro:
	$(PYTHON) scripts/TestMaestro.py

zip:
	$(PYTHON) scripts/Skill.py list > /dev/null
	zip -r skillstack.zip . -x "*/node_modules/*" "*/__pycache__/*"

# Aggregate target: run all local checks (lint + smoke-test + test-maestro).
ci-local: lint smoke-test test-maestro
	@echo "All local checks passed."

# Default target: list available recipes.
default:
	@echo "SkillStack Makefile targets:"
	@echo "  lint            - python scripts/LintSkills.py"
	@echo "  manifest        - python scripts/GenerateManifest.py"
	@echo "  health          - python scripts/SkillHealth.py"
	@echo "  coverage        - python scripts/CoverageReport.py"
	@echo "  graph           - python scripts/GraphvizChains.py"
	@echo "  links           - python scripts/CheckLinks.py"
	@echo "  citations       - python scripts/VerifyCitations.py"
	@echo "  audit-show      - python scripts/Audit.py show"
	@echo "  cache-all       - python scripts/CacheSkill.py --all"
	@echo "  export-anthropic - python scripts/ExportAnthropic.py"
	@echo "  smoke-test      - python scripts/SmokeTest.py"
	@echo "  test-maestro    - python scripts/TestMaestro.py"
	@echo "  zip             - bundle the repo into skillstack.zip"
	@echo "  ci-local        - run lint + smoke-test + test-maestro"
