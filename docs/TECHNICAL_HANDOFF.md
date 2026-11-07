# TECHNICAL HANDOFF / CONTRACTS

## Runtime and dependency choices

- Windows 10/11, Python 3.12 recommended (>=3.10), `pygame-ce==2.5.8` initial pinned version.
- Import name remains `pygame` for pygame-ce.
- Plain JSON maps/challenges first; `pytest` for tests; Python `subprocess`, `threading`, `queue`, `pathlib`, `json` standard library.
- No cloud infrastructure. No database requirement in MVP.

## Source tree contract

```text
Python_Quest_2D/
├── README.md
├── pyproject.toml
├── requirements.txt
├── START_PYTHON_QUEST_2D.bat
├── docs/
│   ├── MASTER_GAME_DESIGN.md
│   ├── TECHNICAL_HANDOFF.md
│   ├── ACCEPTANCE_AND_TASKS.md
│   └── WORK_MODE_HANDOFF.md
├── assets/
│   ├── characters/
│   ├── tiles/
│   ├── ui/
│   └── audio/
├── content/
│   ├── challenges/                # gameplay-facing JSON, stable IDs
│   ├── authoring/                 # reference solutions, not in runtime imports
│   └── maps/                      # zone tile maps and interactive objects
├── src/python_quest_2d/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── player.py
│   │   ├── world.py
│   │   ├── camera.py
│   │   ├── collision.py
│   │   ├── interactions.py
│   │   ├── scene_manager.py
│   │   ├── events.py
│   │   └── hud.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── terminal.py
│   │   ├── code_editor.py
│   │   ├── test_feedback.py
│   │   ├── menu.py
│   │   └── settings.py
│   └── core/
│       ├── __init__.py
│       ├── challenges.py
│       ├── grade.py
│       ├── worker.py
│       ├── progress.py
│       ├── progression.py
│       └── legacy_migration.py
├── tests/
│   ├── test_content.py
│   ├── test_grader.py
│   ├── test_progress.py
│   ├── test_progression.py
│   ├── test_maps.py
│   └── test_migration.py
└── tools/
    └── export_legacy_lessons.py
```

**The ZIP in this handoff is a blueprint/scaffold, not a finished playable game.** Modules under `game` and `ui` become fully implemented in Work mode. Core lesson data and authoring solution fixtures are present to eliminate content transcription.

## Example challenge-to-world binding

`content/challenges/launch_01.json` is independent of scene coordinates. Map references `challenge_id: "launch_01"`, `object_id: "terminal_power"`, and `unlocks_flag: "gate_launch_east"`. On pass, update progress first, then apply `gate_launch_east` to the current world. Completion check relies on persistent challenge ID.

## World map schema example

```json
{
  "id": "launch",
  "tile_size": 32,
  "width": 20,
  "height": 15,
  "tiles": ["####################", "#..................#"],
  "spawn": {"x": 64, "y": 64},
  "interactables": [
    {"id": "terminal_power", "type": "terminal", "x": 192, "y": 160, "challenge_id": "launch_01"}
  ],
  "gates": [
    {"id": "gate_launch_east", "x": 576, "y": 224, "requires_challenge": "launch_01"}
  ]
}
```

Tile row count and width must equal `height` and `width` respectively; example is illustrative and not the complete file.

## Code grading API

`grade(challenge: Challenge, user_code: str, timeout_s=3.0) -> GradeResult`

The game passes a challenge with stable ID and kind. Function tasks carry function name and cases; script tasks carry expected stdout and optionally named variables. Result contains status and per-case expected/actual/error. A worker uses a separate process; limit result output size. Never test using `eval`/`exec` in game process. Main thread never blocks on grade.

## Save API

`load_progress() -> Progress`  
`save_progress_atomic(progress: Progress) -> None`  
`award_completion(progress, challenge_id, assist_level) -> bool`  
`import_legacy_progress(old_path, new_path, approved_by_user=True) -> MigrationReport`

## First manual integration scenario

1. Start fresh, spawn at orientation hangar.
2. Walk to first terminal; inspect task; submit incorrect code.
3. Display failing test with expected and actual, no crash.
4. Replace code with reference solution, submit; `passed` state persists, XP once.
5. Door opens; walk through and trigger zone transition.
6. Quit and relaunch; same terminal is complete and door stays open.
7. Reset progress and verify clean start.
