# Figures

## `preliminary/`

Intentionally empty: the preliminary stage is documented by tables and the model card; no
figures were produced (the `.gitkeep` keeps the folder in the repository so PR2–PR4 can use
the same layout).

## `pr1/`

| File | Description |
|---|---|
| `class_distribution.png` | Class counts per split (train/validation/test) — 5760/720/720, 2884+2876 / 355+365 / 361+359. |
| `niqe_histogram.png` | NIQE distribution by class (450-image stratified subsample). |
| `brisque_histogram.png` | BRISQUE distribution by class (same subsample). |
| `duplicate_examples.png` | Pixel-verified near-duplicate pairs that fall into different splits. |
| `suspicious_labels.png` | The ten train images with the lowest out-of-sample confidence (Confident Learning inspection). |
| `brightness_blur.png` | Laplacian-variance (blur) and brightness distributions by class. |

All figures are 300-dpi PNG files with Russian axis labels.

## Known gap

The MMD null distribution and the C2ST ROC curve are computed inside the notebook and are
available in its outputs, but were not exported as standalone PNG files in this release.
This is documented as a limitation of the PR1 stage (see the report, section «Ограничения
ПР1»); adding them later requires no restructuring — they belong in this folder.
