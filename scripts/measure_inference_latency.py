"""Measure inference latency of the frozen checkpoint (G-1 supplementary evidence).

Runs on CPU, batch = 1, 100 test images (indices from the stored splits) after
5 warm-up passes. The result is written to results/pr1/inference_latency.json.

Usage:
    python scripts/measure_inference_latency.py [--n-images 100]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data.dataset import list_dataset  # noqa: E402
from src.data.transforms import eval_transforms  # noqa: E402
from src.models.architecture import load_frozen_model  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default=str(REPO_ROOT / "data" / "raw"))
    parser.add_argument("--checkpoint", default=str(REPO_ROOT / "models" / "baseline_model.pt"))
    parser.add_argument("--splits", default=str(REPO_ROOT / "results" / "preliminary" / "split_indices.json"))
    parser.add_argument("--out", default=str(REPO_ROOT / "results" / "pr1" / "inference_latency.json"))
    parser.add_argument("--n-images", type=int, default=100)
    parser.add_argument("--n-warmup", type=int, default=5)
    args = parser.parse_args()

    paths, _ = list_dataset(args.data_root)
    with open(args.splits, "r", encoding="utf-8") as fh:
        test_idx = json.load(fh)["test_indices"]
    selected = test_idx[: args.n_images]
    model = load_frozen_model(args.checkpoint)
    tf = eval_transforms()

    def once(path: Path) -> float:
        with Image.open(path) as img:
            tensor = tf(img.convert("RGB")).unsqueeze(0)
        start = time.perf_counter()
        with torch.no_grad():
            model(tensor)
        return (time.perf_counter() - start) * 1000.0

    for i in selected[: args.n_warmup]:
        once(paths[i])

    times = np.asarray([once(paths[i]) for i in selected], dtype=float)
    payload = {
        "hardware": "CPU",
        "device": "cpu",
        "torch_version": torch.__version__,
        "n_images": int(times.size),
        "n_warmup": args.n_warmup,
        "mean_ms_per_image": float(times.mean()),
        "std_ms_per_image": float(times.std(ddof=1)),
        "median_ms_per_image": float(np.median(times)),
        "p95_ms_per_image": float(np.percentile(times, 95)),
        "min_ms_per_image": float(times.min()),
        "max_ms_per_image": float(times.max()),
        "batch_size": 1,
        "image_size": [224, 224],
        "threads": int(torch.get_num_threads()),
        "checkpoint": "models/baseline_model.pt (frozen, never retrained)",
        "purpose": "G-1 supplementary evidence: training duration is not recoverable; "
                   "inference cost of the frozen checkpoint is measured instead.",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(f"mean {payload['mean_ms_per_image']:.2f} +/- {payload['std_ms_per_image']:.2f} ms/image")
    print("saved:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
