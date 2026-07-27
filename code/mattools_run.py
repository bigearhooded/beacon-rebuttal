"""Run MatTools' real-world tool-usage benchmark, with and without a registry.

MatTools (arXiv:2505.10852, github.com/Grenzlinie/MatTools) is a third-party
benchmark on `pymatgen-analysis-defects`: 49 questions / 138 subtasks, each a
directory holding a prompt, an expected-property list, and a verification
function. Using it answers three reviewer asks at once — a second library, a
**materially different state model**, and **tasks nobody here wrote**, which is
the part a self-authored benchmark can never supply.

Two deviations from the upstream harness, both disclosed in the output:

*Execution.* Upstream runs generated code in a Docker sandbox
(`DockerSandbox(image="mat-tool-ben")`). This host has Apptainer, not Docker,
so functions execute in an isolated conda environment instead. The grading
logic is unchanged — same generated function, same verification file, same
property comparison — only the container differs.

*Scoring.* Uses each task's own ``new_unit_test.py`` — the upstream verifier —
rather than comparing against ``properties.json``. That distinction matters:
the verifier receives **live Python objects**, checks ``isinstance`` against a
declared format, applies ``np.allclose`` where the task asks for it, and only
then compares equality. An earlier version of this script compared string
renderings of ``properties.json`` instead and scored 6.1 % where the paper
reports 18.4 %, because ``[(138, 0, 1), (138, 1, 1)]`` does not equal its own
repr, ``True`` does not equal ``"True"``, and an 8 % numerical difference that
``np.allclose`` accepts fails an exact match. Two rates, as upstream:
**function-runnable** and **task-accuracy** (verifier returns ``"ok"``).

Arms
----
``baseline``  the question prompt alone — comparable to the paper's
              "pure agent" numbers (GPT-4o 18.36 %).
``beacon``    the same prompt plus a `registry_lookup` over an auto-decorated
              registry for the target library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MATTOOLS = Path("<MATTOOLS>")
QUESTIONS = MATTOOLS / "src" / "question_segments" / "pymatgen_analysis_defects"
# The interpreter generated code runs in. Overridable because reproducing
# upstream's numbers needs upstream's pins: they built on numpy 1.26.4 /
# pymatgen 2024.8.9, and numpy 2 changed scalar repr (`np.True_` where 1.x
# printed `True`), which their result parser cannot read. `beacon_mat_pin`
# matches their Dockerfile; `beacon_mat2` is what our own arms ran under.
MAT_PY = os.environ.get("OVBENCH_MT_PYTHON",
                        "<ENV>/bin/python")

SYSTEM = """You are a materials scientist writing Python with pymatgen.

