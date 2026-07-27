# deepseek_full — run summary

Models: `deepseek-v4-flash` · Seeds: [np.int64(0), np.int64(1), np.int64(2)] · Tasks: 42 · Trajectories: 229

## Pass@1 by system

| system | passed | total | Pass@1 | mean wallclock |
|---|---:|---:|---:|---:|
| deepseek_baseline | 84 | 115 | 73.04% | 533s |
| deepseek_omicverse | 97 | 114 | 85.09% | 590s |

## Pass@1 by layer × system

| layer | deepseek_baseline | deepseek_omicverse |
|---|---:|---:|
| A | 15/15 (100%) | 15/15 (100%) |
| B | 22/31 (71%) | 26/31 (84%) |
| C | 5/13 (38%) | 8/13 (62%) |
| E | 13/19 (68%) | 18/19 (95%) |
| F | 12/12 (100%) | 12/12 (100%) |
| G | 13/15 (87%) | 14/15 (93%) |
| L | 4/10 (40%) | 4/9 (44%) |

## Failure-mode breakdown (failed trajectories only)

| system             |   exceeded_turns |   wrong_tool_choice |   wrong_workflow_order |
|:-------------------|-----------------:|--------------------:|-----------------------:|
| deepseek_baseline  |                7 |                  16 |                      8 |
| deepseek_omicverse |                5 |                   8 |                      4 |

