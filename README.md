# Trusted AI Practical Cycle — COVID-19 X-ray Classifier (БИИ Course)

Binary chest X-ray classification (COVID / Normal) with a **frozen ResNet-18 baseline**,
studied through the practical cycle of the course
«Безопасность и доверенность систем искусственного интеллекта»
(*Security and Trustworthiness of Artificial Intelligence Systems*).

This repository contains the **completed preliminary stage** (methodology §1) and
**Practical Work №1 — Data Quality Investigation** (methodology §2). Practical works
PR2, PR3 and PR4 are represented by placeholders and will be added without restructuring.

---

## 1. Project title

**Trusted AI Practical Cycle — COVID-19 X-ray Classifier**:
a reproducible audit of a medical imaging model — from the baseline experiment
to a quantitative data-quality profile.

## 2. Course information

| Item | Value |
|---|---|
| Course | «Безопасность и доверенность систем искусственного интеллекта» (БИИ), master's programme |
| Instructor | Новикова Е.С. |
| Group | 1378 |
| Students | Панов А. Ю., Семенов М. Д., Ханна М. Н. |

## 3. Overview

The practical cycle studies the trustworthiness of one model on one dataset:
data quality (PR1), robustness to natural corruptions (PR2), adversarial robustness (PR3)
and privacy (PR4). The baseline is trained once and then **frozen** — every subsequent
experiment loads the same checkpoint, so all differences in measured properties are
attributable to the studied effect rather than to retraining.

**What is included now**

1. **Preliminary stage (§1)** — seven foundation steps: analytical task and application
   context, dataset description, input/output modalities, train/validation/test splits,
   architecture and baseline training, primary quality metric, and full fixation of the
   experimental parameters (seed, splits, library versions, checkpoint).
2. **PR1 (§2)** — a quantitative, multidimensional data-quality profile: completeness,
   validity, uniqueness, train↔test leakage, balance, label quality (Confident Learning),
   representativeness (MMD + C2ST) and image anomalies (BRISQUE, NIQE, blur, borders).

**What is not included (yet):** PR2, PR3, PR4 results and the final consolidated report.
Their folders exist as placeholders so that future work does not require renaming or
moving any file. The dataset itself, the course PDFs and the original demo application
are **not** redistributed here.

## 4. Repository structure

```
BI-COURSE-REPO/
├── .github/workflows/ci.yml        # GitHub Actions: smoke tests on push/PR
├── .gitattributes                  # Git LFS rules (*.pth, *.pt, ...)
├── .gitignore                      # Python / Jupyter / OS / internal notes
├── LICENSE                         # MIT (code only; dataset has its own terms)
├── README.md                       # this file (English)
├── README.ru.md                    # Russian mirror
├── CITATION.cff                    # machine-readable citation metadata
├── CHANGELOG.md                    # version history (Keep a Changelog)
├── requirements.txt                # pinned library versions
├── environment.yml                 # conda environment (Python 3.13)
├── Makefile                        # install / reproduce / test / clean
├── docs/                           # documentation index, syllabus, reproduction guide
├── data/                           # dataset instructions (data itself is NOT committed)
├── models/                         # baseline_model.pt (Git LFS) + model card
├── src/                            # reusable code: data, models, utilities
│   ├── data/                       # dataset listing/loading + transforms
│   ├── models/                     # ResNet-18 architecture + frozen loader
│   └── utils/                      # seed, metrics (Wilson/bootstrap), I/O helpers
├── notebooks/                      # 00_train_baseline.ipynb, 01_data_quality.ipynb
├── configs/                        # preliminary_config.yaml, pr1_config.yaml
├── results/
│   ├── preliminary/                # metrics.json, training_history.json, split_indices.json, latency
│   └── pr1/                        # metrics_pr1.json, quality_profile.csv, label_inspection.csv, ...
├── reports/                        # preliminary_report.(pdf|docx), pr1_report.(pdf|docx)
├── figures/                        # preliminary/ (empty for now), pr1/ (300-dpi PNGs)
├── scripts/                        # reproduce_preliminary.py, reproduce_pr1.py, latency tool
├── tests/                          # pytest smoke tests (data, model, metrics)
├── PR2/                            # placeholder: Corruption Robustness (TODO)
├── PR3/                            # placeholder: Adversarial Robustness (TODO)
├── PR4/                            # placeholder: Privacy / MIA (TODO)
└── final_report/                   # placeholder: consolidated report (TODO after PR4)
```

## 5. Key results

**Baseline (preliminary stage).** ResNet-18 with ImageNet initialisation, all layers
frozen except `layer4` and the head (`Dropout(0.5) + Linear(512→2)`); 20 training epochs,
best epoch 15 (validation accuracy 0.9917). On the unmodified test set (720 images,
361 COVID / 359 Normal):

| Metric | Value |
|---|---|
| Accuracy **M(0)** | **0.9833** |
| 95% CI (Wilson) | **[0.9711; 0.9904]** |
| Confusion matrix | **TP 354 / FN 7 / FP 5 / TN 354** |
| Inference latency (CPU, batch 1) | 14.70 ± 0.81 ms per image |

