"""Object contracts, physical bay traversal, presentation and save regression."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import Game, ROOT, checked, navigate, key, capture, pg
from python_quest_2d.core.challenges import LESSONS
from python_quest_2d.core.grade import grade
from python_quest_2d.ui.hud import fit_text


class Workshop(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        os.environ["PYTHONQUEST_SAVE"] = str(Path(self.temp.name) / "save.json")
        self.g = Game()

    def tearDown(self):
        self.g.pool.shutdown()
        self.temp.cleanup()

    def test_class_contracts(self):
        for n in range(1, 5):
            ch = LESSONS[f"workshop_{n:02}"]
            code = (ROOT / f"content/authoring/{ch['id']}.py").read_text()
            result = grade(ch, code)
            self.assertTrue(result["passed"], result)
            self.assertEqual(result["effect"], ch["cases"][0]["expected"])
            self.assertFalse(grade(ch, ch["starter_code"])["passed"])
        ch = LESSONS["workshop_03"]
        code = (ROOT / "content/authoring/workshop_03.py").read_text()
        self.assertFalse(
            grade(
                ch,
                code.replace(
                    "type(value) not in (int, float)", "not isinstance(value, (int, float))"
                ),
            )["passed"]
        )
        ch = LESSONS["workshop_04"]
        code = (ROOT / "content/authoring/workshop_04.py").read_text()
        self.assertFalse(
            grade(ch, code.replace("self.supply -= moved", "self.supply = self.supply"))["passed"]
        )

    def test_bays_save_and_presentations(self):
        g = self.g
        # Existing arbitrary completed mission, draft, flag and review must survive.
        g.p["completed"] = ["orientation_01"]
        g.p["player"]["xp"] = 100
        g.p["drafts"]["orientation_01"] = 'print("retained")'
        g.p["world_flags"]["previous_checkpoint"] = True
        g.persist()
        key(g, pg.K_j)
        key(g, pg.K_8)
        self.assertEqual(g.world.zone, "workshop")
        self.assertIsNotNone(g.presentation.arrival)
        g.draw()
        capture(g, "workshop-arrival")
        key(g, pg.K_RETURN)
        self.assertIsNone(g.presentation.arrival)
        for n, t in enumerate(g.world.map["interactables"][:4], 1):
            if n < 4:
                self.assertFalse(navigate(g, g.world.map["interactables"][n], False))
            self.assertTrue(navigate(g, t))
            key(g, pg.K_e)
            self.assertEqual(g.scene, "terminal")
            code = (ROOT / f"content/authoring/workshop_{n:02}.py").read_text()
            checked(g, code)
            self.assertIn(f"workshop_{n:02}", g.p["completed"], g.term.rows)
            key(g, pg.K_ESCAPE)
            g.update_field(0.1)
            g.draw()
            capture(g, f"workshop-bay-{n}")
            xp = g.p["player"]["xp"]
            key(g, pg.K_e)
            checked(g, code)
            key(g, pg.K_ESCAPE)
            self.assertEqual(g.p["player"]["xp"], xp)
        g.persist()
        g.pool.shutdown()
        self.g = g = Game()
        self.assertEqual(g.world.zone, "workshop")
        self.assertEqual(g.p["player"]["xp"], 500)
        self.assertEqual(g.p["drafts"]["orientation_01"], 'print("retained")')
        self.assertTrue(g.p["world_flags"]["previous_checkpoint"])
        for i in range(4):
            g.world.pos.update(270 + i * 512, 600)
            g.world.sync()
            g.refresh()
            g.draw()
            capture(g, f"workshop-restored-{i + 1}")
        key(g, pg.K_t)
        g.expeditions.preview = True
        key(g, pg.K_2)
        g.draw()
        capture(g, "workshop-orion-arrival")
        key(g, pg.K_t)
        key(g, pg.K_1)
        self.assertEqual(g.world.zone, "workshop")
        key(g, pg.K_j)
        key(g, pg.K_1)
        self.assertEqual(g.world.zone, "orientation")
        g.draw()
        capture(g, "workshop-astra-hud")

    def test_fitted_text_and_mouse_travel(self):
        s = pg.Surface((1088, 690))
        for ch in LESSONS.values():
            self.assertLessEqual(fit_text(s, ch["title"], (850, 240, 207, 44)), 44, ch["id"])
        g = self.g
        key(g, pg.K_t)
        g.window = pg.display.set_mode((1280, 720), pg.RESIZABLE)
        g.draw()
        x = g.view.x + 320 * g.view.w / 1088
        y = g.view.y + 390 * g.view.h / 690
        event = pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=(x, y))
        g.event(event)
        self.assertEqual(g.world.zone, "orientation")
        self.assertIn("locked", g.notice)
        key(g, pg.K_d)
        g.event(event)
        self.assertEqual(g.world.zone, "orion_moon")
        g.p["settings"]["reduced_motion"] = True
        g.draw()


if __name__ == "__main__":
    unittest.main(verbosity=2)
