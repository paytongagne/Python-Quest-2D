# Current development state

- 76 playable missions; 76 planned. Save schema 4.
- PQ11-001 through PQ11-004 verified on Windows. Evidence is in `docs/evidence/`.
- The import is based on the completed PQ11-003 source checkpoint. Git tag: `checkpoint/pq11-003`.
- Next in dependency order: PQ11-005, the game-owned fixed-tick action runner and atomic milestone reducer.
- `handoff/12_TASK_STATE.json` is live. The Bible's own ledger is a preserved template.
- Contracts are opt-in (`PYTHONQUEST_CONTRACTS_V1=1`). PQ11-004 captures immutable game observations and validates real worker-produced plans against current world state. The runner and player interface follow.
- 32 runtime tests passed during PQ11-004; 81 planning checks passed during import. This is a development checkpoint; the full-campaign release gates remain open.
