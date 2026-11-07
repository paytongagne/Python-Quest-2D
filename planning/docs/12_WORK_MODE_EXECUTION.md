# 12 — Astra / Work Implementation Handoff and Usage-Efficient Execution

**Status: preproduction only.** Baseline: shipped v1.4 source ZIP, **76 implemented mission IDs**, **76 still planned**; 152 is a future **design target**, not a current playable count. Schema-4 saves are protected. Tickets: authoritative `backlog/11_IMPLEMENTATION_TICKETS.json`; validation: `qa/10_ACCEPTANCE_CATALOG.csv` and `release/10_RELEASE_GATES.json`. The next Work task is **PQ11-001**, not an unbounded order to build all 152 missions.

## A. Handoff package and decision authority

1. Upload the **actual current editable source** or use the same Work repository. Obtain a clean copy and note checksum. Never use the older Greenline/v1.0 source merely because its filename looks similar. If the Work source is newer than v1.4, inventory mission IDs and saves **first**, reconcile differences, and regenerate eligible tickets; do not overwrite newer implemented work.
2. Upload this full Bible once, or keep it in the repository under `planning/`. Work reads just `handoff/12_REPOSITORY_CONTEXT.md`, `handoff/12_RUNBOOK.md`, `handoff/12_TASK_STATE.json`, selected ticket and test references at the start. Do **not** paste every long previous chat or all 14 stages into each prompt.
3. A ticket definition in Stage 11 specifies **what to implement**. Stage 09 specifies protocol boundaries; Stage 10 determines **what counts as passing**. Actual source and executed test results override speculative design descriptions. Stage 13 will review outstanding risks; do not represent Stage 12 as final sign-off.
4. Release state is evidence-based. A ticket must not become DONE because code was generated or a test plan exists. Report tested on the current source, with executable command, test artifact and source identifier.
5. Existing mission IDs, saved drafts, XP, world flags, unknown save fields and accessibility settings must survive. Never run tests on the player's real save. Feature flags default OFF until current-build gates pass.

## B. Source reading order — exact entrypoints

**First scan (small and bounded):** `docs/PROJECT_STATE.md` (if present), `handoff/12_REPOSITORY_CONTEXT.md`, `handoff/12_TASK_STATE.json`, `backlog/11_IMPLEMENTATION_TICKETS.json` (just selected ticket), `release/10_RELEASE_GATES.json` (relevant gates), and `git status` or file hashes. Then read only the `source_anchors` of the selected ticket plus called interfaces. Read large monolith `src/python_quest_2d/game/app.py` by relevant symbol/range instead of dumping it. Do not print whole source files in chat.

**Feature-specific path:**
- Grading/protocol: `src/python_quest_2d/core/{challenges,grade,worker}.py`, Stage09 schemas/examples, selected existing tests.
- Saves: `src/python_quest_2d/core/progress.py`, `core/legacy_migration.py`, Stage09 save matrix, disposable profile tests.
- Robot/world: `game/{app,expedition,nursery,world}.py`, `core/route.py`, Stage03, Stage09 plan contracts.
- UI/art/travel: `ui/{hud,code_editor,terminal}.py`, `game/{pixel_world,planet_art,presentation,diagnostics}.py`, existing visual tests.
- Biomedical: `core/engineering_cases.py`, `game/instruments.py`, Stage08 fixtures, contracts, 96 proposed biomedical cases.
- Packaging: native scripts in `tools/`, `START_PYTHON_QUEST_2D.bat`, Stage10 release gates.

**Stop and report a blocker** if source files, an established save path, or an essential test fixture are missing; do not invent filenames and claim the work shipped.

## C. Model and reasoning allocation

Use the specific models available **in the account UI**, with no assumption of a fixed token exchange rate. Models and usage rules may change. Typical task allocation:

| Task | Suggested model | Effort | Use condition |
|---|---|---|---|
| Source checks / straightforward ticket / 4-mission data batch | GPT-6.1 Sol (or currently available comparable coding model) | Medium | Default for cost-sensitive bounded work |
| High-risk worker boundary, persistence migration, deterministic action reducer, biomedical geometry | GPT-6 Astra | Medium | High risk or repeated failing integration |
| Root-cause analysis of unresolved multi-module bug | GPT-6 Astra | High | Only if medium effort is inadequate; one narrow diagnosis |
| Docs/copy/CSV formatting | Lower-cost available model or ordinary chat | Low | Not used to mark tested implementation done |
| Planning, scripts, draft tests, acceptance specs | Regular ChatGPT | As needed | Work/Codex allowance separate from normal chat; verify current account UI |

