"""Assemble the MatTools comparison once every arm is scored the same way.

Everything here reads ``rescore_*__theirs.jsonl``: same interpreter (numpy
1.26.4 / pymatgen 2024.8.9, matching upstream's Dockerfile), same
print-round-trip verification, same aggregation. Arms scored any other way are
not comparable and are deliberately not read.

Uncertainty is a paired bootstrap over the 49 tasks with the subtask counts
carried along, because the metric is a ratio of subtasks but the sampling unit
is a task — resampling subtasks would treat the 18 properties of
``test_substitution`` as 18 independent observations, which they are not.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RES = REPO / "data" / "results"
QUESTIONS = Path("<MATTOOLS>/src/"
                 "question_segments/pymatgen_analysis_defects")

# label -> (display name, corpus size)
OURS = [
    ("ours_mt2_baseline",      "no retrieval (baseline)",       None),
    ("ours_mt6_theirdoc",      "their 7192 docs · TF-cosine",   7192),
    ("ours_mt8_embed_theirs",  "their 7192 docs · MiniLM",      7192),
    ("ours_mt4_semantic_B",    "registry 98 · TF-cosine",       98),
    ("ours_mt5_A2",            "registry 98+tests · TF-cosine",  98),
    ("ours_mt7_wide",          "registry 263 · TF-cosine",      263),
    ("ours_mt8_embed_registry", "registry 263 · MiniLM",        263),
]
THEIRS = [
    (["pin2_pureagent_round1", "pin2_pureagent_round2", "pin2_pureagent_round3"],
     "their pure agent (1 call)", None),
    (["pin2_coderag_round1"],
     "their code RAG (5-iter loop)", None),
    (["pin2_llmdocfull_r1", "pin2_llmdocfull_round2", "pin2_llmdocfull_round3"],
     "their LLM-doc RAG (5-iter loop)", 7192),
]


def counts() -> dict[str, int]:
    return {t.name: len(json.loads((t / "properties.json").read_text())["properties"])
            for t in sorted(QUESTIONS.iterdir()) if (t / "properties.json").exists()}


def load(label: str, npro: dict[str, int]) -> dict[str, int] | None:
    """Task -> correct subtasks."""
    p = RES / f"rescore_{label}__theirs.jsonl"
    if not p.exists():
        return None
    out = {}
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        n = npro.get(r["task"], 0)
        if r.get("passed"):
            out[r["task"]] = n
        elif r.get("n_props") and r.get("n_errors") is not None:
            out[r["task"]] = r["n_props"] - r["n_errors"]
        else:
            out[r["task"]] = 0
    return out


def acc(v: dict[str, int], tasks: list[str], npro: dict[str, int]) -> float:
    return 100 * sum(v[t] for t in tasks) / sum(npro[t] for t in tasks)


def boot(a: dict, b: dict, tasks: list[str], npro: dict[str, int],
         n: int = 10000, seed: int = 0) -> tuple[float, float]:
    rng = random.Random(seed)
    diffs = []
    for _ in range(n):
        s = [rng.choice(tasks) for _ in tasks]
        d = sum(npro[t] for t in s)
        diffs.append(100 * (sum(a[t] for t in s) - sum(b[t] for t in s)) / d)
    diffs.sort()
    return diffs[int(0.025 * n)], diffs[int(0.975 * n)]


def sign_test(a: dict, b: dict, tasks: list[str]) -> tuple[int, int, float]:
    from math import comb
    w = sum(1 for t in tasks if a[t] > b[t])
    l = sum(1 for t in tasks if a[t] < b[t])
    n = w + l
    if n == 0:
        return w, l, 1.0
    k = min(w, l)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
    return w, l, p


def main() -> int:
    npro = counts()
    assert sum(npro.values()) == 138

    rows = []
    for label, name, size in OURS:
        v = load(label, npro)
        if v:
            rows.append({"name": name, "size": size, "v": v, "who": "ours"})
    for labels, name, size in THEIRS:
        vs = [load(l, npro) for l in labels]
        vs = [v for v in vs if v]
        if not vs:
            continue
        avg = {t: sum(v.get(t, 0) for v in vs) / len(vs) for t in npro}
        rows.append({"name": name, "size": size, "v": avg, "who": "theirs",
                     "n_rounds": len(vs)})

    tasks = sorted(set.intersection(*[set(r["v"]) for r in rows]))
    print(f"paired on {len(tasks)} tasks / {sum(npro[t] for t in tasks)} subtasks\n")

    base = next(r for r in rows if r["name"].startswith("no retrieval"))
    tbase = next((r for r in rows if r["name"].startswith("their pure agent")), None)

    print(f"{'arm':34s} {'corpus':>7s} {'subtask':>9s} {'vs own base':>12s}  rounds")
    print("-" * 78)
    for r in rows:
        a = acc(r["v"], tasks, npro)
        ref = base if r["who"] == "ours" else (tbase or base)
        d = a - acc(ref["v"], tasks, npro)
        size = str(r["size"]) if r["size"] else "—"
        nr = r.get("n_rounds", 1)
        star = "" if r is ref else f"{d:+11.2f}"
        print(f"{r['name']:34s} {size:>7s} {a:8.2f}% {star:>12s}  {nr}")

    print("\n\nPaired contrasts (10k bootstrap over tasks, sign test over tasks)\n")
    ours_best = max((r for r in rows if r["who"] == "ours"
                     and not r["name"].startswith("no retrieval")),
                    key=lambda r: acc(r["v"], tasks, npro))
    pairs = [
        (ours_best, base, "our best registry vs our baseline"),
        (next(r for r in rows if r["name"].startswith("their 7192 docs · MiniLM")),
         base, "their corpus (best retriever) vs our baseline"),
        (ours_best,
         next(r for r in rows if r["name"].startswith("their 7192 docs · MiniLM")),
         "our registry vs their corpus, same retriever"),
    ]
    cr = next((r for r in rows if r["name"].startswith("their code RAG")), None)
    if cr:
        pairs.append((ours_best, cr,
                      "our registry (1 call) vs their code RAG (5-iter loop)"))
    ld = next((r for r in rows if r["name"].startswith("their LLM-doc")), None)
    if ld:
        pairs.append((ld, ours_best,
                      "their LLM-doc RAG (5-iter loop) vs our registry (1 call)"))

    for a, b, name in pairs:
        va = {t: a["v"][t] for t in tasks}
        vb = {t: b["v"][t] for t in tasks}
        d = acc(va, tasks, npro) - acc(vb, tasks, npro)
        lo, hi = boot(va, vb, tasks, npro)
        # Rounded so a 3-round mean does not read as a fractional subtask win.
        w, l, p = sign_test({t: round(va[t], 3) for t in tasks},
                            {t: round(vb[t], 3) for t in tasks}, tasks)
        flag = "" if (lo > 0 or hi < 0) else "   [CI includes 0]"
        print(f"{name:56s} {d:+6.2f}  CI[{lo:+.1f},{hi:+.1f}]  "
              f"{w}v{l} p={p:.3f}{flag}")

    print("\nPublished, for reference (their accuracy_summary.xlsx, 3-round mean):")
    print("  pure agent 18.36%   code RAG 34.06%   LLM-doc RAG 55.31%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
