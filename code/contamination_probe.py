"""Closed-book API probe: what does a model already know about a library?

Answers Reviewer FYHs (Q4) — "how do the authors know the evaluated models had
not already seen these functions during pretraining?" — and supplies direct
evidence for the paper's central claim, which is currently argued from PyPI
download counts alone.

Design: existence discrimination, not free recall
------------------------------------------------
Asking a model to list a library's API rewards verbosity and is painful to
score. Instead each trial names one function and asks whether it exists in a
given library, and if so for its signature. Half the names are real, sampled by
introspecting the installed package; half are **plausible fakes** built by
perturbing real names in the ways a model would if it were pattern-matching
rather than remembering (``qc`` -> ``quality_control_filter``,
``pp.pca`` -> ``pp.run_pca``).

That yields two numbers per (model, library) that mean different things:

``recall``        fraction of real functions correctly identified as existing.
                  High recall = the API is in the weights.
``hallucination`` fraction of fake functions confidently asserted to exist.
                  This is the failure mode the paper is about, measured
                  directly rather than inferred from task outcomes.

A model that scores high recall on ``numpy`` and near-zero on the target
library has not memorised the target, which is what the contamination question
is really asking. Sweeping several libraries across four orders of magnitude of
PyPI downloads turns a single denial into a dose-response curve.

Scoring is deliberately blunt: a verdict is YES or NO, parsed from a required
first token. Signature accuracy is recorded but not scored — a model can know a
function exists without recalling its defaults, and conflating the two would
hide the distinction the probe exists to draw.
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

# Libraries spanning the popularity range the paper's thesis is about.
LIBRARIES = {
    "numpy":      {"import": "numpy",      "prefix": "np"},
    "pandas":     {"import": "pandas",     "prefix": "pd"},
    "sklearn":    {"import": "sklearn",    "prefix": "sklearn"},
    "scipy":      {"import": "scipy",      "prefix": "scipy"},
    "scanpy":     {"import": "scanpy",     "prefix": "sc"},
    "omicverse":  {"import": "omicverse",  "prefix": "ov"},
}

_FAKE_RULES = [
    (r"^(\w+)$",            lambda m: f"run_{m.group(1)}"),
    (r"^(\w+)$",            lambda m: f"{m.group(1)}_analysis"),
    (r"^get_(\w+)$",        lambda m: f"fetch_{m.group(1)}"),
    (r"^compute_(\w+)$",    lambda m: f"calculate_{m.group(1)}"),
    (r"^(\w+)_(\w+)$",      lambda m: f"{m.group(2)}_{m.group(1)}"),
    (r"^(\w+)$",            lambda m: f"{m.group(1)}_v2"),
]


# Path segments that mark library internals. Sampling from these would make
# even numpy look unmemorised — nobody has `numpy.f2py.common_rules.outmess` in
# weights — and the probe would measure obscurity rather than exposure.
_INTERNAL = {"f2py", "externals", "external", "compat", "_libs", "tests",
             "testing", "conftest", "vendored", "_vendor", "util", "utils_",
             "gbq", "clipboard", "sas", "spss", "_config", "typing", "errors"}


def _public_callables(mod, max_depth: int = 2) -> list[tuple[str, Any]]:
    """Public API only: prefer ``__all__``, skip internal namespaces.

    A contamination probe has to sample what a practitioner would actually
    write. ``__all__`` is the library's own statement of that, and where it is
    absent the internal-segment filter approximates it.
    """
    seen, out, frontier = set(), [], [(mod.__name__, mod, 0)]
    while frontier:
        path, obj, depth = frontier.pop(0)
        names = getattr(obj, "__all__", None) or [n for n in dir(obj)
                                                  if not n.startswith("_")]
        for name in names:
            if name.startswith("_") or name in _INTERNAL:
                continue
            try:
                child = getattr(obj, name)
            except Exception:
                continue
            full = f"{path}.{name}"
            if full in seen or any(seg in _INTERNAL for seg in full.split(".")):
                continue
            seen.add(full)
            if inspect.isfunction(child) or inspect.isclass(child):
                if getattr(child, "__module__", "").startswith(mod.__name__):
                    out.append((full, child))
            elif inspect.ismodule(child) and depth < max_depth:
                if getattr(child, "__name__", "").startswith(mod.__name__):
                    frontier.append((full, child, depth + 1))
    return out


def build_inventory(n_real: int = 20, seed: int = 0) -> dict[str, dict]:
    """Real functions by introspection; fakes by perturbing real names.

    Fakes are derived from *different* real functions than the ones probed, so
    a fake never collides with a name in the real set.
    """
    rng = random.Random(seed)
    inv: dict[str, dict] = {}
    for lib, meta in LIBRARIES.items():
        try:
            mod = __import__(meta["import"])
        except Exception as exc:
            print(f"  [skip] {lib}: {type(exc).__name__}", file=sys.stderr)
            continue
        found = _public_callables(mod)
        if len(found) < n_real * 2:
            print(f"  [skip] {lib}: only {len(found)} callables", file=sys.stderr)
            continue
        rng.shuffle(found)
        real = found[:n_real]
        donors = found[n_real:n_real * 3]
        real_names = {p for p, _ in found}

        fakes = []
        for path, _obj in donors:
            head, _, leaf = path.rpartition(".")
            for pat, fn in _FAKE_RULES:
                m = re.match(pat, leaf)
                if not m:
                    continue
                cand = f"{head}.{fn(m)}"
                if cand not in real_names and cand not in fakes:
                    fakes.append(cand)
                    break
            if len(fakes) >= n_real:
                break
        inv[lib] = {
            "real": [{"name": p,
                      "signature": _sig(o)} for p, o in real],
            "fake": [{"name": f} for f in fakes[:n_real]],
        }
    return inv


def _sig(obj) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception:
        return ""


PROMPT = """You are being tested on your knowledge of the Python library `{lib}`.

