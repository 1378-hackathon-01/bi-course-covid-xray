# PR3 — Adversarial Robustness (§4)

**Status: complete.** The report, configuration, results, figures and executed notebook
are in the repository; this folder is the human-readable entry point to the practical work.

## Scope (methodology §4)

- Frozen baseline, the same `models/baseline_model.pt` used in PR1 and PR2, never retrained:
  M(0) = 0.9833 [0.9711; 0.9904] on the 720-image test set,
  TP/FN/FP/TN = 354/7/5/354.
- **Explicit threat model (§4.2):** white-box access to the architecture, weights and input
  gradients; untargeted goal (any wrong prediction); L∞ perturbation in the [0, 1] pixel
  space after `Resize(224, 224)`; ε ∈ {1, 2, 4, 8, 16}/255; query budget N/A.
- **Attacks (§4.3):** FGSM (1 step) and PGD-10 (10 steps, α = ε/4, random start,
  3 restarts, best-of-loss). Both are implemented directly in PyTorch.
- **Metrics (§4.4):** FR = ASR with the denominator equal to the number of clean-correct
  objects (197), Robust Accuracy with the denominator 200, Wilson 95 % intervals,
  perturbation L₂/L∞, Validity Rate, and R-AUC_ε with a percentile bootstrap
  (B = 2000, the whole curve is rebuilt on every resample).
- **Stability checks (§4.6):** multi-seed PGD at ε = 8/255 (seeds 42/43/44) and an
  independent APGD-CE sanity check (`torchattacks`, 100 iterations, 20 images).
- White-box only: no black-box or physical attacks. Natural corruptions belong to PR2,
  membership inference belongs to PR4.

The attack subset is a deterministic stratified sample of 200 test images
(100 COVID / 100 Normal); 197 of them are classified correctly on clean inputs
(98 COVID / 99 Normal), so M_sub(0) = 0.9850 [0.9568; 0.9949]. ASR is computed over
these 197 objects, while Robust Accuracy is computed over all 200.

## Key results

| Attack | ε, /255 | FR = ASR [95 % CI] | Robust accuracy [95 % CI] | R-AUC_ε [95 % CI] |
|---|---:|---|---|---|
| PGD-10 | 1, 2, 4, 8 | 1.000 [0.981; 1.000] | 0.000 [0.000; 0.019] | 0.0320 [0.0303; 0.0348] |
| PGD-10 | 16 | 0.995 [0.972; 0.999] | 0.005 [0.001; 0.028] | — |
| FGSM | 1 | 0.558 [0.489; 0.626] | 0.435 [0.368; 0.504] | 0.5111 [0.4497; 0.5798] |
| FGSM | 2, 4, 8, 16 | 0.503 [0.433; 0.572] | 0.500 [0.431; 0.569] | — |

- **PGD-10** breaks all 197 clean-correct images at the smallest budget ε = 1/255;
  at ε = 16/255 one image survives. The near-zero R-AUC_ε reflects a curve that stays at
  zero across almost the whole grid.
- **FGSM** is weaker because of its single coarse step and saturates at ε ≥ 2/255:
  the plateau FR = 0.503 / RA = 0.500 corresponds to the random-guessing level on a
  balanced subset, not to retained robustness. The higher FGSM R-AUC_ε is the reason it
  carries the ★ in Table 12 of the report; the star ranks the measured curves only and is
  **not** a claim that FGSM is a safer scenario.
- **Multi-seed PGD** at ε = 8/255: FR = 1.000 and RA = 0.000 for all three seeds,
  max − min = 0.000 — the result is not an artefact of one random start.
- **APGD-CE sanity check** at ε = 8/255 on 20 images: FR = 1.000 [0.839; 1.000],
  RA = 0.000 [0.000; 0.161]. The independent attack is not weaker than the custom PGD,
  so there is no sign of gradient masking on the checked subset.
- **Validity Rate** = 1.000 for all 10 (attack, ε) cells (2000/2000 valid); the maximum
  L∞ norm is 0.06275, i.e. the 16/255 budget up to float32 rounding.

