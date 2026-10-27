"""Statistical utilities: Wilson / bootstrap / paired bootstrap confidence intervals.

All functions are dependency-light (NumPy + SciPy) and deterministic given `seed`.
"""
from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
from scipy import stats

DEFAULT_BOOTSTRAP: int = 2000
DEFAULT_ALPHA: float = 0.05


def wilson_ci(k: int, n: int, alpha: float = DEFAULT_ALPHA) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion k/n (95% by default).

    Args:
        k: Number of successes.
        n: Number of trials.
        alpha: Significance level (0.05 -> 95% interval).

    Returns:
        (lower, upper) bounds, clipped to [0, 1].
    """
    if n <= 0:
        return (0.0, 0.0)
    z = float(stats.norm.ppf(1.0 - alpha / 2.0))
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = z * np.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
    return (max(0.0, float(center - half)), min(1.0, float(center + half)))


def bootstrap_ci(
    values: Sequence[float],
    statistic: Callable[[np.ndarray], float] = np.mean,
    n_boot: int = DEFAULT_BOOTSTRAP,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 42,
) -> tuple[float, float]:
    """Percentile bootstrap interval for an arbitrary statistic of one sample.

    Args:
        values: One-dimensional sample (e.g. NIQE scores).
        statistic: Function computing the point statistic (default: mean).
        n_boot: Number of bootstrap resamples (course rule: >= 2000).
        alpha: Significance level.
        seed: RNG seed.

    Returns:
        (lower, upper) percentile bounds.
    """
    arr = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        idx = rng.integers(0, arr.size, arr.size)
        draws[i] = statistic(arr[idx])
    lo, hi = np.percentile(draws, [100.0 * alpha / 2.0, 100.0 * (1.0 - alpha / 2.0)])
    return (float(lo), float(hi))


def paired_bootstrap_delta(
    clean: Sequence[float],
    perturbed: Sequence[float],
    n_boot: int = DEFAULT_BOOTSTRAP,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 42,
) -> dict[str, float]:
    """Paired bootstrap for the difference of means on the SAME objects.

    The same resampled indices are applied to both arrays, so the interval
    reflects paired comparison rather than two independent samples.

    Args:
        clean: Per-object values on clean data.
        perturbed: Per-object values on perturbed data (same order).
        n_boot: Number of resamples.
        alpha: Significance level.
        seed: RNG seed.

    Returns:
        Dict with keys: delta (point estimate), ci_low, ci_high, significant
        (True when the interval excludes zero).
    """
    a = np.asarray(clean, dtype=float)
    b = np.asarray(perturbed, dtype=float)
    if a.shape != b.shape:
        raise ValueError("paired arrays must have identical shape")
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        idx = rng.integers(0, a.size, a.size)
        draws[i] = a[idx].mean() - b[idx].mean()
    lo, hi = np.percentile(draws, [100.0 * alpha / 2.0, 100.0 * (1.0 - alpha / 2.0)])
    delta = float(a.mean() - b.mean())
    return {"delta": delta, "ci_low": float(lo), "ci_high": float(hi),
            "significant": bool(lo > 0.0 or hi < 0.0)}


def rauc_trapezoid(values: Sequence[float], grid: Sequence[float]) -> float:
    """Normalized area under a robustness curve (trapezoidal rule).

    Args:
        values: Metric values at the grid points (same length as `grid`).
        grid: Severity/budget grid, ascending, e.g. [0, 1, 2, 3, 4, 5].

    Returns:
        Normalized area 1/(s_max - s_min) * integral(values ds).
    """
    y = np.asarray(values, dtype=float)
    x = np.asarray(grid, dtype=float)
    if y.shape != x.shape or x.size < 2:
        raise ValueError("values and grid must have equal length >= 2")
    return float(np.trapezoid(y, x) / (x[-1] - x[0]))


if __name__ == "__main__":
    print("wilson(354+354, 720):", wilson_ci(708, 720))
    print("bootstrap mean:", bootstrap_ci(np.linspace(1.0, 5.0, 100)))
    print("paired delta:", paired_bootstrap_delta(np.ones(50) * 0.9, np.ones(50) * 0.7))
    print("rauc:", rauc_trapezoid([0.98, 0.96, 0.75, 0.50], [0, 1, 2, 3]))