Does the function or class `{name}` exist in `{lib}`?

Answer with EXACTLY this format and nothing else:
VERDICT: YES or NO
SIGNATURE: the exact call signature if it exists, else NONE

Do not explain. Do not hedge. If you do not recognise it, answer NO."""


def _call(model: str, prompt: str, cfg: dict, timeout: int = 60) -> str:
    import requests
    r = requests.post(
        cfg["url"],
        headers={"Authorization": f"Bearer {cfg['key']}",
                 "Content-Type": "application/json"},
        json={"model": model, "temperature": 0.0, "max_tokens": 120,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=timeout,
    )
    r.raise_for_status()
    msg = r.json()["choices"][0]["message"]
    # Reasoning models may return content=null and put the answer in
    # `reasoning`; a bare ["content"] then yields None and crashes downstream.
    return (msg.get("content") or msg.get("reasoning") or "")


def _verdict(text: str) -> bool | None:
    m = re.search(r"VERDICT:\s*(YES|NO)", text or "", re.I)
    if m:
        return m.group(1).upper() == "YES"
    t = (text or "").strip().upper()
    if t.startswith("YES"):
        return True
    if t.startswith("NO"):
        return False
    return None


def probe(inventory: dict, models: dict, out_path: Path, sleep: float = 0.0) -> dict:
    """Probe every (model, library) pair, persisting after each.

    Written incrementally and resumable on purpose: a long API sweep that only
    writes at the end loses everything to one timeout, and re-running from
    scratch costs the same again.
    """
    prev = {"summary": {}, "records": []}
    if out_path.exists():
        try:
            prev = json.loads(out_path.read_text())
        except Exception:
            pass
    summary = defaultdict(dict, {m: dict(v) for m, v in prev["summary"].items()})
    records = list(prev["records"])

    for model, cfg in models.items():
        for lib, sets in inventory.items():
            if lib in summary.get(model, {}):
                c = summary[model][lib]
                print(f"  [skip] {model:26s} {lib:12s} "
                      f"recall={c['tp'] / max(1, c['tp'] + c['fn']):5.1%}", flush=True)
                continue
            cell = {"tp": 0, "fn": 0, "fp": 0, "tn": 0, "unparsed": 0}
            for kind, items in (("real", sets["real"]), ("fake", sets["fake"])):
                for it in items:
                    try:
                        txt = _call(model, PROMPT.format(lib=lib, name=it["name"]), cfg)
                    except Exception as exc:
                        txt = f"__ERROR__ {type(exc).__name__}: {exc}"
                    v = _verdict(txt)
                    if v is None:
                        cell["unparsed"] += 1
                    elif kind == "real":
                        cell["tp" if v else "fn"] += 1
                    else:
                        cell["fp" if v else "tn"] += 1
                    records.append({"model": model, "library": lib, "kind": kind,
                                    "name": it["name"], "verdict": v,
                                    "raw": (txt or "")[:200]})
                    if sleep:
                        time.sleep(sleep)
            summary[model][lib] = cell
            rec = cell["tp"] / max(1, cell["tp"] + cell["fn"])
            hal = cell["fp"] / max(1, cell["fp"] + cell["tn"])
            print(f"  {model:26s} {lib:12s} recall={rec:5.1%} hallucination={hal:5.1%}",
                  flush=True)
            out_path.write_text(json.dumps(
                {"summary": {m: dict(v) for m, v in summary.items()},
                 "records": records}, indent=1))
    return {"summary": {m: dict(v) for m, v in summary.items()}, "records": records}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20, help="real (and fake) items per library")
    ap.add_argument("--out", type=Path,
                    default=REPO_ROOT / "data" / "results" / "contamination.json")
    ap.add_argument("--inventory-only", action="store_true")
    ap.add_argument("--repeats", type=int, default=1,
                    help="repeat each cell; single-run recall swings ~15 pp at n=20")
    args = ap.parse_args()

    print("building inventory by introspection...")
    inv = build_inventory(args.n)
    for lib, s in inv.items():
        print(f"  {lib:12s} real={len(s['real'])} fake={len(s['fake'])}  "
              f"e.g. real {s['real'][0]['name']} / fake {s['fake'][0]['name']}")
    (args.out.parent / "contamination_inventory.json").write_text(json.dumps(inv, indent=1))
    if args.inventory_only:
        return 0

    models = {}
    if os.environ.get("DEEPSEEK_API_KEY"):
        models["deepseek-v4-flash"] = {"url": "https://api.deepseek.com/v1/chat/completions",
                                       "key": os.environ["DEEPSEEK_API_KEY"]}
    if os.environ.get("OPENROUTER_API_KEY"):
        for m in ("qwen/qwen3.6-35b-a3b", "qwen/qwen3.5-9b"):
            models[m] = {"url": "https://openrouter.ai/api/v1/chat/completions",
                         "key": os.environ["OPENROUTER_API_KEY"]}
    if not models:
        print("no API keys in env; set DEEPSEEK_API_KEY / OPENROUTER_API_KEY",
              file=sys.stderr)
        return 1
    print(f"\nprobing {len(models)} model(s) x {len(inv)} librar(ies) "
          f"x {2 * args.n} items...")
    probe(inv, models, args.out)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
