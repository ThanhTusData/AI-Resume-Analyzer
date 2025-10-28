# src/ai_resume_analyzer/monitoring/drift_detector.py
import json
import os
import numpy as np

MON_DIR = os.environ.get("MONITORING_DIR", "monitoring")
LOG_PATH = os.path.join(MON_DIR, "requests.log")

def _load_numeric_series(field: str):
    vals = []
    if not os.path.exists(LOG_PATH):
        return np.array(vals)
    with open(LOG_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            try:
                obj = json.loads(line)
                if field in obj and isinstance(obj[field], (int, float)):
                    vals.append(float(obj[field]))
            except Exception:
                continue
    return np.array(vals)

def compare_distribution(field: str, baseline: np.ndarray = None, bins: int = 50):
    """
    Simple comparison: compute histogram of baseline vs current and return a symmetric KL-ish divergence.
    baseline: if None, uses first half of data as baseline.
    """
    cur = _load_numeric_series(field)
    if cur.size == 0:
        return {"ok": False, "reason": "no_data"}
    if baseline is None:
        # heuristic: first 25% as baseline
        n = len(cur)
        if n < 10:
            return {"ok": False, "reason": "insufficient_data", "n": n}
        baseline = cur[: max(1, int(0.25 * n))]
        current = cur[int(0.25 * n):]
    else:
        current = cur
    # histograms
    try:
        minv = min(baseline.min(), current.min())
        maxv = max(baseline.max(), current.max())
    except ValueError:
        return {"ok": False, "reason": "value_error"}
    if minv == maxv:
        return {"ok": True, "distance": 0.0}
    hb, _ = np.histogram(baseline, bins=bins, range=(minv, maxv), density=True)
    hc, _ = np.histogram(current, bins=bins, range=(minv, maxv), density=True)
    # smooth
    hb = hb + 1e-8
    hc = hc + 1e-8
    # symmetric KL
    kl1 = np.sum(hb * np.log(hb / hc))
    kl2 = np.sum(hc * np.log(hc / hb))
    sym_kl = 0.5 * (kl1 + kl2)
    return {"ok": True, "distance": float(sym_kl), "baseline_count": int(len(baseline)), "current_count": int(len(current))}
