# Course and repository scope

**Course:** «Безопасность и доверенность систем искусственного интеллекта»
*(Security and Trustworthiness of Artificial Intelligence Systems)*, master's programme.
Instructor: Новикова Е.С. Group: 1378.
Students: Панов А. Ю., Семенов М. Д., Ханна М. Н.

## The practical cycle

The course runs a four-stage practical cycle on a single dataset and a single baseline
model, so that every measured property is comparable across stages:

1. **Data quality** (§2 of the methodology) — a multidimensional profile: completeness,
   validity, uniqueness, train↔test leakage, balance, label quality (Confident Learning),
   representativeness (MMD/C2ST) and anomalies (BRISQUE, NIQE).
2. **Corruption robustness** (§3) — R(s) curves and R-AUC under natural corruptions
   (noise, blur, JPEG).
3. **Adversarial robustness** (§4) — white-box attacks (FGSM, PGD) with ASR and R-AUC_ε,
   plus an independent strong-attack sanity check.
4. **Privacy** (§5) — Membership Inference Attack with ROC-AUC, TPR@FPR and the
   generalization gap.

A consolidated final report (§6) closes the cycle.

## Scope of this repository

This repository contains the **preliminary stage** (seven foundation steps of §1:
task and context, dataset, modalities, splits, architecture and baseline training, primary
metric, full fixation of experimental parameters) and **Practical Work №1** (§2).
Practical works 2–4 and the final report are represented by placeholder folders with
their planned scope; they will be added without restructuring the repository.

## Why the baseline is frozen

All stages must measure properties of the *same* model. Retraining between stages would
confound the measured effects with random variation of training. The checkpoint
`models/baseline_model.pt` is therefore loaded as-is by every program in the repository,
and its SHA-256 is recorded in the model card. This is the foundational rule of the course
methodology (§1, closing paragraph).
