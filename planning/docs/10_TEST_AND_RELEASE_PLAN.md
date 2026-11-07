# 10 — Testing, Performance and Release Engineering

**Status:** Stage-10 planning complete; test/catalog artifacts are **not new gameplay implementation**.  
**Baseline:** original v1.4 (76 implemented missions, schema-4 saves), source under `pq_stage09_source`.  
**Authority:** `qa/10_ACCEPTANCE_CATALOG.csv`, `qa/10_PERFORMANCE_BUDGETS.json`, `release/10_RELEASE_GATES.json`, and `tools/verify_windows_archive.py`.  
**Safety boundary:** learner programs still run with local user privileges in a short-lived process. That is **not** a security sandbox. Never execute unknown third-party code in tests.  

## 1. Design contract: distinguish evidence from aspirations

Stage 08's 96 synthetic biomedical acceptance scenarios are design specifications, not yet executable game tests. Stage 09's schemas and pure-Python unit tests verify proposed protocols and selected v1.4 behavior. The v1.4 scripted suite exercises 76 real missions *in its own release environment*. Stage 10 contributes a traceable release test plan and new standalone verification tooling. Do not mark all coverage PASS because a fixture parser passed.

**Test status vocabulary:** `PLAN_ONLY`, `IMPLEMENTED_NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`, `SKIPPED_WITH_REASON`. Report `PASS` only with concrete command, host/environment, timestamp, artifact or log; keep a failed gate red until re-tested on the current build. Distinguish `HEADLESS_LINUX`, `NATIVE_WINDOWS`, `HUMAN`, `SYNTHETIC_FIXTURE`, and `STATIC_RELEASE_AUDIT`.

## 2. Baseline test topology

- Baseline source: `tests/test_flight.py`, `test_content.py`, `test_controls.py`, `test_greenline.py`, `test_expeditions.py`, `test_workshop.py`, `test_visual_revision.py`.
- Current Python minimum 3.10; pygame-ce pinned 2.5.8. The test suite uses `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy`, temporary `PYTHONQUEST_SAVE`, and imports app through the project `src` path.
- Real grader uses `core/grade.py` and `core/worker.py` with local subprocess execution. Existing timeout/source limits do not provide OS isolation.
- Baseline native scripts recorded in the **actual v1.4 release ZIP**: `tools/native_smoke.py`, `native_visual_revision.py`, `visual_matrix.py`. Native verification must run on Windows, not inferred from headless mode.
- The v1.4 checkpoint states 21 unittest methods passed and native screenshots at three sizes. This is prior-release evidence, **not** execution of this new Stage 10 plan.

## 3. Acceptance suite and traceability

`qa/10_ACCEPTANCE_CATALOG.csv` maps unique test IDs to failure class, originating source/contract, expected result, implementation scope and gate. Subsystems: `LEG`, `WRK`, `TRV`, `SAV`, `PRG`, `DEV`, `BIO`, `VIS`, `PERF`, `WIN`, `HUM`, `SEC`.

For every new mission, developers must add four cases: (1) reference solution succeeds and changes correct world-owned effect; (2) wrong/edge input fails without reward; (3) unfinished action survives restart at safe checkpoint; (4) replay/retry does not duplicate XP or device effects. Stage 08's original 24 × 4 = 96 proposed acceptance cases remain authoritative for the biomedical missions. Do not count them as shipped tests until executable tests run.

**Failure triage:** P0 = crash, persistent save corruption, XP duplication, invisible progress blocker, unsafe plan authorization, broken Windows launch. P1 = inaccessible console, repeated UI clipping, unstable input, significant performance regression. P2 = cosmetic inconsistency, minor typos, animation polish. Block release on P0, and on unresolved P1 affecting core progression or accessibility.

## 4. Recommended execution commands

**Stage 08–10 planning integrity (works without Pygame):**

```bash
cd Python_Quest_2D_Preproduction_Bible_v1
PYTHONQUEST_V14_ROOT=/path/to/v14/source python -m unittest discover -s tests -p 'test_biomed_planning.py' -v
PYTHONQUEST_V14_ROOT=/path/to/v14/source python -m unittest discover -s tests -p 'test_stage09_*.py' -v
python -m unittest discover -s tests -p 'test_stage10_*.py' -v
```

**Existing game on development machine with pygame-ce 2.5.8 installed:**

```bash
cd /path/to/v14/source
python -m pip install -e '.[dev]'
python -m pytest -q tests
```

**Native extracted Windows release, command prompt or PowerShell, with disposable save location:**

```bat
cd "<extracted>\Python Quest 2D"
set "PYTHONQUEST_SAVE=%TEMP%\pythonquest-qa-smoke.json"
runtime\python.exe tools\native_smoke.py
runtime\python.exe tools\native_visual_revision.py
runtime\python.exe tests\test_visual_revision.py
```

Run `START_PYTHON_QUEST_2D.bat` separately on actual Windows and manually verify first screen, play, quit, save, and restart. Do not test against the real user profile. Verify names from current archive before running; newer release scripts may differ.

**Static release archive audit, any OS:**

```bash
python tools/verify_windows_archive.py /path/to/Python-Quest-2D-v1.4-Windows-x64.zip --json report.json
```

