# Python Quest 2D — Master preproduction progress index

**Last updated:** 2026-11-06 (Stage 13 final). **Design baseline:** v1.4 Windows source (76 implemented missions, schema-4 saves). **Remaining planned runtime missions:** 76. This index tracks **preproduction deliverables**, not shipped gameplay. Do not use counts in this file as claims about current Work source beyond v1.4.

## Stage status and authoritative files

| Stage | Focus | Status | Deliverable | Evidence/next criterion |
|---|---|---|---|---|
| 00 | Executive direction | COMPLETE | `docs/00_EXECUTIVE_DECISIONS.md` | pillars, exclusions, baseline and compatibility locked |
| 01 | Complete game experience | COMPLETE | `docs/01_GAME_DESIGN_BIBLE.md` | core loop, player abilities, rewards, success criteria |
| 02 | v1.4 source architecture audit | COMPLETE | `docs/02_SOURCE_AUDIT.md` | identified real code seams, save and grader behavior |
| 03 | Programmable world and Mica | COMPLETE | `docs/03_PROGRAMMABLE_WORLD.md` | worker/parent contract, deterministic plans, replay |
| 04 | World atlas and navigation | COMPLETE | `docs/04_WORLD_ATLAS.md` | distinct world verbs, landmark layouts and travel |
| 05 | Visual/audio/UI art direction | COMPLETE | `docs/05_VISUAL_AUDIO_UI.md` | layer rules, visuals, UX and accessibility |
| 06 | Story, NPCs and exploration | COMPLETE | `docs/06_STORY_NPCS_EXPLORATION.md` | narrative beats, secrets, objectives and NPC roles |
| 07 | Curriculum and assessment | COMPLETE | `docs/07_CURRICULUM_AND_ASSESSMENT.md` | 76-mission skill progression and grading philosophy |
| **08** | **Biomedical endgame (Helix/Aurora)** | **COMPLETE** | **`docs/08_BIOMEDICAL_ENDGAME.md`** | **24 contracts, 96 acceptance cases, 3 reproducible fixtures, 7 integrity tests passed** |
| **09** | **Architecture and data contracts** | **COMPLETE** | **`docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md`** | **13 schemas, 13 valid and 12 invalid examples, 5 state machines, 12 adapters, 2 diagrams, 21 Stage-09 checks passed** |
| **10** | **Test, performance and release** | **COMPLETE** | **`docs/10_TEST_AND_RELEASE_PLAN.md`** | **86 planned acceptance checks, 12 Stage-10 integrity checks passed; v1.4 Windows ZIP passed 427-member static audit (not native launch)** |
| **11** | **Development sequencing and sprint backlog** | **COMPLETE** | **`docs/11_DEVELOPMENT_SEQUENCING.md`** | **37 source-linked tickets, 19 four-mission batches/76 mission rows, 224 QA traceability links, 12 Stage11 checks passed** |
| **12** | **Work execution handoff** | **COMPLETE** | **`docs/12_WORK_MODE_EXECUTION.md`** | **compact runbook, model assignments, 5 prompts, 37-ticket selector/state/evidence workflow; 17 Stage12 checks passed** |
| **13** | **Risks, design decisions, readiness** | **COMPLETE** | **`docs/13_RISKS_AND_DECISIONS.md`** | **16 prioritized risks, 14 binding decisions, source-linked final audit, conditional go for implementation; 12 Stage13 tests passed** |

**Stage 09 reconciliation update (supersedes earlier caution):** The source-linked Stage09 architecture and 13 schema registry are complete; they remain design-only until Work implements their adapters. Stage13 audit is authoritative when earlier notes conflict.

## Stage 08 delivery inventory

- `docs/08_BIOMEDICAL_ENDGAME.md`: mission-by-mission Helix/Aurora, synthetic signal/map systems, gameplay, architecture boundary, math, UX, accessibility, save/replay, player scenarios and release gates.
- `missions/biomed_24_contracts.csv`: 24 design-only mission contracts (Helix 05–16, Aurora 05–16), including clarified signatures and world effects.
- `tests/biomed_acceptance.csv`: 96 planned positive/edge/integration/save cases, four per mission; these are **not yet runtime tests**.
- `engineering/08_BIOMED_CONTRACTS.json`: machine-readable synthetic schema and computation rules, design only.
- `reference/biomed_fixture_generator.py` plus `reference/fixtures/{helix_clean,helix_faults,aurora_toy_chamber}.json`: deterministic, original toy fixtures.
- `tests/test_biomed_planning.py`: 7 runnable stdlib unittest cases, verifying artifacts, IDs, schemas and deterministic regeneration.
- `tools/build_biomed_stage.py`: reconstructs mission and acceptance catalogs from the existing outlined mission rows.

