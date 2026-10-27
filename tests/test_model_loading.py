"""Smoke test: the frozen checkpoint loads into the reconstructed architecture."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

torch = pytest.importorskip("torch")
CKPT = REPO_ROOT / "models" / "baseline_model.pt"


def _is_lfs_pointer(path: Path) -> bool:
    with open(path, "rb") as fh:
        head = fh.read(64)
    return head.startswith(b"version https://git-lfs")


@pytest.mark.skipif(not CKPT.exists(), reason="checkpoint missing (run `git lfs pull`)")
def test_checkpoint_loads() -> None:
    if _is_lfs_pointer(CKPT):
        pytest.skip("checkpoint is a Git LFS pointer; run `git lfs pull`")
    from src.models.architecture import load_frozen_model

    net = load_frozen_model(CKPT)
    assert tuple(net.fc[1].weight.shape) == (2, 512)
    assert sum(p.numel() for p in net.parameters()) == 11_177_538
    assert net.training is False
