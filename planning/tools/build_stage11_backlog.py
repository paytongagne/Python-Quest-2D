from pathlib import Path
import csv,json,collections,hashlib,zipfile,io,sys
from datetime import datetime
B=Path('/mnt/data/Python_Quest_2D_Preproduction_Bible_v1');SRC=Path('/mnt/data/pq_stage09_source'); OUT=Path('/mnt/data')
read=lambda p:p.read_text(encoding='utf-8')
mission_cols=['zone','sequence','title','topic','api','player_action','world_effect','edge_cases','example','tier']
with (B/'missions/mission_blueprints.psv').open(encoding='utf-8') as f:
    next(f); missions=list(csv.DictReader(f,delimiter='|',fieldnames=mission_cols))
acceptance=list(csv.DictReader((B/'qa/10_ACCEPTANCE_CATALOG.csv').open(encoding='utf-8-sig')))
areas=collections.defaultdict(list)
for r in acceptance:areas[r['area']].append(r['test_id'])
anchor=lambda a: ';'.join(areas[a][:4])
SEAMS={
'baseline':'src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py;src/python_quest_2d/core/progress.py;tests/test_flight.py;tests/test_visual_revision.py',
'contracts':'src/python_quest_2d/core/grade.py;src/python_quest_2d/core/worker.py;src/python_quest_2d/core/challenges.py;src/python_quest_2d/game/app.py',
'save':'src/python_quest_2d/core/progress.py;src/python_quest_2d/game/app.py',
'world':'src/python_quest_2d/game/world.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py',
'robot':'src/python_quest_2d/game/nursery.py;src/python_quest_2d/game/expedition.py;src/python_quest_2d/core/route.py',
'ui':'src/python_quest_2d/ui/hud.py;src/python_quest_2d/ui/code_editor.py;src/python_quest_2d/game/diagnostics.py',
'visual':'src/python_quest_2d/game/pixel_world.py;src/python_quest_2d/game/planet_art.py;src/python_quest_2d/game/presentation.py;src/python_quest_2d/game/workshop_art.py',
'workshop':'src/python_quest_2d/core/object_cases.py;src/python_quest_2d/game/workshop_art.py;content/planets/workshop.json',
'algorithm_tower':'src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/world.py;content/maps/algorithm.json',
'titan_cloud':'src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/titan_cloud.json',
'helix_bio':'src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/helix_bio.json',
'aurora_ep':'src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/instruments.py;content/planets/aurora_ep.json',
'mission_control':'src/python_quest_2d/core/engineering_cases.py;src/python_quest_2d/game/expedition.py;content/universe/destinations.json',
}
# verify anchors against extracted source; new paths only planned not assumed
assert all((SRC/p).exists() for files in SEAMS.values() for p in files.split(';')),[(p) for files in SEAMS.values() for p in files.split(';') if not (SRC/p).exists()]
write=lambda p,s:(p.parent.mkdir(parents=True,exist_ok=True),p.write_text(s,encoding='utf-8'))
# ordering: horizontal slice, then chapters (Workshop, Titan, Helix, Tower, Aurora, Finale)
meta={
'workshop':('Workshop District','OOP, fixtures, stateful systems','Astra workshop production line','object;worker;save;visual'),
'algorithm_tower':('Algorithm Tower','data structures, graph algorithms and complexity','tower simulation boards and routing panels','worker;contract;visual;travel'),
'titan_cloud':('Titan Cloudworks','event queues, topic routing, retries, deterministic async','pulsing packet network and relay devices','contract;worker;visual;save'),
'helix_bio':('Helix Biomedical','synthetic time series, filtering, timestamps','synthetic signal monitor and pump recovery','synthetic;worker;visual;save'),
'aurora_ep':('Aurora Observatory','toy 3D mesh, interpolation, transforms, mapping','chamber mesh layers and mapping consoles','synthetic;worker;visual;save'),
'mission_control':('Mission Control Annex','integration, concurrency models, fault recovery','multi-world systems and staged final boss','contract;worker;save;travel')}

