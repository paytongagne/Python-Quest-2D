# Current development state

- 76 playable missions; 76 planned. Save schema 4.
- PQ11-001 through PQ11-007 verified on Windows. Evidence is in `docs/evidence/`.
- The import is based on the completed PQ11-003 source checkpoint. Git tag: `checkpoint/pq11-003`.
- Current rollback tag: `checkpoint/pq11-007`. Next: PQ11-008, HUD and diagnostics accessibility.
- `handoff/12_TASK_STATE.json` is live. The Bible's own ledger is a preserved template.
- Contracts are opt-in (`PYTHONQUEST_CONTRACTS_V1=1`). PQ11-004 captures immutable game observations and validates real worker-produced plans against current world state. PQ11-005 runs verified action data at fixed logical steps, interpolates the rover in the world, and commits device state and replay together. PQ11-006 adds the B-key opt-in library, persistent revisions, Hangar and Workshop docks, deployment, rehearsal, and step-by-step comparison.
- 39 runtime tests passed for PQ11-007; 81 planning checks passed during import. GitHub CI passed for PQ11-004. The portable packaging tool passed static archive checks and a native first-repair smoke test on the imported baseline. This is a development checkpoint; the full-campaign release gates remain open.

PQ11-007 adds two Orion relay objectives. The outpost activates a physical weather gate. The transfer starts from Mica's saved cell and rewards reusable pathfinding around the storm barriers. The campaign still contains 76 mission IDs.
