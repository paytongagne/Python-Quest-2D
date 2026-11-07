"""PQ11-004: real worker plans rechecked against live world geometry and state."""

import copy
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import pg
from python_quest_2d.core.contracts import ContractError
from python_quest_2d.core.grade import grade_program
from python_quest_2d.core.progress import fresh
from python_quest_2d.game.mica_observation import MicaState, observe, prepare, verify
from python_quest_2d.game.world import World

SOURCE = """def plan(observation):
    observation['robot']['energy'] = 9999
    return [{'type': 'move', 'direction': 'east'},
            {'type': 'interact', 'target': 'test-relay'}]
"""


class MicaObservationTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {"PYTHONQUEST_CONTRACTS_V1": "1"})
        env.start()
        self.addCleanup(env.stop)
        self.world = World(fresh())
        self.world.map = copy.deepcopy(self.world.map)
        self.world.map["mica_devices"] = [
            {"id": "test-relay", "cell": [5, 3], "capabilities": ["activate"]},
            {"id": "other-relay", "cell": [3, 4], "capabilities": ["activate"]},
        ]
        self.mica = MicaState((3, 3), 4)

    def prepared(self, source=SOURCE):
        pending = prepare(self.world, self.mica, "test-relay", source, seed=17)
        return pending, grade_program(pending.request())

    def test_real_worker_is_deterministic_and_never_mutates_world(self):
        initial = copy.deepcopy(self.world.p)
        pending, report = self.prepared()
        self.assertTrue(report["passed"], report)
        request = pending.request()
        request["observation"]["robot"]["energy"] = 1000
        self.assertEqual(pending.request()["observation"]["robot"]["energy"], 4)
        result = verify(self.world, self.mica, pending, report, SOURCE)
        self.assertEqual(result["final_cell"], [4, 3])
        self.assertEqual(result["remaining_energy"], 2)
        self.assertEqual(
            result["proposed_intents"],
            [dict(device_id="test-relay", operation="activate", at_step=1)],
        )
        again, report_again = self.prepared()
        self.assertEqual(result, verify(self.world, self.mica, again, report_again, SOURCE))
        self.assertEqual(again.snapshot_digest, pending.snapshot_digest)
        self.assertEqual(self.world.p, initial)

    def test_current_walls_unlocks_energy_and_source_invalidate_old_response(self):
        pending, report = self.prepared()
        for robot, source in ((MicaState((3, 3), 3), SOURCE), (self.mica, SOURCE + "# edited")):
            with self.assertRaisesRegex(ContractError, "rescan"):
                verify(self.world, robot, pending, report, source)
        self.world.walls.append(pg.Rect(4 * 32, 3 * 32, 32, 32))
        with self.assertRaisesRegex(ContractError, "rescan"):
            verify(self.world, self.mica, pending, report, SOURCE)
        rejected = self.prepared()[1]
        self.assertFalse(rejected["passed"])
        self.assertIn("Step 1: COLLISION", rejected["rows"][0])
        self.world.walls.pop()
        self.world.p["completed"].append("orientation_01")
        with self.assertRaisesRegex(ContractError, "rescan"):
            verify(self.world, self.mica, pending, report, SOURCE)

        self.world.enter("launch")
        with self.assertRaisesRegex(ContractError, "Destination changed"):
            verify(self.world, self.mica, pending, report, SOURCE)

    def test_parent_rejects_invalid_candidate_even_with_passing_worker_envelope(self):
        pending, report = self.prepared()
        for actions, error in [
            ([dict(type="interact", target="other-relay")], "MISSING_CAPABILITY"),
            ([dict(type="interact", target="test-relay")], "DEVICE_NOT_ADJACENT"),
            ([dict(type="move", direction="west")] * 3, "COLLISION"),
            ([dict(type="scan", direction="east")] * 3, "ENERGY_EXHAUSTED"),
            ([dict(type=[], direction="east")], "INVALID_ACTION"),
        ]:
            candidate = copy.deepcopy(report)
            candidate["effect"]["actions"] = actions
            with self.subTest(error=error), self.assertRaises(ContractError) as caught:
                verify(self.world, self.mica, pending, candidate, SOURCE)
            self.assertEqual(caught.exception.code, error)
            self.assertIsNotNone(caught.exception.step)
        self.world.map["mica_devices"][0]["requires"] = ["orientation_01"]
        self.assertFalse(self.prepared()[1]["passed"])
        with (
            patch.dict(os.environ, {"PYTHONQUEST_CONTRACTS_V1": "0"}),
            self.assertRaises(ContractError),
        ):
            observe(self.world, self.mica, "test-relay")


if __name__ == "__main__":
    unittest.main(verbosity=2)