All 10 point estimates and Wilson intervals in the report are re-derived from
`pr3_masks.pkl` by `scripts/reproduce_pr3.py`, which reports `RESULT: PASS`.

## Artifacts

| Path | Content |
|---|---|
| `reports/БИИ_PR3.pdf` / `.docx` | Standalone Russian report (14 pages, 13 content tables, 2 figures, no formulas). |
| `configs/pr3_config.yaml` | Threat model, ε grid, attack parameters, bootstrap settings, results and documented deviations (repo-path adaptation). |
| `results/pr3/metrics_pr3.json` | Machine-readable results (verbatim PR3 bundle file). |
| `results/pr3/pr3_adv_attacks.csv` | The 10-row FR / Robust Accuracy table with Wilson intervals, L₂ and L∞. |
| `results/pr3/pr3_rauc.csv` | R-AUC_ε for FGSM and PGD-10 with percentile bootstrap intervals. |
| `results/pr3/pr3_validity_l2.csv` | Validity Rate and L₂/L∞ statistics for all 10 cells. |
| `results/pr3/pr3_multiseed_pgd.csv` | PGD-10 at ε = 8/255 for seeds 42, 43 and 44. |
| `results/pr3/pr3_autoattack.json` | APGD-CE sanity check at ε = 8/255 on 20 images. |
| `results/pr3/pr3_summary.json` | Compact notebook summary: attack rows, R-AUC, bootstrap bands. |
| `results/pr3/pr3_masks.pkl` | Per-object clean/adversarial correctness masks for all 10 cells — the input of the verification script. |
| `results/pr3/pr3_masks_fgsm.pkl` | Per-object FGSM correctness masks (intermediate notebook cache). |
| `results/pr3/checksums.sha256` | Checksums of the PR3 artifacts and inherited files. |
| `figures/pr3/pr3_adversarial_examples.png` | PGD ε = 8/255 visual pairs, clean vs adversarial (Рис. 1 in §7.1). |
| `figures/pr3/pr3_robustness_vs_eps.png` | Robust Accuracy curves with 95 % bands (Рис. 2 in §8). |
| `notebooks/03_adversarial_robustness.ipynb` | Executed analysis notebook (12 cells, 11 code cells). |
| `scripts/reproduce_pr3.py` | Model-free verification of all 10 FR/RA rows, Wilson intervals, both R-AUC values, validity, multi-seed and APGD-CE results. |

## Reproduction

```bash
python scripts/reproduce_pr3.py     # expects RESULT: PASS
```

The script reads only `results/pr3/pr3_masks.pkl` and the stored tables — no model, images
or GPU are needed. The full pipeline (attack generation, bootstrap bands, figures) is
reproduced by `notebooks/03_adversarial_robustness.ipynb` with the frozen checkpoint and the
dataset described in `docs/reproduction_guide.md`. The main PGD run took about 1026 s on
CUDA; FGSM took about 49 s.

## Documented deviations

- FGSM and PGD-10 are implemented directly in PyTorch rather than through `torchattacks`;
  their signatures and parameters follow `torchattacks` 3.5.1.
- The independent check uses APGD-CE, the key component of AutoAttack; the targeted/DLR
  components are not defined for a two-class problem, and only 20 images are used because
  of the VRAM behaviour of the library on a 4 GB GPU.
- No separate paired bootstrap was built for F1/ROC-AUC: these metrics are not part of the
  §4.4 set for PR3.
- The inference latency 14.70 ± 0.81 ms/image is carried over from PR1 and is not a new
  PR3 measurement; the source JSON names the checkpoint `baseline_model.pt`.
- No adversarial training or other defence was applied: the checkpoint is frozen by design.
- No multiple-comparison correction across the 10 grid cells; the reported intervals are
  pointwise.
- The direction of the error (COVID → Normal vs Normal → COVID) is not separated.
- The train↔test leakage documented in PR1 (7 exact + 64 near pairs) remains a caveat:
  a perturbation crafted for one duplicate may not transfer to its twin, so absolute
  robustness values should be read with this limitation in mind.
