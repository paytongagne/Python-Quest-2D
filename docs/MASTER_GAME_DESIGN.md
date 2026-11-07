# PYTHON QUEST 2D: CODE RUNNER
## Game Design Document (GDD) + Product Requirements Document (PRD)

**Status:** Build-ready blueprint v1.0 — November 5, 2026  
**Platform:** Windows 10/11 desktop first, offline-first  
**Target player:** Beginner/intermediate Python learner progressing toward real technical interviews  
**Genre:** Single-player top-down 2D exploration + practical coding puzzles  
**Design principle:** The player learns by *writing real Python*, not picking multiple-choice answers.

---

## 1. Executive vision

Python Quest 2D transforms the earlier Python Quest coding application into a genuine, explorable two-dimensional adventure. The player is a trainee engineer repairing a malfunctioning research ship and its adjoining facilities. The player moves through small handcrafted maps, explores, interacts with characters and terminals, collects rewards, and unlocks physical changes to the world by solving real Python problems.

The world should be enjoyable even between code challenges: responsive movement, appealing pixel-art direction, small secrets, sound, animated gates, collectible items, a mission log, and rewarding feedback. The coding must remain the primary cause of progress, not a detached menu.

### Outcome goals

1. Learn core Python syntax and execution semantics through deliberate repetition.
2. Write from memory, avoiding excessive reliance on autocomplete or multiple choice.
3. Develop debugging skill using real interpreter errors and failing tests.
4. Transfer to independent coding problems: collections, parsing, dictionaries, and Two Sum.
5. Reuse all 20 missions from Python Quest v1, preserving source material and test coverage.
6. Play fully offline on Windows using a simple launcher.

### Non-goals for the first shippable version

- Multiplayer, online accounts, purchases, social features, procedural open worlds.
- A fully featured IDE, AI generated lesson content, production anti-cheat, cloud sync.
- Real-time competitive combat that interrupts coding.
- Strong sandbox security against hostile, intentionally malicious Python programs.

## 2. Core player fantasy and setting

You are a new pilot-engineer assigned to the **Astra Research Facility**. A cascading software fault has shut down navigation, sensor networks, engines, and finally the central algorithm core. An onboard assistant, **PIP**, guides you through repairs. Every completed code mission activates something visible: a power grid, hatch, lift, shield, radar, drone, conveyor, or gateway. As the player becomes more capable, the facility becomes more alive.

**Tone:** Approachable sci-fi, not childish. A clean pixel-art science station, expressive characters, animated machinery, readable terminal interfaces. Technology motifs deliberately echo the player's interests in embedded telemetry and software engineering.

**Spatial model:** 2D top-down tile world with multiple rooms connected by doors. Not a platformer. Camera tracks the player within map bounds.

### Gameplay verbs

- **Move:** WASD or arrow keys.
- **Interact:** E near terminals, NPCs, doors, collectables.
- **Inspect:** Walk to data kiosks and readable signs.
- **Code:** Open a terminal overlay, type and submit Python.
- **Debug:** Read exact error messages, edit and rerun.
- **Upgrade:** Unlock zones and earn experience/collectibles.
- **Review:** Revisit completed terminals and optional spaced-repetition encounters.

## 3. The repeated gameplay loop

1. Explore a room, optionally speak with PIP or examine a machine.
2. Interact with a terminal bearing a clear visual objective.
3. See a **micro-lesson** (30–90 words), a concise example, and the actual coding assignment.
4. Write code in the integrated multi-line Python editor. Starter code scaffolds syntax but does not complete the task.
5. Run the code. A separate local Python worker runs deterministic test cases.
6. See helpful results: pass counts, expected versus actual, exceptions and tracebacks.
7. Correct your code and rerun; unlimited attempts with no health or XP loss for mistakes.
8. Passing fires a `ChallengePassed` event. The world reacts: lights return, gates unlock, PIP comments, XP is granted, and a new objective appears.
9. Optional retrieval practice revisits old concepts without blocking story progress.

Target **per-room cadence**: 20–45 seconds of movement/exploration, 1–5 minutes of coding and debugging, 10–20 seconds of rewarding world feedback. Longer algorithm bosses may take 10–20 minutes. Do not force delays or flashy cutscenes between attempts.

## 4. Player experience and UI

### Screen composition

