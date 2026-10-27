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

## Provenance

All numbers were produced by the executed notebooks in `notebooks/` and are consistent with
the reports in `reports/`. The PR1 files were verified against the executed notebook during
an independent internal audit; `quality_profile.csv` rows for anomalies carry Wilson
intervals recomputed from the actual counts (NIQE: 2/90 = 2.22% [0.61; 7.74]%;
blur: 180/7200 = 2.50% [2.16; 2.89]%).
