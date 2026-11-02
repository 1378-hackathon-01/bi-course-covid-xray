# PR4 - Privacy: Membership Inference

**Status: completed.** The full V2 submission package is maintained separately and is not
stored in this repository; this folder keeps the package README.

Key result: image-level MIA finds a **weak, borderline** membership signal — ROC-AUC 0.556,
Attack Accuracy 0.546, TPR@FPR ≤ 1% essentially zero. The BCa loss lower bound is 0.5017,
the entropy BCa interval includes 0.5, and loss/confidence/entropy are monotone views of the
same signal, not independent evidence.

## Scope (methodology §5)

- Privacy unit defined explicitly: image-level. Patient-level analysis is not possible
  because the dataset has no patient identifiers.
- Member/non-member samples with equal sizes, comparable class distribution and the same
  origin; the threshold is tuned on a separate validation split, not on evaluation data.
- Loss-, confidence- and entropy-threshold attacks with ROC-AUC, Attack Accuracy (Wilson
  interval), TPR@FPR = 1% and 0.1%, and the generalization gap.
- Stratified bootstrap for ROC-AUC and TPR@FPR; conclusion on observable membership
  leakage, framed as weak/borderline rather than strong leakage.

## Artifacts

The completed artifacts are collected in the separate V2 package: `config.yaml`,
`metrics.json`, report PDF/DOCX, `checksums.sha256` and `MISSING_ITEMS.md`. The frozen
checkpoint and the same splits were reused.
