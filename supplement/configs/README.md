# Run configurations

Each YAML file in this directory defines **one reproducible benchmark run**.
`bench.runner --config configs/<name>.yaml` materialises the cross-product of
`scope.systems × scope.task_ids × scope.seeds` and writes one trajectory JSON
per run into `trajectories/<run_name>/`.

The grader is a separate postprocessing step:

```bash
python -m bench.grader --traj-dir trajectories/<run_name>
```

It reads the trajectory JSONs and emits `results/<run_name>/grades.csv` plus a
markdown summary.

## Schema

Field          | Description
--             | --
`run_name`     | Output namespace. All artefacts shard under this name. Convention: `<scope_tag>` (e.g. `smoke_a_layer`, `full_v1`).
`description`  | Free-text — shown in the run summary, useful as a record of intent.
`llm.model`    | Model id passed verbatim to every adapter.
`llm.endpoint` | OpenAI-compatible base URL (default: local ollama).
`llm.api_key_env` | Name of the environment variable holding the API key.
`llm.temperature` | Sampling temperature (the runner adds a small per-seed jitter).
`agent.max_agent_turns` | Cap on agent loop iterations (per-task `max_turns` overrides this if smaller).
`scope.systems` | Subset of `{mini_swe_omicverse, mini_swe_baseline, human_scanpy}`. The two `mini_swe_*` arms share the same loop, model, and tools — only the system prompt differs (treatment vs. control).
`scope.task_ids` | Explicit task ids; if empty, falls back to `layers` / `difficulties`.
`scope.layers` | Layer filter (`A`–`G`); used only if `task_ids` is empty.
`scope.difficulties` | Difficulty filter (`easy`/`medium`/`hard`).
`scope.seeds` | One or more integer seeds.
`scope.skip_completed` | If `true`, skip trajectories that already exist on disk.
`paths.trajectories_dir` | Default `trajectories/` — sharded by `run_name`.
`paths.results_dir` | Default `results/` — sharded by `run_name`.
`paths.workspace_dir` | Per-run sandbox parent; default `data/workspace/`.
`paths.logs_dir` | Default `logs/` — sharded by `run_name`.

## Available configs

- `smoke_a_layer.yaml` — A-layer only × 3 systems × seed 0. ~1 hr.
- `full_v1.yaml` — full 21-task suite × 3 systems × seed 0. ~5–7 hr.
- `multiseed_full_v1.yaml` — full suite × 3 systems × seeds 0,1,2. ~15–20 hr.
- `xmodel_full_v1.yaml` — 4b + 14b + 35b-a3b × 3 systems × seed 0. ~24 hr.
- `debug_single_task.yaml` — debug template: both mini-swe arms on a single task.
