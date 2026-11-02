---
name: reproducibility-checklist-author
description: Author a reproducibility checklist for a submitted manuscript covering code on GitHub with DOI, data on Zenodo with DOI, environment lockfile (requirements.txt or environment.yml), seeds fixed, random partitions documented, hardware and software stated, compute time reported, and a license file present. Use when the user is finalizing a manuscript submission and needs the reproducibility artifacts in order.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [reproducibility, checklist, zenodo, doi, environment-lock]
related: [academic-research/research-repo-builder, academic-research/open-science-advocate, ml-engineering/reproducible-experiment-runner]
prerequisites: []
outputs: [markdown, bash]
difficulty: intermediate
estimated_tokens: 820
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Reproducibility Checklist Author

## When To Use
- The user is about to submit a manuscript and needs reproducibility artifacts.
- The user asks "what do I need for reproducibility", "checklist for code release", or "ML Reproducibility Checklist".
- A venue requires a reproducibility checklist (NeurIPS, ICLR, ACM).
- Trigger keywords: reproducibility checklist, ML reproducibility, code release, environment lockfile, random seeds, compute time, license file.

## Workflow
1. Identify the venue's required checklist (NeurIPS Reproducibility Checklist, ML Reproducibility Checklist, ACM Artifact Badging).
2. Confirm the code repository is public on GitHub and that a release tag is linked to Zenodo for a DOI.
3. Confirm the dataset is archived (Zenodo/Figshare/Dryad) with a DOI and a license.
4. Generate the environment lockfile: `requirements.txt` (pip) or `environment.yml` (conda); pin versions exactly.
5. Set all random seeds (Python, NumPy, PyTorch, CUDA) in code AND document them in the README.
6. Document the random partition: train/val/test split files (or hashes), per-run seed assignment.
7. State hardware (GPU model, count, RAM, interconnect) and software (OS, driver, CUDA, PyTorch version).
8. Report compute time per experiment and total compute budget (GPU-hours).
9. Include a LICENSE file (MIT/Apache-2.0 for code, CC-BY 4.0 for data).
10. Provide a one-command reproduction script (`reproduce.sh` or `Makefile` target) that runs the main result table.
11. Output the filled checklist with links to every artifact.

## Inputs
- Manuscript (final draft).
- Code repository URL.
- Dataset archive (or description if restricted).
- Hardware/software environment in use.
- Per-experiment compute time logs.
- Venue-specific checklist (NeurIPS, ICLR, ACM).

## Outputs
- `reproducibility_checklist.md` — filled checklist with links and DOIs.
- `requirements.txt` or `environment.yml` — pinned environment.
- `reproduce.sh` — one-command reproduction script.
- `LICENSE`, `DATA_LICENSE` files.
- `compute_log.md` — per-experiment GPU-hours.

## Key Rules
- Code must be on a public GitHub repo with a Zenodo DOI for at least one release.
- Environment lockfile must pin exact versions; never `>=`.
- Random seeds set in code AND documented in README.
- Hardware, software, and compute time reported in the paper or appendix.
- LICENSE file present in every artifact (code + data).
- A one-command reproduction script runs the main results table without manual setup.

## Examples
```text
Checklist excerpt (NeurIPS-style):
  [x] Code released: https://github.com/org/repo (DOI 10.5281/zenodo.1234567)
  [x] Data archived: https://zenodo.org/record/7654321 (CC-BY 4.0)
  [x] Environment: requirements.txt pinned; conda env yml also provided.
  [x] Seeds: 42, 123, 2024, 7777, 31415 documented in README.
  [x] Splits: split_seed_42.json with SHA-256 9f4c... in repo.
  [x] Hardware: 4x NVIDIA A100 80GB; 512 GB RAM; NVLink.
  [x] Software: Ubuntu 22.04, CUDA 12.1, PyTorch 2.3.
  [x] Compute: 192 GPU-hours total; main table 32 GPU-hours.
  [x] License: code MIT; data CC-BY 4.0.
  [x] reproduce.sh runs main table in one command.
```
```bash
# reproduce.sh (excerpt)
set -e
pip install -r requirements.txt
python Main.py --config Configs/main_result.yaml --seed 42
python Main.py --config Configs/main_result.yaml --seed 123
python src/utils/aggregate_results.py --out outputs/main_table.csv
```

## References
- NeurIPS Reproducibility Checklist: https://neurips.cc/Conferences/2025/PaperInformation/CodeSubmission
- ML Reproducibility Checklist: https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf
- ACM Artifact Badging: https://www.acm.org/publications/artifacts-and-artifact-evaluation
- Zenodo-GitHub integration: https://guides.github.com/activities/citable-code/
- PyTorch reproducibility guide: https://pytorch.org/docs/stable/notes/randomness.html
