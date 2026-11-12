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
equivalents are listed in `configs/pr2_config.yaml`.
