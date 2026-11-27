# Reports

| File | Language | Contents |
|---|---|---|
| `БИИ_preliminary.pdf` | Russian | Full cumulative report (mathematical version). Covers the preliminary stage (§1): goal and task, dataset, modalities, splits, architecture and training, primary metric and justification, baseline result with CI, reproducibility, plan for PR1–PR4, limitations. Sections for PR1–PR4 will be appended to the same file as the practical works are completed. |
| `БИИ_preliminary.docx` | Russian | Editable copy of the same report. |
| `БИИ_preliminary_simple.pdf` | Russian | Simplified version of the same preliminary-stage report: exactly the seven stage tasks (analytical task and context, dataset, modalities, splits, architecture and baseline training, primary metric, model saving and experiment fixation). No formulas or mathematical apparatus. |
| `БИИ_preliminary_simple.docx` | Russian | Editable copy of the simplified version. |
| `БИИ_PR1.pdf` | Russian | Standalone report for practical work 1 (data quality, §2): methodology, eight quality characteristics, results with 95 % Wilson CIs, near-duplicate train↔test leakage examples, brightness/blur distributions, anomalies and conclusions. No formulas. |
| `БИИ_PR1.docx` | Russian | Editable copy of the PR1 report. |
| `БИИ_PR2.pdf` | Russian | Standalone report for practical work 2 (corruption robustness, §3): protocol and corruption grid, examples of corruptions, R(s) curves with 95 % intervals, ΔM(s), R_rel(s), R-AUC with percentile/BCa intervals, significant drops and collapse levels, limitations. No formulas. |
| `БИИ_PR2.docx` | Russian | Editable copy of the PR2 report (13 pages, 11 tables, 2 embedded figures). |
| `БИИ_PR3.pdf` | Russian | Standalone report for practical work 3 (adversarial robustness, §4): threat model, white-box FGSM and PGD-10 on the ε grid, ASR over clean-correct objects, Robust Accuracy, Validity Rate, L₂/L∞, R-AUC_ε, multi-seed PGD, APGD-CE sanity check, limitations. No formulas. |
| `БИИ_PR3.docx` | Russian | Editable copy of the PR3 report (14 pages, 13 content tables, 2 embedded figures). |

## Notes

- There are two versions of the same preliminary-stage report: the full mathematical
  version (`БИИ_preliminary`) and the simplified version (`БИИ_preliminary_simple`) that
  contains only the stage requirements without formulas. Both describe the same model,
  dataset and numbers.
- `БИИ_PR1`, `БИИ_PR2` and `БИИ_PR3` are separate, standalone deliverables for practical
  works 1–3; they are not sections of the cumulative report. The PR4 report will be added
  later as a separate document, and the consolidated report in `final_report/` follows
  after PR4.
- The cumulative report is updated in place when a new practical work is finished.
- Reports are written in Russian (the course language); the repository documentation and
  code are in English.
- Each PDF is a page-for-page rendering of the matching DOCX version.
- The reports are self-contained: they cite the exact numbers stored in `results/` and
  reference the configuration files in `configs/`.
- `БИИ_PR2` embeds the corruption-example figure (Рис. 1 in that report), which also
  appears as Рис. 4 in the consolidated final report, and the robustness curves (Рис. 2).
  Both source PNGs are stored in `figures/pr2/`.
- `БИИ_PR3` embeds the PGD adversarial examples (Рис. 1 in §7.1 of that report) and the
  robust-accuracy curves (Рис. 2 in §8); the source PNGs are stored in `figures/pr3/`.
- Table 12 of the PR3 report marks the attack with the higher R-AUC_ε (FGSM) with a ★; the
  star is a ranking of the measured curves and not a claim of practical robustness.
- The instructor's name (Новикова Е.С.), group 1378 and the three authors are stated on
  the title page.