tickets=[]; mapping=[]
def ticket(id,phase,name,kind,dep,paths,done,qa,gate='G1',risk='medium',size='M',mids=None,checkpoint=None,notes=''):
  tickets.append(dict(ticket_id=id,phase=phase,task=name,kind=kind,depends_on=dep,source_anchors=paths,acceptance=done,stage10_tests=qa,release_gates=gate,risk=risk,effort=size,mission_ids=mids or [],checkpoint=checkpoint or 'source commit + disposable profile + test log',notes=notes,status='PLANNED_NOT_IMPLEMENTED'))
# Phase zero
infras=[
('PQ11-001','0','Establish protected source checkpoint and deterministic baseline','baseline',[], 'Record source hash, 76 IDs, reference solutions, seed/profile isolation, game tests; export rollback ZIP.','legacy','G0/G1/G2','S'),
('PQ11-002','0','Introduce contract registry validator behind opt-in feature flag','contracts',['PQ11-001'],'Versioned request/result adapters retain all legacy grading paths; invalid/oversized worker outputs fail closed.','contract','G1','M'),
('PQ11-003','0','Add additive schema-4 program library and future-schema rejection','save',['PQ11-001'],'Old v2/v3/v4 fixtures preserve unknown fields; future version read-only; backup and atomic save tests.','save','G2','M'),
('PQ11-004','1','Observation snapshots, hashing and action semantic validation','contracts',['PQ11-002','PQ11-003'],'One immutable observation produces deterministic hash; reject stale state, invalid actions, walls, energy, unsupported devices.','contract','G1','L'),
('PQ11-005','1','Bounded fixed-tick game-owned action runner and event reducer','world',['PQ11-004'],'No learner code in Pygame loop; trace and replay deterministic, atomic milestones, cancel/restart harmless.','contract','G1/G2','L'),
('PQ11-006','1','Mica equip, library, deploy, replay and comparison','robot',['PQ11-005'],'Save/reopen a program, equip revision, deploy on 2 known maps, trace step, no repeated XP.','contract','G1/G2','L'),
('PQ11-007','1','In-game Mica flagship Orion quest and transfer puzzle','robot',['PQ11-006'],'Player discovers relay, programs robot, watches repair, reuses program on altered fixture; save/quit works.','travel','G1/G4','L'),
('PQ11-008','2','Polished HUD/readouts without map occlusion','ui',['PQ11-001'],'1280x720,1600x900,1920x1080 screenshots clear; world always primary, text/click targets visible, reduced motion.','visual','G4','M'),
('PQ11-009','2','Distinct original biome tile layers and consistent shadows','visual',['PQ11-008'],'Orion/Astra/Titan/Helix/Aurora have distinct reusable props and landmarks; depth sorts; no collisions regressed.','visual','G4','L'),
('PQ11-010','2','Travel and exploration narrative routing repair','world',['PQ11-008'],'Normal route no longer depends on unshipped Mission Control; preview still accessible; destination reveals objectives.','travel','G1/G2/G4','M'),
('PQ11-011','2','Device interaction catalog and visual coding feedback','world',['PQ11-005','PQ11-008'],'Machines accept validated intents; failure traces show reason; animated world delta clear and replayable.','contract','G1/G4','L'),
('PQ11-012','3','Shared data-driven mission factory for new challenge types','contracts',['PQ11-002','PQ11-005'],'Four mission templates tested: function, object fixture, simulation, bounded plan; authoring round-trip.','contract','G1','L'),
('PQ11-013','3','Chapter maps, travel gating and landmark objective system','world',['PQ11-010','PQ11-012'],'Each world has arrival, return, discoverable next objective, walkable route and locked feedback.','travel','G1/G4','L'),
('PQ11-014','3','Deterministic toy signal and mesh rendering adapter','helix_bio',['PQ11-002','PQ11-011'],'Synthetic fixtures load, null unmeasured, no NaN, units labelled, geometry responds to test outputs.','synthetic','G1/G4','L'),
('PQ11-015','4','Visual debugging playback, code editor hint ladder and error precision','ui',['PQ11-006','PQ11-008'],'Step-through trace with earliest failure; drafts preserved; review and comparison work; no unrelated editor regressions.','worker','G1/G4','M'),
('PQ11-016','9','Windows release, native QA, test evidence and recovery exports','baseline',['PQ11-001'],'Archive/static and Windows native start/saves/path spaces/offline/3 viewport captures; source ZIP + changelog.','release','G0/G1/G2/G3/G4/G6','M'),
]
for id,phase,name,seam,deps,done,area,gate,size in infras:
    ticket(id,phase,name,'system',deps,SEAMS[seam],done,anchor(area),gate,'high' if id in {'PQ11-004','PQ11-005','PQ11-016'} else 'medium',size)
