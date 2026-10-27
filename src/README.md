# Source code (`src/`)

Reusable modules extracted from the training notebook (`notebooks/00_train_baseline.ipynb`)
and the PR1 notebook (`notebooks/01_data_quality.ipynb`). The modules are deliberately
dependency-light and importable from the reproduction programs in `scripts/`.

| Module | Purpose |
|---|---|
| `src/data/transforms.py` | Inference and training preprocessing (Resize 224, ImageNet normalisation, light augmentation). |
| `src/data/dataset.py` | ImageFolder-ordered listing, explicit-index subsets, `torch.utils.data.Dataset` wrapper. |
| `src/models/architecture.py` | ResNet-18 + Dropout/Linear head; `load_frozen_model()` loads the checkpoint in eval mode. |
| `src/utils/seed.py` | `set_seed(42)` for Python/NumPy/PyTorch/CUDA plus deterministic cuDNN. |
| `src/utils/metrics.py` | Wilson interval, percentile bootstrap, paired bootstrap, trapezoidal R-AUC. |
| `src/utils/io.py` | JSON helpers, checkpoint loading, SHA-256 of files. |

## Conventions

- All modules expose a small `__main__` block with a usage example.
- Paths are resolved relative to the repository root, so the code works after a plain
  `git clone` (plus `git lfs pull`) without editing environment variables.
- The statistical helpers follow the course rules: Wilson for proportions, bootstrap
  (B = 2000, percentile) for means and non-linear metrics, paired bootstrap for paired
  comparisons.

## Example

```python
from src.models.architecture import load_frozen_model
from src.data.dataset import list_dataset
from src.data.transforms import eval_transforms

model = load_frozen_model("models/baseline_model.pt")
paths, labels = list_dataset("data/raw")
print(len(paths), labels[:5])
```