Passing static audit only proves archive shape/path/CRC and is not evidence that the Windows launcher actually opens.

## 5. Regression suite by layer

| Layer | What must be covered | First evidence | Next release gate |
|---|---|---|---|
| Baseline gameplay | 76 existing IDs, scripted navigation, grading, missions, XP | Existing `test_flight`, `test_greenline`, `test_expeditions`, `test_workshop` | Re-run full suite on current build |
| Contract boundaries | worker outputs, 13 typed schemas, negative cases, stale snapshots | Stage 09 tests and schemas | Add current-game adapters under feature flags |
| Deployable robots | bounds, energy, walls, capabilities, deterministic replay, duplicate events | Stage 09 pure reference validator | Test parent-owned game reducer in integration |
| Travel | locked previews, safe spawn, busy job, route, mouse letterboxing | Existing travel tests + Stage 10 catalog | Real controller and save tests |
| Persistence | schema 2, 3, 4, unknown keys, partial writes, future guard | Existing migration + Stage 09 matrix | Fault injection and atomicity proof |
| Biomedical | 24 planned missions, clean/faulted traces, isolated vertices, null vs zero | Stage 08 fixtures and 96 cases | Real numeric/visual integration tests |
| UX | focus, clipping, font, UI screenshots, objective findability | Existing v1.4 visual tests | Three-size captures and human checks |
| Performance | frame work p95/p99, memory, startup, save time | Stage 10 proposed budgets | Instrument real Windows build |
| Shipping | archive, launcher, offline fresh extract, source match | Static auditor | Actual native launch + smoke + signatures |

## 6. Determinism, isolation and fault injection

Tests MUST be isolated: set `PYTHONQUEST_SAVE` to a unique temp directory; do not reuse live profile. Generate synthetic fixture IDs/seeds deterministically, remove temporary files only after preserving any failing artifacts, and never copy test execution results into the player's normal save.

Fault-injection matrix lives at `qa/10_FAULT_INJECTION.md`; it defines kill points before/after atomic replace, stale digest, oversized result, syntax errors, mid-travel and lost window focus. Favor deterministic injected exceptions over forcibly killing processes in CI. When testing true crashes, perform them in a disposable subprocess and use protected temp profiles.

**Concurrency release invariant:** Every award must originate from a committed mission/world milestone, and repeated `event_id` applications must be a no-op. A worker crash, timeout, invalid action or stale source revision must not change completion flags, XP, maps, equipment or live save bytes.

## 7. Performance targets, not existing measurements

All numeric targets are proposed, machine-specific budgets and are recorded in `qa/10_PERFORMANCE_BUDGETS.json`. Measure on real hardware and record CPU/GPU, OS, scaling, screen size and power plan. Example release budget: 1280×720 frame-work p95 <= 16.7ms; 1920×1080 p95 <= 25ms on the declared reference desktop; no sustained memory growth above 1MiB/min over 20 minutes. Report actual medians, p95, p99, max and sample count; explain warmup and profiler instrumentation overhead. Frame-work time does not equal end-to-end FPS. The source's existing 3-second worker timeout may freeze an editor momentarily; budget its evaluation separately from frame rendering.

If budgets fail, prioritize lazy/culled tile draws, cached static layers, capped particles, smaller overlay blits, and bounded replay buffers. Do not sacrifice code grading correctness for frame targets.

## 8. Visual accessibility and human acceptance

`qa/10_HUMAN_PLAYTEST_PROTOCOL.md` defines observable 15–30 minute sessions for novice, intermediate and returning player, with explicit task completion timing, navigation errors, tutorial/hint use, frustration and engagement indicators. Test with keyboard-only and mouse, reduced motion, at least 1280×720/1600×900/1920×1080, and more than one camera position per world. Reject overlarge opaque panels occluding play areas. Check that the Workshop entrance can be found by a novice without being told J → 8.

## 9. Windows build and rollback procedure

1. Freeze the verified source tree; record SHA256 of source ZIP and dependency versions.
2. Execute planning/spec tests and runtime tests on frozen source. Stop on failure.
3. Build one release candidate; do not embed live saves, temp files, debug logs or credentials.
4. Run `verify_windows_archive.py`; then extract to a **new folder** containing spaces and non-ASCII characters on native Windows.
5. Use the bundled interpreter to run native smoke and 76-mission campaign tests where feasible; run real `.bat` launcher, resize, quit, reopen and verify disposable save.
6. Capture six-world visual evidence, failures and actual frame telemetry; compare to last known-good release.
7. Release both source and Windows ZIP, `SHA256SUMS.txt`, test report, hardware info, changelog, migration/rollback instructions, open defects and known untested claims.
8. Keep preceding release immutable. Schema changes require a pre-migration backup and tested rollback. Do not silently downgrade newer profile versions.

**Stop-ship policy:** hard gates are defined in `release/10_RELEASE_GATES.json`. Do not release if a P0 failure remains; do not imply human playtesting occurred when it has not.

## 10. Stage 10 deliverable boundary

This stage authors **test policy and verification tools**, not a gameplay patch. The baseline Linux container may lack pygame-ce and cannot native-run Windows `.bat` files. Report source planning tests and static archive audit as separate evidence. Preserve prior Stage 09 tests and artifacts untouched, update the index, and package deterministic stage/full archives.