Never change models inside a prompt by pretending to have switched. Model is selected in product UI. Cheapest request is not always cheapest completed ticket; record rework and regressions. No automatic overnight execution or continuous five-hour runtime is guaranteed.

## D. Work loop (one ticket per bounded iteration)

1. Run ticket selector (`python tools/work_ticket.py next --state handoff/12_TASK_STATE.json`) and get **one eligible ticket**. Override only if dependencies proven and state logged.
2. Inspect source status, read selected anchors, derive executable unit and integration checks. Ensure ticket specific QA IDs and Stage10 gates are not skipped.
3. Make a small coherent patch. Preserve previous feature flags and public APIs where possible. Do not execute learner Python directly in Pygame render loop. Reject invalid/stale/out-of-bounds plans without side effects.
4. Run targeted tests; fix issues; run required subset of the full regression suite. Save command, exit code, environment, source checksum or commit and log path. A planning integrity pass does **not** prove new runtime behavior.
5. Export a recoverable checkpoint containing source, state, tests and notes, **then** mark ticket DONE using evidence. If no native Windows runner, use status `BLOCKED` for native gate, not PASS. A development checkpoint may be delivered while final release stays blocked.
6. Refresh `docs/PROJECT_STATE.md` or equivalent (current mission ID set, active phase, completed ticket IDs, feature flags, known defects, next task). Report in <=180 words, continue on next ticket while tools allow. Stop if any P0 or save integrity issue, rather than blindly progressing.

**Cadence:** system tickets individually; mission batches four IDs only; wider regression once per chapter; Windows binary at named release checkpoints, not every four missions. Preserve source ZIP at every phase gate and at least after any risky schema/protocol change.

## E. Dependency and stage sequencing

Respect Stage11's directed acyclic graph. Phase 0: PQ11-001/002/003. Phase 1: 004–007. Phase 2: 008–011. Phase 3: 012–014. PQ11-015 enables code debugging features. Mission batches follow individual dependencies exactly; see selector output rather than hardcoded phase order alone. All six future chapters add 76 missions via **19 four-mission batches**. PQ11-016/017/018 are late integration, final QA and distribution, not early shortcuts.

Aesthetic work should validate screenshots at 1280x720, 1600x900, and 1920x1080 with multiple camera positions and no obstructive panels. Interactive locations must be visibly discoverable (not only through hidden shortcuts). More mission data is not a substitute for interesting game-state changes.

## F. Worker and persistence invariants

- Worker process computes bounded plain-data results. Main game validates envelope/schema, action legality, snapshot digest, device capabilities and resource budgets; main game owns rendering and state updates.
- Worker runs with local user's rights: **not a secure sandbox**. Never claim it isolates malicious code. Keep execution local, controlled, and use separate processes/timeouts; do not fetch arbitrary third-party challenge scripts for evaluation.
- Plans use deterministic seeds, immutable inputs, stable command identifiers, duplicate event protection. Replay without regranting XP.
- v2/v3/v4 profile migration requires a pre-upgrade backup. New additive data cannot silently erase unknown fields. Reject future save versions without mutation; don't downgrade.
- Original synthetic biomedical fixtures only. Null/unmeasured mesh value is distinct from measured zero. No real patient information or medical decisions.

## G. Test commands / host coverage

**Planning integrity, Linux/macOS/Windows with Python:**

```sh
cd Python_Quest_2D_Preproduction_Bible_v1
PYTHONQUEST_V14_ROOT=/absolute/path/to/source python -m unittest discover -s tests -p 'test_biomed_planning.py' -v
PYTHONQUEST_V14_ROOT=/absolute/path/to/source python -m unittest discover -s tests -p 'test_stage09_*.py' -v
python -m unittest discover -s tests -p 'test_stage10_*.py' -v
PQ11_SOURCE_ROOT=/absolute/path/to/source python -m unittest discover -s tests -p 'test_stage11_*.py' -v
python -m unittest discover -s tests -p 'test_stage12_*.py' -v
```

**Game on appropriate development machine:**

```sh
cd '<game source root>'
python -m pip install -e '.[dev]'
python -m pytest -q tests
```

Use `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy` for headless test runs when applicable, and `PYTHONQUEST_SAVE` in a disposable temp folder. No installed Pygame on the current planning container and no native Windows GUI verification here.

**Actual Windows machine with extracted release:**

```bat
cd "<extracted>\Python Quest 2D"
set "PYTHONQUEST_SAVE=%TEMP%\pythonquest-stage12-qa.json"
runtime\python.exe tools\native_smoke.py
runtime\python.exe tools\native_visual_revision.py
```

