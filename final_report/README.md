# Consolidated final report

**Status: completed.**

- `Final_Report.pdf` — 17 pages, Russian, 10 tables, 7 figures, compact summary table per §6.2.
- `Final_Report.docx` — editable source of the same report.

## Scope

The report follows the methodology §6.1 structure: summary, sections 1–10, appendices A–B.
It covers the frozen baseline and the complete PR1–PR4 cycle:

1. subject area and analytical task;
2. dataset and model;
3. baseline quality with Wilson/bootstrap intervals;
4. PR1 data-quality profile (duplicates, train↔test leakage, label noise, MMD/C2ST);
5. PR2 corruption robustness (Gaussian/Poisson noise, blur, JPEG; R(s), ΔM(s), R-AUC);
6. PR3 adversarial robustness (FGSM, PGD-10, APGD-CE sanity check; white-box, untargeted, L∞);
7. PR4 membership inference (image-level privacy unit; loss/confidence/entropy scores);
8. synthesis of evidence and the consolidated §6.2 table;
9. limitations;
10. conditional conclusion on admissible use and trust boundaries.

## Key caveats carried into the conclusions

- PR3: the independent check is **APGD-CE on n = 20**, not full AutoAttack; APGD-T/FAB-T and
  DLR were not used. The protocol is untargeted, so the error direction (including
  COVID → Normal) is not measured quantitatively.
- PR4: the membership signal is described as **weak and borderline**, not as strong leakage.
  Percentile intervals for loss/confidence exclude 0.5, but the BCa loss lower bound is
  0.5017, the entropy BCa interval includes 0.5, and the Attack Accuracy lower bound is only
  0.0022 above 0.5. TPR@FPR ≤ 1% is essentially zero. Loss, confidence and entropy are
  monotone functions of the same outputs and are not independent evidence.
- Duplicates and train↔test leakage may both amplify and attenuate the measured effects;
  the direction of the aggregate effect is not measured.
- All conclusions are conditional on the frozen checkpoint, the selected data, the threat
  model and the stated statistical uncertainty.

## Verification

- PDF text layer is readable; 0 replacement characters.
- DOCX contains 10 tables and 7 inline figures.
- Reported numbers are reconciled with the V2 packages (`PR2_SUBMISSION_V2`,
  `PR3_SUBMISSION_V2`, `PR4_SUBMISSION_V2`) and the source JSON/CSV artefacts.