# create 19 four-mission tickets, sequencing dependencies; initial workshop after platform
phase={'workshop':'4','titan_cloud':'5','helix_bio':'6','algorithm_tower':'7','aurora_ep':'8','mission_control':'9'}
ordered=['workshop','titan_cloud','helix_bio','algorithm_tower','aurora_ep','mission_control']
previous_for_zone={}
for zone in ordered:
  rows=sorted([m for m in missions if m['zone']==zone],key=lambda r:int(r['sequence']))
  for i in range(0,len(rows),4):
    chunk=rows[i:i+4];ids=[f"{zone}_{int(m['sequence']):02d}" for m in chunk]
    tid=f'PQ11-{101+len(mapping):03d}'
    prereqs=['PQ11-012','PQ11-013']
    if zone in ('helix_bio','aurora_ep'):prereqs.append('PQ11-014')
    if zone in ('titan_cloud','mission_control'):prereqs.append('PQ11-011')
    if zone in previous_for_zone:prereqs.append(previous_for_zone[zone])
    if zone=='mission_control' and i==0:
      prereqs.extend([previous_for_zone[k] for k in ['workshop','titan_cloud','helix_bio','algorithm_tower','aurora_ep']])
    chapter,learning,world,areas_text=meta[zone]
    done=f"Implement {', '.join(ids)} using blueprint APIs and edge cases, each with real worker evaluation, parent semantic checks, visible {world} effect, sequential prerequisites, no duplicate XP, save/replay and error feedback. Four reference solutions and negative/edge fixtures pass."
    qa=';'.join(dict.fromkeys(sum((areas[a][:2] for a in areas_text.split(';')),[])))
    ticket(tid,phase[zone],f'{chapter} missions {chunk[0]["sequence"]}–{chunk[-1]["sequence"]}', 'mission_batch', sorted(set(prereqs)), SEAMS[zone]+';src/python_quest_2d/core/challenges.py;src/python_quest_2d/core/grade.py',done,qa,'G1/G2/G4','high' if zone in ('aurora_ep','mission_control') else 'medium','M',ids, f'commit {tid} + verified 4-mission results + source archive at chapter boundary',f'{learning}; {world}.')
    previous_for_zone[zone]=tid
    for m,mid in zip(chunk,ids):
      mapping.append(dict(mission_id=mid,ticket_id=tid,world=zone,sequence=int(m['sequence']),title=m['title'],python_topic=m['topic'],api=m['api'],objective=m['player_action'],in_world_result=m['world_effect'],edge_cases=m['edge_cases'],sample=m['example'],tier=int(m['tier']),worker_execution='isolated worker',game_validation='parent semantically validates plain JSON result',prerequisite=(f'{zone}_{int(m["sequence"])-1:02d}' if int(m['sequence'])> (9 if zone=='workshop' else 5 if zone in ('titan_cloud','helix_bio','aurora_ep') else 1) else 'existing-world-intro-or-new-chapter-gate'),grading='visible+hidden cases; never source-pattern-only',acceptance_test_ids=qa,source_seam=SEAMS[zone],status='PLANNED_NOT_IMPLEMENTED'))
assert len(mapping)==76,(len(mapping),collections.Counter(x['world'] for x in mapping))
# extra systems after mission completions
completion_deps=list(previous_for_zone.values())
ticket('PQ11-017','9','Unified multi-world postgame and mastery transfer challenges','system',completion_deps,'src/python_quest_2d/game/expedition.py;src/python_quest_2d/game/app.py','All chapters accessible in intended narrative order, preview travel safe, program library reusable in two more worlds, mastery review without XP farming.',anchor('travel'),'G1/G2/G4','medium','L')
ticket('PQ11-018','9','Human playtest triage, accessibility and final performance budget','system',['PQ11-008','PQ11-009','PQ11-017'],SEAMS['ui'],'Record actual novice/returning-player observations; demonstrate no critical overlap, softlocks and unresolved P0; measured p95 FPS on stated hardware.',anchor('manual')+';'+anchor('performance'),'G4/G5','high','M')
# release final must come after 018 and all chapter ticket completion
for t in tickets:
 if t['ticket_id']=='PQ11-016':t['depends_on']=['PQ11-018']+completion_deps
