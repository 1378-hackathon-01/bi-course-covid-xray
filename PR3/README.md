# PR3 — Adversarial Robustness (TODO)

**Status: not started.** Will be added in a future release without restructuring.

## Planned scope (methodology §4)

- Explicit threat model: white-box access, untargeted goal, L∞ perturbation budget,
  fixed ε grid.
- White-box attacks: FGSM and PGD (iterations, step size and restarts documented).
- Metrics: clean and robust performance, ASR computed over clean-correct objects,
  perturbation magnitude (L∞/L2), Validity Rate, R-AUC over the ε grid.
- Independent strong-attack sanity check (AutoAttack-class) to rule out gradient masking.
- Conclusion on the most dangerous attack budgets and directions.

## Planned artifacts

`configs/pr3_config.yaml`, `results/pr3/`, `reports/БИИ_preliminary.(pdf|docx)` (PR3 section
appended to the single cumulative report),
`figures/pr3/`, `scripts/reproduce_pr3.py`, notebook `notebooks/03_adversarial_robustness.ipynb`.
The frozen checkpoint and the same test subset will be reused.
