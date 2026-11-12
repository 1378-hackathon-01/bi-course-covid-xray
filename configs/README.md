# Configuration files

| File | Scope | Contents |
|---|---|---|
| `preliminary_config.yaml` | Preliminary stage (§1) | The seven reproducibility items: dataset source/version, split scheme and seed, model architecture and initialisation, training hyperparameters, library versions, primary metric and its computation method. |
| `pr1_config.yaml` | PR1 (§2) | Analysis parameters: seed, bootstrap (B = 2000, percentile), MMD (RBF kernel, median-heuristic bandwidth, 200 permutations, observed p-value), C2ST (logistic regression, 5-fold CV, AUC and its bootstrap interval), Confident Learning settings, duplicate thresholds, leakage counts, image-quality means, anomaly criteria and thresholds, remediation status for G-1/G-2/G-3. |
| `pr2_config.yaml` | PR2 (§3) | Corruption-robustness protocol: seed, checkpoint identity, test-set composition, four corruption types with their severity grids and repeat counts (r = 5 for stochastic noise, r = 1 for deterministic blur/JPEG), 60 runs / 43 200 corrupted predictions, metric definitions (R(s), ΔM, R_rel, trapezoidal R-AUC weights), bootstrap settings (B = 2000, percentile + BCa), the reported R-AUC values, first significant drops, collapse levels and the documented deviations. |

## Notes

- `preliminary_config.yaml` is the machine-readable counterpart of the human-readable
  report; it is the single source of truth for hyperparameters.
- `pr1_config.yaml` records the *actual* values used, including the number of MMD
  permutations (200) and the actual C2ST interval method (bootstrap for the AUC, Wilson for
  proportions) — these differ from generic defaults and are documented explicitly.
- `pr2_config.yaml` is the repository-path adaptation of the PR2 bundle config: it points to
  `configs/preliminary_config.yaml`, `results/preliminary/split_indices.json` and
  `models/baseline_model.pt` instead of the submission-relative paths, and its
  machine-readable counterpart is `results/pr2/metrics_pr2.json` (kept verbatim).
- All files are plain YAML without custom tags, so `yaml.safe_load` works everywhere.
- Future works (PR3–PR4) will add their own config files in the same folder without
  changing these.
