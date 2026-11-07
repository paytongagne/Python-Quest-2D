"""Export ticket source and evidence, then finalize ledger through its dependency-aware tool."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,sys,subprocess,datetime,platform
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from python_quest_2d.core.challenges import LESSONS
TICKET=sys.argv[1];target=ROOT/'checkpoints'/('000'+TICKET[-1]+'_'+TICKET)
run=json.loads((target/'RUN.json').read_text());assert run['exit_code']==0 and run['passed']>0
statepath=ROOT/'handoff/12_TASK_STATE.json'
catalog=json.loads((ROOT/'planning/backlog/11_IMPLEMENTATION_TICKETS.json').read_text())
ticket=next(t for t in catalog['tickets'] if t['ticket_id']==TICKET)
ids=sorted(LESSONS);assert len(ids)==76
(target/'MISSION_IDS.json').write_text(json.dumps(ids,indent=2))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
changes={
'PQ11-001':'Compared supplied game with current v1.4: all files identical. Preserved baseline; added real worker/effect/replay coverage for every mission and durable isolated test runner. Initial test teardown error fixed; failed log retained.',
'PQ11-002':'Opt-in versioned legacy request/result adapter, bounded worker output transport, contract registry and pure action-plan validation. Feature remains OFF by default; no live Mica deployment authorization added.',
'PQ11-003':'Additive program library/runtime defaults, unknown-key preservation, future-version write refusal, non-destructive recovery and atomic-write coverage. No learner progress reset.'}
(ROOT/'docs/PROJECT_STATE.md').write_text(f'''# Protected development checkpoint {TICKET}
- Existing v1.4 source; 76 playable missions; 76 future missions remain planned.
- Ticket workflow: planning/handoff/13_FINAL_WORK_READ_FIRST.md.
- Authoritative ledger: handoff/12_TASK_STATE.json; use tools/work_ticket.py next.
- Current work: {changes[TICKET]}
- Save schema stays 4. Real player save remains untouched by tests.
- Checkpoints contain source.zip, SHA256, TASK_STATE.json, TEST_LOG.txt, QA_EVIDENCE.json and recovery notes.
- Source archive SHA256 and ledger checksum are in checkpoints/CURRENT.json.
- These are development checkpoints; full Stage10 release gates are not asserted passed.
- G0 source inventory verified. G1/G2 ticket evidence only; wider gates remain partial.
- G3 Windows integration, G4 UX/performance and G5 human sessions NOT RUN for this checkpoint.
- G6 source integrity verified; a final Windows candidate is not declared.
- Prior v1.4 Windows artifacts remain in outputs and retain their historical test reports.
- Do not regenerate prior content or overwrite player saves from planning templates.
''',encoding='utf8')
archive=target/'source.zip';assert not archive.exists(),'Checkpoint source already exists; never replace immutable checkpoint'
manifest={}
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if not p.is_file() or any(part in ('runtime','checkpoints','__pycache__','.ruff_cache') for part in rel.parts):continue
  data=p.read_bytes();z.writestr('Python Quest 2D/'+rel.as_posix(),data);manifest[rel.as_posix()]=hashlib.sha256(data).hexdigest()
with ZipFile(archive) as z:assert z.testzip() is None
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
(target/'SOURCE_SHA256.txt').write_text(sha+'  source.zip\n')
(target/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
evidence=dict(ticket_id=TICKET,source_sha256=sha,checkpoint_path=str(archive.relative_to(ROOT)),test_runs=[run]+([json.loads((target/"PLANNING_RUN.json").read_text())] if (target/"PLANNING_RUN.json").exists() else []),mission_ids_validated=ids,applicable_stage10_cases=ticket['stage10_tests'].split(';'),results_note=changes[TICKET],gates={'G0':'PASS','G1':'PARTIAL: ticket scope passed; all Stage08-10 release suites not run','G2':'PARTIAL: ticket/legacy coverage only','G3':'NOT RUN on current checkpoint','G4':'NOT RUN on current checkpoint','G5':'NOT RUN: human session required','G6':'PARTIAL: source ZIP CRC/SHA256 verified; no final Windows release'})
(target/'QA_EVIDENCE.json').write_text(json.dumps(evidence,indent=2))
(target/'CHANGES.md').write_text(changes[TICKET]+'\nNo mission IDs added.\n')
(target/'RECOVERY.md').write_text('Verify SOURCE_SHA256.txt, extract source.zip into a new folder, then restore TASK_STATE.json to handoff/12_TASK_STATE.json. The archive captures IN_PROGRESS immediately before verified finalization; the external ledger records DONE. Install requirements.txt and run play.py, or use the prior bundled runtime. Never replace a live player save.\n')
subprocess.run([sys.executable,str(ROOT/'tools/work_ticket.py'),'done',TICKET,'--evidence',str(target/'QA_EVIDENCE.json')],check=True)
state=json.loads(statepath.read_text());state.update(status='ACTIVE_WORK_IMPLEMENTATION',source_checkpoint=str(target.relative_to(ROOT)),last_updated_utc=now,note='Actual executed test evidence; no added mission IDs yet.')
statepath.write_text(json.dumps(state,indent=2))
(target/'TASK_STATE.json').write_bytes(statepath.read_bytes())
current=dict(ticket=TICKET,checkpoint=str(target.relative_to(ROOT)),source_sha256=sha,task_state_sha256=hashlib.sha256(statepath.read_bytes()).hexdigest(),mission_count=76,updated_utc=now)
tmp=ROOT/'checkpoints/CURRENT.tmp';tmp.write_text(json.dumps(current,indent=2));tmp.replace(ROOT/'checkpoints/CURRENT.json')
print(json.dumps(current,indent=2))