# Source map and id refs
assert len({t['ticket_id'] for t in tickets})==len(tickets)
allids={t['ticket_id'] for t in tickets}
assert all(set(t['depends_on']) <= allids for t in tickets)
# detect dependency cycles via topo
pending={t['ticket_id']:set(t['depends_on']) for t in tickets};topo=[]
while pending:
 ready=sorted([a for a,b in pending.items() if not b],key=lambda x:next(i for i,t in enumerate(tickets) if t['ticket_id']==x))
 if not ready:raise AssertionError(f'cycles {pending}')
 for id in ready:
  topo.append(id);pending.pop(id)
 for deps in pending.values():deps.difference_update(ready)
order={tid:i for i,tid in enumerate(topo)}
# ensure gate mapping includes actual Stage10 IDs
stage10ids={r['test_id'] for r in acceptance}
for t in tickets:
 assert set(t['stage10_tests'].split(';'))<=stage10ids,(t['ticket_id'],t['stage10_tests'])
 assert all((SRC/p).exists() for p in t['source_anchors'].split(';')),(t['ticket_id'],t['source_anchors'])

# write TSV/CSV and JSON
sprint=B/'backlog';sprint.mkdir(exist_ok=True)
def csv_out(p,rows,cols):
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
cols=list(tickets[0].keys());csvrows=[{**t,'depends_on':';'.join(t['depends_on']),'mission_ids':';'.join(t['mission_ids'])} for t in tickets]
csv_out(sprint/'11_IMPLEMENTATION_TICKETS.csv',csvrows,cols)
csv_out(sprint/'11_MISSION_TO_TICKET.csv',mapping,list(mapping[0]))
json_out=dict(schema_version=1,status='DESIGN_ONLY',baseline='v1.4 76 implemented; schema 4',new_missions=76,plan_target=152,stages=['stabilize','programmable worlds','visual and travel','mission infrastructure','workshop','titan','helix','algorithm tower','aurora','finale'],tickets=tickets,topological_order=topo,source_root='Python Quest 2D/',authoritative_docs=['docs/03_PROGRAMMABLE_WORLD.md','docs/07_CURRICULUM_AND_ASSESSMENT.md','docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md','docs/10_TEST_AND_RELEASE_PLAN.md'],provenance='planning, not implementation')
write(sprint/'11_IMPLEMENTATION_TICKETS.json',json.dumps(json_out,indent=2)+'\n')
checkpoints={
 '0':'Baseline SHA256; 76 IDs and XP; disposable schema2/3/4 fixtures; original ZIP','1':'Flag-off legacy regressions and verified Mica plan replay with no parent-side Python execution',
 '2':'Three viewport captures per world; UI overlap log; reachable travel, entry and exits',
 '3':'Four authoring templates; worker/parent boundary; no duplicate XP; synthetic fixture repeatability',
 '4':'Workshop 09-16 source archive + restoration save + object tests',
 '5':'Titan 05-16 source archive + deterministic packet replay',
 '6':'Helix 05-16 source archive + signal fixture replay with unit labels',
 '7':'Algorithm Tower 01-16 source archive + graph optimality tests',
 '8':'Aurora 05-16 source archive + null/unmeasured mesh tests',
 '9':'Mission Control 01-16 + campaign end + native Windows release gates'}