### Independent check completed for this stage

`python -m unittest discover -s tests -p 'test_biomed_planning.py' -v` → **7 tests passed**. These tests verify **design data integrity**, not actual game simulation, medical correctness or GUI performance. No runtime missions were added by this stage.

### Corrections to earlier rough outline

1. `aurora_ep_10` gains `vertex_count` argument so isolated vertices are representable. Proposed signature in `biomed_24_contracts.csv`; not a change to shipped missions.
2. `aurora_ep_11` returns nullable vertex colors to distinguish no measurement from measured zero; not a change to shipped missions.
3. Fixed timing and queue semantics explicitly to avoid flaky concurrency tests or fabricated overflow conditions.
4. 3D view remains optional in-game Pygame UI; do **not** add Qt as game dependency without separate integration review.

## Stage 09 delivery inventory (COMPLETE)

- `docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md`: full source-specific architecture, 13 contract definitions, worker-to-game split, migration/rollback, error taxonomy, lifecycle sequencing, security limitations and implementation gates.
- `engineering/09_CONTRACT_REGISTRY.json`: authoritative 13-schema versions, size/action limits, source seams and protected profile fields.
- `engineering/schemas/*.schema.json`: JSON Schema 2020-12, with 13 matching positive and 12 expected-negative examples in `engineering/examples/`.
- `engineering/09_STATE_MACHINES.json`: five lifecycle machines for evaluation, deployment, travel, device and profile.
- `engineering/09_SOURCE_ADAPTERS.csv`: 12 concrete v1.4 code-to-contract adapters.
- `engineering/09_SAVE_COMPATIBILITY_MATRIX.csv`: v2/v3/v4 preservation, future-version guard, event replay and duplicate-XP tests.
- `engineering/09_ARCHITECTURE.mmd` and `engineering/09_DEPLOYMENT_SEQUENCE.mmd`: editable architecture and deployment sequence diagrams.
- `engineering/09_ERROR_TAXONOMY.json`: machine-readable error handling and nonmutating rejection guarantees.
- `reference/contracts_v1.py`: pure reference JSON guard, hashing, legacy normalization, robot-plan validation and additive save view (design-only).
- `tests/test_stage09_contracts.py`, `test_stage09_source_integration.py`, `test_stage09_documentation.py`: schema examples, source integration and documentation integrity tests.
- `tools/build_stage09_schemas.py`: original reproducible schema/example generator, retained for future edits.

### Independent check completed for Stage 09

`PYTHONQUEST_V14_ROOT=/mnt/data/pq_stage09_source python -m unittest discover -s tests -p 'test_stage09_*.py' -v` from the Bible root → **21 tests passed (0 skipped)**, including an actual v1.4 worker path and disposable legacy save migration checks. **These tests validate architecture planning and selected v1.4 behavior, not newly implemented world features.** The stage-08 7-test suite remains available and was not modified.

### Stage 09 changes since the interruption checkpoint

Written and saved the full narrative architecture, two editable diagrams, 18-error taxonomy, and cross-artifact tests. The `Stage09_IN_PROGRESS_Checkpoint.zip` is retained as a recovery archive; the current authoritative package is `Python_Quest_2D_Preproduction_Bible_Stages_00-09.zip`.

## Stage 10 delivery inventory (COMPLETE)

