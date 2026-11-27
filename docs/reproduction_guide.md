# Reproduction guide

## English

### 1. Prerequisites

- Python 3.13 (the environment used for the reported results).
- Git with Git LFS installed (`git lfs version` must work).
- ~50 MB for the checkpoint plus ~1 GB for the dataset.
- CPU is sufficient; a GPU is optional. Inference on CPU takes ~14.7 ms per image.

### 2. Clone the repository with LFS

```bash
git clone https://github.com/minaNabil96/bi-course-covid-xray.git
cd bi-course-covid-xray
git lfs pull
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Obtain the dataset

Follow [`../data/README.md`](../data/README.md). The expected layout after extraction is
`data/raw/{COVID,Normal}` with **3600 images per class** (7200 total). The dataset is not
redistributed here.

### 5. Verify the checkpoint

```bash
python -c "from src.utils.io import sha256_file; print(sha256_file('models/baseline_model.pt'))"
# must print: 0ba793cb43d0f058af66673a1026e6eef4bd898d98cae05eaf6694cb20b504f0
```

### 6. Reproduce the baseline metric

```bash
python scripts/reproduce_preliminary.py
# expected: accuracy 0.983333 [Wilson 95% CI: 0.9711; 0.9904],
#           TP=354 FN=7 FP=5 TN=354, RESULT: PASS
```

### 7. Reproduce the PR1 analysis

```bash
python scripts/reproduce_pr1.py           # full, including near duplicates
python scripts/reproduce_pr1.py --skip-phash   # faster deterministic subset
```

The program re-computes readability, colour modes, MD5 duplicates and (optionally)
pixel-verified near duplicates, and compares them with `results/pr1/quality_profile.csv`.
Embedding-based checks (MMD, C2ST) and label-quality analysis are reproduced by the
executed notebook `notebooks/01_data_quality.ipynb`.

### 8. Reproduce the PR2 robustness metrics

```bash
python scripts/reproduce_pr2.py
# expected: M(0) = 0.983333, 20 R(s)/ΔM/R_rel checks and 4 R-AUC checks, RESULT: PASS
```

The program is model-free: it rebuilds R(s), ΔM(s), R_rel(s) and R-AUC from the stored
per-object correctness (`results/pr2/correctness.pkl`) and compares them with
`results/pr2/summary_table.tsv` and `results/pr2/rauc.csv`. The bootstrap confidence
intervals (hierarchical/paired bootstrap, B = 2000, percentile + BCa) are reproduced by
`notebooks/02_corruption_robustness.ipynb`, which needs the checkpoint and the dataset;
the resulting curves are in `figures/pr2/robustness_curves.png`.

### 9. Reproduce the PR3 adversarial-robustness metrics

```bash
python scripts/reproduce_pr3.py
# expected: 10 (attack, epsilon) rows, both R-AUC_eps values,
#           validity, multi-seed and APGD-CE checks, RESULT: PASS
```

The program is model-free: it recomputes FR (= ASR), Robust Accuracy, the Wilson
intervals and R-AUC_ε from the stored per-object correctness masks
(`results/pr3/pr3_masks.pkl`) and compares them with `results/pr3/pr3_adv_attacks.csv`,
`results/pr3/pr3_rauc.csv`, `results/pr3/pr3_validity_l2.csv`,
`results/pr3/pr3_multiseed_pgd.csv` and `results/pr3/pr3_autoattack.json`. The attack
pipeline, the percentile bootstrap bands and the figures are reproduced by
`notebooks/03_adversarial_robustness.ipynb`, which needs the checkpoint, the dataset and
a GPU (the main PGD run took about 1026 s on CUDA; FGSM took about 49 s).

### 10. Verify stored artifacts

Every artifact in `results/` was produced by the executed notebooks;
`results/pr1/checksums.sha256` lists the PR1 files, `results/pr2/checksums.sha256`
lists the PR2 files plus the inherited preliminary artifacts, and
`results/pr3/checksums.sha256` lists the PR3 files. Compare the outputs of the
programs above with the stored JSON/CSV.

## Русский

### 1. Требования

- Python 3.13 (среда, в которой получены результаты).
- Git с установленным Git LFS (`git lfs version`).
- ~50 МБ под чекпойнт и ~1 ГБ под набор данных.
- Достаточно CPU; GPU опционален. Инференс на CPU — около 14,7 мс на снимок.

### 2. Клонирование с LFS

```bash
git clone https://github.com/minaNabil96/bi-course-covid-xray.git
cd bi-course-covid-xray
git lfs pull
```

### 3. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

### 4. Получение данных

См. [`../data/README.md`](../data/README.md). После распаковки структура должна быть
`data/raw/{COVID,Normal}`, по **3600 снимков на класс** (всего 7200). Набор данных в
репозитории не распространяется.

### 5. Проверка чекпойнта

```bash
python -c "from src.utils.io import sha256_file; print(sha256_file('models/baseline_model.pt'))"
# должно вывести: 0ba793cb43d0f058af66673a1026e6eef4bd898d98cae05eaf6694cb20b504f0
```

### 6. Воспроизведение базовой метрики

```bash
python scripts/reproduce_preliminary.py
# ожидается: accuracy 0.983333 [ДИ Уилсона 95%: 0.9711; 0.9904],
#            TP=354 FN=7 FP=5 TN=354, RESULT: PASS
```

### 7. Воспроизведение анализа ПР1

```bash
python scripts/reproduce_pr1.py                 # полный прогон, включая близкие дубликаты
python scripts/reproduce_pr1.py --skip-phash    # быстрый детерминированный набор проверок
```

Программа пересчитывает читаемость, цветовые режимы, точные дубликаты (MD5) и (опционально)
пиксельно подтверждённые близкие дубликаты, сравнивая результат с
`results/pr1/quality_profile.csv`. Проверки на эмбеддингах (MMD, C2ST) и анализ качества
разметки воспроизводятся исполненным ноутбуком `notebooks/01_data_quality.ipynb`.

### 8. Воспроизведение метрик устойчивости ПР2

```bash
python scripts/reproduce_pr2.py
# ожидается: M(0) = 0.983333, 20 проверок R(s)/ΔM/R_rel и 4 проверки R-AUC, RESULT: PASS
```

Программа не требует модели: она восстанавливает R(s), ΔM(s), R_rel(s) и R-AUC из
сохранённой поэкземплярной правильности (`results/pr2/correctness.pkl`) и сравнивает
с `results/pr2/summary_table.tsv` и `results/pr2/rauc.csv`. Bootstrap-интервалы
(иерархический/парный bootstrap, B = 2000, percentile + BCa) воспроизводятся ноутбуком
`notebooks/02_corruption_robustness.ipynb`, для которого нужны чекпойнт и данные;
итоговые кривые — в `figures/pr2/robustness_curves.png`.

### 9. Воспроизведение состязательных метрик ПР3

```bash
python scripts/reproduce_pr3.py
# ожидается: 10 строк (атака, ε), оба значения R-AUC_ε,
#            проверки валидности, multi-seed и APGD-CE, RESULT: PASS
```

Программа не требует модели: она пересчитывает FR (= ASR), Robust Accuracy, интервалы
Уилсона и R-AUC_ε из сохранённых поэкземплярных масок правильности
(`results/pr3/pr3_masks.pkl`) и сравнивает с `results/pr3/pr3_adv_attacks.csv`,
`results/pr3/pr3_rauc.csv`, `results/pr3/pr3_validity_l2.csv`,
`results/pr3/pr3_multiseed_pgd.csv` и `results/pr3/pr3_autoattack.json`. Конвейер атак,
процентильные bootstrap-полосы и рисунки воспроизводятся ноутбуком
`notebooks/03_adversarial_robustness.ipynb`, для которого нужны чекпойнт, данные и GPU
(основной прогон PGD занял около 1026 с на CUDA, FGSM — около 49 с).

### 10. Проверка артефактов

Все артефакты в `results/` получены исполненными ноутбуками; `results/pr1/checksums.sha256`
содержит контрольные суммы файлов ПР1, `results/pr2/checksums.sha256` — файлов ПР2
и унаследованных артефактов предварительного этапа, а `results/pr3/checksums.sha256` —
файлов ПР3. Сравните вывод программ с сохранёнными JSON/CSV.
