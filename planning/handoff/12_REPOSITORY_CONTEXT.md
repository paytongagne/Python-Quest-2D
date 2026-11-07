# 12 — Minimal repository context for Work

- **Current verified baseline**: v1.4 Windows ZIP contains editable source, 76 implemented missions, save schema 4. Original ZIP is `Python-Quest-2D-v1.4-Windows-x64.zip`. Newer Work source must be audited instead of assumed equivalent.
- **Product**: top-down Python learning adventure in Pygame CE. Five worlds: Astra/Greenline/Workshop, Orion, Titan, Helix, Aurora. Extra planned chapters: Algorithm Tower and Mission Control. 152 missions **planned**, not shipped.
- **Worker boundary**: `core/grade.py` -> `core/worker.py` separate Python process -> result -> game-owned visual/state updates. No learner code in live renderer; worker is not a hostile-code sandbox.
- **Game source anchors**: `core/{challenges,grade,worker,progress,route,engineering_cases,object_cases}.py`; `game/{app,world,expedition,nursery,instruments,pixel_world,presentation}.py`; `ui/{hud,code_editor,terminal}.py`; `content/` challenge files and `tests/`.
- **Save rule**: retain IDs, XP, drafts, unknown keys, flags; validate schema 2/3 migration and schema 4 roundtrip; reject future saves safely; never test real user profile.
- **Design inputs**: Stage03 programmable world, Stage04 atlas, Stage05 visuals, Stage07 curriculum, Stage08 biomedical, Stage09 typed contracts, Stage10 release gates, Stage11 ticket catalog. Read **only the subset relevant to selected ticket**.
- **Ticket source**: `backlog/11_IMPLEMENTATION_TICKETS.json` 37 tickets, of which 19 mission batches cover remaining 76 IDs. `backlog/11_MISSION_TO_TICKET.csv` holds mission contracts.
- **QA source**: 86 Stage10 named acceptance cases in `qa/10_ACCEPTANCE_CATALOG.csv`; 96 additional Stage08 proposed biomedical cases. Planning checks are not gameplay tests.
- **First task**: PQ11-001, protect real source & baseline. Then ticket dependencies determine next eligible.
- **Reporting**: one source hash + ticket ID + mission count + executable test evidence + checkpoint link + next eligible. Unknown statuses stay unverified.
