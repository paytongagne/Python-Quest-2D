# Phase 0 development checkpoint

The existing 76 playable missions remain. No planned mission is counted as implemented.

PQ11-001 protects the baseline and tests every actual reference solution, worker effect, wrong submission and replay. PQ11-002 introduces opt-in versioned worker envelopes, output limits, and pure Mica action validation. PQ11-003 prepares additive saved-program fields and protects newer saves from older builds, with atomic-write failure tests.

The new protocol is OFF by default. Development testing may opt in with PYTHONQUEST_CONTRACTS_V1=1. There is not yet a new reusable-Mica deployment UI or live action runner; those follow dependency tickets 004–007.

Use `python tools/work_ticket.py next` from this project. The live ledger is `handoff/12_TASK_STATE.json`. The Bible's `planning/handoff/12_TASK_STATE.json` remains an untouched design template so its own integrity tests remain reproducible.

The supplied inner ZIP names were reversed; contents were identified before extracting. Imported game files matched the working v1.4 baseline byte-for-byte. Planning fixture generation was made LF-deterministic on Windows; planning tests run with UTF-8 enabled and jsonschema installed as a development-only dependency. Gameplay runtime dependencies are unchanged.

This is an interim playable development checkpoint, not a final 152-mission release. See exported ticket state, source hashes, logs and gate status. Next ticket: PQ11-004 (world observation snapshots and current-state validation), then the fixed-tick action runner and reusable-program workflow.