write(sprint/'11_CHECKPOINT_AND_ROLLBACK.json',json.dumps(dict(status='PROPOSED_POLICY',rules=['Before any system or chapter batch preserve source checkpoint and disposable profile, not player live save','Rollback only to last tested checkpoint with source/fixtures and hashes; never overwrite unknown save fields','For new features disable feature flag on failure and allow original 76 to remain playable','Never mark entire campaign released without G0/G1/G2/G3/G4/G6 native evidence'],checkpoints=checkpoints,delivery=['source archive','SHA256','passing targeted tests','relevant Stage10 gate evidence','known failing tests','new mission count verified'],stop_ship=['source missing or partial','legacy save corruption','untrusted result mutates world','XP duplication','Windows startup failure','critical UI occlusion or softlock']),indent=2)+'\n')
# comprehensive source verified ownership notes
ownership='''# Stage 11 — Source ownership and implementation seams\n\nOnly existing files below are claimed to exist. **Additive modules are proposed paths**, not already implemented. Read `docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md` before editing.\n\n| Domain | Existing source and responsibility | Recommended additive module | Contract/test gate |\n|---|---|---|---|\n'''
seam_details=[
('Evaluation and content','core/challenges.py; core/grade.py; core/worker.py','core/program_contracts.py','adapt version 1 JSON to legacy grade; reject invalid returns; preserve original mission evaluator'),
('Profile / XP','core/progress.py','core/program_library.py','atomic save, future schema no overwrite, idempotent completion'),
('Robot route','core/route.py; game/nursery.py','game/program_runner.py; core/action_validator.py','bounds/collision/energy/snapshot hash; fixed tick; independent parent checks'),
('Travel','game/expedition.py; game/world.py','game/travel_routes.py','gating/entry/recovery, legacy completion and preview travel'),
('HUD / diagnostics','ui/hud.py; game/diagnostics.py; ui/code_editor.py','ui/replay_view.py','trace, failure UI, accessible focus, 3 resolutions'),
('Environment','game/pixel_world.py; game/planet_art.py; game/presentation.py; game/workshop_art.py','game/biome_layers.py','original art, depth/collision/clear hierarchy'),
('Biomedical','game/instruments.py; core/engineering_cases.py','core/synthetic_pipeline.py; game/mapping_view.py','fixtures/units/no NaN/nullable missing no clinical data'),
('World state','game/app.py; game/expedition.py','game/world_event_reducer.py','single authority for state mutations and XP milestone')]
for domain,old,new,g in seam_details:
 ownership+=f'| {domain} | `{old}` | `{new}` | {g} |\n'
ownership+='\n**Review rule:** verify an actual file/method on the checked-out latest source before changing it; if Work has a newer tree than v1.4, refresh this matrix without rewriting existing features.\n'
write(sprint/'11_SOURCE_OWNERSHIP.md',ownership)
# manuscript
phase_names={'0':'Protect baseline','1':'Programmable Mica vertical slice','2':'Game feel, visuals and navigation','3':'Reusable mission authoring and world surfaces','4':'Workshop completing OOP','5':'Titan networking','6':'Helix synthetic signal lab','7':'Algorithm Tower','8':'Aurora toy mapping','9':'Integration finale and release'}
md='''# 11 — Development Sequencing and Sprint Backlog\n\n**Status: preproduction planning only.** Based on authoritative v1.4 game, 76 already playable + 76 planned = proposed total 152. Save schema 4. No new runtime game features have been implemented by this stage.\n\n## Non-negotiable execution principle\n\nBuild **one complete, replayable and visibly reactive Python-powered encounter** before multiplying content. Every four-mission batch must have a functioning world object, true worker grading, parent validation, test fixtures, XP-safe effect, and a rollback checkpoint. Never inflate a mission count from blueprint JSON files alone. Each chapter is gated by real automated and interactive checks.\n\n## Dependencies and development order\n\n- Phase 0: baseline and schema guard.\n- Phase 1: save-owned programs + action validator + fixed tick + Mica flagship quest.\n- Phase 2: readable UI and a distinct world visual grammar; fix preview travel gating and discovery.\n- Phase 3: reusable content factory and contract-driven devices.\n- Phases 4–9: staged content rollout in the order below, with chapter rollback.\n\n**The mission target is not the delivery gate.** Gate on meaningful gameplay, compatibility and testing, not a raw content count. Existing 76 IDs stay unchanged.\n\n## Explicit stage gates\n\n| Phase | Named gate | Objective proof | If failing |\n|---|---|---|---|\n'''
for ph,label in phase_names.items():
 md+=f'| {ph} | {label} | {checkpoints[ph]} | Stop batch; preserve failing trace and roll back only changed feature |\n'
