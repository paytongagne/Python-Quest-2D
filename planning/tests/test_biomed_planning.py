"""Test stage-08 *planning fixture integrity*, NOT game runtime or clinical accuracy."""
from __future__ import annotations
import csv
import hashlib
import json
import math
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'reference/fixtures'


def load(filename):
    return json.loads((FIX/filename).read_text(encoding='utf8'), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


class BiomedPlanningTests(unittest.TestCase):
    def test_has_exact_24_unshipped_ids(self):
        with (ROOT/'missions/biomed_24_contracts.csv').open(newline='',encoding='utf8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows), 24)
        self.assertEqual(len({r['mission_id'] for r in rows}),24)
        self.assertEqual({r['world'] for r in rows},{'helix_bio','aurora_ep'})
        for world in ('helix_bio','aurora_ep'):
            self.assertEqual({int(r['sequence']) for r in rows if r['world']==world},set(range(5,17)))
            self.assertTrue(all(r['status']=='DESIGN_ONLY' for r in rows if r['world']==world))

    def test_acceptance_covers_all_missions_four_ways(self):
        with (ROOT/'tests/biomed_acceptance.csv').open(newline='',encoding='utf8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),96)
        byid={}
        for r in rows:
            byid.setdefault(r['mission_id'],set()).add(r['case_type'])
        self.assertEqual(len(byid),24)
        self.assertTrue(all(s=={'positive','edge','integration','save_regression'} for s in byid.values()))

    def test_clean_wave_data(self):
        obj=load('helix_clean.json')
        self.assertEqual(obj['source'],'SYNTHETIC_ONLY')
        self.assertEqual(set(obj['channels']),{'SYN_A','SYN_B'})
        for ch,series in obj['channels'].items():
            self.assertEqual(len(series),64)
            for i,frame in enumerate(series):
                self.assertEqual(frame['channel'],ch)
                self.assertEqual(frame['seq'],i)
                self.assertEqual(frame['time_ms'],i*4.0)
                self.assertTrue(math.isfinite(frame['value']))
                self.assertEqual(frame['source'],'SYNTHETIC_ONLY')

    def test_fault_fixture_has_expected_anomalies(self):
        obj=load('helix_faults.json')
        events=obj['events']
        seqs=[ev['frame']['seq'] for ev in events]
        self.assertNotIn(12,seqs)
        self.assertGreater(seqs.count(6),1)
        self.assertTrue(any(ev['frame']['value'] is None and ev['frame']['quality']=='MISSING' for ev in events))
        self.assertTrue(any(isinstance(ev['frame']['value'],str) for ev in events))
        self.assertTrue(all(ev['arrival_tick']>=0 for ev in events))

    def test_toy_mesh_and_rejected_points(self):
        obj=load('aurora_toy_chamber.json')
        verts=obj['mesh']['vertices']; faces=obj['mesh']['faces']
        self.assertEqual(len(verts),6)
        self.assertEqual(len(faces),8)
        for face in faces:
            self.assertEqual(len(face),3)
            self.assertEqual(len(set(face)),3)
            self.assertTrue(all(type(n) is int and 0<=n<len(verts) for n in face))
        self.assertEqual(sum(bool(p['contact'] and p['confidence']>=.8) for p in obj['observations']),6)
        self.assertEqual(set(p['source'] for p in obj['observations']),{'SYNTHETIC_ONLY'})

    def test_design_contract_has_required_safety_boundary(self):
        obj=json.loads((ROOT/'engineering/08_BIOMED_CONTRACTS.json').read_text())
        self.assertFalse(obj['clinical_use'])
        self.assertFalse(obj['patient_data'])
        self.assertFalse(obj['worker_boundary']['learner_code_in_pygame_thread'])
        self.assertTrue(obj['worker_boundary']['parent_revalidates_result'])
        self.assertEqual(obj['intentional_blueprint_corrections']['aurora_ep_10'].split('(')[0],'mesh_neighbors')

    def test_fixture_regeneration_byte_identical(self):
        from sys import path
        path.insert(0,str(ROOT/'reference'))
        import biomed_fixture_generator as gen
        tracked=['helix_clean.json','helix_faults.json','aurora_toy_chamber.json']
        before={name:hashlib.sha256((FIX/name).read_bytes()).hexdigest() for name in tracked}
        gen.generate()
        after={name:hashlib.sha256((FIX/name).read_bytes()).hexdigest() for name in tracked}
        self.assertEqual(before,after)


if __name__=='__main__':
    unittest.main(verbosity=2)
