# Beacon: A Benchmark and System for Library-Native Agentic Bioinformatics

NeurIPS 2026 supplementary code.

This archive contains the benchmark harness, agent prompts, sweep
configurations, and per-arm grade outputs reported in the main paper.
Trajectory JSONs are excluded for size reasons (~30 GB across all runs);
all derived numbers come from `results/<run>/grades.csv`.

## What's here

```
nips_supplementary/
├── README.md                       (this file)
├── supplement.pdf                  technical appendices (12 pages)
├── bench-env.template.sh           shell env template — fill in API keys
│
├── bench/                          benchmark harness (Python package)
│   ├── tasks.py                    38-task canonical suite
│   ├── grader.py                   per-task pass/fail rules
│   ├── runner.py                   sweep dispatcher
│   ├── grade_run.py                grades.csv writer
│   ├── report.py / figures.py      summary + paper figures
│   ├── stats.py                    bootstrap CIs, McNemar
│   ├── config.py                   YAML loader, system whitelist
│   ├── failure_taxonomy.py         per-trajectory failure-mode tagger
│   ├── _paths.py / types.py        utilities
│   └── adapters/
│       ├── mini_swe.py             mini-swe-agent + LiteLLM (6 LLMs)
│       ├── codex_oauth_model.py    ChatGPT OAuth bridge for gpt-5.5
│       ├── human_scanpy.py         deterministic scanpy reference
│       └── persistent_env.py       cross-step IPython kernel
│
├── prompts/                        three system-prompt variants
│   ├── omicverse_system.md             FULL Beacon (registry+skill discovery)
│   ├── omicverse_system_no_registry.md Beacon minus discovery section
│   └── omicverse_system_doc_rag.md     Beacon with embedding-RAG instead
│
├── scripts/
│   ├── run.sh                      launch a sweep from a YAML config
│   ├── grade.sh                    grade trajectories → grades.csv
│   ├── build_doc_rag_index.py      build MiniLM-L6-v2 index over 613 callables
│   ├── doc_lookup.py               doc-RAG retrieval (used by doc_rag prompt)
│   ├── build_task_md.py            generate human-readable task spec sheet
│   ├── per_check_report.py         per-grader-check failure analysis
│   ├── per_check_detail.py         per-trajectory drill-down
│   ├── analyze.sh                  end-to-end stats pipeline
│   └── sweep.sh                    multi-config dispatcher
│
├── configs/                        sweep configs (one per arm × ablation)
│   ├── codex_{abc,c,e,f,g,l}.yaml  gpt-5.5 sweep, sharded by layer
│   ├── deepseek_full.yaml          deepseek-v4-flash, full suite
│   ├── deepseek_v4_pro_full.yaml   deepseek-v4-pro, full suite
│   ├── gemini_full.yaml            gemini-3.1-flash-lite-preview
│   ├── glm_full.yaml               GLM-5.1
│   ├── minimax_full.yaml           MiniMax-M2.7
│   ├── full_v1.yaml                qwen3.6:35b-a3b local (single-seed)
│   ├── multiseed_full_v1.yaml      qwen3.6, seeds 0/1/2
│   ├── ablation_codex_no_registry.yaml
│   ├── ablation_codex_doc_rag.yaml
│   ├── ablation_v4flash_no_registry.yaml
│   └── ablation_v4flash_doc_rag.yaml
│
├── results/                        grades.csv + summary.md per run
│   ├── codex_full_canonical/       gpt-5.5 (3 seeds, merged)
│   ├── deepseek_v4_pro_full/       deepseek-v4-pro (3 seeds)
│   ├── deepseek_full/              deepseek-v4-flash (3 seeds)
│   ├── deepseek_v4flash_canonical/ deepseek-v4-flash, post-prompt-cleanup
│   ├── gemini_full/                gemini-3.1-flash-lite (3 seeds)
│   ├── glm_full/                   GLM-5.1 (3 seeds)
│   ├── minimax_full/               MiniMax-M2.7 (3 seeds)
│   ├── qwen_local_full/            qwen3.6:35b-a3b (1 seed, local ollama)
│   ├── ablation_codex_no_registry/ Beacon minus discovery (1 seed)
│   ├── ablation_codex_doc_rag/     Beacon with embedding RAG (1 seed)
│   ├── ablation_v4flash_no_registry/
│   └── ablation_v4flash_doc_rag/
│
└── omicverse_components/           Beacon-side library hooks
    ├── _ovagent_lookup.py          public wrappers (registry/skill lookup)
    └── ovagent/
        ├── registry_scanner.py     AST scanner over the omicverse tree
        ├── bootstrap.py            skill-registry initialization
        ├── prompt_builder.py       compact registry summary builder
        ├── tool_runtime_exec.py    handle_search_functions
        └── tool_runtime_workspace.py  handle_skill
```

