"""Scripted Windows campaign playtest. All saves are temporary."""

from collections import deque
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame as pg
from python_quest_2d.game.app import Game
from python_quest_2d.core.grade import grade
from python_quest_2d.core.challenges import LESSONS, ZONES
from python_quest_2d.core.progress import load, save
from python_quest_2d.core.legacy_migration import migrate


def key(g, k, mods=0):
    g.event(pg.event.Event(pg.KEYDOWN, key=k, mod=mods))


def navigate(g, obj, walk=True):
    w = g.world
    cell = lambda x, y: (int(x // 32), int(y // 32))
    blocked = {cell(r.x, r.y) for r in w.walls}
    blocked.update(cell(t["x"], t["y"]) for t in w.map["interactables"])
    blocked.update(
        cell(t["x"], t["y"])
        for t in w.map["gates"]
        if t["requires_challenge"] not in g.p["completed"]
    )
    start = cell(*w.pos)
    seen = {start: None}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if pg.Vector2(x * 32 + 16, y * 32 + 16).distance_to((obj["x"], obj["y"])) <= 43:
            break
        for other in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (
                other not in seen
                and other not in blocked
                and 0 <= other[0] < w.map["width"]
                and 0 <= other[1] < w.map["height"]
            ):
                seen[other] = (x, y)
                queue.append(other)
    else:
        return False
    if not walk:
        return True
    path = [(x, y)]
    while seen[path[-1]] is not None:
        path.append(seen[path[-1]])
    for x, y in reversed(path):
        for axis, target in enumerate((x * 32 + 16, y * 32 + 16)):
            for _ in range(50):
                d = target - w.pos[axis]
                if abs(d) < 0.1:
                    break
                direction = 1 if d > 0 else -1
                w.move(
                    direction if axis == 0 else 0,
                    direction if axis == 1 else 0,
                    min(0.025, abs(d) / 174),
                )
            else:
                raise AssertionError(f"Blocked walking to {(x, y)} from {w.pos}")
    return True


def checked(g, code):
    key(g, pg.K_a, pg.KMOD_CTRL)
    g.event(pg.event.Event(pg.TEXTINPUT, text=code))
    key(g, pg.K_RETURN, pg.KMOD_CTRL)
    assert g.future
    deadline = time.monotonic() + 8
    while g.future and time.monotonic() < deadline:
        g.draw()
        g.collect()
        pg.time.delay(8)
    assert not g.future
    g.draw()


def capture(g, name):
    if "PQ_CAPTURE" in os.environ:
        target = Path(os.environ["PQ_CAPTURE"])
        target.mkdir(parents=True, exist_ok=True)
        pg.image.save(g.canvas, target / (name + ".png"))


class Flight(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        os.environ["PYTHONQUEST_SAVE"] = self.temp.name + "/progress.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_campaign(self):
        g = Game()
        for zone in ZONES:
            self.assertEqual(g.world.zone, zone)
            for j, t in enumerate(g.world.map["interactables"]):
                if j < 3:
                    self.assertFalse(navigate(g, g.world.map["interactables"][j + 1], False))
                self.assertTrue(navigate(g, t))
                self.assertEqual(g.world.nearest(), t)
                k = t["challenge_id"]
                g.draw()
                if k == "orientation_01":
                    capture(g, "01-hangar")
                key(g, pg.K_e)
                self.assertEqual(g.term.ch["id"], k)
                if k == "orientation_01":
                    checked(g, "print('Offline')")
                    self.assertFalse(g.p["completed"])
                    capture(g, "02-debug")
                if k == "orientation_02":
                    key(g, pg.K_F1)
                solution = (ROOT / "content/authoring" / (k + ".py")).read_text(encoding="utf-8")
                checked(g, solution)
                self.assertIn(k, g.p["completed"], g.term.rows)
                if k == "orientation_01":
                    capture(g, "03-repair")
                    checked(g, solution)
                    self.assertEqual(g.p["player"]["xp"], 100)
                key(g, pg.K_ESCAPE)
                if k == "orientation_01":
                    pos = tuple(g.world.pos)
                    g.pool.shutdown()
                    g = Game()
                    self.assertEqual(tuple(g.world.pos), pos)
                    self.assertTrue(g.p["world_flags"]["gate_orientation_01"])
                    self.assertEqual(g.p["drafts"][k], solution)
            self.assertTrue(navigate(g, g.world.map["exit"]))
            key(g, pg.K_e)
        self.assertEqual(g.scene, "ending")
        self.assertEqual(g.p["player"]["xp"], 2375)
        g.draw()
        capture(g, "04-complete")
        g.pool.shutdown()

    def test_worker_failures(self):
        ch = LESSONS["launch_04"]
        for source, status in [
            ("def broken(", "syntax_error"),
            ("", "runtime_error"),
            ("raise RuntimeError('oops')", "runtime_error"),
            ("while True: pass", "timeout"),
            ("def can_launch(*a): return 1", "finished"),
            ("import os; os._exit(9)", "worker_crash"),
        ]:
            with self.subTest(status=status):
                result = grade(ch, source, 0.8)
                self.assertEqual(result["status"], status, result)
                self.assertFalse(result["passed"])
        ch = LESSONS["orientation_02"]
        self.assertFalse(grade(ch, "charge='25'\nprint(charge)")["passed"])

    def test_legacy_and_corruption(self):
        p = load()
        path = Path(self.temp.name) / "old.json"
        path.write_text('{"completed":[0],"hinted":[2],"drafts":{"1":"abc"},"xp":90}')
        migrate(path, p)
        self.assertEqual(load()["completed"], ["launch_01"])
        self.assertEqual(load()["player"]["xp"], 90)
        self.assertEqual(load()["drafts"], {"launch_02": "abc"})
        self.assertEqual(load()["hinted"], ["launch_03"])
        self.assertEqual(path.read_bytes(), path.with_suffix(".pre-2d.bak").read_bytes())
        Path(os.environ["PYTHONQUEST_SAVE"]).write_text("{")
        self.assertEqual(load()["completed"], [])
        self.assertTrue(list(path.parent.glob("*.damaged*")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
