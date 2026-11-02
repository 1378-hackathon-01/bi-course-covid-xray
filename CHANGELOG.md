# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/), adheres to
[Semantic Versioning](https://semver.org/).

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

## [Unreleased]

### Planned

- PR2: Corruption Robustness (noise, blur, JPEG, brightness) — R(s) curves and R-AUC.
- PR3: Adversarial Robustness (white-box: FGSM, PGD, AutoAttack sanity check).
- PR4: Privacy — Membership Inference Attack (ROC-AUC, TPR@FPR, generalization gap).
- Final consolidated report.
