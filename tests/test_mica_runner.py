"""PQ11-005: fixed-step execution, cancel/restart and atomic game-owned effects."""

import copy
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import Game, pg
from python_quest_2d.core import progress
from python_quest_2d.core.grade import grade_program
from python_quest_2d.game.mica_observation import MicaState, prepare
from python_quest_2d.game.mica_runner import MicaRunner, replay

SOURCE = """def plan(observation):
    return [{'type': 'move', 'direction': 'east'},
            {'type': 'wait', 'ticks': 2},
            {'type': 'interact', 'target': 'test-relay'}]
"""


class MicaRunnerTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "profile.json"
        env = patch.dict(
            os.environ, {"PYTHONQUEST_CONTRACTS_V1": "1", "PYTHONQUEST_SAVE": str(self.path)}
        )
        env.start()
        self.addCleanup(env.stop)
        self.g = Game()
        self.addCleanup(self.g.pool.shutdown)
        self.g.world.map = copy.deepcopy(self.g.world.map)
        self.g.world.map["mica_devices"] = [
            {"id": "test-relay", "cell": [5, 3], "capabilities": ["activate"]}
        ]
        self.g.p["player"]["xp"] = 75
        self.g.p["unknown"] = {"keep": [1, 2]}
        self.g.persist()
        self.mica = MicaState((3, 3), 4)
        self.pending = prepare(self.g.world, self.mica, "test-relay", SOURCE)
        self.report = grade_program(self.pending.request())
        self.assertTrue(self.report["passed"], self.report)

    def runner(self):
        return MicaRunner(self.g.world, self.mica, self.pending, self.report, SOURCE)

    def test_game_advances_and_draws_robot_then_saves_at_one_milestone(self):
        g = self.g
        original = self.path.read_bytes()
        job = g.deploy_mica(self.mica, self.pending, self.report, SOURCE)
        g.update_field(0.1)
        self.assertEqual(g.world.mica_visual, (128.0, 112.0))
        g.draw()
        g.update_field(0.6)
        self.assertEqual(job.ticks, 3)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(g.p["runtime_v1"]["device_state"], {})
        g.update_field(0.1)
        self.assertEqual(job.status, "committed")
        self.assertIsNone(g.world.mica_visual)
        restored = progress.load()
        self.assertEqual(
            restored["runtime_v1"]["device_state"], {"orientation.test-relay": "online"}
        )
        self.assertEqual(restored["runtime_v1"]["mica_by_world"]["orientation"]["energy"], 2)
        self.assertEqual(restored["player"]["xp"], 75)
        self.assertEqual(restored["unknown"], {"keep": [1, 2]})
        event = replay(restored, job.event_id)
        self.assertEqual(event["event"]["timestamp_tick"], 4)
        self.assertEqual(event["result"]["final_cell"], [4, 3])
        event["result"]["trace"].clear()
        self.assertEqual(len(replay(restored, job.event_id)["result"]["trace"]), 3)

    def test_different_frame_cadences_match_and_duplicate_is_a_no_op(self):
        g = self.g
        pristine = copy.deepcopy(g.p)
        a, duplicate = self.runner(), self.runner()
        self.assertEqual(a.advance(0.8), "committed")
        first = replay(g.p, a.event_id)
        committed = self.path.read_bytes()
        self.assertEqual(duplicate.advance(2.0), "duplicate")
        self.assertEqual(self.path.read_bytes(), committed)
        g.p.clear()
        g.p.update(pristine)
        b = self.runner()
        for dt in (0.03, 0.28, 0.11, 0.17, 0.21):
            b.advance(dt)
        self.assertEqual(b.status, "committed")
        self.assertEqual(replay(g.p, b.event_id), first)

    def test_cancel_and_failed_save_leave_restart_at_safe_state(self):
        original = self.path.read_bytes()
        job = self.runner()
        job.advance(0.6)
        job.cancel()
        self.assertEqual(job.advance(10), "cancelled")
        self.assertEqual(self.path.read_bytes(), original)
        self.assertIsNone(progress.load()["runtime_v1"]["active_job"])
        job = self.runner()
        with patch(
            "python_quest_2d.game.mica_runner.progress.save",
            side_effect=OSError("test write failure"),
        ):
            self.assertEqual(job.advance(0.8), "rejected")
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(self.g.p["runtime_v1"]["device_state"], {})
        self.assertEqual(self.runner().advance(0.8), "committed")

    def test_obstacle_inserted_mid_run_rejects_entire_transaction(self):
        original = self.path.read_bytes()
        job = self.runner()
        job.advance(0.2)
        self.g.world.walls.append(pg.Rect(4 * 32, 3 * 32, 32, 32))
        self.assertEqual(job.advance(0.6), "rejected")
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(self.g.p["runtime_v1"]["device_state"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
