"""Build a few-shot index over the usage examples in `omicverse`'s own docstrings.

Reviewer pwNR asks for a few-shot prompting baseline: "many software libraries
provide documentation with basic usage examples". This builds exactly that
corpus and nothing else — no Beacon field is consulted.

The unit is a **worked call**, not a description: for each public callable whose
docstring carries an ``Examples`` section or ``>>>`` lines, the chunk is the
signature plus the example code. That is what makes this a fair few-shot
baseline rather than a second `doc_RAG`: `doc_RAG` retrieves signature and prose
docstring, and most of those docstrings contain no runnable call.

The coverage number is itself part of the answer. Of the public callables we
walk, only a minority document a usage example, so a few-shot prompt assembled
from library documentation can demonstrate that fraction of the surface and no
more. We report the count the script prints rather than assuming it.

Mirrors ``build_doc_rag_index.py`` in retriever, namespaces and exclusions, so
the two arms differ only in what a retrieved chunk contains.
"""
from __future__ import annotations

import inspect
import pickle
import re
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "data" / "fewshot_index" / "index.pkl"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_MODELS = "<MODELS>"

# Same namespaces as the doc-RAG index, and the same exclusion of
# ``omicverse.utils.*`` where the registry scanners live.
SUBMODULES = [
    "omicverse.bulk", "omicverse.single", "omicverse.space", "omicverse.micro",
    "omicverse.pp", "omicverse.pl", "omicverse.popv", "omicverse.bulk2single",
    "omicverse.alignment", "omicverse.external.scllm",
    "omicverse.external.PyWGCNA", "omicverse.external.single",
]

# An ``Examples``/``Example`` numpydoc section, or bare doctest lines.
_SECTION = re.compile(
    r"\n\s*(?:Examples?|Example usage)\s*\n\s*-{3,}\s*\n(?P<body>.*?)"
    r"(?=\n\s*[A-Z][A-Za-z ]+\n\s*-{3,}|\Z)", re.S)
_DOCTEST = re.compile(r"^\s*>>>.*(?:\n(?:\s*\.\.\..*|\s*>>>.*|\s{4,}\S.*))*",
                      re.M)


def extract_examples(doc: str) -> str:
    """Return the worked-call text in a docstring, or '' if there is none."""
    if not doc:
        return ""
    m = _SECTION.search(doc)
    if m:
        body = m.group("body").strip()
        if body:
            return body
    blocks = _DOCTEST.findall(doc)
    return "\n".join(b.strip() for b in blocks).strip() if blocks else ""


# Beacon's own machinery is re-exported into several public namespaces
# (``ov.space.register_function`` among them) and its docstring demonstrates the
# decorator's fields. Indexing it would show the few-shot baseline the schema it
# is meant to be a control for, so it is excluded by name — the same reason
# ``build_doc_rag_index.py`` skips ``omicverse.utils.*``.
_BEACON_NAMES = {
    "register_function", "registry_lookup", "skill_lookup", "registry_summary",
    "RegistryScanner", "FunctionRegistry", "agent_function",
}


def walk() -> list[dict]:
    import importlib
    chunks, seen, scanned, dropped = [], set(), 0, []
    for modname in SUBMODULES:
        try:
            mod = importlib.import_module(modname)
        except Exception:
            continue
        for name in dir(mod):
            if name.startswith("_"):
                continue
            obj = getattr(mod, name, None)
            if not callable(obj) or id(obj) in seen:
                continue
            seen.add(id(obj))
            if name in _BEACON_NAMES:
                dropped.append(f"{modname}.{name}")
                continue
            scanned += 1
            ex = extract_examples(inspect.getdoc(obj) or "")
            if not ex:
                continue
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = "(...)"
            full = f"{modname.replace('omicverse', 'ov')}.{name}"
            chunks.append({
                "name": full,
                "text": f"{full}{sig}\n\nExample usage:\n{ex}"[:2400],
            })
    print(f"scanned {scanned} public callables; "
          f"{len(chunks)} document a usage example "
          f"({100 * len(chunks) / max(1, scanned):.1f} %)")
    if dropped:
        print(f"excluded {len(dropped)} Beacon-machinery callables: "
              f"{', '.join(sorted(dropped))}")
    return chunks


def main() -> int:
    chunks = walk()
    if not chunks:
        print("no examples found; nothing to index")
        return 1
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(MODEL_NAME, cache_folder=LOCAL_MODELS)
    emb = m.encode([c["text"] for c in chunks], batch_size=64,
                   normalize_embeddings=True).astype("float32")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("wb") as f:
        pickle.dump({"chunks": chunks, "embeddings": emb,
                     "model_name": MODEL_NAME}, f)
    print(f"wrote {OUT}  ({emb.shape[0]} chunks, dim {emb.shape[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