- `docs/10_TEST_AND_RELEASE_PLAN.md`: source-linked test layers, gate policy, regression flow, performance methodology, migration and Windows acceptance.
- `qa/10_ACCEPTANCE_CATALOG.csv`: **86 named verification cases** across LEG/WRK/TRV/SAV/PRG/DEV/BIO/VIS/PERF/WIN/HUM/SEC, with unique IDs, expected result, code anchor, severity, and evidence status. This is a planned catalog, not 86 already executed game tests.
- `qa/10_PERFORMANCE_BUDGETS.json`: eight **proposed** measurable targets, hardware assumptions and fallback actions; not achieved metrics.
- `qa/10_FAULT_INJECTION.md`: 13 fault classes and crash/resume criteria using temporary profiles.
- `qa/10_HUMAN_PLAYTEST_PROTOCOL.md`: novice, intermediate and returning player sessions, accessibility passes, and behavioral observation metrics. Human sessions are outstanding.
- `qa/10_CI_MATRIX.md`: host-specific reproducible commands, with explicit coverage limitations.
- `release/10_RELEASE_GATES.json`: seven release gates, hard/soft rules and stop-ship cases.
- `tools/verify_windows_archive.py`: self-contained static ZIP path/symlink/credential/CRC/required-path audit. Does **not** execute Windows code.
- `tools/frame_budget_report.py`: frame timing percentile analysis of **supplied** samples; not a profiler or actual measurement.
- `tests/test_stage10_planning.py`: **12 passing integrity tests** verifying these materials and synthetic auditor behavior.
- `release/10_V14_STATIC_AUDIT.json`: read-only static audit of original uploaded v1.4 Windows ZIP: 427 members, all CRCs valid, required paths present, no listed structural/security issues. **No native Windows launch was performed.**
- `release/10_TEST_RUN_RECORD.md`: commands, outcomes, environment and known untested work.

### Stage 10 independent verification (2026-11-06)

- Stage08: **7/7** planning checks PASS.
- Stage09: **21/21** architecture/source-integration checks PASS, with `PYTHONQUEST_V14_ROOT=/mnt/data/pq_stage09_source`.
- Stage10: **12/12** integrity checks PASS.
- v1.4 release ZIP: **static structure and CRC audit PASS** (427 entries); **Windows native launch: BLOCKED** because this environment is Linux, **headless Pygame gameplay suite: BLOCKED** because `pygame-ce` is not installed here; human playtesting NOT RUN. These are release requirements for implementation Work, not evidence to assume.

## Stage 11 delivery inventory (COMPLETE)

- `docs/11_DEVELOPMENT_SEQUENCING.md`: full implementation order with source ownership, gates, ticket acceptance and recovery strategy.
- `backlog/11_IMPLEMENTATION_TICKETS.json` and `.csv`: **37 planned implementation tickets**, including 18 platform/experience/release tickets and **19 four-mission batches**. Dependencies form a verified acyclic graph.
- `backlog/11_MISSION_TO_TICKET.csv`: **76 unique new-mission rows** linked to Python API, world effect, edge cases, development ticket and Stage10 tests. These are NOT implemented missions.
- `backlog/11_TICKET_QA_TRACEABILITY.csv`: **224 traceability links** between tickets and existing Stage10 acceptance cases.
- `backlog/11_CHECKPOINT_AND_ROLLBACK.json`: 10 phase checkpoints, stop-ship policy, safe rollbacks and required recovery artifacts.
- `backlog/11_SOURCE_OWNERSHIP.md`: source-verified anchor paths and clearly marked proposed additive modules.
- `tests/test_stage11_planning.py`: 12 passing integrity and source-anchor tests.
- `/mnt/data/build_pq_stage11.py` is the local build generator; exported `tools/build_stage11_backlog.py` is a copy of it for reproducibility in this Bible.

### Stage 11 verification (2026-11-06)

- **52/52 planning and selected v1.4 source-integration tests passed** across Stages 08–11 (7+21+12+12).
- All 76 mission rows unique and assigned to exactly one batch; ticket graph acyclic; references point to real source files in the extracted v1.4 source; QA IDs reference the 86 Stage10 acceptance catalog cases.
- v1.4 game source **not modified**. Future gameplay, native Windows operation and human playtesting **not executed** by Stage11.

## Stage 12 delivery inventory (COMPLETE)