Return ONLY a Python function inside a single ```python code block. No prose
before or after. The function takes no arguments and returns a dict mapping
each requested property name to its computed value. If a property cannot be
computed, set it to None and still return the others."""


def tasks() -> list[Path]:
    return sorted(p for p in QUESTIONS.iterdir() if (p / "question.txt").exists())


def _extract(text: str) -> tuple[str, str] | None:
    """Pull the function source and its name out of a model response."""
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text or "", re.S)
    src = blocks[0] if blocks else (text or "")
    m = re.search(r"^\s*def\s+(\w+)\s*\(", src, re.M)
    if not m:
        return None
    # Drop anything before the first def so stray imports at module level do
    # not shadow the sandbox's own preamble.
    return src[src.index(m.group(0)):] if m.start() else src, m.group(1)


def call_model(prompt: str, model: str, key: str, url: str, timeout: int = 180) -> str:
    import requests
    r = requests.post(url, headers={"Authorization": f"Bearer {key}"},
                      json={"model": model, "temperature": 0.0,
                            "messages": [{"role": "system", "content": SYSTEM},
                                         {"role": "user", "content": prompt}]},
                      timeout=timeout)
    r.raise_for_status()
    msg = r.json()["choices"][0]["message"]
    return msg.get("content") or msg.get("reasoning") or ""


RUNNER = '''
import json, sys, os, traceback, runpy
os.chdir({workdir!r})
sys.path.insert(0, {workdir!r})
ns = {{}}
try:
    exec(open({fn_file!r}).read(), ns)
    out = ns[{fname!r}]()
except Exception:
    print("__RESULT__" + json.dumps({{"status": "error",
          "traceback": traceback.format_exc()[-1200:]}}))
    raise SystemExit(0)
if not isinstance(out, dict):
    print("__RESULT__" + json.dumps({{"status": "not_a_dict",
          "type": type(out).__name__}}))
    raise SystemExit(0)
# Verification runs in this same process because the upstream verifier expects
# live objects (isinstance checks, np.allclose); serialising the dict across a
# process boundary would change exactly what it is testing.
try:
    tns = runpy.run_path({test_file!r})
    fn = next(v for k, v in tns.items()
              if k.startswith("test_") and callable(v))
    verdict = fn(out)
except Exception:
    print("__RESULT__" + json.dumps({{"status": "verifier_error",
          "traceback": traceback.format_exc()[-1200:], "runnable": True}}))
    raise SystemExit(0)
if isinstance(verdict, str) and verdict.strip() == "ok":
    print("__RESULT__" + json.dumps({{"status": "ok", "runnable": True,
          "passed": True, "n_errors": 0}}))
elif isinstance(verdict, list) and len(verdict) >= 2:
    print("__RESULT__" + json.dumps({{"status": "ok", "runnable": True,
          "passed": False, "n_errors": verdict[-2], "n_props": verdict[-1],
          "errors": [str(e)[:160] for e in verdict[:-2]][:6]}}))
else:
    print("__RESULT__" + json.dumps({{"status": "ok", "runnable": True,
          "passed": False, "verdict": str(verdict)[:200]}}))
'''


def execute(func_src: str, fname: str, task: Path, workdir: Path,
            timeout: int = 300) -> dict:
    """Execute the generated function and verify it, both in the isolated env."""
    with tempfile.TemporaryDirectory() as td:
        fn_file = Path(td) / "gen.py"
        fn_file.write_text(func_src)
        runner = Path(td) / "run.py"
        runner.write_text(RUNNER.format(workdir=str(workdir), fn_file=str(fn_file),
                                        fname=fname,
                                        test_file=str(task / "new_unit_test.py")))
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["baseline", "beacon", "theirdoc", "embed"], default="baseline")
    ap.add_argument("--model", default="openai/gpt-4o-2024-08-06")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("set OPENROUTER_API_KEY", file=sys.stderr)
        return 1
    url = "https://openrouter.ai/api/v1/chat/completions"

    ts = tasks()
    if a.limit:
        ts = ts[:a.limit]
    out_path = a.out or (REPO_ROOT / "data" / "results" /
                         f"mattools_{a.arm}_{a.model.split('/')[-1]}.jsonl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out_path.exists():
        done = {json.loads(l)["task"] for l in out_path.read_text().splitlines() if l.strip()}

    workdir = MATTOOLS / "src"
    print(f"arm={a.arm} model={a.model} tasks={len(ts)} (resuming past {len(done)})")
    with out_path.open("a") as fh:
        for i, t in enumerate(ts, 1):
            if t.name in done:
                continue
            prompt = (t / "question.txt").read_text()
            if a.arm == "beacon":
                from mattools_registry import augment          # noqa: F401
                prompt = augment(prompt)
            elif a.arm == "embed":
                from mattools_embed import augment as eaug     # noqa: F401
                prompt = eaug(prompt)
            elif a.arm == "theirdoc":
                from mattools_theirdoc import augment as taug   # noqa: F401
                prompt = taug(prompt)
            try:
                resp = call_model(prompt, a.model, key, url)
            except Exception as exc:
                resp = f"__ERROR__ {type(exc).__name__}: {exc}"
            ext = _extract(resp)
            if not ext:
                rec = {"task": t.name, "arm": a.arm, "runnable": False,
                       "passed": False, "reason": "no function in response",
                       "function": (resp or "")[:4000]}
            else:
                src, fname = ext
                res = execute(src, fname, t, workdir)
                rec = {"task": t.name, "arm": a.arm, "function_name": fname,
                       "runnable": bool(res.get("runnable")),
                       "passed": bool(res.get("passed")),
                       "status": res.get("status"),
                       "n_errors": res.get("n_errors"),
                       "n_props": res.get("n_props"),
                       "errors": res.get("errors", []),
                       "error": (res.get("traceback") or "")[-400:],
                       # Keep the source: re-scoring under a changed verifier
                       # should never require paying for the model again.
                       "function": src[:6000]}
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            mark = "PASS" if rec["passed"] else ("run " if rec["runnable"] else "ERR ")
            ne, npr = rec.get("n_errors"), rec.get("n_props")
            detail = f"{npr - ne}/{npr}" if (ne is not None and npr) else ""
            print(f"  [{i:3d}/{len(ts)}] {mark} {t.name:44s} {detail}", flush=True)
    print(f"\nwrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
