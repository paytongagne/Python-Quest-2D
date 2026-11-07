import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame as pg
from python_quest_2d.game.app import Game
from python_quest_2d.core.progress import load
from python_quest_2d.ui.terminal import Terminal
from python_quest_2d.core.challenges import LESSONS


class Controls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["PYTHONQUEST_SAVE"] = self.tmp.name + "/save.json"
        self.g = Game()
        self.g.scene = "terminal"
        self.g.term = Terminal(LESSONS["orientation_01"], self.g.p)

    def tearDown(self):
        self.g.pool.shutdown()
        self.tmp.cleanup()

    def key(self, key, mod=0):
        self.g.event(pg.event.Event(pg.KEYDOWN, key=key, mod=mod))

    def type(self, text):
        self.g.event(pg.event.Event(pg.TEXTINPUT, text=text))

    def test_edit_history_selection_and_pointer(self):
        ed = self.g.term.editor
        self.key(pg.K_a, pg.KMOD_CTRL)
        self.type("if True:")
        self.key(pg.K_RETURN)
        self.type("print(1)")
        self.assertEqual(ed.text, "if True:\n    print(1)")
        self.key(pg.K_z, pg.KMOD_CTRL)
        self.assertTrue(ed.text.endswith("    "))
        self.key(pg.K_y, pg.KMOD_CTRL)
        self.key(pg.K_HOME)
        self.key(pg.K_TAB, pg.KMOD_SHIFT)
        self.assertEqual(ed.text, "if True:\nprint(1)")
        self.g.draw()
        self.g.event(pg.event.Event(pg.MOUSEBUTTONDOWN, pos=(451, 143), button=1))
        self.assertEqual(ed.pos, 0)
        self.g.event(pg.event.Event(pg.MOUSEBUTTONUP, pos=(451, 143), button=1))
        self.key(pg.K_s, pg.KMOD_CTRL)
        self.assertEqual(load()["drafts"]["orientation_01"], ed.text)

    def test_reveal_requires_second_press(self):
        self.key(pg.K_F2)
        self.key(pg.K_ESCAPE)
        self.assertFalse(self.g.term.confirm)
        self.assertFalse(self.g.p.get("revealed"))
        self.key(pg.K_F2)
        self.key(pg.K_F2)
        self.key(pg.K_RETURN, pg.KMOD_CTRL)
        self.g.future.result(timeout=5)
        self.g.collect()
        self.assertEqual(load()["player"]["xp"], 25)

    def test_gate_and_wall_collision(self):
        w = self.g.world
        w.pos.update(370, 144)
        for _ in range(80):
            w.move(1, 0, 0.02)
        self.assertLess(w.pos.x, 384)
        w.pos.update(70, 80)
        for _ in range(80):
            w.move(-1, 0, 0.02)
        self.assertGreaterEqual(w.pos.x, 39)

    def test_clipboard(self):
        self.key(pg.K_a, pg.KMOD_CTRL)
        self.type("print(42)")
        self.key(pg.K_a, pg.KMOD_CTRL)
        self.key(pg.K_x, pg.KMOD_CTRL)
        self.assertEqual(self.g.term.editor.text, "")
        self.key(pg.K_v, pg.KMOD_CTRL)
        self.assertEqual(self.g.term.editor.text, "print(42)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
