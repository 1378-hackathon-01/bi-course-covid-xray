"""Reproduce the core PR3 adversarial-robustness metrics from stored artifacts.

Bounded, deterministic re-computation: FR (= ASR), robust accuracy, their
Wilson intervals and R-AUC_eps are rebuilt from the per-object correctness
masks in `results/pr3/pr3_masks.pkl` and compared with the stored PR3 tables.
No model, images or GPU are required, so the check runs in CI.

What is verified:
  * 10 (attack, epsilon) rows: n_fooled, FR, robust accuracy, n_wrong_all;
  * both Wilson 95 % intervals for every row;
  * R-AUC_eps for FGSM and PGD-10 on the epsilon grid 0, 1, 2, 4, 8, 16 (/255);
  * validity statistics: 200/200 valid examples for all 10 cells;
  * the multi-seed PGD series (seeds 42/43/44) and the APGD-CE sanity check;
  * cross-consistency of `metrics_pr3.json` with the CSV tables.

The percentile bootstrap interval for R-AUC_eps is produced by
`notebooks/03_adversarial_robustness.ipynb` and is not recomputed here; only
the point estimate is checked.

Usage:
    python scripts/reproduce_pr3.py
"""
from __future__ import annotations

import csv
import json
import pickle
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.utils.metrics import rauc_trapezoid, wilson_ci  # noqa: E402

RESULTS = REPO_ROOT / "results" / "pr3"
EPS = (1.0, 2.0, 4.0, 8.0, 16.0)
GRID = (0.0, 1.0, 2.0, 4.0, 8.0, 16.0)
METHODS = ("FGSM", "PGD10")
TOL = 1e-12


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(float(a) - float(b)) <= tol


