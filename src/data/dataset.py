"""Dataset listing/loading in the exact ImageFolder order used by the baseline.

The ordering (class directories sorted alphabetically, files sorted
lexicographically inside each class) is what `results/preliminary/split_indices.json`
refers to, so it must be preserved when reproducing the splits.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Sequence

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

CLASS_NAMES: tuple[str, str] = ("COVID", "Normal")  # ImageFolder alphabetical order
IMAGE_SUFFIXES: tuple[str, ...] = (".png", ".jpg", ".jpeg")


def list_dataset(root: str | Path) -> tuple[list[Path], np.ndarray]:
    """Return (paths, labels) in ImageFolder order for a `root/<CLASS>/*.png` tree.

    Args:
        root: Directory containing `COVID/` and `Normal/` subdirectories.

    Returns:
        Tuple of file paths and integer labels (COVID=0, Normal=1).
    """
    root = Path(root)
    paths: list[Path] = []
    labels: list[int] = []
    for label, name in enumerate(CLASS_NAMES):
        class_dir = root / name
        if not class_dir.is_dir():
            raise FileNotFoundError(f"class directory not found: {class_dir}")
        files = sorted(p for p in class_dir.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)
        paths.extend(files)
        labels.extend([label] * len(files))
    return paths, np.asarray(labels, dtype=np.int64)


class XRaySubset(Dataset):
    """Subset of a chest X-ray dataset defined by explicit indices."""

    def __init__(self, paths: Sequence[Path], labels: np.ndarray,
                 indices: Sequence[int], transform: Callable | None = None) -> None:
        self.paths = [paths[i] for i in indices]
        self.labels = labels[np.asarray(indices, dtype=np.int64)]
        self.transform = transform

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        with Image.open(self.paths[idx]) as img:
            rgb = img.convert("RGB")
            tensor = self.transform(rgb) if self.transform is not None else torch.from_numpy(
                np.asarray(rgb)).permute(2, 0, 1).float() / 255.0
        return tensor, int(self.labels[idx])


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2] / "data" / "raw"
    try:
        paths, labels = list_dataset(root)
        print("files:", len(paths), "| COVID:", int((labels == 0).sum()),
              "| Normal:", int((labels == 1).sum()))
    except FileNotFoundError as exc:
        print("dataset not found:", exc, "- see data/README.md")
