"""Few-shot lookup: retrieve worked call examples from the library's own docs.

The baseline Reviewer pwNR asked for. Loads the index built by
``build_fewshot_index.py`` and prints the top-K usage examples for a query.
Each chunk is a signature plus the runnable example code that the library's
maintainers wrote into the docstring — no Beacon field is consulted, so this is
a documentation baseline and not a second registry.

The difference from ``doc_lookup.py`` is what a chunk contains: `doc_RAG`
returns signature plus prose docstring, most of which document no call at all;
this returns only entries that carry a worked example, which is what makes it a
few-shot prompt rather than a documentation dump.

Usage from the agent's bash::

    python <REPO>/scripts/fewshot_lookup.py "cell type annotation"
    python <REPO>/scripts/fewshot_lookup.py --k 4 "spatial domain"
"""
from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import numpy as np

_INDEX_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "fewshot_index" / "index.pkl"
)


def _load_index():
    with open(_INDEX_PATH, "rb") as f:
        return pickle.load(f)


def fewshot_lookup(query: str, k: int = 8,
                   max_chars_per_chunk: int = 1500) -> str:
    """Return the top-K documented usage examples most similar to ``query``."""
    idx = _load_index()
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(idx["model_name"])
    q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    sims = (idx["embeddings"] @ q.T).ravel()
    top = np.argsort(-sims)[: int(k)]
    out = []
    for rank, i in enumerate(top, 1):
        chunk = idx["chunks"][i]["text"]
        if len(chunk) > max_chars_per_chunk:
            chunk = chunk[:max_chars_per_chunk] + "\n[...truncated]"
        out.append(f"--- example {rank}/{k}  similarity={float(sims[i]):.3f} ---"
                   f"\n{chunk}")
    return "\n\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="natural-language query")
    ap.add_argument("--k", type=int, default=8, help="top-K (default 8)")
    ap.add_argument("--max-chars", type=int, default=1500,
                    help="cap each returned chunk (default 1500)")
    a = ap.parse_args()
    print(fewshot_lookup(a.query, k=a.k, max_chars_per_chunk=a.max_chars))


if __name__ == "__main__":
    main()
