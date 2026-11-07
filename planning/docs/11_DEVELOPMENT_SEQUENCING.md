# 11 — Development Sequencing and Sprint Backlog

**Status: preproduction planning only.** Based on authoritative v1.4 game, 76 already playable + 76 planned = proposed total 152. Save schema 4. No new runtime game features have been implemented by this stage.

## Non-negotiable execution principle

Build **one complete, replayable and visibly reactive Python-powered encounter** before multiplying content. Every four-mission batch must have a functioning world object, true worker grading, parent validation, test fixtures, XP-safe effect, and a rollback checkpoint. Never inflate a mission count from blueprint JSON files alone. Each chapter is gated by real automated and interactive checks.

## Dependencies and development order

- Phase 0: baseline and schema guard.
- Phase 1: save-owned programs + action validator + fixed tick + Mica flagship quest.
- Phase 2: readable UI and a distinct world visual grammar; fix preview travel gating and discovery.
- Phase 3: reusable content factory and contract-driven devices.
- Phases 4–9: staged content rollout in the order below, with chapter rollback.

**The mission target is not the delivery gate.** Gate on meaningful gameplay, compatibility and testing, not a raw content count. Existing 76 IDs stay unchanged.

## Explicit stage gates

| Phase | Named gate | Objective proof | If failing |
|---|---|---|---|
| 0 | Protect baseline | Baseline SHA256; 76 IDs and XP; disposable schema2/3/4 fixtures; original ZIP | Stop batch; preserve failing trace and roll back only changed feature |
| 1 | Programmable Mica vertical slice | Flag-off legacy regressions and verified Mica plan replay with no parent-side Python execution | Stop batch; preserve failing trace and roll back only changed feature |
| 2 | Game feel, visuals and navigation | Three viewport captures per world; UI overlap log; reachable travel, entry and exits | Stop batch; preserve failing trace and roll back only changed feature |
| 3 | Reusable mission authoring and world surfaces | Four authoring templates; worker/parent boundary; no duplicate XP; synthetic fixture repeatability | Stop batch; preserve failing trace and roll back only changed feature |
| 4 | Workshop completing OOP | Workshop 09-16 source archive + restoration save + object tests | Stop batch; preserve failing trace and roll back only changed feature |
| 5 | Titan networking | Titan 05-16 source archive + deterministic packet replay | Stop batch; preserve failing trace and roll back only changed feature |
| 6 | Helix synthetic signal lab | Helix 05-16 source archive + signal fixture replay with unit labels | Stop batch; preserve failing trace and roll back only changed feature |
| 7 | Algorithm Tower | Algorithm Tower 01-16 source archive + graph optimality tests | Stop batch; preserve failing trace and roll back only changed feature |
| 8 | Aurora toy mapping | Aurora 05-16 source archive + null/unmeasured mesh tests | Stop batch; preserve failing trace and roll back only changed feature |
| 9 | Integration finale and release | Mission Control 01-16 + campaign end + native Windows release gates | Stop batch; preserve failing trace and roll back only changed feature |

## Task cards and dependency order

Each ticket below is authoritative with full detail in `backlog/11_IMPLEMENTATION_TICKETS.json` and links to Stage10 test IDs. Source files are paths **inside** project root.

### Phase 0: Protect baseline

**PQ11-001 — Establish protected source checkpoint and deterministic baseline** (S; medium risk). Depends on: baseline.

- Source: `src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py;src/python_quest_2d/core/progress.py;tests/test_flight.py;tests/test_visual_revision.py`
- Acceptance: Record source hash, 76 IDs, reference solutions, seed/profile isolation, game tests; export rollback ZIP.
- QA: PQ10-LEG-001;PQ10-LEG-002;PQ10-LEG-003;PQ10-LEG-004; gates G0/G1/G2.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-002 — Introduce contract registry validator behind opt-in feature flag** (M; medium risk). Depends on: PQ11-001.

- Source: `src/python_quest_2d/core/grade.py;src/python_quest_2d/core/worker.py;src/python_quest_2d/core/challenges.py;src/python_quest_2d/game/app.py`
- Acceptance: Versioned request/result adapters retain all legacy grading paths; invalid/oversized worker outputs fail closed.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-PRG-003;PQ10-PRG-004; gates G1.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-003 — Add additive schema-4 program library and future-schema rejection** (M; medium risk). Depends on: PQ11-001.

