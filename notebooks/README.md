# Notebooks

| Order | File | Content | Status |
|---|---|---|---|
| 1 | `00_train_baseline.ipynb` | Original training notebook: dataset organisation, 80/10/10 split (seed 42), ResNet-18 transfer learning, 20 epochs, checkpoint saving. | Executed (source of the frozen baseline) |
| 2 | `01_data_quality.ipynb` | PR1 analysis: inventory, image statistics, duplicates/leakage, embeddings, Confident Learning, MMD/C2ST, NIQE/BRISQUE, profile table and conclusions. | Executed (saved with outputs) |

## Notes

- `01_data_quality.ipynb` is the **executed** notebook: its outputs contain the intermediate
  counters used in the reports and figures. It was produced in the original working
  environment (absolute paths, local dataset); the reusable, path-independent logic is
  extracted into `src/` and `scripts/` so that reproduction does not depend on those paths.
- The split scheme is deterministic (seed = 42, `torch.utils.data.random_split`); the exact
  indices are stored in `results/preliminary/split_indices.json` and are the canonical
  reference for all programs.
- Runtime on a laptop-class CPU: the PR1 notebook takes about 10–15 minutes (hashing 7200
  files, embedding extraction, image-quality metrics); the training notebook requires a GPU
  and is **not** re-run — the checkpoint is frozen.
