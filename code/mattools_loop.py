"""MatTools' iterative arm: retrieve, generate, execute, criticise, re-retrieve.

Why this is a reconstruction and not a port
-------------------------------------------
Upstream's loop lives in ``mtr_rag_test/rag.py::RAGPipeline.pipeline``
(``iteration_limit = 5``). **The published copy cannot execute past iteration
one.** ``generate`` reaches for ``state.memory`` where ``state`` is the plain
dict built as ``{"question": message}``, which raises ``AttributeError``; and
``memory`` is set from ``messages.append(...)``, which is always ``None``
anyway. Nothing catches either, and ``run()`` writes its JSONL only after every
question finishes — so the first question needing a second pass would have
killed the run and produced no output file. The output files exist and are
complete, so the published results came from code that is not in the
repository.

This module therefore implements the loop **as described**, with those two
defects repaired (a real message history is threaded through). Everything that
does run in their copy is copied verbatim: the four prompts from
``mtr_rag_test/prompts.py``, the ``<answer>/<code>/<name>`` extraction, four
model calls per iteration (generate, format-check, critique, critique-format-
check), the ``extra_info`` block that carries runtime output and the critic's
feedback forward, and the replacement — not accumulation — of retrieved context
by the critic's rewritten query.

The consequence for interpretation is stated rather than hidden: the
``theirs`` arm is a **calibration cell**, not a reproduction. If it lands on
their published 52.66 %, the reconstruction is faithful to whatever they ran.
If it does not, we cannot separate "our reconstruction is wrong" from "their
unpublished version differed", and no conclusion about the registry arm
survives.

Stopping rule
-------------
Theirs: the printed dict parses and every value is non-``None``. That is a
*self-assessment* — it never consults the verifier — so the loop cannot leak
answers. Kept exactly, including the consequence that a confidently wrong
answer stops the loop early.

Arms
----
``none``      no retrieval; their single-call baseline prompt, iterated.
              This cell does not exist upstream, and it is the one that
              separates what retrieval contributes from what self-repair does.
``theirs``    their 7,192 LLM-written documents.
``registry``  our semantic registry (file per ``OVBENCH_MT_REGISTRY``).

Both retrieval arms go through MiniLM (``mattools_embed``) so the retriever is
held constant across corpora; upstream used ``text-embedding-3-large``, which
needs an OpenAI embeddings endpoint we do not have.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mattools_run import MAT_PY, MATTOOLS, QUESTIONS, tasks  # noqa: E402

WORKDIR = MATTOOLS / "src"

# ---------------------------------------------------------------- their prompts

SYSTEM_PROMPT = ("You are an assistant for code generation tasks. Use the "
                 "following retrieved contents to answer the user’s question.\n")

ANSWER_FORMAT = """**Answer format**:
Please make sure the response is enclosed within `<answer>`, `<code>` and `<name>` tags. Follow this example format:

