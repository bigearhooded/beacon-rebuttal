"""Re-score already-generated MatTools functions, ours or theirs.

Why this exists
---------------
MatTools ships the functions its published runs generated —
``mtr_rag_test/round{1,2,3}/gpt-4o-2024-08-06_4/function_generation_results.jsonl``
is the exact output that produced the numbers in their
``accuracy_summary.xlsx``. Running those through *our* verifier answers a
question no amount of re-running our own arms can: is our scoring pipeline
measuring the same thing theirs is?

That matters because our reproduction of their retrieval arm lands far below
their published figure, and there are two candidate explanations — our harness
scores differently, or their published arm is doing something ours is not.
Their arm runs a five-iteration self-repair loop with execution feedback
(``mtr_rag_test/rag.py``: ``iteration_limit = 5``) while their baseline is a
single call (``pure_agent_test/build_agent.py``); ours are all single-shot. This
script rules the first explanation in or out on their own artifacts, at zero
API cost.

Two scoring modes
-----------------
``live``   what ``mattools_run.execute`` does: hand the verifier the dict the
           generated function actually returned.

``theirs`` what ``result_analysis.py`` does: print the returned dict, parse the
           printed text back with their ``ComplexDictParser``, and hand *that*
           to the verifier. Their sandbox has no other channel — the function
           runs in one container and the verifier in another, so everything
           crosses as ``print`` output.

The two are not equivalent, and the direction is knowable in advance. The
verifiers type-check with ``isinstance(value, eval(declared_format))``, and
``isinstance(np.int64(2), int)`` is ``False`` while the same value printed and
``literal_eval``-ed is a plain ``int``. The round trip therefore *launders*
numpy scalars into the types the verifier demands. Anything the round trip
cannot parse, on the other hand, is scored a total loss.

``theirs`` also reproduces two quirks of their harness rather than correcting
them, because the point is to measure what their numbers measure:

* ``run_test`` serialises the verifier's return with ``json.dumps`` and then
  tests ``"ok" in test_result``. That is a substring test against the whole
  JSON, so an error message containing the letters "ok" scores the task as a
  full pass. Tasks passing only by this route are counted and reported.
* A parse failure is ``FunctionError`` — the task loses every subtask, even
  when the function ran and returned a correct value that simply did not
  survive ``repr``.

Aggregation follows ``result_analysis.py:245-255`` in both modes: a fully
passing task contributes all its subtasks, a partial one contributes
``n_props - n_errors``, and the denominator is the fixed 138.

Subtask counts come from each task's own ``properties.json`` keyed by task
name, not from the positional ``ref_sub_tasks_list`` upstream uses — that list
is indexed by ``os.walk`` order, which is not guaranteed to match ours. The
totals are asserted equal to 138, which is the check that the keying is right.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mattools_run import MAT_PY, MATTOOLS, QUESTIONS, execute  # noqa: E402

WORKDIR = MATTOOLS / "src"
OUTDIR = REPO_ROOT / "data" / "results"

# Their path, faithfully: run -> print -> ComplexDictParser -> verifier, with
# their json.dumps + substring "ok" acceptance. `their_src` is imported rather
# than reimplemented so the parser is theirs, bugs included.
THEIRS_RUNNER = '''
import json, sys, os, traceback, runpy
os.chdir({workdir!r})
sys.path.insert(0, {workdir!r})

def emit(**kw):
    print("__RESULT__" + json.dumps(kw))
    raise SystemExit(0)

ns = {{}}
try:
    exec(open({fn_file!r}).read(), ns)
    out = ns[{fname!r}]()
except Exception:
    emit(status="error", runnable=False, passed=False,
         traceback=traceback.format_exc()[-1200:])

# Their `code_validation` captures stdout of `print(func())`; a function that
# returns None or prints nothing is a FunctionError before any comparison.
printed = str(out)
if out is None or printed.strip() == "":
    emit(status="no_stdout", runnable=False, passed=False)

from utils import ComplexDictParser
try:
    parsed = ComplexDictParser().parse(printed)
except Exception:
    parsed = None
if not isinstance(parsed, dict) or parsed == {{}}:
    # Their FunctionError branch: the whole task is lost, all subtasks wrong.
    emit(status="FunctionError", runnable=False, passed=False,
         printed=printed[:400])

try:
    tns = runpy.run_path({test_file!r})
    verdict = tns[{test_name!r}](parsed)
except Exception:
    emit(status="verifier_error", runnable=True, passed=False,
         traceback=traceback.format_exc()[-1200:])

# run_test(): json.dumps then `"ok" in test_result` -- a substring test applied
# to the serialised list, not an equality test on the string "ok".
try:
    dumped = json.dumps(verdict, default=lambda o: repr(o))
except Exception:
    dumped = str(verdict)
is_real_ok = isinstance(verdict, str) and verdict.strip() == "ok"
if "ok" in dumped:
    emit(status="ok", runnable=True, passed=True, n_errors=0,
         ok_by_substring=not is_real_ok, verdict=dumped[:300])
if isinstance(verdict, list) and len(verdict) >= 2:
    emit(status="ok", runnable=True, passed=False,
         n_errors=verdict[-2], n_props=verdict[-1],
         errors=[str(e)[:160] for e in verdict[:-2]][:6])
emit(status="ok", runnable=True, passed=False, verdict=str(verdict)[:200])
'''


def execute_theirs(func_src: str, fname: str, task: Path, workdir: Path,
                   timeout: int = 300) -> dict:
    with tempfile.TemporaryDirectory() as td:
        fn_file = Path(td) / "gen.py"
        fn_file.write_text(func_src)
        runner = Path(td) / "run.py"
        runner.write_text(THEIRS_RUNNER.format(
            workdir=str(workdir), fn_file=str(fn_file), fname=fname,
            test_file=str(task / "new_unit_test.py"), test_name=task.name))
        try:
            p = subprocess.run([MAT_PY, str(runner)], capture_output=True,
                               text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "runnable": False, "passed": False}
    line = next((l for l in reversed(p.stdout.splitlines())
                 if l.startswith("__RESULT__")), None)
    if line:
        try:
            return json.loads(line[len("__RESULT__"):])
        except Exception:
            pass
    return {"status": "no_output", "runnable": False, "passed": False,
            "stderr": (p.stderr or "")[-800:]}


def subtask_counts() -> dict[str, int]:
    """Task name -> number of properties it asks for."""
    out = {}
    for t in sorted(QUESTIONS.iterdir()):
        p = t / "properties.json"
        if p.exists():
            out[t.name] = len(json.loads(p.read_text())["properties"])
    return out


def load_records(path: Path) -> list[dict]:
    """Accept both upstream and our own record shapes."""
    recs = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        name = d.get("question_file_path") or d.get("task")
        src = d.get("function") or ""
        fname = d.get("function_name") or ""
        if not fname:
            # Our own files store the extracted source; recover the entry point.
            import re
            m = re.search(r"^\s*def\s+(\w+)\s*\(", src, re.M)
            fname = m.group(1) if m else ""
        recs.append({"task": name, "function": src, "function_name": fname})
    return recs


def score_one(rec: dict, mode: str = "live") -> dict:
    task = QUESTIONS / rec["task"]
    if not rec["function"] or not rec["function_name"] or not task.exists():
        return {**rec, "runnable": False, "passed": False,
                "status": "empty_or_missing", "n_errors": None, "n_props": None}
    runner = execute if mode == "live" else execute_theirs
    res = runner(rec["function"], rec["function_name"], task, WORKDIR)
    return {**rec, "mode": mode,
            "runnable": bool(res.get("runnable")),
            "passed": bool(res.get("passed")),
            "status": res.get("status"),
            "n_errors": res.get("n_errors"),
            "n_props": res.get("n_props"),
            "ok_by_substring": bool(res.get("ok_by_substring")),
            "errors": res.get("errors", []),
            "error": (res.get("traceback") or "")[-300:]}


def aggregate(scored: list[dict], counts: dict[str, int]) -> dict:
    total_sub = sum(counts.values())
    correct_sub = 0
    for r in scored:
        n = counts.get(r["task"], 0)
        if r["passed"]:
            correct_sub += n
        elif r["n_props"] and r["n_errors"] is not None:
            correct_sub += r["n_props"] - r["n_errors"]
    n = len(scored)
    return {
        "n_tasks": n,
        "total_subtasks": total_sub,
        "correct_subtasks": correct_sub,
        "task_accuracy": 100 * sum(r["passed"] for r in scored) / max(1, n),
        "subtask_accuracy": 100 * correct_sub / max(1, total_sub),
        "runnable_rate": 100 * sum(r["runnable"] for r in scored) / max(1, n),
    }


def published(d: Path) -> dict | None:
    """Their own scores for this directory, if the xlsx is present."""
    x = d / "accuracy_summary.xlsx"
    if not x.exists():
        return None
    try:
        import pandas as pd
        df = pd.read_excel(x)
    except Exception:
        return None
    row = {str(r["Task/ Sub-task"]).strip(): r for _, r in df.iterrows()}
    t, s = row.get("Tasks"), row.get("Sub-tasks")
    if t is None or s is None:
        return None
    return {"task_accuracy": float(t["Accuracy (%)"]),
            "subtask_accuracy": float(s["Accuracy (%)"]),
            "runnable_rate": float(t["Function Runnable Rate"]),
            "correct_subtasks": int(s["Correct"])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, required=True,
                    help="directory holding function_generation_results.jsonl, "
                         "or a .jsonl file directly")
    ap.add_argument("--label", default=None)
    ap.add_argument("--mode", choices=["live", "theirs"], default="live")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    src = a.path if a.path.suffix == ".jsonl" else \
        a.path / "function_generation_results.jsonl"
    if not src.exists():
        print(f"no such file: {src}", file=sys.stderr)
        return 1
    label = (a.label or src.parent.name) + ("" if a.mode == "live" else "__theirs")

    counts = subtask_counts()
    assert sum(counts.values()) == 138, \
        f"subtask total is {sum(counts.values())}, expected 138"

    recs = load_records(src)
    unknown = [r["task"] for r in recs if r["task"] not in counts]
    if unknown:
        print(f"WARNING {len(unknown)} unrecognised task names, e.g. {unknown[:3]}")

    print(f"{label}: {len(recs)} records from {src}  [mode={a.mode}]", flush=True)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / f"rescore_{label}.jsonl"

    scored: list[dict] = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for i, r in enumerate(ex.map(lambda x: score_one(x, a.mode), recs), 1):
            scored.append(r)
            mark = "PASS" if r["passed"] else ("run " if r["runnable"] else "ERR ")
            ne, npr = r.get("n_errors"), r.get("n_props")
            detail = f"{npr - ne}/{npr}" if (ne is not None and npr) else ""
            print(f"  [{i:3d}/{len(recs)}] {mark} {r['task'][:46]:46s} {detail}",
                  flush=True)
    with out.open("w") as fh:
        for r in scored:
            fh.write(json.dumps(r) + "\n")

    ours = aggregate(scored, counts)
    theirs = published(src.parent)
    n_sub = sum(bool(r.get("ok_by_substring")) for r in scored)
    if n_sub:
        subs = [r["task"] for r in scored if r.get("ok_by_substring")]
        print(f"\n{n_sub} task(s) scored a full pass only because \"ok\" appeared "
              f"as a substring of the error JSON: {', '.join(subs)}")
    print(f"\n{'':22s} {'task':>8s} {'subtask':>9s} {'runnable':>9s} {'correct':>8s}")
    print("-" * 60)
    print(f"{'ours (this verifier)':22s} {ours['task_accuracy']:7.2f}% "
          f"{ours['subtask_accuracy']:8.2f}% {ours['runnable_rate']:8.2f}% "
          f"{ours['correct_subtasks']:6d}/138")
    if theirs:
        print(f"{'theirs (xlsx)':22s} {theirs['task_accuracy']:7.2f}% "
              f"{theirs['subtask_accuracy']:8.2f}% {theirs['runnable_rate']:8.2f}% "
              f"{theirs['correct_subtasks']:6d}/138")
        print(f"{'delta':22s} {ours['task_accuracy']-theirs['task_accuracy']:+7.2f}  "
              f"{ours['subtask_accuracy']-theirs['subtask_accuracy']:+8.2f}  "
              f"{ours['runnable_rate']-theirs['runnable_rate']:+8.2f}")

    summary = OUTDIR / "rescore_summary.jsonl"
    with summary.open("a") as fh:
        fh.write(json.dumps({"label": label, "mode": a.mode, "source": str(src),
                             "ok_by_substring": n_sub,
                             "ours": ours, "theirs": theirs}) + "\n")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