- Source: `src/python_quest_2d/core/progress.py;src/python_quest_2d/game/app.py`
- Acceptance: Old v2/v3/v4 fixtures preserve unknown fields; future version read-only; backup and atomic save tests.
- QA: PQ10-SAV-001;PQ10-SAV-002;PQ10-SAV-003;PQ10-SAV-004; gates G2.
- Checkpoint: source commit + disposable profile + test log.

### Phase 1: Programmable Mica vertical slice

**PQ11-004 — Observation snapshots, hashing and action semantic validation** (L; high risk). Depends on: PQ11-002, PQ11-003.

- Source: `src/python_quest_2d/core/grade.py;src/python_quest_2d/core/worker.py;src/python_quest_2d/core/challenges.py;src/python_quest_2d/game/app.py`
- Acceptance: One immutable observation produces deterministic hash; reject stale state, invalid actions, walls, energy, unsupported devices.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-PRG-003;PQ10-PRG-004; gates G1.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-005 — Bounded fixed-tick game-owned action runner and event reducer** (L; high risk). Depends on: PQ11-004.

- Source: `src/python_quest_2d/game/world.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py`
- Acceptance: No learner code in Pygame loop; trace and replay deterministic, atomic milestones, cancel/restart harmless.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-PRG-003;PQ10-PRG-004; gates G1/G2.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-006 — Mica equip, library, deploy, replay and comparison** (L; medium risk). Depends on: PQ11-005.

- Source: `src/python_quest_2d/game/nursery.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/core/route.py`
- Acceptance: Save/reopen a program, equip revision, deploy on 2 known maps, trace step, no repeated XP.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-PRG-003;PQ10-PRG-004; gates G1/G2.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-007 — In-game Mica flagship Orion quest and transfer puzzle** (L; medium risk). Depends on: PQ11-006.

- Source: `src/python_quest_2d/game/nursery.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/core/route.py`
- Acceptance: Player discovers relay, programs robot, watches repair, reuses program on altered fixture; save/quit works.
- QA: PQ10-TRV-001;PQ10-TRV-002;PQ10-TRV-003;PQ10-TRV-004; gates G1/G4.
- Checkpoint: source commit + disposable profile + test log.

### Phase 2: Game feel, visuals and navigation

**PQ11-008 — Polished HUD/readouts without map occlusion** (M; medium risk). Depends on: PQ11-001.

- Source: `src/python_quest_2d/ui/hud.py;src/python_quest_2d/ui/code_editor.py;src/python_quest_2d/game/diagnostics.py`
- Acceptance: 1280x720,1600x900,1920x1080 screenshots clear; world always primary, text/click targets visible, reduced motion.
- QA: PQ10-VIS-001;PQ10-VIS-002;PQ10-VIS-003;PQ10-VIS-004; gates G4.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-009 — Distinct original biome tile layers and consistent shadows** (L; medium risk). Depends on: PQ11-008.

- Source: `src/python_quest_2d/game/pixel_world.py;src/python_quest_2d/game/planet_art.py;src/python_quest_2d/game/presentation.py;src/python_quest_2d/game/workshop_art.py`
- Acceptance: Orion/Astra/Titan/Helix/Aurora have distinct reusable props and landmarks; depth sorts; no collisions regressed.
- QA: PQ10-VIS-001;PQ10-VIS-002;PQ10-VIS-003;PQ10-VIS-004; gates G4.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-010 — Travel and exploration narrative routing repair** (M; medium risk). Depends on: PQ11-008.

- Source: `src/python_quest_2d/game/world.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py`
- Acceptance: Normal route no longer depends on unshipped Mission Control; preview still accessible; destination reveals objectives.
- QA: PQ10-TRV-001;PQ10-TRV-002;PQ10-TRV-003;PQ10-TRV-004; gates G1/G2/G4.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-011 — Device interaction catalog and visual coding feedback** (L; medium risk). Depends on: PQ11-005, PQ11-008.

