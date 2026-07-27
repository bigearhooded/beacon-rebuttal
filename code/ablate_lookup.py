"""Leave-one-out ablation over the registry's contract components.

A3 (``prose_lookup``) varies the *rendering* while holding every fact
constant, so it cannot say whether any given field is load-bearing. This
module removes one component at a time — from the retrieval signal as well
as from the rendered output, wherever that component participates in both —
and leaves everything else identical to the +Beacon arm. Comparing each arm
against full +Beacon gives the per-component contribution that Reviewer
z7uB (Q2), Reviewer FYHs (W2) and the AC (W3) ask for.

The component is selected by the ``OVBENCH_ABLATE_COMPONENT`` environment
variable, so a single adapter and a single prompt variant serve every arm;
the arm's identity comes from the sweep's ``run_name``.

Components
----------
``aliases``       drop the alias list — it drives ``alias_score`` (weight
                  100, the second-strongest ranking term), so this is
                  primarily a *retrieval* ablation.
``description``   drop the Beacon-authored one-line description (also a
                  ``weak_score`` term).
``docstring``     drop the docstring block. Not Beacon-authored — included
                  as a scale reference for how much any single text block
                  is worth.
``prerequisites`` drop "Must run first".
``requires``      drop the required-state map.
``produces``      drop the produced-state map.
``contract``      drop prerequisites + requires + produces together — the
                  data-shape contract as a whole.
``examples``      drop the example call.
``dispatch``      drop AST-derived dispatch-branch entries (``name[p=v]``)
                  from the result set entirely.
``none``          no ablation; sanity control that must reproduce +Beacon.

Usage from the agent's bash, mirroring the +Beacon call shape::

    from ablate_lookup import registry_lookup
    print(registry_lookup("pca"))
"""

from __future__ import annotations

import argparse
import copy
import logging
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
for _p in (str(REPO_ROOT), str(REPO_ROOT / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

logger = logging.getLogger(__name__)

ENV_VAR = "OVBENCH_ABLATE_COMPONENT"

VALID = {
    "none", "aliases", "description", "docstring", "prerequisites",
    "requires", "produces", "contract", "examples", "dispatch",
}

# Which entry keys each component clears. ``dispatch`` is handled separately
# because it removes whole entries rather than fields.
_FIELD_MAP: dict[str, tuple[str, ...]] = {
    "aliases":       ("aliases",),
    "description":   ("description",),
    "docstring":     ("docstring",),
    "prerequisites": ("prerequisites",),
    "requires":      ("requires",),
    "produces":      ("produces",),
    "contract":      ("prerequisites", "requires", "produces"),
    "examples":      ("examples",),
}

_EMPTY: dict[str, Any] = {
    "aliases": [], "description": "", "docstring": "", "examples": [],
    "prerequisites": {}, "requires": {}, "produces": {},
}


def component() -> str:
    c = (os.environ.get(ENV_VAR) or "none").strip().lower()
    if c not in VALID:
        raise ValueError(f"{ENV_VAR}={c!r} not in {sorted(VALID)}")
    return c


def _strip(entry: dict[str, Any], comp: str) -> dict[str, Any]:
    if comp in ("none", "dispatch"):
        return entry
    out = copy.deepcopy(entry)
    for f in _FIELD_MAP[comp]:
        out[f] = copy.deepcopy(_EMPTY[f])
    return out


def _install(comp: str) -> None:
    """Strip the component before ranking, so retrieval loses it too.

    Ablating only the rendered output would leave, say, ``aliases`` still
    driving ``alias_score`` — the entry would keep its rank while hiding the
    reason. Stripping ahead of ``rank_entry`` makes the ablation total, which
    is what "is this field necessary?" means.
    """
    from omicverse.utils.ovagent.registry_scanner import RegistryScanner

    if getattr(RegistryScanner, "_ovbench_ablated", None) == comp:
        return
    original = getattr(RegistryScanner, "_ovbench_orig_rank", None) or RegistryScanner.rank_entry
    RegistryScanner._ovbench_orig_rank = staticmethod(original)

    def ablated_rank_entry(request: str, entry: dict[str, Any]):
        if comp == "dispatch" and entry.get("branch_parameter"):
            return None
        return original(request, _strip(entry, comp))

    RegistryScanner.rank_entry = staticmethod(ablated_rank_entry)
    RegistryScanner._ovbench_ablated = comp


def registry_lookup(query: str, max_results: int = 15) -> str:
    """+Beacon lookup with one component removed, same field rendering."""
    _ = max_results
    query = (query or "").strip()
    if not query:
        return "Please provide a non-empty function search query."
    comp = component()
    try:
        _install(comp)
        from omicverse.utils._ovagent_lookup import (
            _RegistryLookupContext, _create_registry_scanner,
        )
        from omicverse.utils.ovagent.tool_runtime_exec import handle_search_functions
        ctx = _RegistryLookupContext(_create_registry_scanner())
        matches = list(ctx._collect_relevant_registry_entries(query, max_entries=20))
        if not matches:
            return f"No functions found matching '{query}'. Try broader keywords."
        # Strip again on the rendering path: rank_entry sees a stripped copy,
        # but the collector returns the original dicts.
        class _Ctx:
            def _collect_relevant_registry_entries(self, q, max_entries=8):
                return [_strip(m, comp) for m in matches[:max_entries]]
        return handle_search_functions(_Ctx(), query)
    except Exception as exc:
        logger.warning("ablate_lookup(%s) failed: %s", comp, exc)
        return ("OmicVerse RegistryScanner not available -- "
                "use `import omicverse as ov; help(ov)` for API reference.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query")
    ap.add_argument("--component", default=None)
    a = ap.parse_args()
    if a.component:
        os.environ[ENV_VAR] = a.component
    print(registry_lookup(a.query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
