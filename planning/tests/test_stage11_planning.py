import csv, json, unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
import os
SROOT=Path(os.environ.get('PQ11_SOURCE_ROOT','/mnt/data/pq_stage09_source'))
class Stage11PlanningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((BASE/'backlog/11_IMPLEMENTATION_TICKETS.json').read_text())
        cls.tickets=cls.data['tickets']
        cls.missions=list(csv.DictReader((BASE/'backlog/11_MISSION_TO_TICKET.csv').open()))
        cls.acceptance={r['test_id'] for r in csv.DictReader((BASE/'qa/10_ACCEPTANCE_CATALOG.csv').open())}
    def test_baseline_and_counts(self):
        self.assertEqual(self.data['new_missions'],76)
        self.assertEqual(self.data['plan_target'],152)
        self.assertEqual(len(self.missions),76)
    def test_unique_missions(self):
        mids=[m['mission_id'] for m in self.missions]
        self.assertEqual(len(set(mids)),76)
        self.assertEqual({z:sum(m['world']==z for m in self.missions) for z in set(m['world'] for m in self.missions)}, {'workshop':8,'algorithm_tower':16,'mission_control':16,'titan_cloud':12,'helix_bio':12,'aurora_ep':12})
    def test_four_mission_batches(self):
        for t in self.tickets:
            if t['kind']=='mission_batch': self.assertEqual(len(t['mission_ids']),4)
    def test_every_mission_joins_ticket(self):
        ids={t['ticket_id'] for t in self.tickets}
        self.assertTrue(all(m['ticket_id'] in ids for m in self.missions))
        self.assertEqual({mid for t in self.tickets for mid in t['mission_ids']},{m['mission_id'] for m in self.missions})
    def test_dependencies_exist_and_dag(self):
        ids={t['ticket_id'] for t in self.tickets}
        self.assertEqual(len(ids),len(self.tickets))
        done=set()
        for tid in self.data['topological_order']:
            t=next(t for t in self.tickets if t['ticket_id']==tid)
            self.assertTrue(set(t['depends_on'])<=done,tid)
            done.add(tid)
        self.assertEqual(done,ids)
    def test_stage10_references(self):
        for t in self.tickets:
            self.assertTrue(set(t['stage10_tests'].split(';'))<=self.acceptance,t['ticket_id'])
    def test_exact_source_anchors(self):
        if not SROOT.is_dir(): self.skipTest('source not locally mounted; pass PQ11_SOURCE_ROOT')
        for t in self.tickets:
            self.assertTrue(all((SROOT/path).exists() for path in t['source_anchors'].split(';')),t['ticket_id'])
    def test_interface_and_edge_cases_per_mission(self):
        for m in self.missions:
            for key in ['api','edge_cases','in_world_result','grading','source_seam']:
                self.assertTrue(m[key].strip(),(m['mission_id'],key))
    def test_design_status_not_runtime(self):
        self.assertTrue(all(t['status']=='PLANNED_NOT_IMPLEMENTED' for t in self.tickets))
    def test_stage09_contracts_retained(self):
        registry=json.loads((BASE/'engineering/09_CONTRACT_REGISTRY.json').read_text())
        self.assertIsInstance(registry,dict)
        self.assertEqual(len(list((BASE/'engineering/schemas').glob('*.schema.json'))),13)
    def test_gate_statuses(self):
        allowed={f'G{i}' for i in range(7)}
        self.assertTrue(all(set(t['release_gates'].split('/'))<=allowed for t in self.tickets))
    def test_biomed_contract_coverage(self):
        rows=list(csv.DictReader((BASE/'missions/biomed_24_contracts.csv').open()))
        self.assertEqual(len(rows),24)
        self.assertEqual(sum(m['world'] in ('helix_bio','aurora_ep') for m in self.missions),24)
if __name__=='__main__': unittest.main()
