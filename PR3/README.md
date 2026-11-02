# PR3 - Adversarial Robustness

**Status: completed.** The full V2 submission package is maintained separately and is not
stored in this repository; this folder keeps the package README.

Key result: in the white-box untargeted L∞ protocol, PGD-10 fools 197/197 clean-correct
objects at ε = 1/255 (ASR = 1.000), R-AUC_ε = 0.032. The independent check is APGD-CE on
n = 20, not full AutoAttack; the untargeted protocol does not measure the error direction.

## Scope (methodology §4)

- Explicit threat model: white-box access, untargeted goal, L∞ perturbation budget,
  fixed ε grid {1, 2, 4, 8, 16}/255.
- White-box attacks: FGSM and PGD-10 (iterations, step size and restarts documented).
- Metrics: clean and robust performance, ASR computed over clean-correct objects,
  perturbation magnitude (L∞/L2), Validity Rate, R-AUC over the ε grid.
- Independent check: APGD-CE at ε = 8/255 on n = 20. This is not the full AutoAttack
  composition; APGD-T/FAB-T and DLR losses were not used.
- The protocol is untargeted, so the direction of errors (including COVID → Normal) is
  not measured quantitatively.

## Artifacts

The completed artifacts are collected in the separate V2 package: `config.yaml`,
`metrics.json`, report PDF/DOCX, `checksums.sha256` and `MISSING_ITEMS.md`. The frozen
checkpoint and the same test subset were reused.
