"""Smoke test: dataset listing preserves the ImageFolder order and counts."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
DATA = REPO_ROOT / "data" / "raw"


@pytest.mark.skipif(not (DATA / "COVID").is_dir(), reason="dataset not downloaded (see data/README.md)")
def test_dataset_listing() -> None:
    from src.data.dataset import CLASS_NAMES, list_dataset

    paths, labels = list_dataset(DATA)
    assert CLASS_NAMES == ("COVID", "Normal")
    assert len(paths) == len(labels) == 7200
    assert int((labels == 0).sum()) == 3600
    assert int((labels == 1).sum()) == 3600


@pytest.mark.skipif(not (DATA / "COVID").is_dir(), reason="dataset not downloaded (see data/README.md)")
def test_transforms_shape() -> None:
    torch = pytest.importorskip("torch")
    from PIL import Image
    from src.data.dataset import list_dataset
    from src.data.transforms import eval_transforms

    paths, _ = list_dataset(DATA)
    with Image.open(paths[0]) as img:
        tensor = eval_transforms()(img.convert("RGB"))
    assert tuple(tensor.shape) == (3, 224, 224)
    assert isinstance(tensor, torch.Tensor)
