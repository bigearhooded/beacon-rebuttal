"""Combined headline figure for the Beacon paper.

Three panels:
  (a) Multi-model Pass@1 bars.            [top-left]
  (b) Per-model turn distribution scatter.[top-right]
  (c) Per-layer Pass@1 Δ heatmap.         [bottom, spanning]

Output: figures/fig_headline.pdf (and .png).
Sources: figures/multi_model_summary.json (a, c),
         data/results/<canonical-sweeps>/grades.csv (b).
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
SUMMARY = HERE / "multi_model_summary.json"
OUT_PDF = HERE / "fig_headline.pdf"
OUT_PNG = HERE / "fig_headline.png"
RESULTS = HERE.parent.parent.parent / "data" / "results"

# Per-model canonical sweep directory for n_turns scatter
SWEEP_DIR = {
    "qwen3.5-9b":                    "qwen35_9b_full",
    "qwen3.6:35b-a3b-256k":          "qwen_local_full",
    "gemini-3.1-flash-lite-preview": "gemini_full",
    "gpt-5.5":                       "codex_full_canonical",
    "deepseek-v4-pro":               "deepseek_v4_pro_full",
    "deepseek-v4-flash":             "deepseek_v4flash_canonical",
    "glm-5.1":                       "glm_full",
    "MiniMax-M2.7":                  "minimax_full",
}

PROVIDERS = {
    "qwen3.5-9b":                    "Alibaba",
    "qwen3.6:35b-a3b-256k":          "Alibaba",
    "deepseek-v4-flash":             "DeepSeek",
    "deepseek-v4-pro":               "DeepSeek",
    "gemini-3.1-flash-lite-preview": "Google",
    "gpt-5.5":                       "OpenAI",
    "glm-5.1":                       "Zhipu",
    "MiniMax-M2.7":                  "MiniMax",
}
SHORT = {
    "qwen3.6:35b-a3b-256k":          "qwen3.6-35b-a3b",
    "qwen3.5-9b":                    "qwen3.5-9b",
    "gemini-3.1-flash-lite-preview": "gemini-3.1",
    "deepseek-v4-pro":               "ds-v4-pro",
    "deepseek-v4-flash":             "ds-v4-flash",
    "gpt-5.5":                       "gpt-5.5",
    "glm-5.1":                       "glm-5.1",
    "MiniMax-M2.7":                  "MiniMax",
}
ORDER = [
    "qwen3.5-9b",
    "qwen3.6:35b-a3b-256k",
    "gemini-3.1-flash-lite-preview",
    "deepseek-v4-pro",
    "deepseek-v4-flash",
    "gpt-5.5",
    "glm-5.1",
    "MiniMax-M2.7",
]
LAYERS = ["A", "B", "C", "E", "F", "G", "L"]


def _load_turns(model: str) -> dict:
    """Return {'baseline': np.array, 'omicverse': np.array} of n_turns."""
    path = RESULTS / SWEEP_DIR[model] / "grades.csv"
    out = {"baseline": [], "omicverse": []}
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                t = int(r["n_turns"])
            except (ValueError, KeyError):
                continue
            sys_ = r["system"]
            if "baseline" in sys_:
                out["baseline"].append(t)
            elif "omicverse" in sys_:
                out["omicverse"].append(t)
    return {k: np.asarray(v) for k, v in out.items()}


def main() -> None:
    data = json.loads(SUMMARY.read_text())

    fig = plt.figure(figsize=(15.5, 8.4))
    gs = fig.add_gridspec(
        2, 2, height_ratios=[1.05, 1.0], width_ratios=[1.15, 0.85],
        hspace=0.58, wspace=0.26,
    )

    # -- Panel (a): multi-model bars --------------------------------
    ax = fig.add_subplot(gs[0, 0])
    n = len(ORDER)
    x = np.arange(n)
    w = 0.38
    base_vals = [data[m]["baseline_pass"] for m in ORDER]
    ov_vals = [data[m]["ov_pass"] for m in ORDER]
    ax.bar(x - w / 2, base_vals, w, color="#cc7a3a", label="baseline")
    ax.bar(x + w / 2, ov_vals, w, color="#1f4f8c", label=r"+omicverse (Beacon)")
    for xi, m in enumerate(ORDER):
        d = data[m]
        b_pct = d["baseline_pass"]
        o_pct = d["ov_pass"]
        # Label each bar with its own height. The previous version printed
        # ``*_n_passed``, a seed-0 count, on bars whose height is a multi-seed
        # mean; the two disagree for every multi-seed model (gpt-5.5 +Beacon
        # sat at 91.2 % labelled 37/38 = 97.4 %).
        ax.text(xi - w / 2, b_pct + 1.5, f"{b_pct:.1f}",
                ha="center", va="bottom", fontsize=8.5)
        ax.text(xi + w / 2, o_pct + 1.5, f"{o_pct:.1f}",
                ha="center", va="bottom", fontsize=8.5)
        ax.text(xi, max(b_pct, o_pct) + 10.5, rf"$\Delta\!=\!{(o_pct - b_pct):+.1f}$",
                ha="center", va="bottom", fontsize=9.5, weight="bold")
    labels = [f"{SHORT[m]}\n({PROVIDERS[m]})" for m in ORDER]
    ax.set_xticks(x)
    # Rotated: with eight models the horizontal labels collided, which is the
    # overlap a reviewer flagged in the submitted figure.
    ax.set_xticklabels(labels, fontsize=8.5, rotation=32, ha="right",
                       rotation_mode="anchor")
    ax.set_ylabel("Pass@1 (%)")
    ax.set_ylim(0, 120)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=2,
              frameon=False, fontsize=9.5)
    # Note: n_tasks per arm is 38; seeds vary (1 for qwen, 3 for the rest).
    # Multi-seed Pass@1 is averaged per task across seeds, then across tasks.
    ax.text(1.0, 1.05, "n = 38 tasks/model;  all models seeds 0–2",
            transform=ax.transAxes,
            ha="right", va="bottom", fontsize=9, color="#555555")
    ax.grid(axis="y", linestyle=":", linewidth=0.5, alpha=0.6)
    ax.text(-0.07, 1.02, "(a)", transform=ax.transAxes, fontsize=11, weight="bold")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # -- Panel (b): per-model turn-count scatter ---------------------
    ax_t = fig.add_subplot(gs[0, 1])
    rng = np.random.default_rng(0)
    arms = [("baseline", "#cc7a3a", -w / 2),
            ("omicverse", "#1f4f8c", +w / 2)]
    for xi, m in enumerate(ORDER):
        turns = _load_turns(m)
        for arm, color, dx in arms:
            t = turns[arm]
            jitter = rng.uniform(-0.10, 0.10, size=len(t))
            ax_t.scatter(np.full_like(t, xi + dx, dtype=float) + jitter, t,
                         s=10, color=color, alpha=0.55, edgecolor="none")
            # median tick
            med = float(np.median(t)) if len(t) else 0.0
            ax_t.plot([xi + dx - 0.16, xi + dx + 0.16], [med, med],
                      color="black", lw=1.2, solid_capstyle="round")
    ax_t.set_xticks(x)
    ax_t.set_xticklabels([SHORT[m] for m in ORDER], fontsize=8, rotation=30, ha="right")
    ax_t.set_ylabel("turns per task")
    # Use log scale because gpt-5.5 sits near 3 turns and ds-v4-pro hits 50
    ax_t.set_yscale("log")
    ax_t.set_ylim(1.5, 70)
    ax_t.set_yticks([2, 3, 5, 10, 20, 30, 50])
    ax_t.set_yticklabels(["2", "3", "5", "10", "20", "30", "50"])
    ax_t.grid(axis="y", which="both", linestyle=":", linewidth=0.5, alpha=0.6)
    ax_t.text(-0.10, 1.02, "(b)", transform=ax_t.transAxes, fontsize=11, weight="bold")
    for sp in ("top", "right"):
        ax_t.spines[sp].set_visible(False)
    # Inline horizontal-tick legend at the top of panel
    ax_t.text(0.5, 1.05, "tick = median;  log y", ha="center",
              transform=ax_t.transAxes, fontsize=8.5, color="#555555")

    # -- Panel (c): per-layer Δ heatmap (spans both columns) ---------
    ax2 = fig.add_subplot(gs[1, :])
    mat = np.full((len(ORDER), len(LAYERS)), np.nan)
    text = [["" for _ in LAYERS] for _ in ORDER]
    for i, m in enumerate(ORDER):
        for j, L in enumerate(LAYERS):
            cell = data[m]["by_layer"].get(L)
            if not cell:
                text[i][j] = "—"
                continue
            d = cell["ov_pass"] - cell["baseline_pass"]
            mat[i, j] = d
            # Show the delta and the layer size only. The previous cell text
            # carried ``ov_n_passed``, a seed-0 count, beneath a multi-seed
            # delta — the same mismatch corrected in panel (a).
            text[i][j] = f"{int(d):+d}\n(n={int(cell['ov_n_total'])})"
    cmap = plt.get_cmap("RdYlGn")
    norm = mcolors.TwoSlopeNorm(vmin=-20, vcenter=0, vmax=80)
    im = ax2.imshow(mat, aspect="auto", cmap=cmap, norm=norm)
    ax2.set_xticks(range(len(LAYERS)))
    ax2.set_xticklabels(LAYERS)
    ax2.set_yticks(range(len(ORDER)))
    ax2.set_yticklabels([SHORT[m] for m in ORDER], fontsize=9)
    ax2.set_xlabel("Layer")
    for i in range(len(ORDER)):
        for j in range(len(LAYERS)):
            v = mat[i, j]
            color = "white" if (np.isfinite(v) and abs(v) > 40) else "black"
            ax2.text(j, i, text[i][j], ha="center", va="center", fontsize=8.2, color=color)
    cb = fig.colorbar(im, ax=ax2, label=r"$\Delta$ (pp)", shrink=0.85, pad=0.02)
    cb.ax.tick_params(labelsize=8)
    ax2.text(-0.04, 1.05, "(c)", transform=ax2.transAxes, fontsize=11, weight="bold")

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
    print("wrote", OUT_PDF.name, "and", OUT_PNG.name)


if __name__ == "__main__":
    main()
