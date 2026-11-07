# Stage 13 — Implementer GO / NO-GO checklist

## Before first Work patch
- [ ] Inspect the latest editable source, not just ZIP release artifacts; reconcile any newer implementation with the v1.4 source baseline.
- [ ] Confirm all original 76 mission keys, original XP semantics, save schema, and worker grading paths.
- [ ] Record SHA256 of source, executable environment and test runner versions.
- [ ] Export an immutable original-source checkpoint with rollback instructions.
- [ ] Run existing scripted tests using an appropriate Python+pygame-ce installation and disposable save profiles; record failures without hiding them.
- [ ] Run `python tools/work_ticket.py next --state handoff/12_TASK_STATE.json`; verify dependencies and source anchors before coding.

## Every ticket
- [ ] Read just linked files, relevant design contract and Stage10 cases.
- [ ] Implement feature-gated, small patch. Preserve legacy mode by default.
- [ ] Run focused tests plus relevant baseline checks, recording command, host, exit code and log.
- [ ] Test invalid requests, failure/cancellation/resume and no-repeat XP where applicable.
- [ ] Checkpoint source+state+tests and point `CURRENT.json` to a verified complete snapshot.
- [ ] Mark DONE only with evidence and pass; otherwise BLOCKED/TEST_FAILED.

## Before Windows release
- [ ] G0: exact source hash/version and reproducible build.
- [ ] G1: old/new runtime grading/worker/plan tests pass.
- [ ] G2: v2/v3/v4 saves, unknown fields, future schema rejection, idempotent XP/replay pass.
- [ ] G3: extracted Windows x64 launcher tested *on Windows*, including save/restart and paths with spaces.
- [ ] G4: screenshot matrix, no overlaps/clipping, input and reduced motion validated.
- [ ] G5: measured real frame time / memory targets on specified hardware, not synthetic examples.
- [ ] G6: human sessions per protocol and outstanding known bugs documented.
- [ ] Any missing hard gate => development preview only; never label a final public release ready.

## Stop-work / recover
- Stop new changes on P0 data loss, unsupported source version, broken original grader, crash/XP double-awards or source checkpoint mismatch.
- Preserve diagnostics and current source, then fix or rollback the isolated patch. Never overwrite users' saved progress during test.
- If limited by Work allowance, export latest stable source.zip, task state, logs and exact next ticket before stopping.