<answer>
<code>
```python
# The generated function code
def example_function():
    pass
```
</code>
<name>name_of_generated_function</name>
</answer>"""

USER_PROMPT_LLM_DOC = (
    "**Question**:\n{question}\n\n"
    "**Retrieved code documents from helper**:\n{retrieved_code_documents}\n\n"
    "***Notes on documents usage***\n"
    "1. When attempting to load a file, do not use the file path from the "
    "retrieved documents, be sure to use the path provided in the question.\n"
    "2. If the question provides some code, the code provided in the question "
    "must be used in the generated function.\n\n" + ANSWER_FORMAT)

FORMAT_CHECKER_PROMPT = (
    "Here is your task:\n"
    "1. Please check if the generated code is enclosed within the `<answer>`, "
    "`<code>`, and `<name>` tags:\n" + ANSWER_FORMAT + "\n\n"
    "If the code does not conform to this format, please revise it accordingly.\n"
    "2. Example usages include statements like `result = example_function()` or "
    "`print(example_function())`, which should be removed. The final code should "
    "contain only the function definition without any example calls or comments.\n\n"
    "If the format is correct and no modifications are needed, return the "
    "generated code in the same format as shown above.\n\n"
    "Otherwise, please make the necessary changes and return the corrected code "
    "in the same format as shown above.\n\n"
    "Return only the corrected code in the specified format without any "
    "additional discussion, explanation, or commentary.\n\n"
    "**Generated code:**\n{generated_code}")

CRITICAL_FEEDBACK_PROMPT = (
    "You're a critical feedback agent. Provide feedback on the generated code.\n"
    "The original question is as follows:\n{question}\n\n"
    "The generated code is as follows:\n{generated_code}\n\n"
    "The runtime output of the code is as follows:\n{runtime_output}\n\n"
    "Please provide feedback on the generated code.\n"
    "The goal is to ensure the runtime output is a dictionary and all values in "
    "the dictionary are not None, which means the code has been successfully "
    "executed.\n"
    "If the code is correct, please provide positive feedback. If the code is "
    "incorrect, please provide constructive feedback and summarize the "
    "successful code that can solve the problem in the generated code.\n"
    "After your code feedback, please identify and list specific information or "
    "knowledge that would be helpful to retrieve for improving the code further. "
    "This should include relevant documentation, examples, or reference "
    "materials that a Retrieval Augmented Generation (RAG) system could "
    "provide.\n"
    "Your answer format should be as follows:\n"
    "<think>Your thoughts on the code</think>\n"
    "<feedback>Your feedback on the code</feedback>\n"
    "<next_rag_retrieval>\n"
    "- List specific documentation, APIs, or examples that would be helpful to "
    "retrieve\n"
    "- Include specific topics that would improve code implementation\n"
    "- Mention any libraries, functions, or patterns that would be beneficial "
    "to reference\n"
    "</next_rag_retrieval>")

CRITIC_FORMAT_PROMPT = (
    "Here is your task:\n"
    "1. Please check if the content below is enclosed within the `<think>`, "
    "`<feedback>`, and `<next_rag_retrieval>` tags:\n"
    "<think>Your thoughts on the code</think>\n"
    "<feedback>Your feedback on the code</feedback>\n"
    "<next_rag_retrieval>\n"
    "- List specific documentation, APIs, or examples that would be helpful to "
    "retrieve\n"
    "- Include specific topics that would improve code implementation\n"
    "- Mention any libraries, functions, or patterns that would be beneficial "
    "to reference\n"
    "</next_rag_retrieval>"
    "2. If the content does not conform to this format, please revise it "
    "accordingly.\n"
    "3. If the format is correct and no modifications are needed, return the "
    "content in the same format as shown above.\n\n"
    "Otherwise, please make the necessary changes and return the corrected "
    "content in the same format as shown above.\n\n"
    "Return only the corrected content in the specified format without any "
    "additional discussion, explanation, or commentary.\n\n"
    "**Content:**\n{content}")

# ------------------------------------------------------------------- extraction


def extract_answer(text: str) -> tuple[str, str] | None:
    """Their `<code>`/`<name>` extraction, with a fenced-block fallback."""
    code = re.search(r"<code>\s*```(?:python|py)?\s*(.*?)```\s*</code>",
                     text or "", re.S)
    name = re.search(r"<name>(.*?)</name>", text or "", re.S)
    if code and name:
        return code.group(1).strip(), name.group(1).strip()
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text or "", re.S)
    if not blocks:
        return None
    src = blocks[0]
    m = re.search(r"^\s*def\s+(\w+)\s*\(", src, re.M)
    if not m:
        return None
    return src, (name.group(1).strip() if name else m.group(1))


def extract_critic(text: str) -> tuple[str, str]:
    fb = re.search(r"<feedback>(.*?)</feedback>", text or "", re.S)
    nq = re.search(r"<next_rag_retrieval>(.*?)</next_rag_retrieval>", text or "", re.S)
    if fb and nq:
        return fb.group(1).strip(), nq.group(1).strip()
    return (text or "").strip(), ""          # their fallback: the whole reply

# -------------------------------------------------------------------- execution

# Their `code_check`: run `print(func())`, keep stdout, then decide convergence
# by parsing that stdout. The verifier is never consulted here.
CHECK_RUNNER = '''
import json, sys, os, io, traceback, contextlib
os.chdir({workdir!r})
sys.path.insert(0, {workdir!r})

def emit(**kw):
    sys.__stdout__.write("__CHECK__" + json.dumps(kw) + "\\n")
    raise SystemExit(0)

buf = io.StringIO()
ns = {{}}
try:
    with contextlib.redirect_stdout(buf):
        exec(open({fn_file!r}).read(), ns)
        out = ns[{fname!r}]()
        print(out)
except Exception:
    emit(stdout=buf.getvalue()[-800:], stderr=traceback.format_exc()[-1500:],
         converged=False)

printed = buf.getvalue().strip()
if not printed:
    emit(stdout="", stderr="No dict output from code execution", converged=False)

from utils import ComplexDictParser
with contextlib.redirect_stdout(io.StringIO()):
    try:
        parsed = ComplexDictParser().parse(printed)
    except Exception:
        parsed = None
ok = isinstance(parsed, dict) and parsed != {{}} and \\
     all(v is not None for v in parsed.values())
emit(stdout=printed[-2500:], stderr="", converged=bool(ok))
'''


def code_check(func_src: str, fname: str, timeout: int = 300) -> dict:
    with tempfile.TemporaryDirectory() as td:
        fn = Path(td) / "gen.py"
        fn.write_text(func_src)
        rn = Path(td) / "check.py"
        rn.write_text(CHECK_RUNNER.format(workdir=str(WORKDIR), fn_file=str(fn),
                                          fname=fname))
        try:
            p = subprocess.run([MAT_PY, str(rn)], capture_output=True,
                               text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": f"timeout after {timeout}s",
                    "converged": False}
    line = next((l for l in reversed(p.stdout.splitlines())
                 if l.startswith("__CHECK__")), None)
    if line:
        try:
            return json.loads(line[len("__CHECK__"):])
        except Exception:
            pass
    return {"stdout": "", "stderr": (p.stderr or "")[-800:], "converged": False}

# ------------------------------------------------------------------- the loop


def retrieve(arm: str, query: str) -> str:
    """Top-5 for `query`. The corpus is fixed for the process by `main`,
    because the embedding index is built once and cached."""
    if arm == "none":
        return ""
    import mattools_embed
    return mattools_embed.context(query, k=5)


def call(messages: list[dict], model: str, key: str, url: str,
         temperature: float, timeout: int = 240) -> str:
    import requests
    r = requests.post(url, headers={"Authorization": f"Bearer {key}"},
                      json={"model": model, "temperature": temperature,
                            "messages": messages}, timeout=timeout)
    r.raise_for_status()
    m = r.json()["choices"][0]["message"]
    return m.get("content") or m.get("reasoning") or ""


def run_task(task: Path, arm: str, model: str, key: str, url: str,
             limit: int, temperature: float) -> dict:
    question = (task / "question.txt").read_text().strip()
    ctx = retrieve(arm, question)
    if arm == "none":
        first = question + "\n" + ANSWER_FORMAT
        messages = [{"role": "user", "content": first}]
    else:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_LLM_DOC.format(
                question=question, retrieved_code_documents=ctx)}]

    trace, src, fname, calls = [], "", "", 0
    for it in range(1, limit + 1):
        raw = call(messages, model, key, url, temperature); calls += 1
        checked = call([{"role": "user",
                         "content": FORMAT_CHECKER_PROMPT.format(generated_code=raw)}],
                       model, key, url, temperature); calls += 1
        got = extract_answer(checked) or extract_answer(raw)
        if not got:
            res = {"stdout": "", "converged": False,
                   "stderr": "The response format is incorrect."}
        else:
            src, fname = got
            res = code_check(src, fname)
        trace.append({"iteration": it, "converged": res["converged"],
                      "stderr": (res.get("stderr") or "")[-300:]})
        if res["converged"] or it == limit:
            break

        critic = call([{"role": "user", "content": CRITICAL_FEEDBACK_PROMPT.format(
            question=question, generated_code=checked,
            runtime_output=json.dumps(
                {"stdout": res.get("stdout", ""), "stderr": res.get("stderr", "")},
                ensure_ascii=False, indent=2))}],
            model, key, url, temperature); calls += 1
        critic = call([{"role": "user",
                        "content": CRITIC_FORMAT_PROMPT.format(content=critic)}],
                      model, key, url, temperature); calls += 1
        feedback, next_query = extract_critic(critic)
        if arm != "none" and next_query:
            ctx = retrieve(arm, next_query)          # replaces, as theirs does
        extra = (f"Runtime output of the code:\n"
                 f"{json.dumps({'stdout': res.get('stdout',''), 'stderr': res.get('stderr','')}, ensure_ascii=False, indent=2)}\n\n"
                 f"Suggestions from critic agent:\n{feedback}\n\n"
                 f"New retrieved content from critic agent:\n{ctx}\n\n"
                 f"Now, please generate a new python function based on the "
                 f"above information.")
        messages = messages + [{"role": "assistant", "content": checked},
                               {"role": "user", "content": extra}]

    return {"task": task.name, "arm": arm, "function": src[:8000],
            "function_name": fname, "iterations": len(trace),
            "llm_calls": calls, "converged": trace[-1]["converged"] if trace else False,
            "trace": trace}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["none", "theirs", "registry"], required=True)
    ap.add_argument("--model", default="openai/gpt-4o-2024-08-06")
    ap.add_argument("--iterations", type=int, default=5)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("set OPENROUTER_API_KEY", file=sys.stderr)
        return 1
    url = "https://openrouter.ai/api/v1/chat/completions"

    if a.arm != "none":
        os.environ["OVBENCH_MT_EMBED_CORPUS"] = \
            "theirs" if a.arm == "theirs" else "registry"

    ts = tasks()
    if a.limit:
        ts = ts[:a.limit]
    out = a.out or (REPO_ROOT / "data" / "results" / f"mtloop_{a.arm}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {json.loads(l)["task"] for l in out.read_text().splitlines() if l.strip()}

    print(f"arm={a.arm} model={a.model} iters<={a.iterations} temp={a.temperature} "
          f"tasks={len(ts)} (resuming past {len(done)})", flush=True)
    total_calls = 0
    with out.open("a") as fh:
        for i, t in enumerate(ts, 1):
            if t.name in done:
                continue
            try:
                rec = run_task(t, a.arm, a.model, key, url, a.iterations,
                               a.temperature)
            except Exception as exc:
                rec = {"task": t.name, "arm": a.arm, "function": "",
                       "function_name": "", "iterations": 0, "llm_calls": 0,
                       "converged": False,
                       "error": f"{type(exc).__name__}: {exc}"[:300]}
            total_calls += rec.get("llm_calls", 0)
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            mark = "conv" if rec["converged"] else "----"
            print(f"  [{i:3d}/{len(ts)}] {mark} it={rec['iterations']} "
                  f"calls={rec['llm_calls']:2d} {t.name}", flush=True)
    print(f"\n{total_calls} model calls this session -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