These files are mirrored from the upstream omicverse repository
(https://github.com/omicverse/omicverse, Apache-2.0). They are
included here for one-archive reproducibility — installing omicverse
from PyPI also makes them available.

## Headline results

**38 tasks · 7 layers (A B C E F G L) · seeds 0/1/2 unless noted.**

### LLM × System (Pass@1)

| LLM                   | Baseline | Beacon  | Δ      |
|-----------------------|---------:|--------:|-------:|
| gpt-5.5               | 71.9%    | 91.2%   | +19.2  |
| deepseek-v4-pro       | 71.1%    | 89.5%   | +18.4  |
| deepseek-v4-flash     | 73.0%    | 85.1%   | +12.1  |
| GLM-5.1               | 67.9%    | 87.5%   | +19.6  |
| MiniMax-M2.7          | 77.2%    | 79.8%   | +2.6   |
| gemini-3.1-flash-lite | 63.4%    | 79.5%   | +16.1  |
| qwen3.6:35b-a3b       | 44.7%    | 79.0%   | +34.2  |

### Discovery-section ablation (1 seed each, gpt-5.5 and v4-flash)

| Variant            | gpt-5.5 | v4-flash |
|--------------------|--------:|---------:|
| Baseline           | 73.7%   | 71.1%    |
| Beacon — no_registry (drop discovery) | 63.2%   | 84.2%    |
| Beacon — doc_rag (vanilla embedding RAG) | 76.3% | 71.1% |
| Beacon — full      | 92.1%   | 86.8%    |

The doc_rag column is the key control: vanilla embedding retrieval over
docstrings is **statistically equivalent to baseline** on both LLMs.
Beacon adds ~+15 pp on top of doc_rag, demonstrating that the gain comes
from the **structured library-side contract** (curated registry + skill
metadata), not from "any retrieval helps".

## Task suite (38 tasks)

```
A  basic data ops          (5)
B  preprocessing/QC          (10)  ← incl. B10 SCENIC GRN
C  clustering/embedding      (4)   ← incl. C04 spatial-trajectory
E  cell-type/annotation      (6)   ← incl. E04 WGCNA module discovery
F  visualization             (4)
G  GO/pathway/enrichment     (5)
L  foundation models / large (4)   ← scGPT, Geneformer, perturbation
```

Tasks are defined in `bench/tasks.py` as a single list of dicts; each
entry specifies `id`, `layer`, `prompt`, `must_have`, and grader hooks.
Run `python -m bench.tasks` (or `scripts/build_task_md.py`) to produce a
human-readable task spec sheet.

## Reproducing the headline numbers

### Path placeholders (anonymization)

To preserve double-blind review, all author-machine paths in this archive
have been replaced with placeholders. Before running, do a global
find-and-replace (or set the matching env vars in `bench-env.sh`):

| Placeholder              | What to put there                                        |
|--------------------------|----------------------------------------------------------|
| `<OVBENCH_ROOT>`         | Absolute path of this unpacked archive.                  |
| `<CONDA_PREFIX>`         | Conda prefix of your omicverse env (the `bin/python` parent). |
| `<BIOMNI_PREFIX>`        | (optional) Conda prefix for biomni baselines.            |
| `<FM_CHECKPOINT_ROOT>`   | Directory holding scGPT/Geneformer/SCimilarity weights.  |
| `<SCENIC_DATA_ROOT>`     | Directory with cisTarget mm10 feathers + motifs (B10).   |
| `<USER_HOME>`            | `$HOME` on your machine.                                 |
| `<DATA_ROOT>`            | Catch-all for any remaining absolute references.         |

Files that contain placeholders: `bench/_paths.py`, `bench/tasks.py`
(fixture roots), `bench/adapters/mini_swe.py`, all `scripts/*.sh`,
`scripts/build_task_md.py`, `scripts/doc_lookup.py`,
`prompts/omicverse_system_doc_rag.md`, `configs/codex_l.yaml`.
A quick sed-pass with `bench-env.sh` sourced is sufficient.

### 1. Set up the environment

```bash
# 1.1  Install the conda env with omicverse and its dependencies.
#      Tested with omicverse 0.4.x, scanpy 1.10, anndata 0.10, scipy 1.13.
conda create -n omicverse python=3.11
conda activate omicverse
pip install omicverse  # or install from source for matching commits

# 1.2  Install bench-side deps.
pip install pyyaml pandas litellm openai mini-swe-agent sentence-transformers

# 1.3  (optional) For local qwen runs, install ollama and pull qwen3.6:35b-a3b.

# 1.4  Configure environment.
cp bench-env.template.sh bench-env.sh
$EDITOR bench-env.sh    # fill in DEEPSEEK_API_KEY etc.
source bench-env.sh
```

### 2. Build the doc-RAG index (only for doc_rag ablation)

```bash
python scripts/build_doc_rag_index.py
# Writes data/doc_rag_index/index.pkl (~1.5 MB, 613 chunks).
```

### 3. Launch a sweep

```bash
# Full Beacon vs baseline on DeepSeek-v4-pro (3 seeds × 38 tasks × 2 arms = 228 traj):
bash scripts/run.sh configs/deepseek_v4_pro_full.yaml

# Discovery-section ablation on gpt-5.5:
bash scripts/run.sh configs/ablation_codex_no_registry.yaml
bash scripts/run.sh configs/ablation_codex_doc_rag.yaml
```

Trajectories land at `trajectories/<run_name>/<task>__<arm>__<model>__seed<n>.json`.

### 4. Grade and summarize

```bash
bash scripts/grade.sh <run_name>
# Writes results/<run_name>/grades.csv and summary.md.
```

The grader is **deterministic** — given a fixed trajectory it always
produces the same pass/fail. Re-running graders against the supplied
trajectories therefore reproduces the per-row Pass@1 in `grades.csv`.

## Beacon system overview

**Three components.** Beacon turns a generic coding agent into a
library-native one without any model fine-tuning:

1. **Static domain prompt** (`prompts/omicverse_system.md`) — names
   omicverse, the high-level workflow phases, and the *contract* the
   agent should follow. Always present.
2. **Function-registry discovery** — exposed as `registry_lookup(query)`
   that returns ranked candidate APIs from a hand-curated registry of
   ~613 callables. The registry is built **once per process** by
   AST-walking the omicverse source tree (`registry_scanner.py`); a
   disk cache keyed on the source-tree mtime makes lookup constant-time
   on warm runs.
3. **Skill discovery** — exposed as `skill_lookup(query)` that loads
   short Markdown "skill" guides describing common workflows. Each
   skill embeds compressed reasoning ("when X fails, fall back to Y")
   that would otherwise consume agent turns.

The two ablations turn each component off in isolation:
- `no_registry` removes both `registry_lookup` and `skill_lookup` from
  the prompt, leaving only the static domain text.
- `doc_rag` replaces the structured registry with a vanilla
  sentence-transformers index over the same 613 callables' docstrings,
  served via `doc_lookup(query)`.

## Citation

```bibtex
@inproceedings{beacon2026,
  title  = {Beacon: A Benchmark and System for Library-Native Agentic Bioinformatics},
  author = {Anonymous},
  booktitle = {Advances in Neural Information Processing Systems},
  year   = {2026}
}
```

## License

The benchmark harness (everything under `bench/`, `scripts/`, `prompts/`,
`configs/`, `results/`) is released under MIT.

The code under `omicverse_components/` is mirrored from
[omicverse](https://github.com/omicverse/omicverse) and remains
under its original license (Apache-2.0).
