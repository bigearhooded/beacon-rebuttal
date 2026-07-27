"""Embedding retrieval, applied to whichever corpus is being served.

Upstream MatTools retrieves with an embedding model; the TF-cosine retriever
used elsewhere in these arms is a different device, and a comparison that gives
one corpus embeddings and the other bag-of-words measures the retriever, not
the corpus. This module supplies the same embedding retriever to both, so the
remaining difference is content.

Corpus chosen by OVBENCH_MT_EMBED_CORPUS:
  ``theirs``   MatTools' 7,192 LLM-written documents
  ``registry`` our semantic registry (file per OVBENCH_MT_REGISTRY)

Embeddings are cached to disk keyed by corpus; encoding 7k documents is the
expensive part and it should happen once.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL = "<MODELS>"
THEIRS = Path("<MATTOOLS>/src/"
              "documents_llm_doc_gemini_20_flash_full.json")


def _texts() -> tuple[list[str], list[str], str]:
    """(text to embed, text to inject, cache tag)."""
    which = os.environ.get("OVBENCH_MT_EMBED_CORPUS", "theirs")
    if which == "theirs":
        raw = json.loads(THEIRS.read_text())
        emb = [(d.get("page_content") or "")[:2000] for d in raw]
        inj = []
        for d in raw:
            src = (d.get("metadata") or {}).get("source") or ""
            inj.append(f"Source: {src}\n{(d.get('page_content') or '')[:2500]}")
        keep = [i for i, t in enumerate(emb) if t.strip()]
        return [emb[i] for i in keep], [inj[i] for i in keep], "theirs"
    import mattools_registry as R
    ents = R.load()
    emb = [" ".join([e["short_name"], " ".join(e.get("aliases") or []),
                     e.get("description") or ""]) for e in ents]
    inj = [R.render([e]) for e in ents]
    tag = "reg_" + os.environ.get("OVBENCH_MT_REGISTRY", "mechanical")
    return emb, inj, tag


@lru_cache(maxsize=1)
def _index():
    emb, inj, tag = _texts()
    h = hashlib.sha1(("|".join(emb)).encode()).hexdigest()[:12]
    cache = REPO / "data" / f"mt_embed_{tag}_{h}.npy"
    from sentence_transformers import SentenceTransformer
    os.environ.setdefault("HF_HOME", LOCAL)
    if cache.exists():
        V = np.load(cache)
    else:
        m = SentenceTransformer(MODEL, cache_folder=LOCAL)
        V = m.encode(emb, batch_size=64, show_progress_bar=False,
                     normalize_embeddings=True)
        np.save(cache, V)
    m = SentenceTransformer(MODEL, cache_folder=LOCAL)
    return V, inj, m


def context(query: str, k: int = 5) -> str:
    """Top-k documents for an arbitrary query.

    Separate from `augment` because the iterative arm re-retrieves with the
    critic's rewritten query, which is not the text shown to the model.
    """
    V, inj, model = _index()
    q = model.encode([query[:2000]], normalize_embeddings=True)[0]
    idx = np.argsort(-(V @ q))[:k]
    return "\n\n".join(f"[{i+1}] {inj[j]}" for i, j in enumerate(idx))


def augment(prompt: str, k: int = 5) -> str:
    return ("The following retrieved documents describe relevant pymatgen "
            "code. Use them as needed.\n\n" + context(prompt, k)
            + "\n\n---\n\n" + prompt)