def read_csv(name: str) -> list[dict[str, str]]:
    with open(RESULTS / name, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def read_json(name: str) -> dict:
    with open(RESULTS / name, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    with open(RESULTS / "pr3_masks.pkl", "rb") as fh:
        blob = pickle.load(fh)

    clean = np.asarray(blob["clean_ok"], dtype=bool)
    masks_ok = blob["masks_ok"]
    n_sub = int(clean.size)
    n_clean = int(clean.sum())
    m_sub = float(clean.mean())

    ok = True
    print(f"subset n = {n_sub}, clean-correct = {n_clean}, M_sub = {m_sub:.6f}")
    ok &= n_sub == 200 and n_clean == 197
    ok &= close(m_sub, float(blob["M_sub"]))

    adv_rows = {(r["method"], float(r["eps"])): r for r in read_csv("pr3_adv_attacks.csv")}
    ok &= len(adv_rows) == 10
    print(f"{'attack':7s}{'eps':>4s}{'n_fooled':>10s}{'FR':>9s}{'RA':>9s}  check")

    curves: dict[str, list[float]] = {}
    for method in METHODS:
        curve = [m_sub]
        for eps in EPS:
            mask = np.asarray(masks_ok[(method, eps)], dtype=bool)
            n_fooled = int((clean & ~mask).sum())
            n_wrong = int((~mask).sum())
            fr = n_fooled / n_clean
            ra = float(mask.mean())
            fr_ci = wilson_ci(n_fooled, n_clean)
            ra_ci = wilson_ci(int(mask.sum()), n_sub)
            curve.append(ra)

            row = adv_rows[(method, eps)]
            row_ok = all((
                int(row["n_correct_clean"]) == n_clean,
                int(row["n_fooled"]) == n_fooled,
                int(row["n_wrong_all"]) == n_wrong,
                close(row["FR"], fr),
                close(row["robust_acc"], ra),
                close(row["FR_low"], fr_ci[0]),
                close(row["FR_high"], fr_ci[1]),
                close(row["RA_low"], ra_ci[0]),
                close(row["RA_high"], ra_ci[1]),
            ))
            ok &= row_ok
            print(f"{method:7s}{eps:4.0f}{n_fooled:10d}{fr:9.4f}{ra:9.4f}  "
                  f"{'OK' if row_ok else 'MISMATCH'}")
        curves[method] = curve

        area = rauc_trapezoid(curve, GRID)
        print(f"  {method} R-AUC_eps = {area:.8f}")

    stored_rauc = {r["method"]: float(r["R-AUC_eps"]) for r in read_csv("pr3_rauc.csv")}
    for method in METHODS:
        area = rauc_trapezoid(curves[method], GRID)
        good = close(area, stored_rauc[method])
        ok &= good
        print(f"  R-AUC check {method:7s} stored {stored_rauc[method]:.8f}  "
              f"{'OK' if good else 'MISMATCH'}")

    # Validity: all generated examples are finite and inside [0, 1].
    validity = read_csv("pr3_validity_l2.csv")
    ok &= len(validity) == 10
    n_valid_total = n_generated_total = 0
    for r in validity:
        n_gen, n_val = int(r["n_generated"]), int(r["n_valid"])
        rate = n_val / n_gen
        vr_ci = wilson_ci(n_val, n_gen)
        n_valid_total += n_val
        n_generated_total += n_gen
        good = all((
            n_gen == 200,
            n_val == 200,
            close(r["validity_rate"], rate),
            close(r["VR_ci_low"], vr_ci[0]),
            close(r["VR_ci_high"], vr_ci[1]),
            float(r["linf_max"]) <= float(r["eps_bound"]) + 1e-6,  # float32 storage
        ))
        ok &= good
        if not good:
            print(f"  validity MISMATCH {r['method']} eps={r['eps']}")
    print(f"validity: {n_valid_total}/{n_generated_total} valid, "
          f"{'OK' if n_valid_total == n_generated_total == 2000 else 'MISMATCH'}")
    ok &= n_valid_total == n_generated_total == 2000

    # Multi-seed PGD series.
    multiseed = read_csv("pr3_multiseed_pgd.csv")
    ok &= len(multiseed) == 3
    for r in multiseed:
        n_fooled = int(r["n_fooled"])
        good = all((
            float(r["eps"]) == 8.0,
            int(r["n_correct_clean"]) == n_clean,
            close(r["FR"], n_fooled / n_clean),
            close(r["robust_acc"], 0.0),
            close(r["FR_low"], wilson_ci(n_fooled, n_clean)[0]),
            close(r["FR_high"], wilson_ci(n_fooled, n_clean)[1]),
        ))
        ok &= good
        print(f"multi-seed {int(r['seed'])}: FR = {float(r['FR']):.4f}  "
              f"{'OK' if good else 'MISMATCH'}")

    # APGD-CE sanity check.
    aa = read_json("pr3_autoattack.json")
    aa_ok = all((
        int(aa["n_subset"]) == 20,
        int(aa["n_clean_correct"]) == 20,
        int(aa["n_fooled"]) == 20,
        close(aa["FR"], 1.0),
        close(aa["robust_acc"], 0.0),
        close(aa["FR_ci"][0], wilson_ci(20, 20)[0]),
        close(aa["FR_ci"][1], wilson_ci(20, 20)[1]),
        close(aa["robust_acc_ci"][0], wilson_ci(0, 20)[0]),
        close(aa["robust_acc_ci"][1], wilson_ci(0, 20)[1]),
    ))
    ok &= aa_ok
    print(f"APGD-CE sanity: FR = {aa['FR']:.4f}, RA = {aa['robust_acc']:.4f}  "
          f"{'OK' if aa_ok else 'MISMATCH'}")

    # Cross-check the machine-readable bundle against the CSV tables.
    metrics = read_json("metrics_pr3.json")
    bundle = {(r["method"], float(r["epsilon_255"])): r for r in metrics["results"]}
    bundle_ok = len(bundle) == 10
    for (method, eps), row in adv_rows.items():
        src = bundle[(method, eps)]
        bundle_ok &= all((
            int(src["n_fooled"]) == int(row["n_fooled"]),
            close(src["ASR"], row["FR"]),
            close(src["robust_accuracy"], row["robust_acc"]),
            close(src["ASR_ci95_wilson"][0], row["FR_low"]),
            close(src["ASR_ci95_wilson"][1], row["FR_high"]),
            close(src["robust_accuracy_ci95_wilson"][0], row["RA_low"]),
            close(src["robust_accuracy_ci95_wilson"][1], row["RA_high"]),
        ))
    bundle_ok &= len(metrics["rauc"]) == 2 and len(metrics["validity"]) == 10
    ok &= bundle_ok
    print(f"metrics_pr3.json bundle: {'OK' if bundle_ok else 'MISMATCH'}")

    print()
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
