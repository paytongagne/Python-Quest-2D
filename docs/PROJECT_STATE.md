# Current development state

- 76 playable missions; 76 planned. Save schema 4.
- PQ11-001, PQ11-002, and PQ11-003 verified on Windows. Evidence is in `docs/evidence/`.
- The import is based on the completed PQ11-003 source checkpoint. Git tag: `checkpoint/pq11-003`.
- Next in dependency order: PQ11-004, immutable observations and current-state validation for Mica.
- `handoff/12_TASK_STATE.json` is live. The Bible's own ledger is a preserved template.
- Contracts are opt-in (`PYTHONQUEST_CONTRACTS_V1=1`). Live reusable Mica deployment follows the next tickets.
- 29 runtime tests and 81 planning checks passed before import. This is a development checkpoint; the full-campaign release gates remain open.