- `docs/12_WORK_MODE_EXECUTION.md`: exact source reading order; bounded ticket loop, release gates, save/worker invariants, resource-efficient development, model assignment and release reporting.
- `handoff/12_REPOSITORY_CONTEXT.md` and `12_RUNBOOK.md`: compact startup guide, exact baseline and checkpoint instructions.
- `handoff/12_TASK_STATE.json`: initial machine-readable state for all 37 Stage11 tickets. **All status PLANNED, none marked implemented**; first dependency-eligible ticket PQ11-001.
- `handoff/12_MODEL_ASSIGNMENTS.json`, `12_SOURCE_READING_ORDER.json`, `12_HANDOFF_MANIFEST.json` and `12_EVIDENCE_TEMPLATE.json`: machine-readable model/effort guidance, scope and verification records.
- `prompts/12_INITIAL_WORK_SESSION.md`, `12_BOUNDED_TICKET.md`, `12_RECOVERY.md`, `12_RELEASE.md`, `12_OVERNIGHT.md`: five reusable prompts covering first Work session, bounded work, interrupted session, native release and extended resource-efficient session.
- `tools/work_ticket.py`: stdlib CLI (`next`, `brief`, `status`, `start`, `fail`, `retry`, `block`, `done`), dependency-enforced selection, atomic state writes and structural evidence checking. Does **not** independently validate that reported tests actually ran.
- `tests/test_stage12_handoff.py`: 17 new runnable planning/CLI tests; ensures ID, dependency, Stage10 QA/gate, negative evidence and retry behavior.
- `release/12_HANDOFF_TEST_RECORD.md`: exact commands and scope/host limitations.

### Stage 12 verification (2026-11-06)

**69/69 planned-document and selected v1.4 source-integration tests passed**: Stage08=7; Stage09=21; Stage10=12; Stage11=12; Stage12=17. Source-linked Stage09/11 tests used the fully extracted v1.4 ZIP with `PYTHONQUEST_V14_ROOT` and `PQ11_SOURCE_ROOT`; an earlier attempt against an incomplete extract failed, corrected before final verification. No new gameplay, native Windows launch or human playtesting is claimed.

The Work handoff has **not** yet been executed, and the model assignments are conditional on the actual model picker and account allowances. Do not auto-redeem resets or buy credits. Save a source checkpoint before risky edits or usage limits.

## NEXT continuation instruction

**Stage 13: Final Risks, Decisions, and Readiness Review.** Using completed Stages 00–12, perform an independent cross-stage reconciliation, identify contradictory contracts and unsupported assumptions, prioritize risks, produce go/no-go criteria for the first Work implementation batch, confirm stage completeness with tested manifests and source IDs, and create one final minimal startup prompt. Update the index and complete/stage ZIPs. **Do not** implement gameplay, start Work/Astra, or silently mark release gates passed.


## Stage 13 FINAL — independent implementation-readiness audit

- **Status: COMPLETE, conditional GO to Work implementation; NOT a released game expansion.** All stages 00–13 are preproduction COMPLETE.
- `docs/13_RISKS_AND_DECISIONS.md`: final source-linked audit, 10 clarified contradictions and first Work task.
- `audit/13_SOURCE_MANIFEST.json`: exact original v1.4 archive SHA256, 76 implemented runtime IDs and 12 maps.
- `audit/13_DESIGN_CROSSCHECK.json`: Stage11 ticket/mission/source/QA/release-gate coverage; no unassigned or overlapping IDs.
- `audit/13_RISK_REGISTER.csv` + `.json`: 16 risks, prioritized P0–P2 with owner tickets and release gates.
- `audit/13_DECISION_LOG.json`: 14 recorded design authority decisions.
- `release/13_READINESS_MATRIX.json`, `release/13_GO_NO_GO_CHECKLIST.md`: conditional handoff, no false release readiness.
- `handoff/13_FINAL_WORK_READ_FIRST.md`, `prompts/13_FINAL_MINIMAL_STARTUP.md`: minimal resume path, first task PQ11-001.
- `tests/test_stage13_readiness.py`: 12 Stage13 checks, alongside previously passed Stage08–12 suites.
- **Implementation remains unstarted by this Bible:** all 76 new missions, new programmable systems, native Windows post-change release, performance benchmarks and human playtests require actual Work implementation and validation.
- **Next action:** Attach the final complete Bible to Work with the latest editable game source, use `prompts/13_FINAL_MINIMAL_STARTUP.md` once. Protect source at PQ11-001 before editing.