- **Exploration:** Fullscreen-feeling viewport at 1280×720 logical resolution, resizable; tile environment, player, camera, HUD.
- **HUD:** health or energy indicator (for exploration hazards only), XP, current mission, interaction prompt.
- **Terminal overlay:** 40% instruction pane / 60% code editor split, collapsible help; game pauses while terminal is open.
- **Feedback pane:** Accessible pass/fail results under editor, never hidden behind a popup.
- **Map screen:** chapter map, visited rooms, open/locked doors; no giant quest journal required for MVP.
- **Settings:** volume, UI scale, display mode, reduced animation and text size.

### Input specification

| Action | Key |
|---|---|
| Move | WASD / arrows |
| Interact | E |
| Open mission journal | J |
| Pause / close overlay | Esc |
| Run code/tests | Ctrl+Enter |
| Save draft | Ctrl+S |
| Indent / unindent | Tab / Shift+Tab |
| Undo / redo | Ctrl+Z / Ctrl+Y |
| Copy / paste | Ctrl+C / Ctrl+V |
| Help / hint | H or visible button |

**Editor minimum bar:** Keyboard focus, multiline editing, auto-indent after `:`, four-space indent, accurate cursor, selection, scroll, copy/paste, undo/redo, clear feedback, visual line numbers, error-line highlight. The editor is a critical subsystem; if a native Pygame text editor cannot meet these requirements quickly, use a separate dedicated code editor window as an explicit temporary fallback, not a poor text box.

**Accessibility:** high contrast, text size 100/125/150%, color-independent pass/fail icons and labels, keyboard-only navigation for terminal, reduced motion, no timed coding challenges. Autosave draft on edits/debounce, and on exit.

## 5. Learning science and curriculum rules

### Teaching cadence: Observe → Attempt → Debug → Generalize → Retrieve

- **Observe:** Introduce one concrete construct and show one small example.
- **Attempt:** Require the player to type code, not select the solution.
- **Debug:** Let mistakes teach; interpreter errors are shown alongside a human-readable clue (never hide raw errors).
- **Generalize:** Tests include different inputs, boundary cases, and simple edge cases.
- **Retrieve:** Previously mastered techniques reappear in later missions and optional review terminals.

Default hints have three levels: (1) concept prompt, (2) approach outline, (3) targeted pseudocode. A final **Reveal solution** action is allowed only after an affirmative confirmation and records 'assisted completion'. The goal is mastery, not punishment.

Score: 100 XP first successful completion, 75 XP if hints used, 25 XP for solution-revealed completion, no negative points for wrong runs. **XP is awarded once per unique mission.** Gameplay coins can be earned separately; never gate essential learning behind a currency grind. Replays can train skill but do not repeatedly award campaign XP.

### Mastery classification

- `not_started`: never opened.
- `attempted`: opened or submitted without passing.
- `passed_with_help`: passed after hint/solution.
- `passed_independently`: passed without hint/solution.
- `review_due`: optional spaced review is scheduled; does not revoke a pass.

Track attempts, last submission date, and test coverage separately from XP. Suggested review cadence: next day, +3 days, +7 days, based on *last successful independent practice*. Allow dismissing review quests.

## 6. Campaign: six-zone structure

A brief orientation zone precedes the 20 old missions. All previous Python Quest v1 missions remain intact and in original sequence. Each old chapter contains four terminals; chapters should be represented as explorable spaces rather than menus.

| Zone | Missions | Core concepts | Visible payoff | Completion milestone |
|---|---:|---|---|---|
| 00 — Orientation Hangar | 4 new | print, variables, types, f-strings | boot console, pilot badge, lights, first hatch | player can type simple code |
| 01 — Launch Pad | 4 existing | functions, return, arithmetic, comparison | restore power and authorize takeoff | return a correct value |
| 02 — Control Room | 4 existing | if/elif/else, booleans, range, for loops | shield and routing controls | reason through branches and iteration |
| 03 — Sensor Bay | 4 existing | lists, averages, dictionaries, enumerate | radar and sensors come online | process collections |
| 04 — Engine Workshop | 4 existing | strings, validation, sets, telemetry parsing | restore communications and engines | parse messy real-world data |
| 05 — Algorithm Arena | 4 existing | duplicates, anagrams, hash sets, Two Sum | defeat corrupted algorithm core | O(n) hash map reasoning |

