# 13 — Independent Design Audit, Decisions and Readiness

**Status:** Final preproduction audit of the Stage 00–12 Bible against user-provided v1.4 editable source. This is **planning readiness**, not a release certification or newly implemented game build.

## A. Authoritative baseline and audit method

- Original archive: `Python-Quest-2D-v1.4-Windows-x64.zip`. Unmodified source paths inside `Python Quest 2D/` are the canonical current shipped baseline for this review. `core.challenges.LESSONS` imports with **76 keys**, `MAPS` imports with **12 map keys**; current save `schema_version=4` (source-derived).
- Distribution of 76: six base decks ×4 =24; Hydroponics 16, Workshop 8, Orion 16, Titan 4, Helix 4, Aurora 4. The **76 remaining** are Workshop 8, Algorithm Tower 16, Titan 12, Helix 12, Aurora 12, Mission Control 16.
- Stage11 machine-readable catalog has 37 tickets: 18 system/release tickets + 19 batches ×4 missions, not 37 playable changes. Stage10 catalogs **86 prospective test cases**; Stage08 catalogs **96 prospective biomedical cases**. Neither is evidence of implementation.
- Independent audit compared core source (`progress.py`, `challenges.py`, `grade.py`, `worker.py`, `expedition.py`); Stage03/04/05/07/08/09 specifications; Stage10 gate/test catalog; Stage11 dependency/ticket and mission mappings; Stage12 selector/rubric. Actual Windows playtesting and Pygame performance were **not run** in this Linux planning session.

## B. Resolved design conflicts and authority policy

1. **Game chronology versus implementation chronology:** Stage04's canonical story route is the target player progression. Stage11's DAG is the order engineers implement features. They are not required to be the same. Travel prerequisites must be reachable without Preview; unfinished content stays visibly locked with a truthful reason.
2. **Schema 4 versus additive new systems:** Stage09's optional `program_library`/`runtime_v1` fit inside the current schema-4 profile without forcing a migration. The v1.4 `progress.load()` currently does *not* explicitly reject future save versions. PQ11-003 must add fail-safe nonmutating rejection and tests before shipping a program library.
3. **Standardized new worker contracts versus legacy behavior:** Keep `grade()`/`worker.evaluate()` as the default for the original 76. New data-only request/result adapters remain feature gated until parity across scripts, functions, object fixtures, engineering simulation, and expeditions is demonstrated.
4. **Freeform Mica programs versus game-state security:** Execute learner code in a separate local worker, normalize bounded plain data and *revalidate* against current world snapshot in the parent. This prevents accidental direct game-state mutation, not malicious local code execution. Worker is not a secure hostile-code sandbox.
5. **Mission design files versus runtime missions:** `mission_blueprints.psv`, contract CSVs and test tables are not executable lesson JSON. Count a mission only once the runtime loader finds the ID, its own grader passes, its world interaction works and its rewards/replay behave correctly. Never inflate 'playable missions' from future designs.
6. **Biomedical contract ambiguities:** Aurora 10 takes `vertex_count` so isolated vertices remain representable; Aurora 11 uses nullable values for unmeasured vertices, with measured zero retained. Synthetics must include units, finite inputs and deterministic tie tolerances. No Qt migration or clinical claims.
7. **Visual polish versus project scope:** Stage05 visual grammar is authoritative, but implement the first high-value Orion benchmark before reskinning all worlds. Screenshot/UX evidence at multiple viewports is required, not only code changes and new UI rectangles.
8. **Evidence and release claims:** Stage10 G0–G6 are required release gates. A planning test or static archive audit does not satisfy native Windows launch, human playtest, or runtime performance measurements. Label unavailable host checks BLOCKED or NOT RUN.
9. **Work versus uploaded baseline:** The planning ZIP is not a substitute for the latest Work code if Work has a newer verified build. Compare hashes, runtime lesson IDs and save schema first; never reset an upgraded game to an older archive.
10. **Stage index historical wording:** Earlier Stage09 caution about an alternate stage script was superseded by the completed source-linked Stage09 deliverable. Use this Stage13 audit and the most recent Stage09/11/12 artifacts, not the historical caution.

Full machine-readable resolutions: `audit/13_DECISION_LOG.json`. Exactly enumerated risk ownership: `audit/13_RISK_REGISTER.csv` and `.json`.

## C. Source-specific architecture invariants

**Worker boundary**: `core/grade.py` launches a short-lived process to `core/worker.py`; `core/challenges.py` loads challenges from JSON; `game/app.py` collects results; `game/expedition.py` owns expedition deployment/travel; `game/world.py` owns map/collision; `core/progress.py` owns save/reward. Never run player Python in `Game.draw()` or the Pygame frame loop. Source import was checked, not modified.

**Profile and rewards**: v1.4 profile contains saved drafts, attempts, flags, and custom/unknown keys. XP is 100 unhinted / 75 hinted / 25 solution-revealed, and repeats grant 0. Preserve existing semantics; new transfer/mastery rewards must be explicitly separate and idempotent. Use disposable test profiles with `PYTHONQUEST_SAVE`, not live user data.

