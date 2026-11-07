"""Regression for physical art, diagnostics, navigation and Workshop second wing."""

import os, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import Game, ROOT, checked, navigate, key, pg
from python_quest_2d.core.challenges import LESSONS
from python_quest_2d.core.grade import grade


class VisualRevision(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["PYTHONQUEST_SAVE"] = str(Path(self.tmp.name) / "save.json")
        self.g = Game()

    def tearDown(self):
        self.g.pool.shutdown()
        self.tmp.cleanup()

    def test_entrance_diagnostics_and_sizes(self):
        g = self.g
        entrance = next(s for s in g.world.map["sites"] if s["type"] == "district")
        self.assertTrue(navigate(g, entrance))
        key(g, pg.K_e)
        self.assertEqual(g.world.zone, "workshop")
        for zone in ("orion_moon", "workshop", "titan_cloud", "helix_bio", "aurora_ep"):
            g.world.enter(zone)
            g.refresh()
            self.assertTrue(navigate(g, g.world.map["interactables"][0]))
            key(g, pg.K_o)
            self.assertEqual(g.scene, "diagnostics")
            for size in ((1280, 720), (1600, 900), (1920, 1080)):
                g.window = pg.display.set_mode(size, pg.RESIZABLE)
                g.draw()
                self.assertTrue(g.window.get_rect().contains(g.view))
            key(g, pg.K_ESCAPE)
            self.assertEqual(g.scene, "world")
        g.world.enter("orion_moon")
        g.refresh()
        from python_quest_2d.game.pixel_world import props

        y, kind, x, color, phase = props(g.world)[0]
        g.world.pos.update(x, y)
        g.world.sync()
        # A pre-update save overlapping a new prop can escape without being reset.
        original = g.world.pos.copy()
        for _ in range(15):
            g.world.move(1, 0, 0.025)
        self.assertGreater(g.world.pos.x, original.x + 32)

    def test_second_wing_campaign_and_save(self):
        g = self.g
        g.p["completed"] = [f"workshop_{i:02}" for i in range(1, 5)]
        g.p["player"]["xp"] = 400
        g.p["drafts"]["hydro_01"] = "retained draft"
        key(g, pg.K_j)
        key(g, pg.K_8)
        for i, t in enumerate(g.world.map["interactables"][4:], 5):
            self.assertTrue(navigate(g, t))
            if i < 8:
                self.assertFalse(navigate(g, g.world.map["interactables"][i], False))
            key(g, pg.K_e)
            self.assertEqual(g.scene, "terminal")
            ch = g.term.ch
            self.assertFalse(grade(ch, ch["starter_code"])["passed"])
            code = (ROOT / f"content/authoring/{ch['id']}.py").read_text()
            checked(g, code)
            self.assertIn(ch["id"], g.p["completed"], g.term.rows)
            key(g, pg.K_ESCAPE)
            key(g, pg.K_o)
            g.draw()
            key(g, pg.K_ESCAPE)
            xp = g.p["player"]["xp"]
            key(g, pg.K_e)
            checked(g, code)
            key(g, pg.K_ESCAPE)
            self.assertEqual(g.p["player"]["xp"], xp)
            g.persist()
            g.pool.shutdown()
            self.g = g = Game()
            self.assertEqual(g.p["player"]["xp"], i * 100)
            self.assertEqual(g.p["drafts"]["hydro_01"], "retained draft")
        self.assertEqual(g.p["player"]["xp"], 800)

    def test_incorrect_advanced_contracts(self):
        ch = LESSONS["workshop_05"]
        code = (ROOT / "content/authoring/workshop_05.py").read_text()
        self.assertFalse(
            grade(ch, code.replace("class SurveyRover(Rover):", "class SurveyRover:"))["passed"]
        )
        ch = LESSONS["workshop_07"]
        code = (ROOT / "content/authoring/workshop_07.py").read_text()
        self.assertFalse(grade(ch, code.replace("raise SensorFault", "raise ValueError"))["passed"])
        ch = LESSONS["workshop_08"]
        self.assertFalse(
            grade(
                ch,
                'def count_errors(path):\n    with open(path) as dummy: pass\n    f = open(path)\n    return sum(x.strip().startswith("ERROR:") for x in f)',
            )["passed"]
        )
        self.assertFalse(grade(ch, "def count_errors(path): return 2")["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