**Launch content target:** 24 missions, six connected zones. The optional long-term curriculum extends to 88 missions (24 authored + 64 planned); see `CURRICULUM_EXPANSION.md` for the staged backlog, not a release promise. **Vertical-slice target:** a playable room with movement, a terminal, working test feedback, a physical door, one NPC, and saving.

### Existing missions to import verbatim in logic

| Index | Legacy chapter | Mission |
|---|---|---|
| 01 | Launch Pad | Restore the Power |
| 02 | Launch Pad | Pilot Identification |
| 03 | Launch Pad | Thermal Conversion |
| 04 | Launch Pad | Launch Authorization |
| 05 | Control Room | Temperature Zones |
| 06 | Control Room | Raise the Shields |
| 07 | Control Room | Start the Countdown |
| 08 | Control Room | Count the Battery Drain |
| 09 | Sensor Bay | Find the Hot Sensors |
| 10 | Sensor Bay | Average the Readings |
| 11 | Sensor Bay | Status Counter |
| 12 | Sensor Bay | Locate the Target |
| 13 | Engine Workshop | Clean the Call Sign |
| 14 | Engine Workshop | Validate the Packet |
| 15 | Engine Workshop | Remove Duplicate IDs |
| 16 | Engine Workshop | Parse Live Telemetry |
| 17 | Algorithm Arena | Detect a Duplicate |
| 18 | Algorithm Arena | Check the Anagram Code |
| 19 | Algorithm Arena | Find a Pair |
| 20 | Algorithm Arena | TWO SUM: FINAL BOSS |

### New four orientation challenges

- `orientation_01` — **Wake the Console:** Write a `print()` statement that displays exactly `System online`. Teach strings and standard output.
- `orientation_02` — **Load the Battery:** Set `charge = 25`, then print the value. Teach variables and integers.
- `orientation_03` — **Read the Pilot Badge:** Use `pilot = "Alex"` in an f-string to print `Pilot: Alex`. Teach interpolation.
- `orientation_04` — **Open the Starter Gate:** With `fuel = 12`, use `if/else` to print `READY` for sufficient fuel and `WAIT` otherwise. Teach branches and comparisons.

**Important implementation requirement:** The four orientation missions use `kind: "script"` and check captured stdout and, where relevant, named variable values. The original 20 missions use `kind: "function"` and validate function calls. Work mode must implement both grading modes in the worker, without executing user code in the graphics process. The included validation script tests both modes using trusted authoring solutions.

## 7. World and level design rules

### Tile system

- Tile size: 32×32 at base pixel scale; integer or carefully rounded zoom.
- Target logical canvas: 1280×720; render at 60 FPS where hardware allows, game logic via delta time.
- Player collision: axis-aligned rectangular collision with solid tile groups; move separately on x/y axes to avoid sticking.
- World coordinate origin: top-left. Screen transform: `screen = world - camera_offset`.
- Camera: smooth following, clamped inside map limits; camera position never determines game logic.
- Terminal interaction radius: about 56 world pixels; nearest eligible interactive object takes precedence.
- Trigger zones support gates, portals, checkpoints, and cutscenes.

### Map representation

Use JSON tile grids for MVP (avoid custom editors). Each map has tile layers, collision grid, spawn points, terminals (challenge IDs), exits, persistent gate IDs, and decoration placements. Tiled TMX/JSON export can be added later. Source-of-truth challenge metadata is independent of map data.

### Visual feedback contract

When a mission passes, emit a semantic event and update world state. Example: pass `launch_01` -> generator animation plays -> light sources glow -> `gate_launch_east` opens -> PIP shows one-line feedback -> XP toast. World should not need to know lesson test implementation details.

### Hazards and combat

MVP hazards are optional and never punish code mistakes. Basic patrolling drones and safe zones may be added after the first vertical slice. Combat must not compete with retention; do not add boss combat until terminal flow, save/load, and error feedback are reliable. The Algorithm Arena final boss is primarily a multi-step coding gate with audiovisual payoff, not a reflex test.

## 8. Core systems and API contracts

### Runtime modules

