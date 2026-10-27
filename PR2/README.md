# PR2 — Corruption Robustness (TODO)

**Status: not started.** Will be added in a future release without restructuring.

## Planned scope (methodology §3)

- Baseline metric M(0) on the unmodified test set (already fixed: 0.9833 [0.9711; 0.9904]).
- At least two corruption types with at least four non-zero severity levels each
  (planned: Gaussian noise, Poisson/shot noise, Gaussian blur, JPEG compression).
- Several independent realizations per (corruption, severity) level for stochastic
  corruptions; the object × realization structure is preserved.
- Robustness curves R(s), relative degradation ΔM(s) and R_rel(s).
- R-AUC with bootstrap intervals by objects (the whole curve recomputed per resample).
- Paired bootstrap for ΔM; conclusion on the most critical corruption types/intensities.

## Planned artifacts

`configs/pr2_config.yaml`, `results/pr2/`, `reports/БИИ_preliminary.(pdf|docx)` (PR2 section
appended to the single cumulative report),
`figures/pr2/`, `scripts/reproduce_pr2.py`, notebook `notebooks/02_corruption_robustness.ipynb`.
The frozen checkpoint `models/baseline_model.pt` and the stored splits will be reused as-is.
