# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/), adheres to
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- PR4: Privacy — Membership Inference Attack (ROC-AUC, TPR@FPR, generalization gap).
- Final consolidated report.

## [1.2.0] — 2026-11-27

### Added

- **PR3 — Adversarial Robustness** (methodology §4), complete:
  - Standalone report `reports/БИИ_PR3.docx` / `reports/БИИ_PR3.pdf` (Russian, 14 pages,
    13 content tables, 2 figures, no formulas): explicit threat model, FGSM and PGD-10
    on the ε grid {1, 2, 4, 8, 16}/255, ASR over clean-correct objects, Robust Accuracy,
    Validity Rate, L₂/L∞, R-AUC_ε, multi-seed PGD and APGD-CE sanity check.
  - Config `configs/pr3_config.yaml` (repo-path adaptation of the PR3 bundle config).
  - Results `results/pr3/`: `metrics_pr3.json`, `pr3_adv_attacks.csv`, `pr3_rauc.csv`,
    `pr3_validity_l2.csv`, `pr3_multiseed_pgd.csv`, `pr3_autoattack.json`,
    `pr3_summary.json`, per-object correctness masks and `checksums.sha256`.
  - Figures `figures/pr3/`: `pr3_adversarial_examples.png`, `pr3_robustness_vs_eps.png`.
  - Notebook `notebooks/03_adversarial_robustness.ipynb` (executed, 12 cells).
  - Program `scripts/reproduce_pr3.py`: model-free verification of all 10 FR/RA rows,
    Wilson intervals, both R-AUC_ε values, validity, multi-seed and APGD-CE results
    from `pr3_masks.pkl`.
  - Documentation updated (`README.md`, `README.ru.md`, `docs/`, folder READMEs);
    `PR3/README.md` rewritten from placeholder to a completed-work description.
  - Key results: PGD-10 FR = 1.000 [0.981; 1.000] at ε = 1/255 (197/197);
    FGSM FR = 0.558 [0.489; 0.626] at ε = 1/255 with a plateau FR = 0.503 at ε ≥ 2/255;
    R-AUC_ε = 0.0320 [0.0303; 0.0348] for PGD-10 and 0.5111 [0.4497; 0.5798] for FGSM;
    Validity Rate = 1.000 (2000/2000).

## [1.1.0] — 2026-11-12

### Added

- Standalone **PR1 report** `reports/БИИ_PR1.docx` / `reports/БИИ_PR1.pdf`
  (Russian, 13 pages, no formulas): methodology, eight quality characteristics with
  95 % Wilson CIs, near-duplicate train↔test examples, brightness/blur distributions,
  anomalies and conclusions.
- **PR2 — Corruption Robustness** (methodology §3), complete:
  - Standalone report `reports/БИИ_PR2.docx` / `reports/БИИ_PR2.pdf` (Russian, 13 pages,
    table-driven): protocol, corruption grid, R(s) curves, ΔM(s), R_rel(s), R-AUC, and
    visual corruption examples.
  - Config `configs/pr2_config.yaml` (repo-path adaptation of the PR2 bundle config).
  - Results `results/pr2/`: `metrics_pr2.json`, `summary.json`, `summary_table.tsv`,
    `rauc.csv`, `correctness.pkl`, `checksums.sha256`.
  - Figures `figures/pr2/`: `robustness_curves.png`, `corruption_examples.png`.
  - Notebook `notebooks/02_corruption_robustness.ipynb` (executed, with outputs).
  - Program `scripts/reproduce_pr2.py`: model-free verification of all 20 R(s)/ΔM/R_rel
    values and 4 R-AUC values from `correctness.pkl`.
  - Documentation updated (`README.md`, `README.ru.md`, `docs/`, folder READMEs);
    `PR2/README.md` rewritten from placeholder to a completed-work description.

## [1.0.0] — 2026-02-08

### Added

- **Preliminary stage (course methodology §1)** — seven foundation steps completed:
  - Dataset described: COVID-19 Radiography Database v4, 7200 chest X-ray images,
    binary classification (COVID / Normal).
  - Baseline model: ResNet-18 (transfer learning from ImageNet) with a
    Dropout(0.5) + Linear(512→2) head; frozen for PR1–PR4.
  - Primary metric: Accuracy = 0.9833 (Wilson 95% CI: 0.9711; 0.9904),
    TP/FN/FP/TN = 354/7/5/354.
  - Reproducibility config: seed = 42, splits 5760/720/720, pinned library versions,
    exact split indices, checkpoint checksum.
- **Practical Work №1 (course methodology §2)** — data quality investigation:
  - Eight quality characteristics evaluated with 95% confidence intervals.
  - Confident Learning (`cleanlab`) for label-error detection with
    out-of-sample (cross-validated) probabilities.
  - MMD (permutation p-value) and C2ST for distribution-shift testing.
  - BRISQUE and NIQE for no-reference image quality.
  - Train↔test leakage analysis: 7 exact + 64 near-duplicate pairs.
  - Duplicates: 46 exact (0.6389%) and 262 pixel-verified near duplicates (3.6389%).
- Repository engineering: Git LFS for model weights, pinned requirements,
  smoke tests, CI workflow, bilingual documentation.
