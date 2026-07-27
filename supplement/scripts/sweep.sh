#!/bin/bash
# Driver for sweeping (system × task × model × seed). Resumable via --skip-completed.
#
# Usage:
#   bash scripts/sweep.sh                      # default: 35b-a3b × 4 systems × 19 tasks × seed 0 (~5-7 hr)
#   bash scripts/sweep.sh single 4b            # qwen3:4b only
#   bash scripts/sweep.sh single 14b           # qwen3:14b only
#   bash scripts/sweep.sh multiseed 35b        # 3 seeds for stats CI on one model
#   bash scripts/sweep.sh fast                 # A-layer only on 35b-a3b — smoke (~1 hr)
#   bash scripts/sweep.sh xmodel               # 4b + 14b + 35b-a3b × 1 seed (~24 hr)

set -uo pipefail
cd "$(dirname "$0")/.."
source ./bench-env.sh

OVPY=<CONDA_PREFIX>/bin/python
TS=$(date +%Y%m%d_%H%M%S)
LOG="${OVBENCH_RESULTS}/sweep_${TS}.log"

# defaults
MODELS=("qwen3.6:35b-a3b")
SEEDS=(0)
SYSTEMS=("human_scanpy" "raw_llm" "ov_agent" "biomni")
LAYER_FLAG=()

case "${1:-}" in
    fast)
        LAYER_FLAG=(--layer A)
        ;;
    single)
        case "${2:-35b}" in
            4b)   MODELS=("qwen3:4b") ;;
            8b)   MODELS=("qwen3:8b") ;;
            14b)  MODELS=("qwen3:14b") ;;
            32b)  MODELS=("qwen3:32b") ;;
            35b)  MODELS=("qwen3.6:35b-a3b") ;;
        esac
        ;;
    multiseed)
        SEEDS=(0 1 2)
        case "${2:-35b}" in
            4b)   MODELS=("qwen3:4b") ;;
            14b)  MODELS=("qwen3:14b") ;;
            35b)  MODELS=("qwen3.6:35b-a3b") ;;
        esac
        ;;
    xmodel)
        MODELS=("qwen3:4b" "qwen3:14b" "qwen3.6:35b-a3b")
        ;;
    "")
        ;;  # use defaults
    *)
        echo "unknown mode: $1" >&2; exit 1
        ;;
esac

echo "[$(date '+%H:%M:%S')] sweep start" | tee -a "$LOG"
echo "  models=${MODELS[*]}" | tee -a "$LOG"
echo "  seeds=${SEEDS[*]}" | tee -a "$LOG"
echo "  systems=${SYSTEMS[*]}" | tee -a "$LOG"
[ ${#LAYER_FLAG[@]} -gt 0 ] && echo "  layers=${LAYER_FLAG[*]}" | tee -a "$LOG"

# require ollama
if ! curl -sf http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "ERROR: ollama not at :11434 — run scripts/ollama_up.sh first" | tee -a "$LOG" >&2
    exit 1
fi

# warm models so first task isn't 30s slower
for m in "${MODELS[@]}"; do
    echo "[$(date '+%H:%M:%S')] warm $m" | tee -a "$LOG"
    curl -s "http://127.0.0.1:11434/api/generate" \
         -d "{\"model\":\"$m\",\"prompt\":\"hi\",\"stream\":false,\"options\":{\"num_predict\":1}}" \
         > /dev/null
done

# Iteration order: model > seed > TASK > system.
# This compares all systems head-to-head on each task before moving on.
# Get the task list from bench.tasks (filtered by --layer if set).
TASK_IDS=$($OVPY -c "
import sys; sys.path.insert(0, '.')
from bench.tasks import ALL_TASKS
layers = '${LAYER_FLAG[*]:-}'.replace('--layer ', '').split()
ts = ALL_TASKS if not layers else [t for t in ALL_TASKS if t['layer'] in layers]
print(' '.join(t['id'] for t in ts))
")

for model in "${MODELS[@]}"; do
    for seed in "${SEEDS[@]}"; do
        for task in $TASK_IDS; do
            for system in "${SYSTEMS[@]}"; do
                cmd=( "$OVPY" -m bench.runner
                      --system "$system" --model-id "$model" --seed "$seed"
                      --task "$task" --skip-completed )
                echo "[$(date '+%H:%M:%S')] ${cmd[*]}" | tee -a "$LOG"
                "${cmd[@]}" 2>&1 | tee -a "$LOG"
            done
        done
    done
done

echo "[$(date '+%H:%M:%S')] sweep complete; rebuilding report+figures" | tee -a "$LOG"
"$OVPY" -m bench.report 2>&1  | tee -a "$LOG"
"$OVPY" -m bench.figures 2>&1 | tee -a "$LOG"
echo "[$(date '+%H:%M:%S')] DONE" | tee -a "$LOG"