**PR1 (data quality).** Main findings with 95% confidence intervals:

| Property | Result |
|---|---|
| Completeness | 0 unreadable files out of 7200 (0.0000% [0.0000; 0.0005]) |
| Validity | 100% grayscale, no image below 128 px on the short side |
| Exact duplicates (MD5) | 46 files = 0.6389% [0.0048; 0.0085] (34 groups) |
| Near duplicates (phash + pixel verification) | 262 files = 3.6389% [0.0323; 0.0410] (199 clusters) |
| Train↔test leakage | **7 exact + 64 near pairs** (0.12% and 1.11% of |train|) |
| Balance (test) | 361 / 359, imbalance ratio 0.9945, entropy 0.6931 |
| Label errors (cleanlab, 5-fold CV) | train 0/5760; test 3/720 = 0.4167% [0.0014; 0.0122] |
| Distribution shift | MMD² = −0.000392, permutation p = 0.705; C2ST AUC = 0.4885 [0.4640; 0.5139] → **no shift** |
| Image quality means | NIQE COVID 6.52 [6.31; 6.76] / Normal 5.91 [5.80; 6.02]; BRISQUE 29.06 / 29.73 |
| Anomalies | NIQE outliers 2.22% [0.61; 7.74]%; excessively blurred 2.50% [2.16; 2.89]% |

**What these results mean.** The dataset is balanced and representative (no distribution
shift, negligible label noise), which makes Accuracy a valid primary metric and justifies
measuring robustness curves on this test set. At the same time, 3.64% pixel-confirmed near
duplicates and 7 + 64 train↔test pairs constitute a real file-level leakage: some test
images have near-identical twins in the training set. This property is documented and
carried into the interpretation of PR2–PR4 (it may slightly inflate robustness and
membership-inference signals); it is **not** claimed to be solved here.

## 6. Quickstart

```bash
git clone https://github.com/username/bi-course-covid-xray.git
cd bi-course-covid-xray
git lfs pull                       # fetch models/baseline_model.pt

python -m pip install -r requirements.txt

# Put the dataset into data/raw/{COVID,Normal} (see data/README.md), then:
python scripts/reproduce_preliminary.py   # reproduces M(0) = 0.9833
python scripts/reproduce_pr1.py           # reproduces PR1 core metrics
```

Requirements: Python 3.13, Git LFS, ~50 MB of disk for the checkpoint (plus the dataset).
All reported numbers were obtained on CPU/GPU as documented; inference also works on CPU
(≈14.7 ms per image).

## 7. Reproduction guide

See [`docs/reproduction_guide.md`](docs/reproduction_guide.md) for the full step-by-step
procedure: prerequisites, LFS clone, dataset acquisition, checkpoint SHA-256 verification,
reproduction of the baseline metric and of the PR1 analysis, and verification against the
stored `results/` artifacts. A condensed version:

1. Install dependencies from `requirements.txt`.
2. Download the dataset and build `data/raw/{COVID,Normal}` (3600 images per class).
3. Apply the exact splits from `results/preliminary/split_indices.json`.
4. Load `models/baseline_model.pt` and confirm M(0) = 0.9833 [0.9711; 0.9904].
5. Run `scripts/reproduce_pr1.py` and compare with `results/pr1/metrics_pr1.json`.

## 8. Datasets

The dataset is **not** committed to this repository. Source, version, license and
download instructions are in [`data/README.md`](data/README.md):
Kaggle *COVID-19 Radiography Database* v4 (with a mirror used for byte-level
reproducibility), binary subset of 2 × 3600 chest X-ray images. The dataset is distributed
under its own terms (license label «Data files © Original Authors»); users must comply with
them. The MIT license of this repository applies to the code only.

## 9. License

- **Code and documentation:** MIT — see [`LICENSE`](LICENSE).
- **Dataset:** separate terms; not redistributed here (see `data/README.md`).
- **Reports and figures:** produced by the authors and distributed with the repository
  under the same MIT terms unless stated otherwise.

## 10. Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). GitHub renders a
«Cite this repository» button from it. Replace the placeholder URL with your repository
address after publishing.

## 11. Changelog

Version history follows *Keep a Changelog* — see [`CHANGELOG.md`](CHANGELOG.md).
Current version: **1.0.0** (preliminary stage + PR1).

## 12. Roadmap

| Stage | Topic | Status |
|---|---|---|
| Preliminary | Baseline model, dataset, splits, primary metric, fixation | **done** |
| PR1 | Data quality investigation (§2) | **done** |
| PR2 | Robustness to natural corruptions (noise, blur, JPEG), R(s), R-AUC | planned — `PR2/` |
| PR3 | Adversarial robustness (white-box FGSM/PGD + sanity attack), ASR, R-AUC_ε | planned — `PR3/` |
| PR4 | Privacy: Membership Inference Attack (ROC-AUC, TPR@FPR, gap) | planned — `PR4/` |
| Final | Consolidated report across PR1–PR4 | planned — `final_report/` |

Planned work reuses the same frozen checkpoint, the same splits and the same primary
metric, so all future results will be directly comparable with the numbers above.