md+='\n## Task cards and dependency order\n\nEach ticket below is authoritative with full detail in `backlog/11_IMPLEMENTATION_TICKETS.json` and links to Stage10 test IDs. Source files are paths **inside** project root.\n\n'
for ph,label in phase_names.items():
 subset=[t for t in tickets if t['phase']==ph]
 md+=f'### Phase {ph}: {label}\n\n'
 for t in subset:
  md+=f'**{t["ticket_id"]} — {t["task"]}** ({t["effort"]}; {t["risk"]} risk). Depends on: {", ".join(t["depends_on"]) or "baseline"}.\n\n'
  if t['mission_ids']:md+=f'Planned missions: {", ".join(t["mission_ids"])}.\n\n'
  md+=f'- Source: `{t["source_anchors"]}`\n- Acceptance: {t["acceptance"]}\n- QA: {t["stage10_tests"]}; gates {t["release_gates"]}.\n- Checkpoint: {t["checkpoint"]}.\n\n'
md+='''## Mission-by-mission traceability\n\n`backlog/11_MISSION_TO_TICKET.csv` is the machine-readable authoritative join of every proposed mission to its four-mission ticket, API, Python concept, world effect, cases, source seam and Stage10 references. All 76 rows have unique stable IDs. This does **not** imply those IDs exist in the game yet. Use `missions/mission_blueprints.psv` for detailed learning task wording and `missions/biomed_24_contracts.csv` for clarified Helix/Aurora signatures where they conflict.\n\n## Ticket definition of done\n\n1. Implement real learner-authorable Python challenge; run reference solution on all visible and hidden tests.\n2. Show a failure test and ensure no XP/state mutation on invalid response.\n3. Validate result plain data in *game process* against a fresh snapshot and state machine.\n4. Demonstrate a world-visible effect with replay and accurate error feedback.\n5. Save then restart on disposable profile, verify no replay XP and preservation of unrelated flags.\n6. Run relevant Stage10 IDs and existing regression subset; note **unexecuted** checks explicitly.\n7. Commit + source archive and update `PROJECT_STATE.md` with exact mission count, changed paths and known issues.\n8. Do not repackage full Windows runtime on every four missions; package at chapter or major playable milestone, plus final release.\n\n## Defer without hiding\n\n- Physically based 3D and Qt/real hardware medical device connectivity: out of scope; Pygame synthetic toy mapping only.\n- Multiplayer, cloud saves, online leaderboards, unrestricted code mods: out of scope.\n- Native Windows launch, audio and human UX proof: not verifiable by design documents; defer to execution platform.\n- If a full chapter becomes infeasible, ship last validated four-mission slice and accurate incomplete status, not placeholder missions counted as complete.\n\n## Precise failure response and fallback\n\n- Worker timeout/exception/unexpected JSON: diagnostic + no state mutation; save draft; offer retry.\n- Stale program/world hash: reject deployment + request revalidation; keep verified program revision and draft.\n- Crashed/restarted deployment: resume last *atomic* committed world checkpoint; do not reaward XP.\n- Missing or future schema: quarantine or read-only; back up before migration; never destroy unknown fields.\n- World route locked: explanatory tooltip and reachable safe return, not hard block or silent teleport.\n- Visual regression: stop when UI occlusion blocks movement/interactions at any target viewport; preserve last passing visuals.\n\n## Measurement and evidence\n\nEach sprint records git/source hash; test command and counts; screenshot/trace evidence; saved profile test path; performance samples if taken; before/after mission IDs; latest release gate status (G0–G6). No tests in this planning stage prove the future missions are playable.\n'''
write(B/'docs/11_DEVELOPMENT_SEQUENCING.md',md)
# QA matrix per ticket
qa_map=[]
for t in tickets:
 for c in t['stage10_tests'].split(';'):
  qa_map.append(dict(ticket_id=t['ticket_id'],stage10_test_id=c,gate=t['release_gates'],evidence_required='actual runtime test log, screenshot/trace or disposable profile as appropriate',planned_only=True))
