"""Smoke tests for the statistical helpers."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils.metrics import paired_bootstrap_delta, rauc_trapezoid, wilson_ci


def test_wilson_bounds_for_half() -> None:
    lo, hi = wilson_ci(360, 720)
    assert 0.45 < lo < 0.5 < hi < 0.55


def test_wilson_extremes() -> None:
    assert wilson_ci(0, 720)[0] == 0.0
    hi = wilson_ci(720, 720)[1]
    assert abs(hi - 1.0) < 1e-9


def test_paired_bootstrap_detects_shift() -> None:
    clean = np.full(100, 1.0)
    perturbed = np.zeros(100)
    res = paired_bootstrap_delta(clean, perturbed, n_boot=500)
    assert res["delta"] == 1.0
    assert res["significant"] is True


def test_rauc_trapezoid_constant_curve() -> None:
    assert abs(rauc_trapezoid([1.0, 1.0, 1.0], [0, 1, 2]) - 1.0) < 1e-12
