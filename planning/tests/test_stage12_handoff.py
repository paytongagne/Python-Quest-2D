import csv,json,pathlib,sys,tempfile,unittest,subprocess,copy
BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'tools'))
import work_ticket

class HandoffTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=json.loads((BASE/'backlog/11_IMPLEMENTATION_TICKETS.json').read_text())
  cls.state=json.loads((BASE/'handoff/12_TASK_STATE.json').read_text())
  with (BASE/'qa/10_ACCEPTANCE_CATALOG.csv').open() as f:
   cls.qa={r['test_id'] for r in csv.DictReader(f)}
  cls.gates={g['id'] for g in json.loads((BASE/'release/10_RELEASE_GATES.json').read_text())['gates']}
 def test_all_tickets_present_in_state(self):
  self.assertEqual({t['ticket_id'] for t in self.catalog['tickets']},set(self.state['ticket_states']))
 def test_first_eligible_is_baseline(self):
  self.assertEqual([t['ticket_id'] for t in work_ticket.eligible(self.catalog,self.state)],['PQ11-001'])
 def test_all_QA_case_ids_exist(self):
  for t in self.catalog['tickets']:
   self.assertTrue(set(t['stage10_tests'].split(';')).issubset(self.qa),t['ticket_id'])
 def test_all_gates_exist(self):
  for t in self.catalog['tickets']:
   self.assertTrue(set(t['release_gates'].split('/')).issubset(self.gates),t['ticket_id'])
 def test_76_missions_19_batches(self):
  batches=[t for t in self.catalog['tickets'] if t['kind']=='mission_batch']
  self.assertEqual(len(batches),19)
  mids=[m for t in batches for m in t['mission_ids']]
  self.assertEqual(len(mids),76);self.assertEqual(len(set(mids)),76)
 def test_model_policy_no_fake_cost(self):
  models=json.loads((BASE/'handoff/12_MODEL_ASSIGNMENTS.json').read_text())
  self.assertIn('UI dependent',models['note']);self.assertTrue(models['policy']['no_automatic_credit_spending'])
 def test_reading_context_lists_real_source(self):
  s=(BASE/'handoff/12_REPOSITORY_CONTEXT.md').read_text()
  for part in ['core/worker','game','schema 4','76','Work']:
   self.assertIn(part,s)
 def test_prompt_collection_complete(self):
  man=json.loads((BASE/'handoff/12_HANDOFF_MANIFEST.json').read_text())
  self.assertEqual(len(man['prompt_files']),5)
  self.assertTrue(all((BASE/p).exists() for p in man['prompt_files']))
 def test_bad_evidence_rejected(self):
  t=self.catalog['tickets'][0];e=json.loads((BASE/'handoff/12_EVIDENCE_TEMPLATE.json').read_text());self.assertIsNotNone(work_ticket.evidence_ok(t,e))
 def test_structural_good_evidence_accepted(self):
  t=self.catalog['tickets'][0];e=json.loads((BASE/'handoff/12_EVIDENCE_TEMPLATE.json').read_text())
  e.update(source_sha256='f'*64,test_runs=[{'command':'python -m pytest','host':'headless-linux','exit_code':0,'passed':3,'failed':0,'log_path':'test.log'}]);e['applicable_stage10_cases']=t['stage10_tests'].split(';')
  self.assertIsNone(work_ticket.evidence_ok(t,e))
 def test_cli_brief(self):
  out=subprocess.check_output([sys.executable,str(BASE/'tools/work_ticket.py'),'brief','PQ11-001'],text=True)
  obj=json.loads(out);self.assertEqual(obj['id'],'PQ11-001');self.assertTrue(obj['source_anchors'])
 def test_cli_dependency_enforcement(self):
  with tempfile.TemporaryDirectory() as td:
   state=pathlib.Path(td)/'state.json';state.write_text(json.dumps(self.state))
   cmd=[sys.executable,str(BASE/'tools/work_ticket.py'),'start','PQ11-004','--state',str(state)]
   proc=subprocess.run(cmd,capture_output=True,text=True)
   self.assertNotEqual(proc.returncode,0);self.assertEqual(json.loads(state.read_text())['ticket_states']['PQ11-004'],'PLANNED')
 def test_cli_rejects_premature_done(self):
  with tempfile.TemporaryDirectory() as td:
   state=pathlib.Path(td)/'state.json';state.write_text(json.dumps(self.state))
   cmd=[sys.executable,str(BASE/'tools/work_ticket.py'),'done','PQ11-001','--state',str(state)]
   proc=subprocess.run(cmd,capture_output=True,text=True)
   self.assertNotEqual(proc.returncode,0)
 def test_cli_start_then_block(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/'state.json';p.write_text(json.dumps(self.state))
   b=[sys.executable,str(BASE/'tools/work_ticket.py')]
   self.assertEqual(subprocess.run(b+['start','PQ11-001','--state',str(p)],capture_output=True).returncode,0)
   self.assertEqual(subprocess.run(b+['block','PQ11-001','--state',str(p),'--reason','fixture missing'],capture_output=True).returncode,0)
   self.assertEqual(json.loads(p.read_text())['ticket_states']['PQ11-001'],'BLOCKED')
 def test_failed_ticket_retry(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/"state.json";p.write_text(json.dumps(self.state))
   b=[sys.executable,str(BASE/"tools/work_ticket.py")]
   for args in [("start","PQ11-001"),("fail","PQ11-001","--reason","test assertion"),("retry","PQ11-001")]:
    self.assertEqual(subprocess.run(b+list(args)+["--state",str(p)],capture_output=True).returncode,0,args)
   self.assertEqual(json.loads(p.read_text())["ticket_states"]["PQ11-001"],"IN_PROGRESS")
 def test_no_modified_game_code(self):
  man=json.loads((BASE/'handoff/12_HANDOFF_MANIFEST.json').read_text())
  self.assertFalse(man['game_source_modified']);self.assertFalse(man['native_windows_verified'])
 def test_progress_doc_design_boundary(self):
  s=(BASE/'docs/12_WORK_MODE_EXECUTION.md').read_text()
  for p in ['not a secure sandbox','76 implemented','Stage 13','Actual Windows','banked resets','source checksum']:
   self.assertIn(p,s)

if __name__=='__main__':unittest.main()
