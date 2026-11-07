"""Stage 09 cross-file planning checks; no shipped game modifications."""
import csv
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Stage09Documentation(unittest.TestCase):
    def test_authoritative_document_and_diagrams_exist(self):
        doc = ROOT/'docs/09_ARCHITECTURE_AND_DATA_CONTRACTS.md'
        self.assertGreater(doc.stat().st_size, 15000)
        for word in ['Architecture', 'Data Contracts', 'Save', 'Worker', 'Stage 10', '76', 'v1.4']:
            self.assertIn(word.lower(), doc.read_text(encoding='utf-8').lower())
        for name in ('09_ARCHITECTURE.mmd', '09_DEPLOYMENT_SEQUENCE.mmd'):
            self.assertGreater((ROOT/'engineering'/name).stat().st_size, 300)

    def test_error_taxonomy_unique_complete(self):
        taxonomy = json.loads((ROOT/'engineering/09_ERROR_TAXONOMY.json').read_text())
        codes = [row['code'] for row in taxonomy['errors']]
        self.assertEqual(len(codes), len(set(codes)))
        self.assertGreaterEqual(len(codes), 16)
        for row in taxonomy['errors']:
            self.assertFalse(row['world_mutation'])
            self.assertTrue(row['retry'])

    def test_schema_registry_and_examples_coverage(self):
        registry=json.loads((ROOT/'engineering/09_CONTRACT_REGISTRY.json').read_text())
        self.assertEqual(len(registry['schemas']),13)
        for item in registry['schemas']:
            rootname = item.removesuffix('.schema')
            self.assertTrue((ROOT/'engineering/examples'/f'{rootname}.valid.json').exists())
            self.assertTrue((ROOT/'engineering/schemas'/f'{rootname}.schema.json').exists())
        bad=json.loads((ROOT/'engineering/09_NEGATIVE_EXAMPLES.json').read_text())
        self.assertEqual(len(bad), 12)
        for item in bad:
            self.assertTrue((ROOT/'engineering/examples'/item['file']).exists())

    def test_adapter_sources_and_contracts_resolve(self):
        with (ROOT/'engineering/09_SOURCE_ADAPTERS.csv').open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        registry = json.loads((ROOT/'engineering/09_CONTRACT_REGISTRY.json').read_text())
        supported = {n.removesuffix('.schema') for n in registry['schemas']}
        self.assertEqual(len(rows),12)
        self.assertEqual(len(set(r['adapter_id'] for r in rows)),12)
        for row in rows:
            self.assertIn(row['contract'], supported)

    def test_stage08_still_unchanged_and_present(self):
        self.assertTrue((ROOT/'docs/08_BIOMEDICAL_ENDGAME.md').exists())
        with (ROOT/'missions/biomed_24_contracts.csv').open(newline='',encoding='utf-8') as f:
            self.assertEqual(len(list(csv.DictReader(f))),24)


if __name__=='__main__':
    unittest.main()
