"""PQ11-002 opt-in wire compatibility, response budgets and pure candidate guards."""

import copy, json, os, sys, unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from python_quest_2d.core import protocol
from python_quest_2d.core.grade import grade
from python_quest_2d.core.challenges import ROOT, LESSONS


class ContractAdapter(unittest.TestCase):
    def test_all_76_references_through_versioned_worker(self):
        with patch.dict(os.environ, {"PYTHONQUEST_CONTRACTS_V1": "1"}):
            for key, ch in LESSONS.items():
                result = grade(
                    ch, (ROOT / "content/authoring" / (key + ".py")).read_text(encoding="utf8")
                )
                self.assertTrue(result["passed"], (key, result))
                self.assertEqual(result["protocol_version"], 1)
                self.assertEqual(result["mission_id"], key)
        with patch.dict(os.environ, {"PYTHONQUEST_CONTRACTS_V1": "0"}):
            self.assertFalse(protocol.enabled())

    def test_invalid_outputs_and_request_identity_fail_closed(self):
        ch = LESSONS["workshop_01"]
        req = protocol.request(ch, "pass")
        for raw in [
            b"[]",
            b'{"passed":true,"rows":[]}',
            b"x" * 262145,
            b'{"status":"finished","passed":"yes","rows":[]}',
        ]:
            with self.subTest(raw=raw[:40]):
                with patch("python_quest_2d.core.grade._worker", return_value=raw):
                    self.assertFalse(grade(ch, "pass")["passed"])
        raw = json.dumps(
            dict(
                status="finished",
                passed=True,
                rows=["ok"],
                passed_count=1,
                total_count=1,
                protocol_version=1,
                request_id="wrong",
                mission_id=ch["id"],
            )
        ).encode()
        with self.assertRaises(protocol.ContractError):
            protocol.decode_result(raw, req)
        req["source"] = "changed"
        with self.assertRaises(protocol.ContractError):
            protocol.validate_request(req)
        result = grade(ch, 'import os\nos.write(1,b"x"*300000)')
        self.assertFalse(result["passed"])
        self.assertIn("byte budget", " ".join(result["rows"]))
        self.assertFalse(grade(ch, "#" + "é" * 40000)["passed"])

    def test_plan_trace_collision_energy_capability_and_staleness(self):
        folder = ROOT / "planning/engineering/examples"
        obs = json.loads((folder / "observation.valid.json").read_text())
        plan = json.loads((folder / "action_plan.valid.json").read_text())
        original = copy.deepcopy(obs)
        source = "def plan(obs): pass"

        def validate(o, p=plan, expected=None, code=source):
            return protocol.validate_candidate(
                o,
                p,
                snapshot_digest=expected or protocol.canonical_digest(o),
                source=code,
                source_hash=protocol.source_digest(source),
            )

        result = validate(obs)
        self.assertEqual(result, validate(obs))
        self.assertEqual(obs, original)
        self.assertEqual(result["final_cell"], [2, 1])
        self.assertEqual(result["remaining_energy"], 10)
        for direction in ("south", "north"):
            bad = copy.deepcopy(plan)
            bad["actions"] = (
                [dict(type="move", direction="east"), dict(type="move", direction="south")]
                if direction == "south"
                else [dict(type="move", direction="north")] * 2
            )
            with self.assertRaises(protocol.ContractError) as err:
                validate(obs, bad)
            self.assertEqual(err.exception.code, "COLLISION")
            self.assertEqual(err.exception.step, 1)
        for field, value, expected in [
            ("energy", 0, "ENERGY_EXHAUSTED"),
            ("abilities", [], "MISSING_CAPABILITY"),
        ]:
            bad = copy.deepcopy(obs)
            bad["robot"][field] = value
            with self.assertRaises(protocol.ContractError) as err:
                validate(bad)
            self.assertEqual(err.exception.code, expected)
        changed = copy.deepcopy(obs)
        changed["seed"] = 8
        with self.assertRaises(protocol.ContractError):
            validate(changed, expected=protocol.canonical_digest(obs))
        with self.assertRaises(protocol.ContractError):
            validate(obs, code="new revision")
        bad = copy.deepcopy(plan)
        bad["snapshot_id"] = "stale"
        with self.assertRaises(protocol.ContractError):
            validate(obs, bad)
        self.assertEqual(obs, original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