Run `START_PYTHON_QUEST_2D.bat` manually, test input, save/reopen, multiple display resolutions, new chapter transitions and packaging from a clean extraction. Stage10's `tools/verify_windows_archive.py` checks static archive integrity only, not native launch.

**Gate mapping:** G0 source/versions, G1 code contracts and tests, G2 saves and idempotency, G3 performance, G4 visuals and usability, G5 Windows packaging, G6 human playtest/known issues (read exact authoritative gate IDs; never infer PASS). Stop shipment on P0. Native and human tests require explicit evidence or remain BLOCKED/NOT RUN.

## H. Checkpoint and recovery strategy

Checkpoint tree (relative to Work's project or exported release; save immutable dated copies):

```text
checkpoints/
  CURRENT.json
  0001_PQ11-001/
    SOURCE_SHA256.txt
    source.zip
    TASK_STATE.json
    TEST_LOG.txt
    CHANGES.md
    RECOVERY.md
    QA_EVIDENCE.json
```

`CURRENT.json` points only to a **complete**, verified checkpoint; create `.tmp` files and replace atomically after CRC and manifest validation. On restart, validate checksum, compare source commit/hash, load `TASK_STATE.json`, inspect `CURRENT.json`, and resume the first eligible incomplete ticket. If files changed after checkpoint, do not mark them done without revalidation. Store the source archive outside ephemeral terminal buffers and link it in final response.

Checkpoint status vocabulary: `PLANNED`, `IN_PROGRESS`, `TEST_FAILED`, `BLOCKED`, `DONE`. A failed task retains notes, edits remain inspectable, and Work either fixes the same ticket or reverts only its patch; never reverts or downgrades a user's live save. `DONE` requires current-build evidence; status changes are never automatic from command success alone.

## I. Usage efficiency, overnight execution and approvals

- One concise startup instruction; don't repost a huge Bible on each turn. Keep source-of-truth inside repository. Use prompt templates under `prompts/12_*.md` and `python tools/work_ticket.py brief ID` for selected ticket.
- Prefer one selected ticket per coding task; the user may ask Work to continue through eligible tickets without confirmations **within platform allowances**. Do not suggest it runs indefinitely in the background or guarantees completion during sleep.
- Prioritize smaller meaningful commits/checkpoints, then continue. If nearing limit, stop new work, finalize a valid source checkpoint, and export it before truncation.
- Only invoke human approval when an action actually requires it, especially destructive operations, external account access, checkout/purchases, or altered protected data. Do not disable important confirmations through a prompt.
- Do not buy credits, use banked resets, change billing, or change account settings without explicit user instruction. Keep Work's shared allowance and current UI limits as authoritative; avoid inventing model-price percentages.
- Avoid redundant architecture debates, repeated full file scans, unnecessary images/web searches, long progress narrations, and rebuilds from obsolete source.

## J. Truthful completion and release reporting

Every ticket report includes: selected ticket ID, source identifier, code changed, mission IDs newly **implemented and graded**, targeted/full test counts, test host, status of applicable Stage10 QA and G0–G6, checkpoint, outstanding blockers, and next eligible ID. No mission count changes until actual runtime IDs are added and executable tests pass.

Maintain separate counts: `implemented_v14_baseline=76`, `added_validated_missions`, `playable_total=76+added_validated_missions`, `planned_remaining=76-added_validated_missions`. If task state is uncertain, use `UNVERIFIED` not a confident number. Original 76 ids must remain; no retroactive XP awards.

Final Windows candidate ships only if all required hard gates pass with evidence; otherwise label **development build / source checkpoint**, list blocked gates, and provide next commands for Windows machine. A successful ZIP CRC or synthetic fixture parse does not mean launch or gameplay passed.

## K. Entry/exit package and examples

**Read in order:** `handoff/12_REPOSITORY_CONTEXT.md`, `handoff/12_RUNBOOK.md`, `handoff/12_TASK_STATE.json`, use `tools/work_ticket.py next`, then selected ticket, selected Stage09/10 specifications. Copy `prompts/12_INITIAL_WORK_SESSION.md` once, `prompts/12_BOUNDED_TICKET.md` per task, and `prompts/12_RECOVERY.md` after interruptions. `prompts/12_RELEASE.md` only at checkpoint/release gates.

**Exit condition for Stage 12:** documents, machine-readable state/manifests, tested ticket utility, reference commands, QA traceability and progress index preserved. No game source modifications. **Stage 13 must still perform final readiness review.**
