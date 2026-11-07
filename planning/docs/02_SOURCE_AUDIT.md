# 02 — v1.4 source audit and implementation seams

## Evidence and limits
Inspected `Python-Quest-2D-v1.4-Windows-x64.zip`, including `docs/PROJECT_STATE.md`, `README.md`, source trees, mission JSON, maps and tests. The package states 76 missions and 21 unit test methods. Independently ran the Python-only `tools/check_content.py` in this session: 24 original solutions and six original maps passed. Native game and all regression tests were not rerun here because `pygame-ce` was absent from this environment. Do not confuse the v1.4 embedded report with new independently executed tests.

## Code map and recommended extension seams
| Actual v1.4 path | Existing responsibility | Proposed changes | Do NOT do |
|---|---|---|---|
| `game/app.py` (618 lines) | main loop, events, scene, submission, render | route new services through small composition objects; keep input stable | rewrite into a new engine in one sprint |
| `game/expedition.py` (439) | travel, world gating, physical mission effects, replay | `WorldTravel`, `UnlockPolicy`, `ProgramLibrary` delegation | silently alter XP or current mission IDs |
| `game/world.py` (92) | coordinates, collisions, interactables | add typed device adapter and safe spawn resolution | bypass tile collision for new props |
| `game/pixel_world.py` (478) | sprite and planet rendering | layered authored tile variants, light masks, depth rules | draw gigantic obstructive UI inside world |
| `game/presentation.py` (113) | arrivals and stage cues | world-identifiable transitions with skip/reduced motion | forced cutscenes |
| `game/diagnostics.py` (78) | nearby diagnostic UI | observed state, test traces, execution replay | unbounded text in 768x576 viewport |
| `ui/code_editor.py`, `ui/terminal.py` | code editing, tests, hint flow | diff-based failures, current line highlight, program saves | breaking Ctrl+Enter/F1/F2 shortcuts |
| `core/worker.py` (178) | local Python execution, case validation | extend explicit contracts with bounded actions | run player functions on Pygame render loop |
| `core/grade.py` (47) | isolated subprocess, 3-second timeout | centralized result-size checks, safe JSON parse | call current isolation a hostile-code sandbox |
| `core/progress.py` (88) | schema4 save, XP, backup migrations | additive schema5 migration only if new structure requires it | reset/overwrite player `progress.json` |
| `content/expeditions/*.json` | functions/objects, world effects | new missions with unique IDs, cases, effects | load design blueprint JSON as executable mission without integration |
| `content/planets/*.json` | physical map, spawn, sites | new regions via additive, traversable maps | place collision props on a saved position without escape |
| `content/universe/destinations.json` | world unlocks | revise prerequisite chain after prereq missions exist | remove Expedition Preview before full route ships |

## Current worker behavior: important details
`core/grade.py` starts `worker.py` using `python -I -S`, a temporary cwd, a 3-second timeout and controlled environment. The worker `exec()`s submitted code in a fresh namespace for each case; validates script/function/object contracts, with special expedition path/model validators; returns plain JSON. Grader limits source to 64 KiB and printed output to 8192 characters. Worker can still access local OS resources if learner code is malicious. New persistent programs should be dispatched as bounded on-demand runs against immutable observations, never long-running Python processes tied to FPS.

## Current save behavior
`core/progress.py` writes atomically to `%LOCALAPPDATA%/PythonQuest2D/progress.json` or `PYTHONQUEST_SAVE`; legacy schema 2→3 and 3→4 have backups. `fresh()` includes `player`, `completed`, `hinted`, `drafts`, `attempts`, `world_flags`, `review`, `settings`. The loaded dict may also contain unrecognized extension fields, which should be retained. `award()` assumes `LESSONS[mission_id]["world_effect"]`, grants 100/75/25 XP based on hint/reveal state, and is intentionally idempotent. Design new world-effect keys uniquely. Keep `completed`, `hinted`, `revealed`, `attempts` and other existing fields unchanged.

## High-priority source defects or design risks (not verified bugs)
1. Giant `app.py` and `expedition.py` are integration hotspots. Introduce small adapters, not competing loops.
2. Zone transitions currently use `requires` in `destinations.json`; Orion currently depends on unshipped `mission_control_16`, forcing Preview. Define a coherent unlock chain and test old profiles.
3. `award()` uses every mission's `world_effect`, so failure to include it will crash after passing a newly authored challenge.
4. Test contracts must distinguish `function`, `object`, `script` and `simulation` appropriately, with valid first-case effect semantics.
5. Program replay already uses `p["programs"]`, `p["last_replay"]` and `p["expedition_job"]`. Do not replace these legacy structures; namespace a new program library and migrate their view compatibly.
6. Map pixels use tile_size32; newly laid out landforms can obstruct saved coordinates. The prior release explicitly implemented escape-from-prop behavior, which must be retested.
7. Earlier v3 mission catalog status fields are outdated. Current v1.4 source and `docs/PROJECT_STATE.md` are authority; this package contains a regenerated baseline+planned manifest.

## Normal progression rewrite to implement when prerequisites exist
Astra 24 → Greenline 16 → Workshop 16 → Algorithm Tower 16 → Orion 16 → Titan 16 → Helix 16 → Aurora 16 → Mission Control finale 16. The future `Mission Control` map should be accessible as a hub but *final mission sequence* starts after Aurora; `mission_control_16` must no longer be required to enter Orion. Existing 76 missions retain IDs/completions and remain accessible to old profiles; players in an advanced world never get stranded. Until gates exist, allow existing Preview with clear labeling. A full directed-graph check in tests must prove every canonical mission reachable and no circular unlock dependencies.
