# Configuration files

| File | Scope | Contents |
|---|---|---|
| `preliminary_config.yaml` | Preliminary stage (§1) | The seven reproducibility items: dataset source/version, split scheme and seed, model architecture and initialisation, training hyperparameters, library versions, primary metric and its computation method. |
| `pr1_config.yaml` | PR1 (§2) | Analysis parameters: seed, bootstrap (B = 2000, percentile), MMD (RBF kernel, median-heuristic bandwidth, 200 permutations, observed p-value), C2ST (logistic regression, 5-fold CV, AUC and its bootstrap interval), Confident Learning settings, duplicate thresholds, leakage counts, image-quality means, anomaly criteria and thresholds, remediation status for G-1/G-2/G-3. |

## Notes

- `preliminary_config.yaml` is the machine-readable counterpart of the human-readable
  report; it is the single source of truth for hyperparameters.
- `pr1_config.yaml` records the *actual* values used, including the number of MMD
  permutations (200) and the actual C2ST interval method (bootstrap for the AUC, Wilson for
  proportions) — these differ from generic defaults and are documented explicitly.
- Both files are plain YAML without custom tags, so `yaml.safe_load` works everywhere.
- Future works (PR2–PR4) will add their own config files in the same folder without
  changing these.
