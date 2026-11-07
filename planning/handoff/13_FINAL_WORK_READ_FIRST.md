# Python Quest v1.4 → full campaign: final Work read-first (Stage 13)

**Status:** preproduction complete; actual new game code not implemented by this Bible. User's latest verified attached v1.4 build has **76 missions**; another newer Work project may exist and must be compared before touching files.

**Read in order, once:**
1. This file; `handoff/12_REPOSITORY_CONTEXT.md`; `handoff/12_TASK_STATE.json`.
2. Check editable source, hash/IDs/schema and run baseline tests. Read `audit/13_SOURCE_MANIFEST.json`, `audit/13_DESIGN_CROSSCHECK.json` and `release/13_GO_NO_GO_CHECKLIST.md` only as needed.
3. `python tools/work_ticket.py next --state handoff/12_TASK_STATE.json` (expected PQ11-001). Use `python tools/work_ticket.py brief PQ11-001` and relevant ticket-specific Stage09/10/11 snippets.
4. Start on **PQ11-001**: protect baseline, record 76 IDs, test in disposable profile, export rollback. Do not bulk-generate 76 proposed missions first.

**Invariant:** game-owned mutations only after worker grades data and parent validates action plan. No learner code in render loop. Worker is not a secure code sandbox. Preserve schema4, legacy IDs, unknown save keys, 100/75/25 XP and replay=0. Reject future profile versions without writing. Synthetic toy medical data only.

**Bounded loop:** next ticket → relevant sources → small feature-gated patch → focused tests + regression subset → checkpoint+hash → ledger evidence → next eligible. Stage11 DAG controls order. Stage04 player-story order is not implementation order. Once release gates approach, stop creating new features and finish testing/packaging.

**Delivery:** concise source checksum, actual playable IDs, tickets completed, test log links and host, checkpoint, G0–G6 statuses, blockers, next ticket. Never claim runtime work from the planning package. Native Windows and human tests stay NOT RUN unless actually performed.

**Prompt:** `prompts/13_FINAL_MINIMAL_STARTUP.md` contains one short ready-to-paste message. Full details only in `docs/13_RISKS_AND_DECISIONS.md`.
