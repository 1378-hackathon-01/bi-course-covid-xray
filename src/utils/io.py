"""Small I/O helpers used by the reproduction programs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import torch


def load_json(path: str | Path) -> Any:
    """Load a UTF-8 JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(obj: Any, path: str | Path, indent: int = 1) -> None:
    """Save an object to a UTF-8 JSON file (created parents included)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=indent)


def load_checkpoint(path: str | Path, map_location: str = "cpu") -> dict:
    """Load a PyTorch state_dict (weights only)."""
    return torch.load(str(path), map_location=map_location, weights_only=True)


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    """Return the SHA-256 hex digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


if __name__ == "__main__":
    here = Path(__file__).resolve().parents[2]
    print("repo root:", here)
    ckpt = here / "models" / "baseline_model.pt"
    if ckpt.exists():
        print("checkpoint sha256:", sha256_file(ckpt))
    else:
        print("checkpoint not found (run `git lfs pull` first)")
