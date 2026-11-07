"""Stage13 planning and v1.4 source audit checks; NOT newly implemented gameplay tests."""
from pathlib import Path
import unittest, json, csv, os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
class Stage13Readiness(unittest.TestCase):
 def test_manifest(self):
  m=read('audit/13_SOURCE_MANIFEST.json');self.assertEqual(m['lessons'],76);self.assertEqual(m['maps'],12);self.assertEqual(m['save_schema'],4);self.assertEqual(len(m['original_lesson_ids']),76)
 def test_crosscheck(self):
  x=read('audit/13_DESIGN_CROSSCHECK.json');self.assertEqual(x['audit_status'],'PASS');self.assertFalse(x['problems']);self.assertEqual(x['planned_existing_overlap'],[])
 def test_ticket_count(self):
  t=read('backlog/11_IMPLEMENTATION_TICKETS.json')['tickets'];self.assertEqual(len(t),37);self.assertEqual(len([i for i in t if i['mission_ids']]),19)
 def test_ticket_missions_unique(self):
  t=read('backlog/11_IMPLEMENTATION_TICKETS.json')['tickets'];ids=[m for i in t for m in i['mission_ids']];self.assertEqual(len(ids),76);self.assertEqual(len(set(ids)),76)
 def test_risks_and_owner(self):
  rr=read('audit/13_RISK_REGISTER.json');self.assertGreaterEqual(len(rr),12);t={i['ticket_id'] for i in read('backlog/11_IMPLEMENTATION_TICKETS.json')['tickets']};self.assertTrue(all(i['mitigation_ticket'] in t for i in rr));self.assertGreaterEqual(len([r for r in rr if r['priority']=='P0']),3)
 def test_decisions_unique(self):
  d=read('audit/13_DECISION_LOG.json');self.assertEqual(len({i['decision_id'] for i in d}),len(d));self.assertGreaterEqual(len(d),10)
 def test_gates_complete(self):
  g={i['id'] for i in read('release/10_RELEASE_GATES.json')['gates']};self.assertEqual(g,{f'G{i}' for i in range(7)})
 def test_no_false_implementation_claim(self):
  s=read('handoff/12_TASK_STATE.json');self.assertEqual(s['completed_tickets'],[]);self.assertEqual(s['implemented_new_mission_ids'],[]);self.assertIn('DESIGN',s['status']);
 def test_ready_documentation(self):
  for p in ['docs/13_RISKS_AND_DECISIONS.md','release/13_GO_NO_GO_CHECKLIST.md','handoff/13_FINAL_WORK_READ_FIRST.md','prompts/13_FINAL_MINIMAL_STARTUP.md']:
   self.assertGreater((ROOT/p).stat().st_size,450,p)
 def test_backend_semantics_protected(self):
  d=(ROOT/'docs/13_RISKS_AND_DECISIONS.md').read_text();self.assertIn('100 unhinted / 75 hinted / 25',d);self.assertIn('future',d);self.assertIn('worker',d);self.assertIn('G0–G6',d)
 def test_readiness_not_false_release(self):
  r=read('release/13_READINESS_MATRIX.json');self.assertTrue(any(x['status']=='NOT_RUN' for x in r));self.assertTrue(any('CONDITIONAL' in x['status'] for x in r))
 def test_crosscheck_gate_links(self):
  with (ROOT/'qa/10_ACCEPTANCE_CATALOG.csv').open() as f:
   ids={i['test_id'] for i in csv.DictReader(f)}
  self.assertEqual(len(ids),86)
  ts=read('backlog/11_IMPLEMENTATION_TICKETS.json')['tickets']
  self.assertTrue(all(q in ids for t in ts for q in t['stage10_tests'].split(';') if q))
if __name__=='__main__':unittest.main()
