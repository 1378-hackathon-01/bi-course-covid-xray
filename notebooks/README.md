# Notebooks

| Order | File | Content | Status |
|---|---|---|---|
| 1 | `00_train_baseline.ipynb` | Original training notebook: dataset organisation, 80/10/10 split (seed 42), ResNet-18 transfer learning, 20 epochs, checkpoint saving. | Executed (source of the frozen baseline) |
| 2 | `01_data_quality.ipynb` | PR1 analysis: inventory, image statistics, duplicates/leakage, embeddings, Confident Learning, MMD/C2ST, NIQE/BRISQUE, profile table and conclusions. | Executed (saved with outputs) |
| 3 | `02_corruption_robustness.ipynb` | PR2 analysis: corruption generators (Gaussian/Poisson noise, Gaussian blur, JPEG) on the severity grids, 60 runs over the frozen checkpoint, per-object correctness, R(s)/ΔM/R_rel, R-AUC with percentile and BCa bootstrap, robustness curves. | Executed (saved with outputs) |
| 4 | `03_adversarial_robustness.ipynb` | PR3 analysis: threat model, FGSM and PGD-10 on the ε grid {1, 2, 4, 8, 16}/255, per-object correctness masks, FR/RA with Wilson intervals, Validity Rate and L₂/L∞, R-AUC_ε with percentile bootstrap, multi-seed PGD and the APGD-CE sanity check. | Executed (saved with outputs) |

## Notes

- `01_data_quality.ipynb`, `02_corruption_robustness.ipynb` and
  `03_adversarial_robustness.ipynb` are **executed** notebooks: their outputs contain the
  intermediate counters and the arrays behind the reports and figures. They were produced
  in the original working environment (absolute paths, local dataset, GPU); the reusable,
  path-independent logic is extracted into `src/` and `scripts/` so that reproduction does
  not depend on those paths.
- The split scheme is deterministic (seed = 42, `torch.utils.data.random_split`); the exact
  indices are stored in `results/preliminary/split_indices.json` and are the canonical
  reference for all programs.
- Runtime on a laptop-class CPU: the PR1 notebook takes about 10–15 minutes (hashing 7200
  files, embedding extraction, image-quality metrics); the PR2 notebook performs 60 forward
  passes over the 720-image test set (43 200 predictions) plus B = 2000 bootstrap resamples
  per curve and is substantially faster on a GPU. The PR3 notebook runs the full FGSM/PGD-10
  grid with three restarts (about 1026 s for PGD and 49 s for FGSM on CUDA) plus the
  bootstrap bands. The training notebook requires a GPU and is **not** re-run — the
  checkpoint is frozen.
