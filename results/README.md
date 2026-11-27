# Results artifacts

## `preliminary/`

| File | Contents |
|---|---|
| `metrics.json` | Baseline metric M(0) = 0.9833, Wilson CI [0.9711; 0.9904], confusion matrix 354/7/5/354, secondary metrics, best epoch. |
| `training_history.json` | Per-epoch train/validation loss and accuracy (20 epochs) plus training metadata (date, GPU, PyTorch version, test metrics). |
| `split_indices.json` | Exact train/validation/test indices (5760/720/720, seed 42) referring to the ImageFolder ordering described in `data/README.md`. |
| `inference_latency.json` | CPU inference cost of the frozen checkpoint (G-1 supplementary evidence). The same file also appears under `results/pr1/` because the measurement was produced during PR1. |

## `pr1/`

| File | Contents |
|---|---|
| `metrics_pr1.json` | Machine-readable PR1 metrics: eight quality characteristics, leakage counts, MMD/C2ST results, label-error rates, image-quality means, remediation status. |
| `quality_profile.csv` | The mandatory §2.5 table: property, metric, value, confidence interval (`CI_low`, `CI_high`, `95% CI`), interpretation (21 rows). |
| `label_inspection.csv` | Manual inspection of the objects with the lowest label quality (top-10 train + all flagged test objects). |
| `inference_latency.json` | Copy of the latency measurement (identical content). |
| `checksums.sha256` | Internal checksums of the PR1 submission artifacts. |

## `pr2/`

| File | Contents |
|---|---|
| `metrics_pr2.json` | Machine-readable PR2 results, kept verbatim from the PR2 bundle: task/version, model and checkpoint identity, data, protocol (severities, repeats, total runs), corruption grid, baseline, bootstrap settings, per-level results, R-AUC with percentile/BCa CIs, summary and verification block. |
| `summary.json` | Compact summary: baseline M(0), per-corruption curves, ΔM, R_rel, R-AUC, first significant drop, collapse levels. |
| `summary_table.tsv` | The 20-row table behind §5 of the report: corruption, severity, R(s), ΔM, R_rel with their 95 % interval bounds. |
| `rauc.csv` | R-AUC per corruption type (point estimate, percentile and BCa intervals). |
| `correctness.pkl` | Per-object, per-realization correctness matrix of the frozen model for the clean test set and all 20 (corruption, severity) cells — the input of `scripts/reproduce_pr2.py`. |
| `checksums.sha256` | Checksums of the PR2 artifacts plus the inherited preliminary files and `models/baseline_model.pt`. |

## `pr3/`

| File | Contents |
|---|---|
| `metrics_pr3.json` | Machine-readable PR3 results, kept verbatim from the PR3 bundle: protocol and threat model, attack parameters, the 10 (attack, ε) rows with Wilson intervals, R-AUC_ε with percentile intervals, validity statistics, multi-seed series and the APGD-CE sanity check. |
| `pr3_adv_attacks.csv` | The 10-row table behind §7 of the report: FR (= ASR), Robust Accuracy and their 95 % Wilson bounds, the number of broken clean-correct objects and the number of wrong adversarial predictions. |
| `pr3_rauc.csv` | R-AUC_ε for FGSM and PGD-10 with 95 % percentile bootstrap intervals. |
| `pr3_validity_l2.csv` | Validity Rate with Wilson bounds, L₂ mean/max and L∞ max for all 10 cells, together with the ε bound. |
| `pr3_multiseed_pgd.csv` | PGD-10 at ε = 8/255 for seeds 42, 43 and 44 (FR, Wilson bounds, Robust Accuracy). |
| `pr3_autoattack.json` | APGD-CE (`torchattacks`) sanity check at ε = 8/255 on 20 clean-correct images, with Wilson intervals. |
| `pr3_summary.json` | Compact notebook summary: attack rows, R-AUC_ε, the ε grid and the bootstrap bands. |
| `pr3_masks.pkl` | Per-object clean/adversarial correctness masks for the 200-image subset over all 10 cells — the input of `scripts/reproduce_pr3.py`. |
| `pr3_masks_fgsm.pkl` | Per-object FGSM correctness masks (intermediate notebook cache). |
| `checksums.sha256` | Checksums of the PR3 artifacts and inherited files. |

## Provenance

All numbers were produced by the executed notebooks in `notebooks/` and are consistent with
the reports in `reports/`. The PR1 files were verified against the executed notebook during
an independent internal audit; `quality_profile.csv` rows for anomalies carry Wilson
intervals recomputed from the actual counts (NIQE: 2/90 = 2.22% [0.61; 7.74]%;
blur: 180/7200 = 2.50% [2.16; 2.89]%). The PR2 point estimates (20 R(s)/ΔM/R_rel values
and 4 R-AUC values) are re-derived from `pr2/correctness.pkl` by
`scripts/reproduce_pr2.py`, which reports `RESULT: PASS`; the bootstrap intervals are
reproduced by `notebooks/02_corruption_robustness.ipynb`.
`metrics_pr2.json` keeps the submission-relative path strings of the original PR2 bundle
(e.g. `PR2.ipynb`, `PRELIMINARY_SUBMISSION_V2/split_indices.json`); the repository-local
equivalents are listed in `configs/pr2_config.yaml`. The PR3 point estimates (10 FR/RA
pairs), their Wilson intervals and both R-AUC_ε values are re-derived exactly from
`pr3/pr3_masks.pkl` by `scripts/reproduce_pr3.py`, which reports `RESULT: PASS`; the
percentile bootstrap intervals for R-AUC_ε and the figures are reproduced by
`notebooks/03_adversarial_robustness.ipynb`. `metrics_pr3.json` likewise keeps the
submission-relative strings of the PR3 bundle; the repository-local equivalents are listed
in `configs/pr3_config.yaml`.
