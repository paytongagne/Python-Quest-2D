# PYTHON QUEST 2D — PREPRODUCTION BIBLE (STAGES 00–13 COMPLETE)

**Baseline:** user-supplied v1.4 Windows source (76 playable missions), 2026-11-06.

This package contains **game planning and engineering specifications**, not a playable expansion. It does not claim any of the additional 76 missions are already implemented or tested in-game.

**Start with `PROGRESS_INDEX.md`.** That file is authoritative for completed and pending preproduction stages and the exact next stage to continue.

### Completed material

- `docs/00_EXECUTIVE_DECISIONS.md`: product vision and non-negotiables.
- `docs/01_GAME_DESIGN_BIBLE.md`: player experience, learning and rewards.
- `docs/02_SOURCE_AUDIT.md`: v1.4 implementation seams and migration risks.
- `docs/03_PROGRAMMABLE_WORLD.md`: Mica plans, actions, determinism and replay.
- `docs/04_WORLD_ATLAS.md`: world identity, exploration and travel.
- `docs/05_VISUAL_AUDIO_UI.md`: original graphics and user experience.
- `docs/06_STORY_NPCS_EXPLORATION.md`: story beats and discoverable gameplay.
- `docs/07_CURRICULUM_AND_ASSESSMENT.md`: mission pedagogy and assessment.
- `docs/08_BIOMEDICAL_ENDGAME.md`: synthetic Helix/Aurora gameplay and engineering contracts.
- `missions/mission_blueprints.psv`: existing outline for 76 proposed missions (verify against implemented v1.4 IDs).
- `missions/biomed_24_contracts.csv`: 24 proposed synthetic biomedical mission contracts.
- `tests/biomed_acceptance.csv`: 96 prospective test scenarios, not live game test results.
- `engineering/08_BIOMED_CONTRACTS.json`: toy data schema, bounds and semantics.
- `reference/biomed_fixture_generator.py` and `reference/fixtures/`: versioned original synthetic samples and toy mesh.
- `tests/test_biomed_planning.py`: 7 planning-integrity checks (passed).

- `docs/11_DEVELOPMENT_SEQUENCING.md` and `backlog/11_*`: 37 dependency-validated tickets including all 76 remaining missions in 19 four-mission batches, save/rollback/QA traceability, and 12 runnable planning checks.

### Still to produce

Stages 12 and 13 are complete; see `docs/12_WORK_MODE_EXECUTION.md`, `docs/13_RISKS_AND_DECISIONS.md`, and `handoff/13_FINAL_WORK_READ_FIRST.md`. Stage 11 backlog is complete. Stages 09 and 10 are complete planning deliverables, not playable expansion features. Do not treat any uncreated paths as existing.

### Source and compatibility rules

- All original v1.4 76 mission IDs, completed flags, XP and schema-4 save records remain authoritative.
- Keep learner Python in the short-lived worker, validate JSON results in the parent, and render only canonical data. This is **not** a secure sandbox for malicious code.
- All Helix/Aurora data are original **synthetic educational** toy data, no clinical applications or proprietary implementation.
- The planned campaign target remains 152, but newly described missions are not playable until Work implements and verifies them.
- Avoid copying third-party game assets or proprietary medical software.

### Run Stage-08 planning checks

From this folder:

```bash
python -m unittest discover -s tests -p 'test_biomed_planning.py' -v
```

Passes here. It checks planning artifacts, **not** Pygame integration or Windows runtime.

## Stage 09 completion (2026-11-06)

Architecture and Data Contracts complete. See `docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md`, versioned JSON Schema, two Mermaid diagrams, source adapter matrix, error taxonomy and 21 passing Stage-09 checks. **Design only**, not deployed features. Stage 10 is complete; see its later entry.

## Stage 10 completion (2026-11-06)

Testing/performance/release planning complete. Read `docs/10_TEST_AND_RELEASE_PLAN.md` and `qa/10_ACCEPTANCE_CATALOG.csv` for 86 prospective cases, proposed measured budgets, Windows host test gates, and fault-injection/human protocols. **12 Stage-10 integrity tests pass**; static archive inspection of the v1.4 Windows ZIP passed (427 entries). Native Windows launch and gameplay playtesting were not performed during this stage. Stage 11 is complete; see its later entry.

## Stage 12 completed: Work execution handoff

Read `handoff/12_REPOSITORY_CONTEXT.md` and `handoff/12_RUNBOOK.md` first. `tools/work_ticket.py next` selects the first dependency-ready Stage11 ticket; `prompts/12_INITIAL_WORK_SESSION.md` is the ready-to-paste startup. Ticket evidence must be recorded, validated and checkpointed before completion. Model recommendations are not billing guarantees. The game is still unchanged from v1.4 and 76 planned new missions are not implemented by these planning documents. Stage 13 is complete.


## FINAL — Stage 13 complete

All 14 stages (00–13) are complete as **planning deliverables**. Read `PROGRESS_INDEX.md`, then `handoff/13_FINAL_WORK_READ_FIRST.md` and `prompts/13_FINAL_MINIMAL_STARTUP.md` for Work. This ZIP does not contain any implementation of the 76 remaining game missions.
