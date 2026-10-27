"""Reproduce the frozen baseline metric M(0) on the test split.

Usage:
    python scripts/reproduce_preliminary.py [--data-root data/raw]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data.dataset import XRaySubset, list_dataset  # noqa: E402
from src.data.transforms import eval_transforms  # noqa: E402
from src.models.architecture import load_frozen_model  # noqa: E402
from src.utils.metrics import wilson_ci  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default=str(REPO_ROOT / "data" / "raw"))
    parser.add_argument("--checkpoint", default=str(REPO_ROOT / "models" / "baseline_model.pt"))
    parser.add_argument("--splits", default=str(REPO_ROOT / "results" / "preliminary" / "split_indices.json"))
    parser.add_argument("--metrics", default=str(REPO_ROOT / "results" / "preliminary" / "metrics.json"))
    args = parser.parse_args()

    paths, labels = list_dataset(args.data_root)
    if len(paths) != 7200:
        print(f"warning: expected 7200 images, found {len(paths)}")

    with open(args.splits, "r", encoding="utf-8") as fh:
        splits = json.load(fh)
    test_idx = splits["test_indices"]

    dataset = XRaySubset(paths, labels, test_idx, transform=eval_transforms())
    loader = torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=False, num_workers=0)
    model = load_frozen_model(args.checkpoint)

    preds: list[int] = []
    targets: list[int] = []
    with torch.no_grad():
        for xb, yb in loader:
            preds.extend(model(xb).argmax(1).tolist())
            targets.extend(yb.tolist())

    pred = np.asarray(preds)
    true = np.asarray(targets)
    tp = int(((true == 0) & (pred == 0)).sum())
    fn = int(((true == 0) & (pred == 1)).sum())
    fp = int(((true == 1) & (pred == 0)).sum())
    tn = int(((true == 1) & (pred == 1)).sum())
    accuracy = (tp + tn) / len(true)
    lo, hi = wilson_ci(tp + tn, len(true))

    print(f"test set: {len(true)} (COVID {int((true == 0).sum())} / Normal {int((true == 1).sum())})")
    print(f"confusion: TP={tp} FN={fn} FP={fp} TN={tn}")
    print(f"accuracy: {accuracy:.6f} [Wilson 95% CI: {lo:.4f}; {hi:.4f}]")

    with open(args.metrics, "r", encoding="utf-8") as fh:
        expected = json.load(fh)
    ok_acc = abs(accuracy - float(expected["value_exact"])) < 1e-9
    ok_ci = abs(lo - expected["ci_95"]["lower"]) < 1e-6 and abs(hi - expected["ci_95"]["upper"]) < 1e-6
    ok_cm = expected["confusion_matrix"] == {"TP": tp, "FN": fn, "FP": fp, "TN": tn}
    print("expected:", expected["value_exact"], expected["ci_95"])
    print("RESULT:", "PASS" if (ok_acc and ok_ci and ok_cm) else "FAIL")
    return 0 if (ok_acc and ok_ci and ok_cm) else 1


if __name__ == "__main__":
    raise SystemExit(main())
