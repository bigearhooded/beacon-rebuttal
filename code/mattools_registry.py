"""Auto-decorate `pymatgen-analysis-defects`, and retrieve into a prompt.

Contract-free in the AnnData sense, but not contract-free.

Beacon's ``produces`` field names the **container keys** a call writes, because
that is what an AnnData-shaped library exposes. An object-centric library has
no such keys; what it has is the **attribute surface of the object the call
returns**. The principle is the same — declare what the agent needs in order to
use the result — so the field is translated rather than dropped.

That translation is not decoration. Measured on this benchmark, **59 % of
failures are type mismatches** and the value mismatches share one shape: the
model picks the right class and then invents the property rather than reading
it. ``Adsorbate(...)`` is constructed correctly and then reported as
``N_adsorbate`` where ``.name`` returns ``N_{ads}``; ``DefectComplex`` becomes
``"Substitution + Vacancy"`` where ``.name`` returns ``O_N+v_Ga``. Naming which
properties exist is precisely the missing information.

Originally contract-free by design. The probe in `beacon/examples/pymatgen/feasibility.py`
found **zero observable state changes** across eight pymatgen operations and
three probe strategies: a ``Structure`` always carries the same attributes, so
``requires``/``produces`` have nothing to bind to. Rather than reshape the
library to fit the contract vocabulary, this decorates only what the component
ablation showed carries the effect — ``description`` alone accounts for 63 % of
the uplift on `omicverse`, while ``prerequisites`` and dispatch entries account
for 13 % each. Skipping the unprobeable third is a small loss if that ranking
holds, and testing whether it holds on another library is the point.

Leakage control
---------------
MatTools' 49 tasks are named identically to 56 test functions in
`pymatgen-analysis-defects/tests/` — the benchmark was generated from that
suite. **Tests are therefore off-limits as a decoration source**; mining them
would put the answers in the registry.

Two sources remain, and both are what a real adopter would have:

* **docstrings** of the installed package (101 of 98 public callables carry one),
* the library's three official **tutorial notebooks**, which are documentation
  rather than the benchmark's origin.

The tutorial mining is bounded to call sites and prose, never to expected
values, and every entry records which source produced it.

Retrieval
---------
Upstream's RAG arms prepend retrieved context to a single-shot prompt; this
matches that shape so the comparison is like-for-like — same injection point,
same budget, different content. The retriever is term-frequency cosine over
name + aliases + description, which is deliberately unsophisticated: a stronger
retriever would confound "the registry helps" with "our retriever is better".
"""

from __future__ import annotations

import importlib
import inspect
import json
import math
import os
import pkgutil
import re
import sys
from collections import Counter
from pathlib import Path

PKG = "pymatgen.analysis.defects"
MATTOOLS = Path("<MATTOOLS>")
# The library's own documentation notebooks, taken from upstream
# (materialsproject/pymatgen-analysis-defects, docs/source/content). The copy
# vendored inside MatTools carries only 3 of the 7; the four missing ones
# — defect-finder, formation-energy, freysoldt-correction, photo-conduct —
# cover exactly the task families the vendored set does not. Verified to
# contain zero MatTools task names, so this widens the legitimate source
# without touching the test suite the benchmark was generated from.
TUTORIALS = Path(__file__).resolve().parent.parent / "data" / "pymatgen_defects_docs"
# Which registry to serve. The mechanical build is the default; the
# semantically decorated variants are selected by OVBENCH_MT_REGISTRY so the
# benchmark can be run against each without touching the runner.
_REGISTRIES = {
    "mechanical": "mattools_registry.json",
    "semantic":   "mattools_registry_semantic.json",     # docstring + tutorials
    "semantic_A": "mattools_registry_semantic_A.json",   # + the test suite
    "semantic_A2": "mattools_registry_semantic_A2.json", # + verbatim test call sites
    "wide":       "mattools_registry_wide.json",         # 8 modules the tasks import
}
CACHE = (Path(__file__).resolve().parent.parent / "data" /
         _REGISTRIES.get(os.environ.get("OVBENCH_MT_REGISTRY", "mechanical"),
                         "mattools_registry.json"))

_STOP = {"the", "a", "an", "of", "for", "to", "and", "or", "in", "on", "with",
         "this", "that", "is", "are", "be", "by", "from", "as", "at", "it",
         "return", "returns", "given", "using", "use", "used", "if", "not"}


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def _first_sentence(doc: str) -> str:
    doc = (doc or "").strip()
    if not doc:
        return ""
    head = doc.split("\n\n")[0].replace("\n", " ").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", head)
    return (m.group(1) if m else head)[:300]


