"""PQ11-006 playthrough using real keyboard events, workers and save reloads."""

import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import Game, pg
from python_quest_2d.core import progress
from python_quest_2d.core.challenges import LESSONS
from python_quest_2d.game.mica_console import STARTER


class MicaLibraryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        env = patch.dict(
            os.environ,
            {
                "PYTHONQUEST_CONTRACTS_V1": "0",
                "PYTHONQUEST_SAVE": str(Path(tmp.name) / "profile.json"),
            },
        )
        env.start()
        self.addCleanup(env.stop)
        self.g = Game()
        self.addCleanup(self.g.pool.shutdown)
        self.g.p["player"]["xp"] = 100
        self.g.p["completed"] = ["orientation_01"]
        self.g.p["extra"] = {"preserved": True}

    def press(self, key, mod=0):
        self.g.event(pg.event.Event(pg.KEYDOWN, key=key, mod=mod))

    def finish_worker(self):
        self.assertIsNotNone(self.g.future)
        deadline = time.monotonic() + 6
        while self.g.future and time.monotonic() < deadline:
            self.g.collect()
            pg.time.delay(3)
        self.assertIsNone(self.g.future)

    def open_library(self):
        self.press(pg.K_b)
        self.assertEqual(self.g.scene, "mica_library")
        if not self.g.p["settings"].get("mica_workshop"):
            self.press(pg.K_RETURN)

    def save_new(self, source=None):
        self.press(pg.K_n)
        self.assertEqual(self.g.scene, "terminal")
        if source is not None:
            self.press(pg.K_a, pg.KMOD_CTRL)
            self.g.event(pg.event.Event(pg.TEXTINPUT, text=source))
        self.press(pg.K_s, pg.KMOD_CTRL)
        self.assertEqual(self.g.scene, "mica_library")
        self.press(pg.K_RETURN)
        return self.g.p["program_library"]["slots"]["mica"]

    def test_revise_reopen_equip_and_deploy_same_program_on_two_maps(self):
        self.open_library()
        first = self.save_new()
        self.press(pg.K_v)
        self.finish_worker()
        self.press(pg.K_e)
        self.g.term.editor.replace("\n# New revision\n")
        self.press(pg.K_s, pg.KMOD_CTRL)
        self.press(pg.K_RETURN)
        second = self.g.p["program_library"]["slots"]["mica"]
        self.assertNotEqual(first, second)
        self.press(pg.K_v)
        self.finish_worker()
        self.press(pg.K_r)
        self.press(pg.K_c)
        self.press(pg.K_UP)
        self.press(pg.K_RIGHT)
        self.g.draw()
        self.assertEqual(self.g.mica_console.step, 1)
        self.assertEqual(self.g.mica_console.compare, 1)
        history = self.g.p["program_library"]["traces"]
        self.assertEqual(history[0]["snapshot_digest"], history[1]["snapshot_digest"])
        self.assertNotEqual(history[0]["source_hash"], history[1]["source_hash"])
        self.press(pg.K_ESCAPE)
        self.press(pg.K_ESCAPE)
        self.g.pool.shutdown()
        self.g = Game()
        self.addCleanup(self.g.pool.shutdown)
        self.open_library()
        library = self.g.p["program_library"]
        self.assertEqual(library["slots"]["mica"], second)
        self.assertEqual(library["revisions"][first]["source"], STARTER)
        self.assertEqual(library["revisions"][second]["parent"], first)
        for zone, relay in (("orientation", "hangar-relay"), ("workshop", "workshop-relay")):
            self.assertEqual(self.g.world.zone, zone)
            self.press(pg.K_d)
            self.finish_worker()
            self.assertEqual(self.g.scene, "world", self.g.mica_console.message)
            self.g.update_field(0.1)
            self.assertIsNotNone(self.g.world.mica_visual)
            self.g.draw()
            self.g.update_field(2)
            self.assertEqual(self.g.mica_job.status, "committed")
            self.assertEqual(
                progress.load()["runtime_v1"]["device_state"][f"{zone}.{relay}"], "online"
            )
            self.open_library()
            self.press(pg.K_d)
            self.assertIsNone(self.g.future)
            self.press(pg.K_ESCAPE)
            if zone == "orientation":
                self.press(pg.K_j)
                self.press(pg.K_8)
                self.open_library()
        restored = progress.load()
        self.assertEqual(restored["player"]["xp"], 100)
        self.assertEqual(restored["completed"], ["orientation_01"])
        self.assertEqual(restored["extra"], {"preserved": True})
        self.assertEqual(len(restored["program_library"]["traces"]), 4)
        self.assertEqual(len(LESSONS), 76)

    def test_invalid_program_and_recall_leave_device_untouched(self):
        self.open_library()
        key = self.save_new(
            'def plan(obs):\n    return [{"type": "move", "direction": "north"}] * 10\n'
        )
        self.press(pg.K_d)
        self.finish_worker()
        self.assertIn("COLLISION", self.g.mica_console.message)
        self.assertFalse(self.g.p["program_library"]["revisions"][key]["verified"])
        self.assertEqual(self.g.p["runtime_v1"]["device_state"], {})
        self.save_new()
        self.press(pg.K_d)
        self.finish_worker()
        self.g.update_field(0.2)
        self.press(pg.K_BACKSPACE)
        self.g.update_field(5)
        self.assertEqual(self.g.mica_job.status, "cancelled")
        self.assertIsNone(self.g.world.mica_visual)
        self.assertEqual(progress.load()["runtime_v1"]["device_state"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
