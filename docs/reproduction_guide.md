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

### 8. Verify stored artifacts

Every artifact in `results/` was produced by the executed notebooks; `results/pr1/checksums.sha256`
lists the PR1 files. Compare the outputs of the programs above with the stored JSON/CSV.

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

### 8. Проверка артефактов

Все артефакты в `results/` получены исполненными ноутбуками; `results/pr1/checksums.sha256`
содержит контрольные суммы файлов ПР1. Сравните вывод программ с сохранёнными JSON/CSV.