| System | Responsibility | Never owns |
|---|---|---|
| `Game` | clock, scene lifecycle, frame/event loop | evaluating Python code |
| `SceneManager` | world/menu/terminal transitions | saving lesson answers |
| `World` | map objects, doors, triggers, collision | code execution |
| `Player` | position, movement, animation, collision body | challenge completion rules |
| `InteractionSystem` | E-nearest eligible object, prompts | file persistence |
| `TerminalScene` | render prompt/editor, submit/run, feedback | engine-level collision |
| `LessonRepository` | load and validate content JSON | sprites, rendering |
| `GradeService` | invoke worker, normalize results | game UI state |
| `ProgressStore` | atomic save/load, migration, schema version | executing lessons |
| `EventBus` | `ChallengePassed`, `GateUnlocked`, `XPGranted` | business calculations |

### Domain events

`TerminalOpened(challenge_id)`  
`CodeSubmitted(challenge_id, code)`  
`CodeChecked(challenge_id, result)`  
`ChallengePassed(challenge_id, assist_level)`  
`XPGranted(challenge_id, amount)`  
`WorldFlagChanged(flag, value)`  
`ZoneCompleted(zone_id)`  
`DraftSaved(challenge_id)`

Event ordering requirement: upon a passed grade, first persist completion state atomically, then apply world changes and display reward. On restart, the world reconstructs open gates from persisted flags or challenge completion, never solely from animation state.

### Challenge JSON schema

Required shared fields: `id`, `kind`, `zone`, `sequence`, `title`, `story`, `lesson`, `objective`, `sample`, `starter_code`, `hint`. For `kind: "function"`, additionally require `function_name`, `cases`. For `kind: "script"`, require `expected_stdout` and optionally `expected_variables`. Authoring-only fields: `reference_solution`, `rubric`, `optional_hints` and solutions with commentary. Each `cases` item has `args` and `expected`. All data stored as valid UTF-8 JSON. `function_name` matches callable name in starter code. `id` stable forever for saved progress.

```json
{
  "id": "launch_01",
  "kind": "function",
  "zone": "launch",
  "sequence": 1,
  "title": "Restore the Power",
  "objective": "Complete add_energy(current, pickup) to return their sum.",
  "function_name": "add_energy",
  "starter_code": "def add_energy(current, pickup):\n    pass\n",
  "cases": [
    {"args": [40, 15], "expected": 55},
    {"args": [0, 10], "expected": 10}
  ]
}
```

## 9. Python evaluator: technical and safety design

**Never run player code inside the Pygame rendering process.** The game uses a `GradeService` to launch a separate Python interpreter process. The worker receives the code, required function name and test cases as a JSON payload over stdin; it returns structured JSON results over stdout. Every run has a timeout. UI must remain responsive while grading; the main thread polls worker completion or receives it via a thread-safe queue. A run can be canceled by terminating the child process.

Illustrative call structure: `subprocess.run([sys.executable, "-I", "-S", worker_path], input=payload, capture_output=True, text=True, timeout=3, cwd=temp_directory, env=restricted_env)`. Limit source size and captured output length. Use only self-authored, local practice code. A separate process, `-I/-S`, restricted builtins, timeouts, AST checks, or Windows Job Objects **do not create a strong security sandbox**. For untrusted submissions or shared/community content, evaluate in an actual OS-isolated container/VM with tight permissions and resource controls. Offline local tests are not secret; do not implement misleading anti-cheat promises.

### Result model

```json
{
  "status": "finished",
  "passed": false,
  "passed_count": 3,
  "total_count": 4,
  "cases": [{"passed": false, "expected": "55", "actual": "54", "error": null}],
  "stdout": "",
  "duration_ms": 42
}
```

Special statuses: `syntax_error`, `runtime_error`, `timeout`, `worker_crash`, `invalid_challenge`, `canceled`. Always distinguish syntax from wrong output. Catch `KeyboardInterrupt` and errors in worker; do not crash main loop. Execution timeouts default 3 seconds for beginner tests; future algorithms may allow per-challenge overrides up to a reasonable cap.

**Test comparison:** exact type check for booleans vs integers, equality for lists and dictionaries, tolerance for numeric floats when explicitly intended. Preserve original v1 test semantics as regression tests. Cases are independent; grade all expected cases rather than stop at first fail.

### Privacy

No login, no analytics SDK, no telemetry, no external network requests. Save locally under `%LOCALAPPDATA%/PythonQuest2D/` by default. Never execute downloaded solutions or arbitrary shared challenge packages automatically.

## 10. Save system and migration

**Save schema v2**, JSON, versioned and written atomically to temporary file then renamed:

