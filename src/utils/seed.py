"""Reproducibility helpers: fix all random sources with a single seed."""
from __future__ import annotations

import os
import random

import numpy as np
import torch

DEFAULT_SEED: int = 42


def set_seed(seed: int = DEFAULT_SEED, deterministic: bool = True) -> int:
    """Seed Python, NumPy, PyTorch and CUDA RNGs.

    Args:
        seed: Seed value (the project uses 42 everywhere).
        deterministic: Enable deterministic cuDNN kernels.

    Returns:
        The seed that was applied.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    return seed


if __name__ == "__main__":
    applied = set_seed()
    print("seed applied:", applied)
    print("cuda available:", torch.cuda.is_available())
