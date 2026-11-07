"""Greenline release acceptance. Only temporary profiles are used."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import Game, ROOT, checked, navigate, key, capture, pg
from python_quest_2d.core.challenges import LESSONS, ZONES
from python_quest_2d.core.grade import grade
from python_quest_2d.core.progress import fresh, load
from python_quest_2d.game.nursery import TRAM, HAZARD


class Greenline(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "progress.json"
        os.environ["PYTHONQUEST_SAVE"] = str(self.path)
        self.g = Game()

    def tearDown(self):
        self.g.pool.shutdown()
        self.temp.cleanup()

    def walk(self, t):
        self.assertTrue(navigate(self.g, t))
        self.assertEqual(self.g.world.nearest()["type"], t["type"])
        key(self.g, pg.K_e)

    def restart(self):
        self.g.persist()
        self.g.pool.shutdown()
        self.g = Game()

    def test_world_and_robot_campaign(self):
        self.walk(TRAM)
        g = self.g
        self.assertEqual(g.world.zone, "hydro")
        mara = g.world.map["sites"][0]
        self.walk(mara)
        self.assertIn("eastbound", g.notice)
        key(g, pg.K_m)
        g.draw()
        self.assertEqual(g.scene, "survey")
        capture(g, "greenline-survey")
        key(g, pg.K_m)
        key(g, pg.K_j)
        g.draw()
        key(g, pg.K_ESCAPE)
        for i, t in enumerate(g.world.map["interactables"], 1):
            if i < 16:
                self.assertFalse(navigate(g, g.world.map["interactables"][i], False))
            self.walk(t)
            k = t["challenge_id"]
            if i == 1:
                checked(g, "def plan_route(grid,start,goal): return ['UP']")
                self.assertIn("leaves the grid", " ".join(g.term.rows))
                self.assertNotIn("deployment", g.p)
            source = (ROOT / "content/authoring" / (k + ".py")).read_text(encoding="utf-8")
            checked(g, source)
            if i == 15:
                capture(g, "greenline-programming")
                key(g, pg.K_F4)
                g.draw()
                self.assertLessEqual(g.term.brief_scroll, max(0, g.term.brief_height - 620))
            key(g, pg.K_ESCAPE)
            if LESSONS[k].get("simulation") == "route":
                self.assertNotIn(k, g.p["completed"])
                g.update_field(0.45)
                self.assertGreater(g.world.flight, 0)
                g.draw()
                if i == 1:
                    capture(g, "greenline-dispatch")
                    previous = g.world.flight
                    self.restart()
                    g = self.g
                    self.assertEqual(g.world.flight, previous)
                for _ in range(600):
                    g.update_field(0.05)
                self.assertNotIn("deployment", g.p)
                if i == 1:
                    self.walk(g.world.map["sites"][0])
                    self.assertIn("seed bank", g.notice)
                    self.walk(t)
                    checked(g, source)
                    key(g, pg.K_ESCAPE)
                    for _ in range(40):
                        g.update_field(0.1)
                    self.assertEqual(g.p["player"]["xp"], 100)
            self.assertIn(k, g.p["completed"], k)
            if i == 2:
                self.assertEqual(g.p["irrigated"], [0, 2])
            if i == 3:
                g.world.pos.update(HAZARD.center)
                g.update_field(0.1)
                self.assertFalse(HAZARD.collidepoint(g.world.pos))
                self.restart()
                g = self.g
                self.assertIn("hydro_03", g.p["completed"])
                self.assertNotIn("hydro_04", g.p["completed"])
        self.assertTrue(g.p["world_flags"]["diagnostic_lens"])
        self.assertEqual(g.scene, "canopy")
        self.assertTrue(g.p["world_flags"]["canopy_celebrated"])
        self.assertEqual(
            g.p["instruments"]["hydro_16"], LESSONS["hydro_16"]["cases"][0]["expected"]
        )
        g.draw()
        capture(g, "greenline-restored")
        key(g, pg.K_RETURN)
        self.walk(g.world.map["sites"][1])
        self.assertTrue(g.p["world_flags"]["grower_log"])
        self.restart()
        g = self.g
        self.assertEqual(g.p["player"]["xp"], 1600)
        self.assertEqual(g.p["irrigated"], [0, 2])
        g.update_field(2)
        self.assertLessEqual(g.world.camera.x, g.world.map["width"] * 32 - 768)
        capture(g, "greenline-gallery") if not g.draw() else None
        self.walk(dict(g.world.map["exit"], type="tram"))
        self.assertEqual(g.world.zone, "orientation")

    def test_all_deck_extensions(self):
        g = self.g
        for zone in ZONES:
            g.world.enter(zone)
            g.refresh()
            m = g.world.map
            self.assertEqual((m["width"], m["height"]), (32, 18))
            for row in m["tiles"]:
                self.assertEqual(len(row), 32)
            site = m["sites"][0]
            self.assertFalse(navigate(g, site, False))
            g.p["completed"].append(zone + "_01")
            self.walk(site)
            g.update_field(2)
            self.assertGreater(g.world.camera.x, 240)
            self.assertLessEqual(g.world.camera.x, 256)
            g.draw()
            self.assertTrue(g.p["world_flags"]["log_" + zone])
            self.walk(TRAM)
            self.assertEqual(g.world.zone, "hydro")
            self.walk(dict(g.world.map["exit"], type="tram"))
            self.assertEqual(g.world.zone, zone)

    def test_route_contract(self):
        ch = LESSONS["hydro_01"]
        for ans, msg in [
            ("['RIGHT']*65", "at most"),
            ("['FLY']", "Step 1"),
            ("[]", "stopped"),
            ("'RIGHT'", "list"),
            ("['LEFT']", "leaves"),
            ("[1]", "Step 1"),
        ]:
            r = grade(ch, "def plan_route(grid,start,goal): return " + ans)
            self.assertFalse(r["passed"])
            self.assertIn(msg, " ".join(r["rows"]))
            self.assertIsNone(r.get("effect"))
        r = grade(LESSONS["hydro_03"], "def plan_route(grid,start,goal): return ['DOWN']")
        self.assertIn("obstruction", " ".join(r["rows"]))
        exploit = "def plan_route(grid,start,goal):\n    goal[:]=start\n    return []"
        self.assertFalse(grade(ch, exploit)["passed"])
        r = grade(ch, "def plan_route(*args):\n    while True: pass", 0.5)
        self.assertEqual(r["status"], "timeout")
        r = grade(ch, "def plan_route(*args): print('x'*20000)")
        self.assertIn("8192", " ".join(r["rows"]))

    def test_sector_travel_and_paused_dispatch(self):
        g = self.g
        key(g, pg.K_j)
        key(g, pg.K_7)
        key(g, pg.K_2)
        self.assertEqual(g.scene, "greenline_travel")
        key(g, pg.K_1)
        self.assertEqual(g.world.zone, "hydro")
        g.p["completed"].append("hydro_04")
        key(g, pg.K_j)
        key(g, pg.K_7)
        key(g, pg.K_2)
        self.assertEqual(g.world.pos.x, 1636)
        g.update_field(0.1)
        g.draw()
        self.assertEqual(g.scene, "world")
        g.p["deployment"] = {"key": "hydro_01", "commands": ["RIGHT"] * 4}
        key(g, pg.K_j)
        key(g, pg.K_7)
        key(g, pg.K_1)
        self.assertEqual(g.scene, "greenline_travel")

    def test_old_save_migration(self):
        p = fresh()
        p.update(
            schema_version=2,
            completed=["orientation_01", "orientation_02", "orientation_03"],
            drafts={"launch_01": "def f(): pass"},
            attempts={"orientation_01": 3},
            novel_field="retain",
        )
        p["player"].update(xp=300, zone="sensor", x=187, y=222)
        p["world_flags"]["gate_orientation_01"] = True
        p["settings"]["sound"] = False
        raw = json.dumps(p).encode()
        self.path.write_bytes(raw)
        upgraded = load()
        self.assertEqual(upgraded, dict(p, schema_version=4, program_library={"schema":1,"slots":{},"revisions":{},"traces":[]}, runtime_v1={"schema":1,"device_state":{},"active_job":None,"last_applied_event_ids":[]}))
        self.assertEqual(self.path.with_suffix(".pre-greenline.json").read_bytes(), raw)
        self.assertEqual(self.path.read_bytes(), raw)
        self.restart_from_file(upgraded)

    def restart_from_file(self, p):
        from python_quest_2d.core.progress import save

        save(p)
        self.g.pool.shutdown()
        self.g = Game()
        self.assertEqual(self.g.p, p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
