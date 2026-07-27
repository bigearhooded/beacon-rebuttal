"""Per-callable semantic decoration of `pymatgen-analysis-defects`.

Replaces the mechanical pass in `mattools_registry.py`, which produced
same-word restatements for 45 % of entries — ``FormationEnergyDiagram`` →
"Formation energy.", ``Interstitial`` → "Interstitial Defect." — and mined
aliases by tokenising those sentences, yielding `different`, `subclass`,
`class`. The component ablation puts 63 % of the uplift on `description`, so
delivering a tautology there is delivering nothing.

This reads each callable's **source**, signature and docstring and asks a model
to judge what it actually does. One call per callable, as
`awe-decoratr/PROTOCOL.md` specifies; the earlier batch pass was a regression
from that protocol, not an implementation of it.

Model separation
----------------
The decorating model is **deepseek-v4-flash**; the benchmark is run with
**gpt-4o**. Using one model to write the documentation another model then
consumes keeps "the registry helps" separable from "a model wrote itself a
cheat sheet". Same reason the benchmark's tasks are third-party.

Leakage control
---------------
Source and docstrings only. `pymatgen-analysis-defects/tests/` is off-limits —
MatTools' 49 tasks carry the same names as 56 functions in that suite, so the
tests are the answers. The decorator never sees them, and never sees a task
prompt.

What is asked for, and why
--------------------------
``purpose``     what the callable is for, in a sentence a practitioner would
                recognise — not a restatement of its name.
``aliases``     what someone would call this operation when searching, drawn
                from domain vocabulary rather than tokenised docstrings.
``key_results`` for a class, which few properties matter in typical use.
                Introspection lists all twelve; the point here is the two or
                three an agent actually needs, and what each returns.
``example``     a minimal runnable call.

``key_results`` is the object-centric translation of Beacon's ``produces``.
Measured on this benchmark, 59 % of failures are the model picking the right
class and then inventing a property — reporting ``N_adsorbate`` where ``.name``
gives ``N_{ads}``. Naming the properties that matter is what that failure needs.
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

OUT = REPO_ROOT / "data" / "mattools_registry_semantic.json"
DECORATOR_MODEL = "deepseek-v4-flash"
URL = "https://api.deepseek.com/v1/chat/completions"

PROMPT = """You are documenting one callable from the Python library
`pymatgen-analysis-defects` so that a coding agent can use it correctly.

CALLABLE: {full_name}
KIND: {kind}
SIGNATURE: {signature}

DOCSTRING:
{docstring}

SOURCE (may be truncated):
{source}

{surface_block}

Return ONLY a JSON object, no prose, with these keys:

{{
  "purpose": "One sentence: what this is FOR and when a materials scientist
              reaches for it. Do not restate the name. If the docstring says
              only 'Interstitial Defect.', say what an interstitial defect is
              and what this class lets you compute.",
  "aliases": ["3-6 terms someone would search for, in domain vocabulary",
              "include the bare name and any standard abbreviation",
              "no generic words like class, type, object, name"],
  "key_results": [
     {{"attr": ".name", "returns": "str", "note": "what the value looks like,
       e.g. 'v_Ga' for a Ga vacancy — be concrete if the source shows it"}}
  ],
  "example": "One minimal runnable line or two showing typical use."
}}

For `key_results`: list only the 2-5 attributes or methods a user of this
callable actually reads. If it is a plain function, describe what the RETURNED
object exposes. Accuracy matters more than coverage — an invented attribute is
worse than a missing one."""


def _source(obj) -> str:
    try:
        return inspect.getsource(obj)[:3500]
    except Exception:
        return "(source unavailable)"


def _surface_block(obj) -> str:
    if not inspect.isclass(obj):
        return ""
    props, meths = [], []
    for n in sorted(dir(obj)):
        if n.startswith("_") or n in ("as_dict", "from_dict", "to_json", "save",
                                      "unsafe_hash"):
            continue
        try:
            a = inspect.getattr_static(obj, n)
        except Exception:
            continue
        if isinstance(a, property):
            props.append(n)
        elif callable(a):
            meths.append(n)
    return (f"PUBLIC PROPERTIES: {', '.join(props)}\n"
            f"PUBLIC METHODS: {', '.join(meths)}\n"
            f"(Choose from these for key_results; do not invent others.)")


def call(prompt: str, key: str, timeout: int = 120) -> str:
    import requests
    r = requests.post(URL, headers={"Authorization": f"Bearer {key}"},
                      json={"model": DECORATOR_MODEL, "temperature": 0.0,
                            "messages": [{"role": "user", "content": prompt}]},
                      timeout=timeout)
    r.raise_for_status()
    m = r.json()["choices"][0]["message"]
    return m.get("content") or m.get("reasoning") or ""


def _parse(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    return d if isinstance(d, dict) and "purpose" in d else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("set DEEPSEEK_API_KEY", file=sys.stderr)
        return 1

    import mattools_registry as R
    base = R.load()
    done = {}
    if OUT.exists():
        done = {e["full_name"]: e for e in json.loads(OUT.read_text())}
    todo = [e for e in base if e["full_name"] not in done]
    if a.limit:
        todo = todo[:a.limit]
    print(f"{len(base)} callables, {len(done)} already decorated, {len(todo)} to do")

    import importlib
    for i, e in enumerate(todo, 1):
        try:
            mod = importlib.import_module(e["module"])
            obj = getattr(mod, e["short_name"])
        except Exception:
            obj = None
        prompt = PROMPT.format(
            full_name=e["full_name"], kind=e["kind"], signature=e["signature"],
            docstring=(e["docstring"] or "(none)")[:1500],
            source=_source(obj) if obj is not None else "(unavailable)",
            surface_block=_surface_block(obj) if obj is not None else "")
        try:
            got = _parse(call(prompt, key))
        except Exception as exc:
            got = None
            print(f"  [{i}/{len(todo)}] ERR {e['short_name']}: {type(exc).__name__}")
        merged = dict(e)
        if got:
            merged["description"] = str(got.get("purpose", ""))[:400]
            al = [str(x) for x in (got.get("aliases") or []) if isinstance(x, str)]
            merged["aliases"] = sorted({e["short_name"], *al})[:8]
            merged["key_results"] = got.get("key_results") or []
            ex = got.get("example")
            if ex and not merged["examples"]:
                merged["examples"] = [str(ex)[:300]]
            merged["source"] = merged["source"] + "+semantic"
        done[e["full_name"]] = merged
        OUT.write_text(json.dumps(list(done.values()), indent=1))
        if got and i % 10 == 0:
            print(f"  [{i}/{len(todo)}] {e['short_name']}: {merged['description'][:70]}",
                  flush=True)
    n_sem = sum(1 for v in done.values() if v["source"].endswith("+semantic"))
    n_kr = sum(1 for v in done.values() if v.get("key_results"))
    print(f"\n{len(done)} entries | {n_sem} semantically decorated | "
          f"{n_kr} with key_results")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