```json
{
  "schema_version": 2,
  "player": {"zone": "launch", "spawn": "door_west", "x": 96, "y": 224, "xp": 200},
  "completed": ["orientation_01", "launch_01", "launch_02"],
  "hinted": ["launch_02"],
  "revealed": [],
  "drafts": {"launch_03": "def to_fahrenheit(celsius):\n    pass\n"},
  "attempts": {"launch_01": 2},
  "world_flags": {"gate_launch_east": false},
  "review": {},
  "settings": {"music_volume": 0.5, "ui_scale": 1.0, "reduced_motion": false}
}
```

**Migration from v1:** Old save lives in `~/.python_quest_progress.json`, contains integer mission indices, `xp`, `hinted`, `revealed`, `drafts` indexed by integer string. Need map index `0..19` onto stable IDs `launch_01..algorithm_04`; preserve completed/hinted/revealed/drafts and XP, but prevent XP farming. On first launch, ask user to import; never destroy original. Write migrated new save independently. Detect corrupted JSON and offer fresh start with backup. On save revision, preserve unknown fields where practical and perform schema upgrades.

## 11. Audio, animation, and art

Art direction: crisp 16–32 px base sprites, steel/navy station surfaces, cyan navigation lighting, magenta warning states, amber collectibles. Avoid excessive neon and tiny text. Every terminal should be distinguishable by icon and nearby label, not only color.

**MVP art assets:** one 4-direction animated player, one PIP avatar, floor/wall tiles, terminal idle/success sprites, one door set open/closed, one coin/pickup, health/XP HUD icons, 6 zone palettes, win/feedback overlays. Placeholder vector/rectangular art is acceptable for vertical slice; gameplay must be correct before art polish.

Sound triggers: footstep, interact, keypress subtle, correct/fail, door activation, collectible, zone-complete cue. Volume options and mute; avoid annoying loops and high-frequency effects. All art/music must be created originally, licensed compatibly, or provided by user; attribute third-party content.

## 12. Architectural quality requirements

- Python 3.12 as default recommended development runtime; support >=3.10.
- `pygame-ce==2.5.8` for initial reproducible 2D runtime; `import pygame` remains import syntax. Upgrade after compatibility tests. Verified PyPI release August 9, 2026.
- One authoritative, version-controlled challenge registry.
- Never hard-code challenges in scene logic or coordinates in evaluation code.
- Fixed game state transitions, deterministic test fixtures, deltatime physics.
- Separate persistence domain from presentation.
- Type hints for core logic, formatted with Ruff, tested with pytest.
- No internet required at run time.
- Target fast startup, no persistent worker processes after exit, 60 FPS on ordinary laptop hardware.

### Architecture diagram

```text
                 +-------------------+
                 |   Pygame game     |
                 | input + 60fps loop|
                 +----------+--------+
                            |
             +--------------+----------------+
             |              |                |
      +------v------+ +-----v------+  +------v--------+
      | World/Player| | Terminal UI|  | Menus/HUD     |
      +------+-----+ +-----+------+  +---------------+
             |             |
             |       +-----v-------+
             |       | GradeService|------> isolated worker subprocess
             |       +-----+-------+         | tests challenge cases
             |             |                 | returns JSON results
             +------> EventBus <-------------+
                        |
                 +------v-------+
                 | ProgressStore|
                 | JSON + flags |
                 +--------------+
```

## 13. Test plan

### Unit tests

- Validate every challenge ID uniqueness, function name existence, JSON schema and test cases.
- Run all 20 legacy reference solutions successfully through the migrated grading API.
- Verify new orientation reference solutions pass tests.
- Check incorrect output, incorrect type, syntax error, exception, infinite loop timeout, missing function.
- Check gate state derivation, XP granted once, hint XP behavior, save atomicity and migration.
- Check tile collision with obstacles and map edges, camera clamp and spawn validation.

### Integration tests

- Interact with terminal -> editor opens -> code submits -> worker responds -> reward/door flags change -> save written.
- Restart game -> player position/completion/door state/draft restored.
- Keyboard navigation works with terminal and pause screens.
- Alt-tab, resize window, keyboard layouts, copy/paste, repeated rapid submissions, click outside during grading.
- Zero test cases invalid; corrupted challenge graceful failure.

### Manual acceptance checklist

