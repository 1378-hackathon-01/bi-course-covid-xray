"""Reproduce the core PR1 data-quality metrics (completeness, validity, duplicates).

This is a bounded re-computation of the deterministic parts of the PR1 analysis:
file readability, colour mode, and exact/near duplicate rates with the same
pixel-verification rule as the notebook. Embedding-based checks (MMD/C2ST) and
label-quality analysis require the model and are reproduced by
`notebooks/01_data_quality.ipynb`.

Usage:
    python scripts/reproduce_pr1.py [--data-root data/raw] [--skip-phash]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data.dataset import list_dataset  # noqa: E402

try:  # optional dependency
    import imagehash
except ImportError:  # pragma: no cover
    imagehash = None


def md5_of(path: Path) -> str:
    digest = hashlib.md5()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default=str(REPO_ROOT / "data" / "raw"))
    parser.add_argument("--profile", default=str(REPO_ROOT / "results" / "pr1" / "quality_profile.csv"))
    parser.add_argument("--skip-phash", action="store_true")
    args = parser.parse_args()

    paths, labels = list_dataset(args.data_root)
    n = len(paths)
    print(f"files: {n}")

    read_ok = 0
    modes = defaultdict(int)
    for p in paths:
        try:
            with Image.open(p) as img:
                img.verify()
            with Image.open(p) as img:
                modes[img.mode] += 1
            read_ok += 1
        except Exception:
            pass
    print(f"readable: {read_ok}/{n} ({100.0 * read_ok / n:.4f}%)")
    print("modes:", dict(modes))

    md5_groups = defaultdict(list)
    for p in paths:
        md5_groups[md5_of(p)].append(p)
    exact_extra = sum(len(v) - 1 for v in md5_groups.values() if len(v) > 1)
    print(f"exact duplicates (MD5): {exact_extra} files, "
          f"{sum(1 for v in md5_groups.values() if len(v) > 1)} groups")

    near_extra = None
    if not args.skip_phash and imagehash is not None:
        phash = {}
        for p in paths:
            with Image.open(p) as img:
                phash[p] = imagehash.phash(img.convert("RGB"))
        buckets = defaultdict(list)
        for p, h in phash.items():
            buckets[int(str(h), 16) >> 56].append((p, h))
        candidates = []
        for members in buckets.values():
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    if members[i][1] - members[j][1] <= 6:
                        candidates.append((members[i][0], members[j][0]))
        verified = []
        for a, b in candidates:
            with Image.open(a) as ia, Image.open(b) as ib:
                ga = np.asarray(ia.convert("L"), dtype=int)
                gb = np.asarray(ib.convert("L"), dtype=int)
            if ga.shape != gb.shape:
                continue
            if np.abs(ga - gb).mean() <= 10.0:
                verified.append((a, b))
        parent = {p: p for p in phash}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in verified:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
        clusters = defaultdict(list)
        for p in phash:
            clusters[find(p)].append(p)
        near_extra = sum(len(v) - 1 for v in clusters.values() if len(v) > 1)
        print(f"candidates (phash<=6): {len(candidates)}; pixel-verified pairs: {len(verified)}")
        print(f"near duplicates (pixel-verified): {near_extra} files, "
              f"{sum(1 for v in clusters.values() if len(v) > 1)} clusters")

    expected = {}
    with open(args.profile, "r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            expected[row["Метрика"]] = float(row["Значение"])
    exp_exact = round(0.006389 * 7200)
    checks = {
        "readable == 7200": read_ok == 7200,
        "exact == 46": exact_extra == exp_exact,
    }
    if near_extra is not None:
        checks["near == 262"] = near_extra == 262
    for name, ok in checks.items():
        print(("PASS " if ok else "FAIL ") + name)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