- Source: `src/python_quest_2d/game/world.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py`
- Acceptance: Machines accept validated intents; failure traces show reason; animated world delta clear and replayable.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-PRG-003;PQ10-PRG-004; gates G1/G4.
- Checkpoint: source commit + disposable profile + test log.

### Phase 3: Reusable mission authoring and world surfaces

**PQ11-012 — Shared data-driven mission factory for new challenge types** (L; medium risk). Depends on: PQ11-002, PQ11-005.

- Source: `src/python_quest_2d/core/grade.py;src/python_quest_2d/core/worker.py;src/python_quest_2d/core/challenges.py;src/python_quest_2d/game/app.py`
- Acceptance: Four mission templates tested: function, object fixture, simulation, bounded plan; authoring round-trip.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-PRG-003;PQ10-PRG-004; gates G1.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-013 — Chapter maps, travel gating and landmark objective system** (L; medium risk). Depends on: PQ11-010, PQ11-012.

- Source: `src/python_quest_2d/game/world.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py`
- Acceptance: Each world has arrival, return, discoverable next objective, walkable route and locked feedback.
- QA: PQ10-TRV-001;PQ10-TRV-002;PQ10-TRV-003;PQ10-TRV-004; gates G1/G4.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-014 — Deterministic toy signal and mesh rendering adapter** (L; medium risk). Depends on: PQ11-002, PQ11-011.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/helix_bio.json`
- Acceptance: Synthetic fixtures load, null unmeasured, no NaN, units labelled, geometry responds to test outputs.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-BIO-003;PQ10-BIO-004; gates G1/G4.
- Checkpoint: source commit + disposable profile + test log.

### Phase 4: Workshop completing OOP

**PQ11-015 — Visual debugging playback, code editor hint ladder and error precision** (M; medium risk). Depends on: PQ11-006, PQ11-008.

- Source: `src/python_quest_2d/ui/hud.py;src/python_quest_2d/ui/code_editor.py;src/python_quest_2d/game/diagnostics.py`
- Acceptance: Step-through trace with earliest failure; drafts preserved; review and comparison work; no unrelated editor regressions.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-WRK-003;PQ10-WRK-004; gates G1/G4.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-101 — Workshop District missions 09–12** (M; medium risk). Depends on: PQ11-012, PQ11-013.

Planned missions: workshop_09, workshop_10, workshop_11, workshop_12.

- Source: `src/python_quest_2d/core/object_cases.py;src/python_quest_2d/game/workshop_art.py;content/planets/workshop.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement workshop_09, workshop_10, workshop_11, workshop_12 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible Astra workshop production line effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-SAV-001;PQ10-SAV-002;PQ10-VIS-001;PQ10-VIS-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-101 + verified 4-mission results + source archive at chapter boundary.

**PQ11-105 — Workshop District missions 13–16** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-101.

Planned missions: workshop_13, workshop_14, workshop_15, workshop_16.

