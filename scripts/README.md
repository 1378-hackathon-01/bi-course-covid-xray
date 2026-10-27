# Programs (`scripts/`)

| Program | Purpose | Inputs | Outputs |
|---|---|---|---|
| `reproduce_preliminary.py` | Loads the frozen checkpoint, evaluates the test split and verifies M(0), its Wilson interval and the confusion matrix against the stored metrics. | `data/raw/`, `models/baseline_model.pt`, `results/preliminary/` | console PASS/FAIL |
| `reproduce_pr1.py` | Re-computes the deterministic PR1 checks: readability, colour modes, MD5 duplicates and pixel-verified near duplicates (phash <= 6 with pixel verification). | `data/raw/`, `results/pr1/quality_profile.csv` | console PASS/FAIL |
| `measure_inference_latency.py` | Measures CPU inference latency of the frozen checkpoint (G-1 supplementary evidence). | dataset, checkpoint, splits | `results/pr1/inference_latency.json` |

## Notes

- The programs are plain Python (no CLI framework) and resolve all paths relative to the
  repository root.
- `reproduce_pr1.py` intentionally covers only the deterministic, model-free part of the
  analysis. Embedding-based tests (MMD, C2ST) and label-quality analysis require the
  frozen model and are reproduced by the executed notebook `notebooks/01_data_quality.ipynb`.
- `measure_inference_latency.py` overwrites `results/pr1/inference_latency.json` with a
  fresh measurement; the committed file records the original run.

## Examples

```bash
python scripts/reproduce_preliminary.py
python scripts/reproduce_pr1.py --skip-phash     # faster, skips near-duplicate scan
python scripts/measure_inference_latency.py --n-images 100
```
