"""Stage10 integrity only; does not claim native playtesting or game implementation."""
import csv,importlib.util,json,math,os,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod
AUDIT=module('pq_release_audit',ROOT/'tools/verify_windows_archive.py')
STATS=module('pq_frame_stats',ROOT/'tools/frame_budget_report.py')

class Stage10Integrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT/'qa/10_ACCEPTANCE_CATALOG.csv').open(newline='',encoding='utf8') as f:
            cls.rows=list(csv.DictReader(f))
        cls.gates=json.loads((ROOT/'release/10_RELEASE_GATES.json').read_text())
        cls.budgets=json.loads((ROOT/'qa/10_PERFORMANCE_BUDGETS.json').read_text())

    def test_unique_ids_and_minimum_coverage(self):
        ids=[r['test_id'] for r in self.rows]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertGreaterEqual(len(ids),80)
        self.assertEqual(len({r['test_id'].split('-')[1] for r in self.rows}),12)

    def test_case_has_trigger_oracle_and_trace(self):
        for r in self.rows:
            for key in ('case','expected','priority','source_anchor','verification','gate','implementation_status'):
                with self.subTest(test_id=r['test_id'],field=key):self.assertTrue(r[key])
            self.assertNotEqual(r['evidence'],'PASS')

    def test_release_stop_ship(self):
        stop=' '.join(self.gates['stop_ship']).lower()
        self.assertTrue(all(x in stop for x in ('save','xp','launcher','medical')))
        self.assertGreaterEqual(len(self.gates['gates']),6)

    def test_budgets_have_measurement_plan(self):
        for b in self.budgets['budgets']:
            self.assertTrue(b['metric'] and b['target'] and b['method'] and b['failure'])
        self.assertIn('PROPOSED',self.budgets['scope'])

    def test_windows_static_auditor_accepts_valid_fixture(self):
        with tempfile.TemporaryDirectory() as t:
            z=Path(t)/'ok.zip'
            with zipfile.ZipFile(z,'w') as f:
                for p in AUDIT.REQUIRED:f.writestr('Python Quest 2D/'+p,'fixture only')
            out=AUDIT.inspect(z)
            self.assertTrue(out['passed'],out['issues'])
            self.assertEqual(out['root'],'Python Quest 2D')

    def test_windows_static_auditor_rejects_unsafe_and_missing(self):
        with tempfile.TemporaryDirectory() as t:
            z=Path(t)/'bad.zip'
            with zipfile.ZipFile(z,'w') as f:
                f.writestr('../escape.txt','x')
                f.writestr('Python Quest 2D/.env','secret')
            out=AUDIT.inspect(z)
            self.assertFalse(out['passed'])
            self.assertTrue(any('unsafe' in s for s in out['issues']))
            self.assertTrue(any('sensitive' in s for s in out['issues']))

    def test_performance_report_quantiles(self):
        report=STATS.summarize({'frame_us':[1000]*95+[20000]*5})
        self.assertEqual(report['count'],100)
        self.assertEqual(report['p95_ms'],1.)
        self.assertEqual(report['p99_ms'],20.)
        self.assertTrue(report['p95_under_16_7_ms'])

    def test_performance_report_rejects_bool_nan_empty(self):
        for vals in ([],[True],[float('nan')],[-10]):
            with self.subTest(vals=vals):
                with self.assertRaises(ValueError):STATS.summarize(vals)

    def test_biomedical_acceptance_crossref(self):
        with (ROOT/'tests/biomed_acceptance.csv').open(newline='',encoding='utf8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),96)
        bio=[r for r in self.rows if r['test_id'].startswith('PQ10-BIO')]
        self.assertGreaterEqual(len(bio),8)

    def test_mandatory_documents(self):
        for filename in ('docs/10_TEST_AND_RELEASE_PLAN.md','qa/10_HUMAN_PLAYTEST_PROTOCOL.md','qa/10_FAULT_INJECTION.md','qa/10_CI_MATRIX.md','release/10_RELEASE_GATES.json'):
            with self.subTest(filename=filename): self.assertGreater((ROOT/filename).stat().st_size,250)

    def test_all_goals_not_claimed_shipped(self):
        for r in self.rows:self.assertEqual(r['evidence'],'Not executed by Stage 10 planning')
        self.assertEqual(self.gates['status'],'PROPOSED_RELEASE_POLICY_NOT_EXECUTED')

    def test_windows_archive_checker_no_execution(self):
        txt=(ROOT/'tools/verify_windows_archive.py').read_text()
        self.assertNotIn('subprocess.run',txt)
        self.assertNotIn('extractall(',txt)

if __name__=='__main__':unittest.main()