csv_out(sprint/'11_TICKET_QA_TRACEABILITY.csv',qa_map,list(qa_map[0]))
# tests plan
unit='''import csv, json, unittest\nfrom pathlib import Path\nBASE=Path(__file__).resolve().parents[1]\nSROOT=Path('/mnt/data/pq_stage09_source')\nclass Stage11PlanningTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.data=json.loads((BASE/'backlog/11_IMPLEMENTATION_TICKETS.json').read_text())\n        cls.tickets=cls.data['tickets']\n        cls.missions=list(csv.DictReader((BASE/'backlog/11_MISSION_TO_TICKET.csv').open()))\n        cls.acceptance={r['test_id'] for r in csv.DictReader((BASE/'qa/10_ACCEPTANCE_CATALOG.csv').open())}\n    def test_baseline_and_counts(self):\n        self.assertEqual(self.data['new_missions'],76)\n        self.assertEqual(self.data['plan_target'],152)\n        self.assertEqual(len(self.missions),76)\n    def test_unique_missions(self):\n        mids=[m['mission_id'] for m in self.missions]\n        self.assertEqual(len(set(mids)),76)\n        self.assertEqual({z:sum(m['world']==z for m in self.missions) for z in set(m['world'] for m in self.missions)}, {'workshop':8,'algorithm_tower':16,'mission_control':16,'titan_cloud':12,'helix_bio':12,'aurora_ep':12})\n    def test_four_mission_batches(self):\n        for t in self.tickets:\n            if t['kind']=='mission_batch': self.assertEqual(len(t['mission_ids']),4)\n    def test_every_mission_joins_ticket(self):\n        ids={t['ticket_id'] for t in self.tickets}\n        self.assertTrue(all(m['ticket_id'] in ids for m in self.missions))\n        self.assertEqual({mid for t in self.tickets for mid in t['mission_ids']},{m['mission_id'] for m in self.missions})\n    def test_dependencies_exist_and_dag(self):\n        ids={t['ticket_id'] for t in self.tickets}\n        self.assertEqual(len(ids),len(self.tickets))\n        done=set()\n        for tid in self.data['topological_order']:\n            t=next(t for t in self.tickets if t['ticket_id']==tid)\n            self.assertTrue(set(t['depends_on'])<=done,tid)\n            done.add(tid)\n        self.assertEqual(done,ids)\n    def test_stage10_references(self):\n        for t in self.tickets:\n            self.assertTrue(set(t['stage10_tests'].split(';'))<=self.acceptance,t['ticket_id'])\n    def test_exact_source_anchors(self):\n        if not SROOT.is_dir(): self.skipTest('source not locally mounted; pass PQ11_SOURCE_ROOT')\n        for t in self.tickets:\n            self.assertTrue(all((SROOT/path).exists() for path in t['source_anchors'].split(';')),t['ticket_id'])\n    def test_interface_and_edge_cases_per_mission(self):\n        for m in self.missions:\n            for key in ['api','edge_cases','in_world_result','grading','source_seam']:\n                self.assertTrue(m[key].strip(),(m['mission_id'],key))\n    def test_design_status_not_runtime(self):\n        self.assertTrue(all(t['status']=='PLANNED_NOT_IMPLEMENTED' for t in self.tickets))\n    def test_stage09_contracts_retained(self):\n        registry=json.loads((BASE/'engineering/09_CONTRACT_REGISTRY.json').read_text())\n        self.assertIsInstance(registry,dict)\n        self.assertEqual(len(list((BASE/'engineering/schemas').glob('*.schema.json'))),13)\n    def test_gate_statuses(self):\n        allowed={f'G{i}' for i in range(7)}\n        self.assertTrue(all(set(t['release_gates'].split('/'))<=allowed for t in self.tickets))\n    def test_biomed_contract_coverage(self):\n        rows=list(csv.DictReader((BASE/'missions/biomed_24_contracts.csv').open()))\n        self.assertEqual(len(rows),24)\n        self.assertEqual(sum(m['world'] in ('helix_bio','aurora_ep') for m in self.missions),24)\nif __name__=='__main__': unittest.main()\n'''
unit=unit.replace("SROOT=Path('/mnt/data/pq_stage09_source')","import os\nSROOT=Path(os.environ.get('PQ11_SOURCE_ROOT','/mnt/data/pq_stage09_source'))")
write(B/'tests/test_stage11_planning.py',unit)
# docs index update after tests outside
print('TICKETS',len(tickets),'MISSION BATCHES',sum(t['kind']=='mission_batch' for t in tickets),'MAPPING',len(mapping),'QA LINKS',len(qa_map))
