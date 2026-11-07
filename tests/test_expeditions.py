"""Travel and executable expedition acceptance using disposable saves."""

import json
import os
import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import Game, ROOT, checked, navigate, key, capture, pg
from python_quest_2d.core.challenges import LESSONS
from python_quest_2d.core.grade import grade
from python_quest_2d.core.progress import fresh, load, save
from python_quest_2d.core.expedition_contract import validate
from python_quest_2d.game.expedition import DESTINATIONS


class Expeditions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "save.json"
        os.environ["PYTHONQUEST_SAVE"] = str(self.path)
        self.g = Game()

    def tearDown(self):
        self.g.pool.shutdown()
        self.temp.cleanup()

    def restart(self):
        self.g.persist()
        self.g.pool.shutdown()
        self.g = Game()

    def test_travel_all_worlds_and_programs(self):
        g = self.g
        g.world.pos.update(180, 225)
        g.world.sync()
        before = g.p["player"].copy()
        key(g, pg.K_t)
        key(g, pg.K_2)
        self.assertEqual(g.world.zone, "orientation")
        key(g, pg.K_d)
        g.draw()
        capture(g, "expedition-star-map")
        for i, d in enumerate(DESTINATIONS[1:], 2):
            if g.scene != "starmap":
                key(g, pg.K_t)
            g.expeditions.preview = True
            key(g, pg.K_1 + i - 1)
            self.assertEqual(g.world.zone, d["zone"])
            key(g, pg.K_m)
            g.draw()
            self.assertEqual(g.scene, "survey")
            key(g, pg.K_ESCAPE)
            self.assertTrue(navigate(g, g.world.map["sites"][0]))
            key(g, pg.K_e)
            for j, t in enumerate(g.world.map["interactables"]):
                if d["id"] == "orion" and j in (0, 4, 8):
                    self.assertFalse(navigate(g, g.world.map["interactables"][j + 4], False))
                self.assertTrue(navigate(g, t))
                g.update_field(0.1)
                key(g, pg.K_e)
                self.assertEqual(g.scene, "terminal")
                ch = g.term.ch
                if ch["id"] == "orion_moon_02":
                    checked(g, "def shortest_route(grid,start,goal): return [start,goal]")
                    self.assertNotIn("expedition_job", g.p)
                    self.assertIn("cardinal", " ".join(g.term.rows))
                solution = (ROOT / "content/authoring" / (ch["id"] + ".py")).read_text()
                checked(g, solution)
                self.assertTrue(g.p.get("programs", {}).get(ch["id"]) is not None)
                if ch["id"] == "orion_moon_02":
                    capture(g, "expedition-python-route")
                key(g, pg.K_ESCAPE)
                if ch["output"] == "path":
                    self.assertNotIn(ch["id"], g.p["completed"])
                    g.update_field(0.1)
                    self.restart()
                    g = self.g
                    self.assertGreater(g.p["expedition_job"]["step"], 0)
                    for _ in range(200):
                        g.update_field(0.05)
                self.assertIn(ch["id"], g.p["completed"])
                if ch["id"] in ("orion_moon_14", "orion_moon_15"):
                    self.restart()
                    g = self.g
                    self.assertIn(ch["id"], g.p["completed"])
                    self.assertNotIn("orion_moon_16", g.p["completed"])
                g.draw()
                capture(g, "expedition-" + d["id"])
                if g.scene == "convoy_complete":
                    self.assertTrue(g.p["world_flags"]["moon_convoy_rescued"])
                    capture(g, "expedition-convoy")
                    key(g, pg.K_RETURN)
                if ch["id"] == "orion_moon_04":
                    key(g, pg.K_r)
                    key(g, pg.K_RIGHT)
                    g.draw()
                    capture(g, "expedition-step-replay")
                    self.assertEqual(g.expeditions.replay_step, 1)
                    key(g, pg.K_ESCAPE)
                if j == 3:
                    xp = g.p["player"]["xp"]
                    key(g, pg.K_e)
                    checked(g, solution)
                    key(g, pg.K_ESCAPE)
                    for _ in range(200):
                        g.update_field(0.05)
                    self.assertEqual(g.p["player"]["xp"], xp)
            self.restart()
            g = self.g
            self.assertEqual(g.world.zone, d["zone"])
            g.expeditions.preview = True
        key(g, pg.K_t)
        key(g, pg.K_1)
        self.assertEqual(g.world.zone, "orientation")
        self.assertEqual((g.world.pos.x, g.world.pos.y), (before["x"], before["y"]))
        self.assertEqual(g.p["player"]["xp"], 2800)

    def test_schema3_backup(self):
        p = fresh()
        p["schema_version"] = 3
        p["player"].update(zone="hydro", xp=3375, x=1460, y=310)
        p["completed"] = ["hydro_01", "hydro_02", "hydro_15"]
        p["deployment"] = {"key": "hydro_15", "commands": ["RIGHT"], "elapsed_steps": 0.25}
        p["world_flags"] = {"canopy_celebrated": True}
        p["custom"] = {"keep": 123}
        self.path.write_text(json.dumps(p))
        raw = self.path.read_bytes()
        upgraded = load()
        self.assertEqual(upgraded, dict(p, schema_version=4, program_library={"schema":1,"slots":{},"revisions":{},"traces":[]}, runtime_v1={"schema":1,"device_state":{},"active_job":None,"last_applied_event_ids":[]}))
        self.assertEqual(self.path.with_suffix(".pre-expedition.json").read_bytes(), raw)
        save(upgraded)
        self.assertEqual(load(), upgraded)
        self.assertEqual(self.path.with_suffix(".pre-expedition.json").read_bytes(), raw)

    def test_invalid_paths_and_worker_errors(self):
        ch = LESSONS["orion_moon_04"]
        for output in [None, {}, [], [[0, 0], [4, 0]], [[0, 0]] * 129, [[0, 0], [1, 1], [4, 0]]]:
            with self.assertRaises(ValueError):
                validate(ch, ch["cases"][0], output)
        for source, status in [
            ("def least_cost(", "syntax_error"),
            ("def least_cost(*a):\n    while True: pass", "timeout"),
            ("def least_cost(*a): raise ValueError('bad')", "runtime_error"),
        ]:
            r = grade(ch, source, 0.5)
            self.assertEqual(r["status"], status)
            self.assertFalse(r["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