**Artwork**: World views must use consistent tile scale and actor depth, avoid unclipped HUD text, preserve hit testing under letterboxing, and provide clear observable object changes after programs execute. Accessibility: static reduced-motion states, noncolor cues, keyboard controls, readable diagnostics.

**Medical**: Synthetic-only signals, timestamps, noise, filters and toy chamber surfaces. Preserve missing-vs-zero distinction, reject nonfinite values, and test explicit units/rounding; no patient data, clinical recommendations, vendor imitation or proprietary APIs.

## D. Risk priorities

**P0:** `R13-01` unknown future save mutation; `R13-02` local worker's unavoidable code-execution risk; `R13-03` duplicate rewards/state after crash. These are not reasons to abandon the handoff, but they are **stop-ship risks** until implementation provides sufficient mitigation and honest user warning. No new software should silently modify a future schema.

**P1:** source compatibility, travel prereqs, stale plans, visual occlusion, unverified Windows build, performance, biomedical edge cases, evidence quality and checkpoint loss. **P2:** learning scaffolds and clinical presentation labeling. See CSV for exact owner ticket and gate.

## E. Readiness verdict: CONDITIONAL GO for Work implementation, NO-GO for claiming a final release

**GO:** Design contracts, mission coverage, dependencies, source anchors, runbook, test catalog, first ticket and recovery policy are sufficiently explicit to begin `PQ11-001` on the most recent editable source. Keep all high-risk architectural changes behind feature flags.

**CONDITIONS:** Work must snapshot the source, reconcile any later mission additions, and verify actual baseline tests using a supported Pygame environment. Later distribution requires Stage10 G0–G6 evidence, native Windows testing, performance sampling and human playtest. A build that lacks these must be labeled **development checkpoint** and never 'verified production release'.

**NO-GO conditions:** Missing editable latest source; unsupported or conflicting save version without read-only recovery; lost original IDs/XP; learner program executing in live game loop; source mismatch with checkpoint without reconciliation; new P0 regression.

See `release/13_READINESS_MATRIX.json` for per-gate statuses and `release/13_GO_NO_GO_CHECKLIST.md` for explicit operator actions.

## F. First Work execution

1. Attach/locate *latest editable* Work game source and `Python_Quest_2D_Preproduction_Bible_Stages_00-13.zip` once.
2. Read `handoff/13_FINAL_WORK_READ_FIRST.md` (short) and `handoff/12_REPOSITORY_CONTEXT.md`; verify file inventory and source revision before any edits.
3. Run `python tools/work_ticket.py next --state handoff/12_TASK_STATE.json`. **Expected initial**: `PQ11-001`; if already completed in newer source, require evidence and update state rather than replaying old task.
4. Implement only PQ11-001 first: secure baseline SHA256 + mission-ID manifest + disposable-profile tests + complete portable source checkpoint; run applicable game tests; record host/results; update ledger with evidence.
5. Then advance by DAG to the next eligible ticket and implement small bounded changes. No bulk mission additions before shared programmable systems pass replay/idempotency tests.
6. Deliver source and logs at checkpoints; run native Windows commands only on a Windows host; never turn tests into fictional pass reports. If blocked, export stable source and state.

**Minimal prompt** (also saved in `prompts/13_FINAL_MINIMAL_STARTUP.md`):

> Continue Python Quest 2D from the latest editable source. Read the attached final Bible `handoff/13_FINAL_WORK_READ_FIRST.md`, verify the source, run `work_ticket.py next`, and execute only dependency-eligible tickets with tests and source checkpoints. Begin with PQ11-001 unless completed with verified evidence. Preserve the 76 original missions, save data, grader behavior, and feature flags. Do not treat design files as playable content or claim native/human tests without logs. Keep progressing through eligible tickets while tools permit; export recovery state before stopping. No new planning exercise or routine approvals.

## G. Files, commands and audit ownership

- Source package: v1.4 ZIP (runtime reference, unmodified). Final Bible ZIP: *planning package* only.
- `audit/13_SOURCE_MANIFEST.json`: original source checksum and runtime counts.
- `audit/13_DESIGN_CROSSCHECK.json`: programmatic ID/anchor/gate/contract consistency.
- `audit/13_DECISION_LOG.json`: resolved design choices and authority.
- `audit/13_RISK_REGISTER.csv`: 16 prioritized risks, mitigation tickets and gating tests.
- `release/13_READINESS_MATRIX.json` and `release/13_GO_NO_GO_CHECKLIST.md`: readiness and outstanding host tasks.
- `tests/test_stage13_readiness.py`: independent integrity checks; Stage08–12 tests must still pass.
- `handoff/13_FINAL_WORK_READ_FIRST.md` and `prompts/13_FINAL_MINIMAL_STARTUP.md`: condensed Work startup.
