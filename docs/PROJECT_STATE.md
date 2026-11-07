# Current development state

- 76 playable missions; 76 planned. Save schema 4.
- PQ11-001 through PQ11-005 verified on Windows. Evidence is in `docs/evidence/`.
- The import is based on the completed PQ11-003 source checkpoint. Git tag: `checkpoint/pq11-003`.
- Current rollback tag: `checkpoint/pq11-005`. Next: PQ11-006, save and equip reusable code revisions, deploy on two maps, and inspect or compare replays.
- `handoff/12_TASK_STATE.json` is live. The Bible's own ledger is a preserved template.
- Contracts are opt-in (`PYTHONQUEST_CONTRACTS_V1=1`). PQ11-004 captures immutable game observations and validates real worker-produced plans against current world state. PQ11-005 runs verified action data at fixed logical steps, interpolates the rover in the world, and commits device state and replay together. The player library and deployment controls follow in PQ11-006.
- 36 runtime tests passed for PQ11-005; 81 planning checks passed during import. GitHub CI passed for PQ11-004. The portable packaging tool passed static archive checks and a native first-repair smoke test on the imported baseline. This is a development checkpoint; the full-campaign release gates remain open.