- Source: `src/python_quest_2d/core/object_cases.py;src/python_quest_2d/game/workshop_art.py;content/planets/workshop.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement workshop_13, workshop_14, workshop_15, workshop_16 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible Astra workshop production line effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-SAV-001;PQ10-SAV-002;PQ10-VIS-001;PQ10-VIS-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-105 + verified 4-mission results + source archive at chapter boundary.

### Phase 5: Titan networking

**PQ11-109 — Titan Cloudworks missions 05–08** (M; medium risk). Depends on: PQ11-011, PQ11-012, PQ11-013.

Planned missions: titan_cloud_05, titan_cloud_06, titan_cloud_07, titan_cloud_08.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/titan_cloud.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement titan_cloud_05, titan_cloud_06, titan_cloud_07, titan_cloud_08 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible pulsing packet network and relay devices effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-109 + verified 4-mission results + source archive at chapter boundary.

**PQ11-113 — Titan Cloudworks missions 09–12** (M; medium risk). Depends on: PQ11-011, PQ11-012, PQ11-013, PQ11-109.

Planned missions: titan_cloud_09, titan_cloud_10, titan_cloud_11, titan_cloud_12.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/titan_cloud.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement titan_cloud_09, titan_cloud_10, titan_cloud_11, titan_cloud_12 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible pulsing packet network and relay devices effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-113 + verified 4-mission results + source archive at chapter boundary.

**PQ11-117 — Titan Cloudworks missions 13–16** (M; medium risk). Depends on: PQ11-011, PQ11-012, PQ11-013, PQ11-113.

Planned missions: titan_cloud_13, titan_cloud_14, titan_cloud_15, titan_cloud_16.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/titan_cloud.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement titan_cloud_13, titan_cloud_14, titan_cloud_15, titan_cloud_16 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible pulsing packet network and relay devices effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-117 + verified 4-mission results + source archive at chapter boundary.

### Phase 6: Helix synthetic signal lab

**PQ11-121 — Helix Biomedical missions 05–08** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-014.

Planned missions: helix_bio_05, helix_bio_06, helix_bio_07, helix_bio_08.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/helix_bio.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement helix_bio_05, helix_bio_06, helix_bio_07, helix_bio_08 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible synthetic signal monitor and pump recovery effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-121 + verified 4-mission results + source archive at chapter boundary.

**PQ11-125 — Helix Biomedical missions 09–12** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-014, PQ11-121.

Planned missions: helix_bio_09, helix_bio_10, helix_bio_11, helix_bio_12.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/helix_bio.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement helix_bio_09, helix_bio_10, helix_bio_11, helix_bio_12 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible synthetic signal monitor and pump recovery effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-125 + verified 4-mission results + source archive at chapter boundary.

**PQ11-129 — Helix Biomedical missions 13–16** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-014, PQ11-125.

Planned missions: helix_bio_13, helix_bio_14, helix_bio_15, helix_bio_16.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/helix_bio.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement helix_bio_13, helix_bio_14, helix_bio_15, helix_bio_16 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible synthetic signal monitor and pump recovery effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-129 + verified 4-mission results + source archive at chapter boundary.

### Phase 7: Algorithm Tower

**PQ11-133 — Algorithm Tower missions 01–04** (M; medium risk). Depends on: PQ11-012, PQ11-013.

Planned missions: algorithm_tower_01, algorithm_tower_02, algorithm_tower_03, algorithm_tower_04.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/world.py;content/maps/algorithm.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement algorithm_tower_01, algorithm_tower_02, algorithm_tower_03, algorithm_tower_04 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible tower simulation boards and routing panels effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-PRG-001;PQ10-PRG-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-133 + verified 4-mission results + source archive at chapter boundary.

**PQ11-137 — Algorithm Tower missions 05–08** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-133.

Planned missions: algorithm_tower_05, algorithm_tower_06, algorithm_tower_07, algorithm_tower_08.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/world.py;content/maps/algorithm.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement algorithm_tower_05, algorithm_tower_06, algorithm_tower_07, algorithm_tower_08 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible tower simulation boards and routing panels effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-PRG-001;PQ10-PRG-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-137 + verified 4-mission results + source archive at chapter boundary.

**PQ11-141 — Algorithm Tower missions 09–12** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-137.

Planned missions: algorithm_tower_09, algorithm_tower_10, algorithm_tower_11, algorithm_tower_12.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/world.py;content/maps/algorithm.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement algorithm_tower_09, algorithm_tower_10, algorithm_tower_11, algorithm_tower_12 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible tower simulation boards and routing panels effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-PRG-001;PQ10-PRG-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-141 + verified 4-mission results + source archive at chapter boundary.

**PQ11-145 — Algorithm Tower missions 13–16** (M; medium risk). Depends on: PQ11-012, PQ11-013, PQ11-141.

Planned missions: algorithm_tower_13, algorithm_tower_14, algorithm_tower_15, algorithm_tower_16.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/world.py;content/maps/algorithm.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement algorithm_tower_13, algorithm_tower_14, algorithm_tower_15, algorithm_tower_16 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible tower simulation boards and routing panels effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-WRK-001;PQ10-WRK-002;PQ10-PRG-001;PQ10-PRG-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-145 + verified 4-mission results + source archive at chapter boundary.

### Phase 8: Aurora toy mapping

**PQ11-149 — Aurora Observatory missions 05–08** (M; high risk). Depends on: PQ11-012, PQ11-013, PQ11-014.

Planned missions: aurora_ep_05, aurora_ep_06, aurora_ep_07, aurora_ep_08.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/aurora_ep.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement aurora_ep_05, aurora_ep_06, aurora_ep_07, aurora_ep_08 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible chamber mesh layers and mapping consoles effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-149 + verified 4-mission results + source archive at chapter boundary.

**PQ11-153 — Aurora Observatory missions 09–12** (M; high risk). Depends on: PQ11-012, PQ11-013, PQ11-014, PQ11-149.

Planned missions: aurora_ep_09, aurora_ep_10, aurora_ep_11, aurora_ep_12.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/aurora_ep.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement aurora_ep_09, aurora_ep_10, aurora_ep_11, aurora_ep_12 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible chamber mesh layers and mapping consoles effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-153 + verified 4-mission results + source archive at chapter boundary.

**PQ11-157 — Aurora Observatory missions 13–16** (M; high risk). Depends on: PQ11-012, PQ11-013, PQ11-014, PQ11-153.

Planned missions: aurora_ep_13, aurora_ep_14, aurora_ep_15, aurora_ep_16.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/aurora_ep.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement aurora_ep_13, aurora_ep_14, aurora_ep_15, aurora_ep_16 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible chamber mesh layers and mapping consoles effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-BIO-001;PQ10-BIO-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-VIS-001;PQ10-VIS-002;PQ10-SAV-001;PQ10-SAV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-157 + verified 4-mission results + source archive at chapter boundary.

### Phase 9: Integration finale and release

**PQ11-016 — Windows release, native QA, test evidence and recovery exports** (M; high risk). Depends on: PQ11-018, PQ11-105, PQ11-117, PQ11-129, PQ11-145, PQ11-157, PQ11-173.

- Source: `src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py;src/python_quest_2d/core/progress.py;tests/test_flight.py;tests/test_visual_revision.py`
- Acceptance: Archive/static and Windows native start/saves/path spaces/offline/3 viewport captures; source ZIP + changelog.
- QA: PQ10-WIN-001;PQ10-WIN-002;PQ10-WIN-003;PQ10-WIN-004; gates G0/G1/G2/G3/G4/G6.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-161 — Mission Control Annex missions 01–04** (M; high risk). Depends on: PQ11-011, PQ11-012, PQ11-013, PQ11-105, PQ11-117, PQ11-129, PQ11-145, PQ11-157.

Planned missions: mission_control_01, mission_control_02, mission_control_03, mission_control_04.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/expedition.py;content/universe/destinations.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement mission_control_01, mission_control_02, mission_control_03, mission_control_04 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible multi-world systems and staged final boss effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-SAV-001;PQ10-SAV-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-161 + verified 4-mission results + source archive at chapter boundary.

**PQ11-165 — Mission Control Annex missions 05–08** (M; high risk). Depends on: PQ11-011, PQ11-012, PQ11-013, PQ11-161.

Planned missions: mission_control_05, mission_control_06, mission_control_07, mission_control_08.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/expedition.py;content/universe/destinations.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement mission_control_05, mission_control_06, mission_control_07, mission_control_08 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible multi-world systems and staged final boss effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-SAV-001;PQ10-SAV-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-165 + verified 4-mission results + source archive at chapter boundary.

**PQ11-169 — Mission Control Annex missions 09–12** (M; high risk). Depends on: PQ11-011, PQ11-012, PQ11-013, PQ11-165.

Planned missions: mission_control_09, mission_control_10, mission_control_11, mission_control_12.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/expedition.py;content/universe/destinations.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement mission_control_09, mission_control_10, mission_control_11, mission_control_12 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible multi-world systems and staged final boss effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-SAV-001;PQ10-SAV-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-169 + verified 4-mission results + source archive at chapter boundary.

**PQ11-173 — Mission Control Annex missions 13–16** (M; high risk). Depends on: PQ11-011, PQ11-012, PQ11-013, PQ11-169.

Planned missions: mission_control_13, mission_control_14, mission_control_15, mission_control_16.

- Source: `src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/expedition.py;content/universe/destinations.json;src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py`
- Acceptance: Implement mission_control_13, mission_control_14, mission_control_15, mission_control_16 using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible multi-world systems and staged final boss effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass.
- QA: PQ10-PRG-001;PQ10-PRG-002;PQ10-WRK-001;PQ10-WRK-002;PQ10-SAV-001;PQ10-SAV-002;PQ10-TRV-001;PQ10-TRV-002; gates G1/G2/G4.
- Checkpoint: commit PQ11-173 + verified 4-mission results + source archive at chapter boundary.

**PQ11-017 — Unified multi-world postgame and mastery transfer challenges** (L; medium risk). Depends on: PQ11-105, PQ11-117, PQ11-129, PQ11-145, PQ11-157, PQ11-173.

- Source: `src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py`
- Acceptance: All chapters accessible in intended narrative order, preview travel safe, program library reusable in two more worlds, mastery review without XP farming.
- QA: PQ10-TRV-001;PQ10-TRV-002;PQ10-TRV-003;PQ10-TRV-004; gates G1/G2/G4.
- Checkpoint: source commit + disposable profile + test log.

**PQ11-018 — Human playtest triage, accessibility and final performance budget** (M; high risk). Depends on: PQ11-008, PQ11-009, PQ11-017.

- Source: `src/python_quest_2d/ui/hud.py;src/python_quest_2d/ui/code_editor.py;src/python_quest_2d/game/diagnostics.py`
- Acceptance: Record actual novice/returning-player observations; demonstrate no critical overlap, softlocks and unresolved P0; measured p95 FPS on stated hardware.
- QA: PQ10-HUM-001;PQ10-HUM-002;PQ10-HUM-003;PQ10-HUM-004;PQ10-PERF-001;PQ10-PERF-002;PQ10-PERF-003;PQ10-PERF-004; gates G4/G5.
- Checkpoint: source commit + disposable profile + test log.

## Mission-by-mission traceability

`backlog/11_MISSION_TO_TICKET.csv` is the machine-readable authoritative join of every proposed mission to its four-mission ticket, API, Python concept, world effect, cases, source seam and Stage10 references. All 76 rows have unique stable IDs. This does **not** imply those IDs exist in the game yet. Use `missions/mission_blueprints.psv` for detailed learning task wording and `missions/biomed_24_contracts.csv` for clarified Helix/Aurora signatures where they conflict.

## Ticket definition of done

1. Implement real learner-authorable Python challenge; run reference solution on all visible and hidden tests.
2. Show a failure test and ensure no XP/state mutation on invalid response.
3. Validate result plain data in *game process* against a fresh snapshot and state machine.
4. Demonstrate a world-visible effect with replay and accurate error feedback.
5. Save then restart on disposable profile, verify no replay XP and preservation of unrelated flags.
6. Run relevant Stage10 IDs and existing regression subset; note **unexecuted** checks explicitly.
7. Commit + source archive and update `PROJECT_STATE.md` with exact mission count, changed paths and known issues.
8. Do not repackage full Windows runtime on every four missions; package at chapter or major playable milestone, plus final release.

## Defer without hiding

- Physically based 3D and Qt/real hardware medical device connectivity: out of scope; Pygame synthetic toy mapping only.
- Multiplayer, cloud saves, online leaderboards, unrestricted code mods: out of scope.
- Native Windows launch, audio and human UX proof: not verifiable by design documents; defer to execution platform.
- If a full chapter becomes infeasible, ship last validated four-mission slice and accurate incomplete status, not placeholder missions counted as complete.

## Precise failure response and fallback

- Worker timeout/exception/unexpected JSON: diagnostic + no state mutation; save draft; offer retry.
- Stale program/world hash: reject deployment + request revalidation; keep verified program revision and draft.
- Crashed/restarted deployment: resume last *atomic* committed world checkpoint; do not reaward XP.
- Missing or future schema: quarantine or read-only; back up before migration; never destroy unknown fields.
- World route locked: explanatory tooltip and reachable safe return, not hard block or silent teleport.
- Visual regression: stop when UI occlusion blocks movement/interactions at any target viewport; preserve last passing visuals.

## Measurement and evidence

Each sprint records git/source hash; test command and counts; screenshot/trace evidence; saved profile test path; performance samples if taken; before/after mission IDs; latest release gate status (G0–G6). No tests in this planning stage prove the future missions are playable.
