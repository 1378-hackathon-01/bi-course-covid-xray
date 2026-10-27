# Documentation index

| Document | Content |
|---|---|
| [`course_syllabus.md`](course_syllabus.md) | Short description of the practical cycle and the scope of this repository. |
| [`reproduction_guide.md`](reproduction_guide.md) | Step-by-step reproduction instructions (English + Russian summary). |
| [`../README.md`](../README.md) | Repository overview (English), structure, key results, roadmap. |
| [`../README.ru.md`](../README.ru.md) | То же на русском языке. |
| [`../CHANGELOG.md`](../CHANGELOG.md) | Version history. |

## How the documentation is organised

The repository documents two completed stages of the practical cycle: the preliminary
stage (methodology §1) and Practical Work №1 (methodology §2). Every claim in the
documentation is backed by a machine-readable artifact: configuration (`configs/`), metrics
(`results/`), reports (`reports/`) or figures (`figures/`). This layout means a reader can
verify a number without re-running any code, and a reviewer can reproduce it end-to-end
using the programs in `scripts/`.

## Where to start

1. Read the top-level `README.md` for context and key results.
2. Open `reports/БИИ_preliminary.pdf` for the full Russian-language report (a single
   cumulative document that starts with the preliminary stage and is extended as each
   practical work is completed).
3. Follow `reproduction_guide.md` to rebuild the numbers locally.
4. Inspect `results/` for the exact values with confidence intervals.

## Conventions

- Reports and configuration comments are written in Russian (the course language);
  code, docstrings and this documentation are in English.
- All confidence intervals are 95%: Wilson for proportions, percentile bootstrap
  (B = 2000) for means and non-linear metrics, permutation p-values for MMD.
- The baseline checkpoint is frozen: no script in this repository ever trains it.