- [ ] Launches from Windows double-click without command-line use after one-time install.
- [ ] Can walk around one complete explorable level at stable, smooth frame timing.
- [ ] Player cannot walk through walls, locked doors, or outside maps.
- [ ] E near terminal reliably opens readable in-game coding panel.
- [ ] Real Python is typed, executed and graded with visible failures.
- [ ] Successful submission visibly opens a gate; unlocked state remains after restart.
- [ ] Bugs/errors do not crash the game and wrong answers carry no penalty.
- [ ] Progress, drafts, settings and help usage persist.
- [ ] All 24 authored challenges pass reference solution tests.
- [ ] No network required, save path accessible, launcher starts reliably.

## 14. Development milestones and exit gates

### Phase 0: Lock product spec and asset-free prototype architecture
Deliver repo structure, JSON schemas, legacy content import, 24 authored tests, `GradeService` and test coverage. **Exit:** all legacy tests pass in core without Pygame.

### Phase 1: First playable vertical slice
One 20×15-ish tile room, smooth player movement/collision, camera, terminal interact, working editor/grading, door unlock, XP and persistent save. **Exit:** manual loop succeeds after restart, from start to unlocked door.

### Phase 2: Real game shell
Menu, pause/settings, chapter map, zone travel, PIP conversation, quest tracking, HUD, audio hooks, control remapping ideally. **Exit:** three rooms, one zone transition, no data loss.

### Phase 3: Complete curriculum campaign
All 24 missions mapped to six zones, unique world state effects, review mode, help UI, algorithm finale. **Exit:** clean profile can finish 24 missions, previous save import works.

### Phase 4: Polish and accessibility
Pixel-art pass, basic ambient animation and music, sound controls, responsive code editor UX, clear troubleshooting, keyboard accessibility. **Exit:** test against 1280×720 and common laptop screen sizes.

### Phase 5: Packaging and release
Windows launcher, isolated virtual environment or packaged executable, clean-install test, README, release notes, data backup guidance. **Exit:** user can open the game without IDE knowledge, fresh machine test.

**Scope guard:** If a milestone fails, stop adding chapters/enemies/art and fix the core game. Don't let a long list of features obscure the learning loop.

## 15. Priority table

| Must have | Should have | Could add later |
|---|---|---|
| 2D movement/collision | NPC conversations | combat/multiple enemies |
| Terminal interaction | chapter map | procedural sidequests |
| Real code editor | accessible audio | voice acting |
| Reliable grading | review scheduling | algorithm battle effects |
| Clear debugging results | unlock animation | crafting/inventory economy |
| Saved progress | legacy progress import | achievements/gallery |
| Existing 20 missions | 4 beginner missions | 100+ mission curriculum |
| Windows launcher | controller support | non-Windows builds |

## 16. Release criteria and success measures

Success is not just minutes spent playing. The game should encourage correct independent code creation.

**Functional success:** player reaches a terminal within 30 seconds; can solve a small challenge in under 3 minutes; controls are discoverable; a wrong run produces a clear corrective signal; game rewards the code action with a world change; save is reliable.

**Learning success:** more independently solved problems across sessions, faster recovery from errors, ability to write solutions on a blank editor, better performance on equivalent unseen inputs. Encourage a five-minute free-writing checkpoint after each zone.

**Long-term extension:** timed interview simulation optional (never required), spaced repetition, telemetry analysis challenges, real-world Python mini-projects, programmable drones that move based on learner-written functions, editor training exercises, project portfolio export.

## 17. Primary risks and mitigations

| Risk | Mitigation |
|---|---|
| Game is boring between tasks | small exploration rewards, visible machine effects, NPC voice, secrets; no busywork |
| Editor fights the learner | treat editor as first-class, keyboard usability test early, external-editor fallback |
| Running code freezes game | worker subprocess and async status polling, timeouts, cancellation |
| Code evaluator is unsafe | local trusted use only, explicit warning, never claim sandbox-grade security |
| Scope explodes | gated five-phase roadmap, vertical slice before assets/enemies |
| Old lessons lost | source-of-truth migration with regression tests |
| Save becomes corrupted | atomic writes, backups, schema version, migration tests |
| Challenges too easy | track independent mastery and add optional harder variations |
| AI writes all code | hints progress gradually, don't auto-fill user answers, reward independent solves |

---

**Final product principle:** When a user solves a coding problem, their Python should cause something real to happen in the world. This cause-and-effect relationship defines Python Quest 2D.