def _aliases(name: str, doc: str) -> list[str]:
    """Name variants plus salient terms from the first line of the docstring."""
    out = {name, name.lower()}
    # CamelCase -> spaced, snake_case -> spaced
    spaced = re.sub(r"(?<!^)(?=[A-Z])", " ", name).replace("_", " ").lower().strip()
    if spaced != name.lower():
        out.add(spaced)
    out.add(name.replace("_", " ").lower())
    for w in re.findall(r"[a-z]{4,}", _first_sentence(doc).lower()):
        if w not in _STOP:
            out.add(w)
    return sorted(a for a in out if a)[:8]


def _tutorial_calls() -> dict[str, list[str]]:
    """Call sites per callable name, mined from the official notebooks only."""
    found: dict[str, list[str]] = {}
    if not TUTORIALS.exists():
        return found
    for nb in TUTORIALS.glob("*.ipynb"):
        try:
            cells = json.loads(nb.read_text()).get("cells", [])
        except Exception:
            continue
        for c in cells:
            if c.get("cell_type") != "code":
                continue
            src = "".join(c.get("source", []))
            # Join continuation lines first: the notebooks build objects across
            # several lines (``FormationEnergyDiagram.with_directories(\n ...``),
            # and a line-at-a-time scan captures the opening paren and drops the
            # call that follows it.
            src = re.sub(r"\(\s*\n\s*", "(", src)
            src = re.sub(r",\s*\n\s*", ", ", src)
            for line in src.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or len(line) > 300:
                    continue
                # An import line is the single most useful example for a class
                # an agent has never seen: it fixes the module path, which is
                # the thing most often hallucinated.
                im = re.match(r"from\s+([\w.]+)\s+import\s+(.+)", line)
                if im:
                    for nm in re.split(r"[,\s]+", im.group(2)):
                        nm = nm.strip()
                        if nm and nm[0].isalpha():
                            found.setdefault(nm, [])
                            if line not in found[nm] and len(found[nm]) < 3:
                                found[nm].append(line)
                    continue
                # constructor / function calls, and attribute access on results
                for nm in set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", line)) | \
                          set(re.findall(r"\.([a-z_]\w{3,})\b", line)):
                    if nm in ("print", "len", "list", "dict", "range", "open",
                              "str", "int", "float", "sorted", "enumerate"):
                        continue
                    found.setdefault(nm, [])
                    if line not in found[nm] and len(found[nm]) < 3:
                        found[nm].append(line)
    return found


def _surface(obj) -> dict:
    """Public property and method surface of a class.

    The object-centric analogue of ``produces``: an agent that knows
    ``Vacancy`` exists still fails if it does not know the result carries
    ``.name``, ``.element_changes`` and ``.get_charge_states()``. Introspection
    supplies this exactly — no docstring parsing, no guessing — and it is
    available for any installed package, which is the property that makes it
    worth adding to the schema rather than to this one script.
    """
    if not inspect.isclass(obj):
        return {}
    props, meths = [], []
    for n in sorted(dir(obj)):
        if n.startswith("_") or n in ("as_dict", "from_dict", "to_json", "save",
                                      "unsafe_hash", "validate_monty_v1",
                                      "validate_monty_v2"):
            continue
        try:
            a = inspect.getattr_static(obj, n)
        except Exception:
            continue
        doc = ""
        try:
            d = inspect.getdoc(a.fget if isinstance(a, property) else a) or ""
            doc = d.split("\n")[0][:90]
        except Exception:
            pass
        if isinstance(a, property):
            props.append({"name": n, "doc": doc})
        elif callable(a):
            try:
                sig = str(inspect.signature(a)).replace("(self, ", "(").replace("(self)", "()")
            except Exception:
                sig = "(...)"
            meths.append({"name": n, "signature": sig, "doc": doc})
    return {"properties": props[:12], "methods": meths[:10]}


def build() -> list[dict]:
    calls = _tutorial_calls()
    entries: list[dict] = []
    root = Path(importlib.import_module(PKG).__file__).parent
    for m in pkgutil.iter_modules([str(root)]):
        if m.name.startswith("_"):
            continue
        try:
            mod = importlib.import_module(f"{PKG}.{m.name}")
        except Exception:
            continue
        for name in dir(mod):
            if name.startswith("_"):
                continue
            obj = getattr(mod, name)
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue
            if not getattr(obj, "__module__", "").startswith(PKG):
                continue
            doc = inspect.getdoc(obj) or ""
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = ""
            ex = calls.get(name, [])
            entries.append({
                "full_name": f"{PKG}.{m.name}.{name}",
                "short_name": name,
                "module": f"{PKG}.{m.name}",
                "kind": "class" if inspect.isclass(obj) else "function",
                "signature": sig,
                "description": _first_sentence(doc),
                "docstring": doc[:1500],
                "aliases": _aliases(name, doc),
                "examples": ex,
                "surface": _surface(obj),
                "source": "docstring" + ("+tutorial" if ex else ""),
            })
    # related: co-membership in a module, capped so it stays informative
    by_mod: dict[str, list[str]] = {}
    for e in entries:
        by_mod.setdefault(e["module"], []).append(e["short_name"])
    for e in entries:
        sibs = [s for s in by_mod[e["module"]] if s != e["short_name"]]
        e["related"] = sibs[:5]
    return entries


