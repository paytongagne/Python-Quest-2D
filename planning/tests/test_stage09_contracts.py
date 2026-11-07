"""Stage-09 design contract tests (not game functionality tests)."""
from __future__ import annotations
import copy, csv, json, os, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'reference'))
from contracts_v1 import ContractError, add_optional_extensions, canonical_digest, normalize_legacy_result, safe_json, source_digest, validate_action_plan
try:
    from jsonschema import Draft202012Validator, RefResolver
except ImportError:
    Draft202012Validator=RefResolver=None


def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))


class ContractExamples(unittest.TestCase):
    @unittest.skipUnless(Draft202012Validator, 'Install optional planning test dependency: jsonschema')
    def test_schema_metavalidation_and_positive_examples(self):
        docs={}
        for p in (ROOT/'engineering/schemas').glob('*.schema.json'):
            s=json.loads(p.read_text(encoding='utf-8'))
            Draft202012Validator.check_schema(s)
            docs[s['$id']]=s
        registry=read('engineering/09_CONTRACT_REGISTRY.json')
        self.assertEqual(len(registry['schemas']),13)
        self.assertEqual(len(docs),13)
        for name in ('observation','action_plan','execution_request','evaluation_result','device_intent',
                     'world_event','render_snapshot','program_library','runtime_extension','mission_content',
                     'save_v4','travel_request','travel_result'):
            with self.subTest(name=name):
                s=read(f'engineering/schemas/{name}.schema.json')
                value=read(f'engineering/examples/{name}.valid.json')
                Draft202012Validator(s,resolver=RefResolver.from_schema(s,store=docs)).validate(value)
                safe_json(value,max_bytes=2_097_152)

    @unittest.skipUnless(Draft202012Validator, 'Install optional planning test dependency: jsonschema')
    def test_negative_examples_are_rejected(self):
        docs={}
        for p in (ROOT/'engineering/schemas').glob('*.schema.json'):
            s=json.loads(p.read_text());docs[s['$id']]=s
        negative=read('engineering/09_NEGATIVE_EXAMPLES.json')
        self.assertGreaterEqual(len(negative),10)
        for entry in negative:
            with self.subTest(case=entry['file']):
                s=read(f"engineering/schemas/{entry['schema']}.schema.json")
                value=read(f"engineering/examples/{entry['file']}")
                self.assertTrue(list(Draft202012Validator(s,resolver=RefResolver.from_schema(s,store=docs)).iter_errors(value)))

    def test_registry_references_exist(self):
        registry=read('engineering/09_CONTRACT_REGISTRY.json')
        for entry in registry['schemas'].values():self.assertTrue((ROOT/entry['path']).is_file())
        for path in registry['references']:self.assertTrue((ROOT/path).is_file())
        for path in ('09_SOURCE_ADAPTERS.csv','09_SAVE_COMPATIBILITY_MATRIX.csv'):
            with (ROOT/'engineering'/path).open(newline='',encoding='utf-8') as f:
                self.assertGreaterEqual(len(list(csv.DictReader(f))),10)

    def test_state_machine_has_valid_transitions(self):
        machines=read('engineering/09_STATE_MACHINES.json')['machines']
        self.assertEqual(set(machines),{'evaluation','deployment','travel','device','profile'})
        for name,m in machines.items():
            self.assertIn(m['initial'],m['states'])
            for before,event,after in m['transitions']:
                with self.subTest(machine=name, event=event):
                    self.assertIn(before,m['states']);self.assertIn(after,m['states'])
                    self.assertTrue(event)

    def test_sample_determinism_and_finiteness(self):
        ob=read('engineering/examples/observation.valid.json')
        b=copy.deepcopy(ob)
        b['robot']=dict(reversed(list(b['robot'].items())))
        self.assertEqual(canonical_digest(ob),canonical_digest(b))
        self.assertEqual(len(source_digest('def plan(o):\n    return []\n')),64)
        for value in (float('nan'),float('inf'),-float('inf'),{1:'bad_key'},object()):
            with self.subTest(value=str(value)), self.assertRaises(ContractError):safe_json(value)

    def test_reference_plan_success_and_no_source_mutation(self):
        ob=read('engineering/examples/observation.valid.json')
        plan=read('engineering/examples/action_plan.valid.json')
        old=copy.deepcopy(ob)
        result=validate_action_plan(ob,plan)
        self.assertEqual(ob,old)
        self.assertEqual(result['final_cell'],[2,1])
        self.assertEqual(result['energy_used'],2)
        self.assertEqual(result['proposed_intents'],[{'device_id':'relay_a','operation':'activate','at_step':1}])
        self.assertEqual(len(result['trace']),3)
        self.assertEqual(result,validate_action_plan(ob,plan))

    def test_reference_plan_rejects_stale_bounds_and_other_abuse(self):
        ob=read('engineering/examples/observation.valid.json')
        plan=read('engineering/examples/action_plan.valid.json')
        def denied(mutate, code):
            o=copy.deepcopy(ob);p=copy.deepcopy(plan)
            mutate(o,p)
            with self.assertRaises(ContractError) as err:validate_action_plan(o,p)
            self.assertEqual(err.exception.code,code)
        denied(lambda o,p:p.update(snapshot_id='other'),'STALE_SNAPSHOT')
        denied(lambda o,p:p['actions'].__setitem__(0,{'type':'delete_world'}),'INVALID_ACTION')
        denied(lambda o,p:p['actions'].__setitem__(0,{'type':'move','direction':'up'}),'INVALID_ACTION')
        denied(lambda o,p:p['actions'].__setitem__(0,{'type':'move','direction':'east','world_flags':True}),'INVALID_ACTION')
        denied(lambda o,p:p['actions'].__setitem__(0,{'type':'move','direction':'north'}) or p['actions'].__setitem__(1,{'type':'move','direction':'north'}),'COLLISION')
        denied(lambda o,p:o['robot'].update(energy=1),'ENERGY_EXHAUSTED')
        denied(lambda o,p:o['robot'].update(abilities=['move']),'MISSING_CAPABILITY')
        denied(lambda o,p:p['actions'].__setitem__(0,{'type':'report','label':'x'}) or p['actions'].__setitem__(1,{'type':'interact','target':'relay_a'}),'DEVICE_NOT_ADJACENT')
        denied(lambda o,p:p['actions'].append({'type':'wait','ticks':0}),'INVALID_ACTION')
        denied(lambda o,p:p['actions'].__setitem__(0,{'type':'report','label':'x'*121}),'INVALID_ACTION')
        denied(lambda o,p:o['visible']['walls'].append([999,999]),'INVALID_INPUT')

    def test_legacy_result_compatibility(self):
        report={'status':'finished','passed':True,'rows':['PASS  1'], 'passed_count':1,'total_count':1,'effect':[1,2]}
        out=normalize_legacy_result(mission_id='hydro_01',request_id='req-01',report=report)
        self.assertTrue(out['passed']);self.assertEqual(out['effect'],[1,2]);self.assertEqual(out['status'],'finished')
        bad=dict(report,passed=False,rows=['FAIL  1'],effect=[99])
        output=normalize_legacy_result(mission_id='hydro_01',request_id='req-02',report=bad)
        self.assertIsNone(output['effect']);self.assertEqual(output['errors'][0]['code'],'TEST_FAILED')
        with self.assertRaises(ContractError):normalize_legacy_result(mission_id='hydro_01',request_id='req-01',report=dict(report,effect=float('nan')))

    def test_save_extension_retains_unknowns_and_does_not_mutate_original(self):
        old=read('engineering/examples/save_v4.valid.json')
        old['programs']={'orion_moon_01':[[0,0]]}
        old['expedition_job']={'key':'orion_moon_01','step':1.0}
        old['custom_plugin']={'settings':{'x':'kept'}}
        snapshot=copy.deepcopy(old)
        p=add_optional_extensions(old)
        self.assertEqual(old,snapshot)
        self.assertEqual(p['programs'],old['programs'])
        self.assertEqual(p['expedition_job'],old['expedition_job'])
        self.assertEqual(p['custom_plugin'],old['custom_plugin'])
        self.assertEqual(p['schema_version'],4)
        self.assertEqual(p['program_library']['schema'],1)
        with self.assertRaises(ContractError):add_optional_extensions({**old,'schema_version':5})

    def test_stage08_coverage_and_no_collisions(self):
        with (ROOT/'missions/biomed_24_contracts.csv').open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),24)
        with (ROOT/'tests/biomed_acceptance.csv').open(newline='',encoding='utf-8') as f:
            accept=list(csv.DictReader(f))
        self.assertEqual(len(accept),96)
        with (ROOT/'missions/mission_blueprints.psv').open(encoding='utf-8') as f:
            blueprint=[x for x in f.readlines() if x.strip() and not x.startswith('#')]
        self.assertEqual(len(blueprint),76)


if __name__=='__main__':unittest.main()
