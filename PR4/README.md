# PR4 — Privacy: Membership Inference (TODO)

**Status: not started.** Will be added in a future release without restructuring.

## Planned scope (methodology §5)

- Privacy unit defined explicitly (image-level; patient-level is not possible because the
  dataset has no patient identifiers).
- Member/non-member samples with equal sizes, comparable class distribution and the same
  origin; the threshold τ tuned on a separate validation split.
- Loss-threshold attack (and, optionally, a stronger attack) with ROC-AUC, Attack Accuracy
  (Wilson interval), TPR@FPR = 1% and 0.1%, generalization gap.
- Stratified bootstrap for ROC-AUC and TPR@FPR; conclusion on observable membership leakage.

## Planned artifacts

`configs/pr4_config.yaml`, `results/pr4/`, `reports/БИИ_preliminary.(pdf|docx)` (PR4 section
appended to the single cumulative report),
`figures/pr4/`, `scripts/reproduce_pr4.py`, notebook `notebooks/04_privacy_mia.ipynb`.
The frozen checkpoint and the same splits will be reused.
