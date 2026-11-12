# PR2 — Corruption Robustness (§3)

**Status: complete.** The report, configuration, results, figures and notebook are in the
repository; this folder is the human-readable entry point to the practical work.

## Scope (methodology §3)

- Frozen baseline (the same `models/baseline_model.pt`, never retrained) evaluated on the
  unmodified 720-image test set: M(0) = 0.9833 [0.9711; 0.9904], TP/FN/FP/TN = 354/7/5/354.
- Four corruption types, each on five non-zero severity levels:

  | Corruption | Parameter | Levels s = 1…5 | Repeats |
  |---|---|---|---|
  | Gaussian noise | σ | 0.005; 0.01; 0.02; 0.04; 0.08 | r = 5 |
  | Poisson (shot) noise | λ | 2048; 1024; 512; 256; 128 | r = 5 |
  | Gaussian blur | σ_px | 0.5; 1; 2; 3.5; 5 | r = 1 |
  | JPEG compression | q | 90; 70; 50; 30; 15 | r = 1 |

- 60 runs in total (20 (corruption, severity) cells with r = 5 or r = 1) and
  43 200 corrupted predictions; the object × realization structure of the test set is
  preserved.
- Robustness curves R(s), relative degradation ΔM(s) = M(0) − R(s) and R_rel(s) = R(s)/M(0)
  with 95 % bootstrap intervals; trapezoidal R-AUC over the uniform grid 0…5 with percentile
  and BCa intervals; paired bootstrap for ΔM.

## Key results

| Corruption | R-AUC | 95 % CI (percentile) | 95 % CI (BCa) |
|---|---|---|---|
| JPEG compression | 0.8218 | [0.8017; 0.8404] | [0.8012; 0.8381] |
| Gaussian blur | 0.7876 | [0.7699; 0.8036] | [0.7698; 0.8039] |
| Gaussian noise | 0.6252 | [0.5958; 0.6527] | [0.5959; 0.6515] |
| Poisson noise | 0.5600 | [0.5266; 0.5913] | [0.5269; 0.5920] |

The first statistically significant drop occurs already at the lowest level: Gaussian noise
σ = 0.005 (R = 0.8181, ΔM = 0.1653 [0.1375; 0.1944]), Poisson noise λ = 2048 (R = 0.5472,
ΔM = 0.4361 [0.4014; 0.4750]), blur σ_px = 1 (R = 0.9611, ΔM = 0.0222 [0.0083; 0.0375]) and
JPEG q = 90 (R = 0.9694, ΔM = 0.0139 [0.0027; 0.0278]). Collapse below R = 0.55 is reached
at σ ≥ 0.02, λ ≤ 2048, σ_px ≥ 3.5 and q = 15.

## Artifacts

| Path | Content |
|---|---|
| `reports/БИИ_PR2.pdf` / `.docx` | Standalone Russian report (13 pages, 11 tables, 2 figures, no formulas). |
| `configs/pr2_config.yaml` | Protocol, grids, metric definitions, bootstrap settings, deviations (repo-path adaptation). |
| `results/pr2/metrics_pr2.json` | Machine-readable results (verbatim PR2 bundle file). |
| `results/pr2/summary_table.tsv` | The 20-row R(s)/ΔM/R_rel table with interval bounds. |
| `results/pr2/rauc.csv` | R-AUC estimates with percentile and BCa intervals. |
| `results/pr2/correctness.pkl` | Per-object correctness used by the verification script. |
| `results/pr2/checksums.sha256` | Checksums of the PR2 artifacts and inherited preliminary files. |
| `figures/pr2/robustness_curves.png` | R(s) curves with 95 % bands (Рис. 2 in the report). |
| `figures/pr2/corruption_examples.png` | Visual corruption examples, clean plus severities 1/3/5 (Рис. 1). |
| `notebooks/02_corruption_robustness.ipynb` | Executed analysis notebook (corruptions, predictions, bootstrap, curves). |
| `scripts/reproduce_pr2.py` | Model-free verification of all 20 R(s)/ΔM/R_rel and 4 R-AUC values. |

## Reproduction

```bash
python scripts/reproduce_pr2.py     # expects RESULT: PASS
```

The script reads only `results/pr2/correctness.pkl` and the stored tables — no model, images
or GPU are needed. The full pipeline, including the bootstrap intervals and the curves, is
reproduced by `notebooks/02_corruption_robustness.ipynb` with the frozen checkpoint and the
dataset (see `docs/reproduction_guide.md`).

## Documented deviations

- Deterministic corruptions (blur, JPEG) use r = 1 rather than the recommended r ≥ 5;
  their uncertainty is assessed by bootstrap resampling of objects.
- The noise grids were fixed after a pilot run and start at low intensity levels; even so,
  the first measured point already shows a significant drop.
- Corruptions are applied after `Resize(224, 224)`, not at the native 299 × 299 resolution.
- No multiple-comparison correction across the 20 grid points; the reported intervals are
  pointwise.
- No external or prospective clinical validation was performed.
