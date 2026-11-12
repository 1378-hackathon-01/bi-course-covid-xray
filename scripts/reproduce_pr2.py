"""Reproduce the core PR2 robustness metrics from the stored artifact.

Bounded, deterministic re-computation: R(s), ΔM(s), R_rel(s) and R-AUC are
rebuilt from `results/pr2/correctness.pkl` (per-object correctness of the frozen
model) and compared with `results/pr2/summary_table.tsv` and
`results/pr2/rauc.csv`. No model, images or GPU are required.

The confidence intervals (hierarchical/paired bootstrap, B = 2000, percentile +
BCa) are produced by `notebooks/02_corruption_robustness.ipynb` and are not
recomputed here; only the point estimates are checked.

Usage:
    python scripts/reproduce_pr2.py
"""
from __future__ import annotations

import csv
import pickle
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS = REPO_ROOT / "results" / "pr2"

# Trapezoidal weights on the uniform severity grid s = 0..5 (same as the notebook).
WEIGHTS = np.array([0.1, 0.2, 0.2, 0.2, 0.2, 0.1], dtype=np.float64)
CORRUPTIONS = ["gaussian_noise", "poisson_noise", "gaussian_blur", "jpeg"]
SEVERITIES = [1, 2, 3, 4, 5]
TOL = 1e-9


def load_correctness() -> dict:
    with open(RESULTS / "correctness.pkl", "rb") as fh:
        return pickle.load(fh)


def compute(blob: dict) -> tuple[float, dict, dict]:
    clean = blob["clean"].astype(np.float64)
    correct = blob["correct"]
    m0 = float(clean.mean())

    rows: dict[str, dict[int, float]] = {}
    areas: dict[str, float] = {}
    for c in CORRUPTIONS:
        r = {0: m0}
        for s in SEVERITIES:
            r[s] = float(correct[(c, s)].mean())
        rows[c] = r
        # Per-object area (the whole curve is recomputed per object), then averaged.
        v = WEIGHTS[0] * clean
        for s in SEVERITIES:
            v = v + WEIGHTS[s] * correct[(c, s)].mean(axis=0).astype(np.float64)
        areas[c] = float(v.mean())
    return m0, rows, areas


def read_summary_table() -> dict[tuple[str, int], tuple[float, float, float]]:
    out: dict[tuple[str, int], tuple[float, float, float]] = {}
    with open(RESULTS / "summary_table.tsv", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh, delimiter="\t")
        next(reader)  # header
        for row in reader:
            out[(row[0], int(row[1]))] = (float(row[2]), float(row[5]), float(row[8]))
    return out


def read_rauc() -> dict[str, float]:
    out: dict[str, float] = {}
    with open(RESULTS / "rauc.csv", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        next(reader)  # header
        for row in reader:
            out[row[0]] = float(row[1])
    return out


def main() -> int:
    blob = load_correctness()
    m0, rows, areas = compute(blob)
    stored_rows = read_summary_table()
    stored_auc = read_rauc()

    ok = True
    print(f"M(0) = {m0:.6f}  (stored baseline accuracy)")
    print(f"{'corruption':16s}{'s':>2s}{'R(s)':>9s}{'dM(s)':>9s}{'R_rel':>9s}  check")
    for c in CORRUPTIONS:
        for s in SEVERITIES:
            r = rows[c][s]
            dm = m0 - r
            rel = r / m0
            sr, sdm, srel = stored_rows[(c, s)]
            good = abs(r - sr) <= TOL and abs(dm - sdm) <= TOL and abs(rel - srel) <= TOL
            ok &= good
            print(f"{c:16s}{s:2d}{r:9.4f}{dm:9.4f}{rel:9.4f}  {'OK' if good else 'MISMATCH'}")
        a = areas[c]
        sa = stored_auc[c]
        good = abs(a - sa) <= TOL
        ok &= good
        print(f"{c:16s}{'-':>2s}{a:9.4f}  R-AUC (stored {sa:.4f})  "
              f"{'OK' if good else 'MISMATCH'}")

    print()
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
