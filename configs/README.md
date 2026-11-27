# Configuration files

| File | Scope | Contents |
|---|---|---|
| `preliminary_config.yaml` | Preliminary stage (§1) | The seven reproducibility items: dataset source/version, split scheme and seed, model architecture and initialisation, training hyperparameters, library versions, primary metric and its computation method. |
| `pr1_config.yaml` | PR1 (§2) | Analysis parameters: seed, bootstrap (B = 2000, percentile), MMD (RBF kernel, median-heuristic bandwidth, 200 permutations, observed p-value), C2ST (logistic regression, 5-fold CV, AUC and its bootstrap interval), Confident Learning settings, duplicate thresholds, leakage counts, image-quality means, anomaly criteria and thresholds, remediation status for G-1/G-2/G-3. |
| `pr2_config.yaml` | PR2 (§3) | Corruption-robustness protocol: seed, checkpoint identity, test-set composition, four corruption types with their severity grids and repeat counts (r = 5 for stochastic noise, r = 1 for deterministic blur/JPEG), 60 runs / 43 200 corrupted predictions, metric definitions (R(s), ΔM, R_rel, trapezoidal R-AUC weights), bootstrap settings (B = 2000, percentile + BCa), the reported R-AUC values, first significant drops, collapse levels and the documented deviations. |
| `pr3_config.yaml` | PR3 (§4) | Adversarial-robustness protocol: explicit white-box threat model, deterministic 200-image subset (100/100, 197 clean-correct), ε grid {1, 2, 4, 8, 16}/255, FGSM and PGD-10 parameters (3 restarts, α = ε/4, best-of-loss), APGD-CE sanity check on 20 images, metric definitions (ASR denominator = clean-correct, R-AUC_ε trapezoid), R-AUC_ε bootstrap settings (B = 2000), the reported results and the documented deviations (custom PyTorch implementations, AutoAttack subset, latency inherited from PR1). |

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
- `pr3_config.yaml` follows the same pattern for PR3: the threat model and attack
  parameters are fixed before the experiment, `results/pr3/metrics_pr3.json` is the
  verbatim machine-readable counterpart, and the deviations record that FGSM/PGD-10 are
  custom PyTorch implementations and that the independent check is APGD-CE on 20 images.
- All files are plain YAML without custom tags, so `yaml.safe_load` works everywhere.
- Future work (PR4) will add its own config file in the same folder without changing these.
