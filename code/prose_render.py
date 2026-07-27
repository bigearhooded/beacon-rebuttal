"""Prose renderer for the A3 ``prose_equivalent`` ablation arm.

The A3 arm answers Reviewer FYHs (Q1/W3), AC issue #1, and Reviewer
1jWF's causal-identification weakness: *is the gain from the structured
contract, or merely from someone having written the contract down?*

To answer that, information must be held constant while representation
varies. This module consumes the **same ranked match list** that
``omicverse.utils.registry_lookup`` renders and emits the same facts as
flowing English, with no field labels, no key-value layout, and no block
dividers.

What is held identical to the structured arm
--------------------------------------------
* the retrieval and ranking (same scanner, same query, same order),
* the ``full_name(signature)`` line,
* the ``Docstring:`` block, verbatim.

Signature and docstring come from ``inspect`` and exist for any Python
library; they are not Beacon's contribution and so are not the variable
under test. Keeping them byte-identical also keeps the two arms close in
length without artificial padding, since the docstring dominates token
count.

What is re-rendered as prose
----------------------------
Exactly the fields the structured formatter emits — description, the
dispatch branch, ``prerequisites.functions``, ``requires``, ``produces``,
and the example call — plus the ``[match i/n]`` / horizontal-rule framing.
Nothing is added and nothing is dropped: ``verify_prose_parity.py``
asserts fact-level equality against the structured output.

The truncation rules (description at 300 chars, at most 10 rendered
matches out of the first 20 candidates, code-example preference) mirror
``handle_search_functions`` in
``omicverse/utils/ovagent/tool_runtime_exec.py`` exactly. If that
formatter changes, this one must change with it.
"""

from __future__ import annotations

from typing import Any

# Container keys keep their literal ``container['key']`` spelling. Turning
# them into English noun phrases would delete the key path the agent needs
# to write code — that is removing *information*, not removing structure,
# and it would make this arm dirty in the one way it must not be. The
# variable under test is whether relations occupy named, separately
# addressable slots, not how their values are spelled.

_ORDINAL = [
    "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
    "eighth", "ninth", "tenth",
]

_NUMBER_WORD = [
    "zero", "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten",
]


def _number_word(n: int) -> str:
    return _NUMBER_WORD[n] if 0 <= n < len(_NUMBER_WORD) else str(n)


def _ordinal(i: int) -> str:
    return _ORDINAL[i] if 0 <= i < len(_ORDINAL) else f"{i + 1}th"


def _join(items: list[str]) -> str:
    """``['a', 'b', 'c']`` -> ``'a, b and c'``."""
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _say_container_keys(mapping: dict[str, list[str]]) -> str:
    """``{'obsm': ['X_pca'], 'uns': ['pca']}`` -> ``X_pca in obsm and pca in uns``.

    Both identifiers survive — the key name and the container it lives in —
    so no fact is lost. What is dropped is the ``container['key']``
    *notation*, which is itself a machine-readable contract: an agent can
    regex it straight out of the text and paste it into code. Keeping the
    notation would leave the structure under test intact while only the
    labels had been removed. Ordinary documentation names the container in
    passing; it does not emit subscript expressions.
    """
    return _join([
        f"{key} in {container}"
        for container, keys in mapping.items()
        for key in keys
    ])


def _pick_example(examples: list[str]) -> str:
    """Mirror the structured formatter's example-selection rule."""
    code = [ex for ex in examples if ex.strip().startswith(("ov.", "sc."))]
    if code:
        return code[0]
    return examples[0] if examples else ""


def render_entry(m: dict[str, Any], index: int, total: int) -> str:
    """Render one match as prose. ``index`` is 0-based."""
    fname = m.get("full_name", m.get("short_name", ""))
    sig = m.get("signature", "")
    desc = (m.get("description") or "")[:300].strip()

    # The structured formatter emits name+signature+description, then the
    # docstring, then the contract fields. The prose keeps that order: moving
    # the contract ahead of the docstring would give this arm a positional
    # salience advantage and stop the comparison from being about structure.
    head: list[str] = [f"The {_ordinal(index)} match is {fname}."]

    if desc:
        head.append(desc if desc.endswith(".") else desc + ".")

    # Signature is kept verbatim — it is inspect-derived, not Beacon-authored.
    head.append(f"Its call signature is {fname}({sig}).")

    # Neutral declarative clauses, woven into one sentence. No second-person
    # imperative and no explicit causal connectives: those raise the
    # pragmatic force above what a terse label carries, which would bias the
    # comparison toward this arm instead of away from it.
    clauses: list[str] = []
    branch_parameter = m.get("branch_parameter")
    branch_value = m.get("branch_value")
    if branch_parameter and branch_value:
        clauses.append(f"it is the {branch_parameter}='{branch_value}' case")

    req_funcs = (m.get("prerequisites") or {}).get("functions") or []
    if req_funcs:
        clauses.append(f"{_join(list(req_funcs))} runs before it")

    # Guard on the *rendered* string, not on the dict: a map like
    # ``{'layers': []}`` is truthy but yields nothing, and the structured
    # formatter emits a bare ``Requires:`` for it. Mirroring that verbatim
    # would produce broken English ("it reads  and it writes ."), so the
    # empty clause is dropped here. No fact is lost — there are no keys.
    requires = _say_container_keys(m.get("requires") or {})
    if requires:
        clauses.append(f"it reads {requires}")

    produces = _say_container_keys(m.get("produces") or {})
    if produces:
        clauses.append(f"it writes {produces}")

    sentences: list[str] = []
    if clauses:
        # Uppercase the leading character only — ``str.capitalize`` would
        # lowercase the rest, corrupting case-sensitive keys such as
        # ``obsm['X_pca']`` and ``varm['PCs']``.
        joined = _join(clauses)
        sentences.append(joined[:1].upper() + joined[1:] + ".")

    example = _pick_example(m.get("examples") or [])
    if example:
        sentences.append(f"Example call: {example}.")

    out = " ".join(head)

    # Docstring block is reproduced verbatim, with the same indentation the
    # structured formatter uses, so neither arm has a text-volume advantage.
    docstring = (m.get("docstring") or "").strip()
    if docstring:
        indented = docstring.replace("\n", "\n      ")
        out += f"\n    Docstring:\n      {indented}"

    if sentences:
        out += "\n    " + " ".join(sentences)

    return out


def render(matches: list[dict[str, Any]], query: str) -> str:
    """Render a ranked match list as prose.

    Mirrors ``handle_search_functions``: at most ten entries are rendered,
    drawn from the first twenty candidates, in rank order.
    """
    if not matches:
        return f"No functions found matching '{query}'. Try broader keywords."

    rendered: list[str] = []
    for m in matches[:20]:
        rendered.append(m)
        if len(rendered) >= 10:
            break

    n = len(rendered)
    head = (
        f"{_number_word(n).capitalize()} function"
        f"{'' if n == 1 else 's'} match that query, "
        f"described below in order of relevance."
    )
    body = "\n\n".join(
        render_entry(m, i, n) for i, m in enumerate(rendered)
    )
    return f"{head}\n\n{body}"


__all__ = ["render", "render_entry"]
