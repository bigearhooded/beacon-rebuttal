"""Relate closed-book API knowledge to benchmark behaviour.

The probe in ``contamination_probe.py`` measures what a model already knows
about a library without tools. This joins that to the benchmark: does prior
knowledge of the target library predict how well a model does *without* the
registry, and how much the registry buys it?

Why discrimination, not recall
------------------------------
Recall alone is uninterpretable here. On ``omicverse``:

    deepseek-v4-flash   recall   0 %   hallucination   0 %   -> answers NO to everything
    qwen3.6-35b-a3b     recall 100 %   hallucination 100 %   -> answers YES to everything

Both models know nothing about the library; read on recall alone the second
looks like it has memorised it. **Discrimination** = recall - hallucination is
zero for both, which is the truth, and it is bounded at 100 only when a model
both recognises real functions and rejects fabricated ones.

That statistic is also exactly the failure the paper is about: a model with
high recall and high hallucination is one that emits confident calls to
functions that do not exist.

Two predictions are tested, and they are not the same claim:

1. discrimination on the target library correlates with **baseline** Pass@1 —
   prior knowledge is what the unaided agent runs on;
2. discrimination correlates **negatively** with the registry's uplift — the
   registry supplies what the weights lack, so it should help least where the
   model already knows the library.

The second is the one that matters. The first could be explained by general
model capability; the second cannot.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Probe model id -> panel model id in multi_model_summary.json
MODEL_MAP = {
    "deepseek-v4-flash":    "deepseek-v4-flash",
    "qwen/qwen3.6-35b-a3b": "qwen3.6:35b-a3b-256k",
    "qwen/qwen3.5-9b":      "qwen3.5-9b",
}


def _spearman(x: list[float], y: list[float]) -> tuple[float, int]:
    n = len(x)
    if n < 3:
        return float("nan"), n

    def rank(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:                       # average ties
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r

    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return (num / den if den else float("nan")), n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=Path,
                    default=REPO_ROOT / "data" / "results" / "contamination.json")
    ap.add_argument("--panel", type=Path,
                    default=REPO_ROOT / "docs" / "a3f_paper" / "figures" /
                            "multi_model_summary.json")
    ap.add_argument("--target", default="omicverse")
    a = ap.parse_args()

    probe = json.loads(a.probe.read_text())["summary"]
    panel = json.loads(a.panel.read_text())

    def cell(model, lib):
        c = probe.get(model, {}).get(lib)
        if not c:
            return None
        rec = c["tp"] / max(1, c["tp"] + c["fn"]) * 100
        hal = c["fp"] / max(1, c["fp"] + c["tn"]) * 100
        return rec, hal, rec - hal

    libs = ["numpy", "pandas", "sklearn", "scipy", "scanpy", "omicverse"]
    print("Closed-book discrimination = recall - hallucination  (100 = perfect, 0 = no signal)\n")
    head = f"{'model':24s}" + "".join(f"{l:>11s}" for l in libs)
    print(head); print("-" * len(head))
    for m in probe:
        row = ""
        for l in libs:
            c = cell(m, l)
            row += f"{c[2]:10.0f} " if c else "         — "
        print(f"{m:24s}{row}")
    print("\n(recall / hallucination separately)")
    for m in probe:
        parts = []
        for l in libs:
            c = cell(m, l)
            parts.append(f"{l}:{c[0]:.0f}/{c[1]:.0f}" if c else f"{l}:—")
        print(f"  {m:24s} " + "  ".join(parts))

    rows = []
    for pm, panel_id in MODEL_MAP.items():
        c = cell(pm, a.target)
        p = panel.get(panel_id)
        if not c or not p:
            continue
        rows.append({"model": pm, "discrimination": c[2],
                     "recall": c[0], "hallucination": c[1],
                     "baseline": p["baseline_pass"],
                     "beacon": p["ov_pass"],
                     "uplift": p["ov_pass"] - p["baseline_pass"]})

    print(f"\n\nOn the target library ({a.target}), joined to the benchmark panel:\n")
    print(f"{'model':24s} {'discrim':>8s} {'recall':>7s} {'halluc':>7s} "
          f"{'baseline':>9s} {'+Beacon':>8s} {'uplift':>7s}")
    print("-" * 76)
    for r in rows:
        print(f"{r['model']:24s} {r['discrimination']:8.0f} {r['recall']:7.0f} "
              f"{r['hallucination']:7.0f} {r['baseline']:8.1f}% {r['beacon']:7.1f}% "
              f"{r['uplift']:+7.1f}")

    if len(rows) >= 3:
        d = [r["discrimination"] for r in rows]
        rho_b, n = _spearman(d, [r["baseline"] for r in rows])
        rho_u, _ = _spearman(d, [r["uplift"] for r in rows])
        print(f"\nSpearman (n = {n}):")
        print(f"  discrimination vs baseline Pass@1 : rho = {rho_b:+.2f}")
        print(f"  discrimination vs Beacon uplift   : rho = {rho_u:+.2f}")
        print(f"\n  n = {n} models is far too few for these to be evidence on their own; "
              f"they are reported\n  as the shape of the relationship, and the "
              f"per-library table above is the finding.")
    else:
        print(f"\nOnly {len(rows)} model(s) joined — need the probe to finish "
              f"before correlations mean anything.")

    out = REPO_ROOT / "data" / "results" / "contamination_correlation.csv"
    if rows:
        with out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
