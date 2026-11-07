"""Source-linked checks; requires env PYTHONQUEST_V14_ROOT pointing at extracted v1.4 project.

Only known safe toy scripts are executed, using a disposable profile. NEVER load
user's actual game progress or run arbitrary learner code in these tests.
"""
from __future__ import annotations
import ast, csv, importlib, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(os.environ['PYTHONQUEST_V14_ROOT']).resolve() if os.environ.get('PYTHONQUEST_V14_ROOT') else None
if ROOT is not None and (ROOT/'Python Quest 2D/src').exists(): ROOT=ROOT/'Python Quest 2D'
if ROOT is not None and (ROOT/'src/python_quest_2d/core/grade.py').exists():
    sys.path.insert(0,str(ROOT/'src'))

@unittest.skipUnless(ROOT is not None and (ROOT/'src/python_quest_2d/core/grade.py').exists(),
                     'Set PYTHONQUEST_V14_ROOT to extracted v1.4 project for source-linked tests')
class SourceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ROOT is None: return
        cls.progress=importlib.import_module('python_quest_2d.core.progress')
        cls.grade=importlib.import_module('python_quest_2d.core.grade')
        cls.challenges=importlib.import_module('python_quest_2d.core.challenges')

    def test_source_symbols_exist_with_expected_signatures(self):
        needles={
          'core/grade.py':['grade'], 'core/worker.py':['evaluate'],
          'core/progress.py':['fresh','save','load','award'],
          'core/expedition_contract.py':['primitive','validate'],
          'game/app.py':['Game'], 'game/expedition.py':['Expeditions'],
          'game/world.py':['World'], 'ui/terminal.py':['Terminal']}
        for path,symbols in needles.items():
            with self.subTest(path=path):
                src=(ROOT/'src/python_quest_2d'/path).read_text(encoding='utf-8')
                node=ast.parse(src)
                names={n.name for n in ast.walk(node) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
                for sym in symbols:self.assertIn(sym,names)
        grade_tree=ast.parse((ROOT/'src/python_quest_2d/core/grade.py').read_text())
        grade_function=next(n for n in grade_tree.body if isinstance(n,ast.FunctionDef) and n.name=='grade')
        self.assertEqual([a.arg for a in grade_function.args.args],['ch','code','timeout_s'])

    def test_existing_76_missions_well_formed_and_unique_effects(self):
        from jsonschema import Draft202012Validator
        schema=json.loads((Path(__file__).resolve().parents[1]/'engineering/schemas/mission_content.schema.json').read_text())
        validate=Draft202012Validator(schema).validate
        lessons=self.challenges.LESSONS
        self.assertEqual(len(lessons),76)
        self.assertEqual(len({v['world_effect'] for v in lessons.values()}),76)
        for key,ch in lessons.items():
            with self.subTest(key=key):
                self.assertEqual(ch['id'],key)
                validate(ch)
                self.assertTrue((ROOT/'content/authoring'/f'{key}.py').exists())
        self.assertEqual(len(self.challenges.MAPS),len(set(self.challenges.MAPS)))

    def test_legacy_worker_grades_known_safe_script(self):
        ch=self.challenges.LESSONS['orientation_01']
        res=self.grade.grade(ch,"print('System online')\n")
        self.assertEqual(res['status'],'finished')
        self.assertTrue(res['passed'],str(res))
        # Adapter reference is checked separately in test_stage09_contracts.

    def test_schema4_unknown_fields_and_idempotent_award(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'progress.json'
            with patch.object(self.progress,'location',return_value=path):
                p=self.progress.fresh()
                p['unexpected_extension']={'hello':['keep']}
                p['programs']={'orion_moon_01':[[0,1]]}
                self.progress.save(p)
                restored=self.progress.load()
                self.assertEqual(restored['unexpected_extension'],p['unexpected_extension'])
                self.assertEqual(restored['programs'],p['programs'])
                self.assertEqual(restored['schema_version'],4)
                first=self.progress.award(restored,'orientation_01')
                second=self.progress.award(restored,'orientation_01')
                self.assertEqual(first,100)
                self.assertEqual(second,0)
                self.assertEqual(restored['player']['xp'],100)
                self.assertTrue(self.progress.load()['world_flags']['gate_orientation_01'])

    def test_schema2_3_backup_paths_in_disposable_profile(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'progress.json'
            with patch.object(self.progress,'location',return_value=path):
                for v in (2,3):
                    p=self.progress.fresh();p['schema_version']=v;p['legacy_note']={'version':v}
                    self.progress.save(p)
                    got=self.progress.load()
                    self.assertEqual(got['schema_version'],4)
                    self.assertEqual(got['legacy_note'],p['legacy_note'])
                self.assertTrue(path.with_suffix('.pre-greenline.json').exists())
                self.assertTrue(path.with_suffix('.pre-expedition.json').exists())

    def test_current_graph_needs_unlock_correction(self):
        destinations=json.loads((ROOT/'content/universe/destinations.json').read_text())
        self.assertEqual(destinations[1]['id'],'orion')
        self.assertEqual(destinations[1]['requires'],'mission_control_16')
        self.assertNotIn('mission_control_16',self.challenges.LESSONS)
        # This is an intentional stage-09 recorded design debt, not a live implementation failure.

if __name__=='__main__':unittest.main()