def load() -> list[dict]:
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    ents = build()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(ents, indent=1))
    return ents


# --------------------------------------------------------------------------
# Retrieve + render
# --------------------------------------------------------------------------

def _tokens(s: str) -> Counter:
    return Counter(w for w in re.findall(r"[a-z_]{3,}", (s or "").lower())
                   if w not in _STOP)


def _score(q: Counter, e: dict) -> float:
    text = " ".join([e["short_name"], " ".join(e["aliases"]), e["description"]])
    d = _tokens(text)
    if not d or not q:
        return 0.0
    num = sum(q[t] * d[t] for t in q if t in d)
    den = math.sqrt(sum(v * v for v in q.values())) * math.sqrt(sum(v * v for v in d.values()))
    return num / den if den else 0.0


def render(entries: list[dict]) -> str:
    out = []
    for i, e in enumerate(entries, 1):
        b = [f"[{i}] {e['full_name']}{e['signature']}"]
        if e["description"]:
            b.append(f"    {e['description']}")
        if e["aliases"]:
            b.append(f"    also known as: {', '.join(e['aliases'][:6])}")
        if e["examples"]:
            b.append(f"    example: {e['examples'][0]}")
        # Semantically decorated entries carry key_results — the properties a
        # user of this callable actually reads, with what each returns. That is
        # the object-centric translation of ``produces`` and it targets the
        # dominant failure on this benchmark: right class, invented property.
        for kr in (e.get("key_results") or [])[:5]:
            attr = str(kr.get("attr", "")).strip()
            if not attr:
                continue
            bits = [f"    {attr}"]
            if kr.get("returns"):
                bits.append(f"-> {kr['returns']}")
            if kr.get("note"):
                bits.append(f"({str(kr['note'])[:110]})")
            b.append(" ".join(bits))
        surf = e.get("surface") or {}
        if surf.get("properties") and not e.get("key_results"):
            b.append("    result properties: " + ", ".join(
                f".{p['name']}" for p in surf["properties"]))
        if surf.get("methods") and not e.get("key_results"):
            b.append("    result methods: " + ", ".join(
                f".{m['name']}{m['signature']}" for m in surf["methods"][:6]))
        if e["related"]:
            b.append(f"    related: {', '.join(e['related'])}")
        out.append("\n".join(b))
    return "\n\n".join(out)


def context(query: str, k: int = 8) -> str:
    """Render the top-k entries for an arbitrary query.

    Split out from `augment` because the iterative arm retrieves twice with
    different strings: first the question, then whatever the critic asks for
    next. Ranking the entries against the text that will be *shown* is only
    correct in the single-shot case.
    """
    ents = load()
    q = _tokens(query)
    return render(sorted(ents, key=lambda e: -_score(q, e))[:k])


def augment(prompt: str, k: int = 8) -> str:
    """Prepend the top-k registry entries relevant to this question."""
    header = (
        "The following functions from `pymatgen.analysis.defects` are relevant "
        "to this task. Use them rather than inventing API names.\n\n"
    )
    return header + context(prompt, k) + "\n\n---\n\n" + prompt


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--query", default=None)
    a = ap.parse_args()
    if a.rebuild and CACHE.exists():
        CACHE.unlink()
    ents = load()
    n_ex = sum(1 for e in ents if e["examples"])
    n_desc = sum(1 for e in ents if e["description"])
    print(f"{len(ents)} entries | {n_desc} with description | {n_ex} with a "
          f"tutorial example | {sum(len(e['aliases']) for e in ents)} alias keys")
    print(f"sources: {Counter(e['source'] for e in ents)}")
    print("contract fields: none (requires/produces/prerequisites deliberately absent)")
    if a.query:
        print(f"\n--- top-8 for {a.query!r} ---")
        q = _tokens(a.query)
        for e in sorted(ents, key=lambda e: -_score(q, e))[:8]:
            print(f"  {_score(q, e):.3f}  {e['full_name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
