# Dataset

**Do NOT commit the dataset to this repository.** Only the download instructions and the
expected layout live here.

## Source

- **Name:** COVID-19 Radiography Database
- **URL:** https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database
- **Version:** v4 (directory layout dated 2021-02-08)
- **License:** «Data files © Original Authors» (as stated on the dataset page). The files
  belong to their original authors; no explicit open license for redistribution is
  declared. The imagery originates from SIRM (COVID class) and the RSNA Pneumonia
  Detection Challenge (Normal class). See the dataset page for the authoritative terms.
- **Citation:** Rahman T., Chowdhury M. E. H., Khandakar A. et al. «Exploring the Effect of
  Image Enhancement Techniques on COVID-19 Detection using Chest X-ray Images»,
  Computers in Biology and Medicine, 2021; plus the Kaggle dataset page.

## Contents of v4

| Class | Images |
|---|---|
| COVID | 3616 |
| Normal | 10192 |
| Lung_Opacity | 6012 |
| Viral Pneumonia | 1345 |

This project uses the **binary subset**: the first 3600 sorted files of the `COVID` and
`Normal` classes (7200 images total, 299×299 grayscale PNG). The cap removes the original
class imbalance.

## Download

Two equivalent options:

1. **Kaggle** (preferred when credentials are configured):
   ```bash
   kaggle datasets download -d tawsifurrahman/covid19-radiography-database --unzip -p data/raw_src
   ```
2. **Public mirror** used for byte-level reproducibility (identical per-class file counts):
   https://github.com/junelsolis/covid-19-radiography-dataset

After extraction, arrange the files as:

```
data/raw/
├── COVID/
│   ├── COVID-1.png
│   └── ...
└── Normal/
    ├── NORMAL-1.png
    └── ...
```

Exactly **3600 files per class** are required, sorted lexicographically — the stored split
indices refer to this ordering (class directories alphabetically, files sorted inside).

## Splits

The exact train/validation/test indices (5760/720/720, seed = 42) are stored in
`results/preliminary/split_indices.json`. To apply them:

```python
import json
from pathlib import Path
from src.data.dataset import list_dataset

splits = json.load(open("results/preliminary/split_indices.json", encoding="utf-8"))
paths, labels = list_dataset(Path("data/raw"))
train = [paths[i] for i in splits["train_indices"]]
test = [paths[i] for i in splits["test_indices"]]
```

## Verification

The dataset page does not publish a single archive checksum for the extracted tree, so the
version is verified by **per-class file counts** (3616 / 10192 / 6012 / 1345 in v4; 3600 +
3600 in the binary subset) and by the uniform 299×299 resolution. Any deviation means a
different dataset version or a different extraction order — in that case the stored split
indices are not applicable.
