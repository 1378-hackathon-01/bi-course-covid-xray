# PR2 - Corruption Robustness

**Status: completed.** The full V2 submission package is maintained separately and is not
stored in this repository; this folder keeps the package README.

Key result: R-AUC = 0.822 (JPEG), 0.788 (blur), 0.625 (Gaussian noise), 0.560 (Poisson
noise); the model is highly sensitive to noise and comparatively robust to JPEG/blur.

## Scope (methodology §3)

- Baseline metric M(0) on the unmodified test set (fixed: 0.9833 [0.9711; 0.9904]).
- Four corruption types (Gaussian noise, Poisson/shot noise, Gaussian blur, JPEG
  compression) with five non-zero severity levels each.
- Several independent realizations per (corruption, severity) level for stochastic
  corruptions; the object × realization structure is preserved.
- Robustness curves R(s), relative degradation ΔM(s) and R_rel(s).
- R-AUC with bootstrap intervals by objects (the whole curve recomputed per resample).
- Paired bootstrap for ΔM; conclusion on the most critical corruption types/intensities.

## Artifacts

The completed artifacts are collected in the separate V2 package: `config.yaml`,
`metrics.json`, report PDF/DOCX, `checksums.sha256` and `MISSING_ITEMS.md`. The frozen
checkpoint `models/baseline_model.pt` and the stored splits were reused as-is.
