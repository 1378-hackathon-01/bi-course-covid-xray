# Figures

## `preliminary/`

Intentionally empty: the preliminary stage is documented by tables and the model card; no
figures were produced (the `.gitkeep` kept the folder in the repository so the later
stages could reuse the same layout).

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

## `pr2/`

| File | Description |
|---|---|
| `robustness_curves.png` | R(s) curves for the four corruption types (test = 720 images; shaded band = 95 % bootstrap CI; dashed line = M(0) = 0.9833). |
| `corruption_examples.png` | Visual examples of the four corruptions for one COVID X-ray: rows = corruption type, columns = clean image and severity levels 1, 3, 5. |

The PR2 report (`reports/БИИ_PR2.pdf`) embeds both figures: the corruption examples as
Рис. 1 in §3 and the robustness curves as Рис. 2 in §6.

## `pr3/`

| File | Description |
|---|---|
| `pr3_adversarial_examples.png` | PGD examples at ε = 8/255: top row — clean X-rays, bottom row — adversarial; all pairs switch the prediction from COVID to Normal while the perturbation stays visually imperceptible. Embedded as Рис. 1 in §7.1 of the PR3 report. |
| `pr3_robustness_vs_eps.png` | Robust Accuracy curves ε → M_robust(ε) for PGD-10 and FGSM (200-image subset; shaded band = 95 % bootstrap CI; dashed line = M_sub(0) = 0.9850; the FGSM curve carries the ★). Embedded as Рис. 2 in §8. |

The PR3 report (`reports/БИИ_PR3.pdf`) embeds both figures.

## Known gap

The MMD null distribution and the C2ST ROC curve are computed inside the notebook and are
available in its outputs, but were not exported as standalone PNG files in this release.
This is documented as a limitation of the PR1 stage (see the report, section «Ограничения
ПР1»); adding them later requires no restructuring — they belong in this folder.
