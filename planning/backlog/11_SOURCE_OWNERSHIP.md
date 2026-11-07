# Stage 11 — Source ownership and implementation seams

Only existing files below are claimed to exist. **Additive modules are proposed paths**, not already implemented. Read `docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md` before editing.

| Domain | Existing source and responsibility | Recommended additive module | Contract/test gate |
|---|---|---|---|
| Evaluation and content | `core/challenges.py; core/grade.py; core/worker.py` | `core/program_contracts.py` | adapt version 1 JSON to legacy grade; reject invalid returns; preserve original mission evaluator |
| Profile / XP | `core/progress.py` | `core/program_library.py` | atomic save, future schema no overwrite, idempotent completion |
| Robot route | `core/route.py; game/nursery.py` | `game/program_runner.py; core/action_validator.py` | bounds/collision/energy/snapshot hash; fixed tick; independent parent checks |
| Travel | `game/expedition.py; game/world.py` | `game/travel_routes.py` | gating/entry/recovery, legacy completion and preview travel |
| HUD / diagnostics | `ui/hud.py; game/diagnostics.py; ui/code_editor.py` | `ui/replay_view.py` | trace, failure UI, accessible focus, 3 resolutions |
| Environment | `game/pixel_world.py; game/planet_art.py; game/presentation.py; game/workshop_art.py` | `game/biome_layers.py` | original art, depth/collision/clear hierarchy |
| Biomedical | `game/instruments.py; core/engineering_cases.py` | `core/synthetic_pipeline.py; game/mapping_view.py` | fixtures/units/no NaN/nullable missing no clinical data |
| World state | `game/app.py; game/expedition.py` | `game/world_event_reducer.py` | single authority for state mutations and XP milestone |

**Review rule:** verify an actual file/method on the checked-out latest source before changing it; if Work has a newer tree than v1.4, refresh this matrix without rewriting existing features.
