"""Native Windows expedition smoke check. Uses a disposable profile."""

import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import pygame as pg
from python_quest_2d.game.app import Game

with tempfile.TemporaryDirectory() as tmp:
    os.environ["PYTHONQUEST_SAVE"] = tmp + "/profile.json"
    g = Game()
    assert pg.display.get_driver() == "windows"
    g.scene = "starmap"
    g.expeditions.preview = True
    g.draw()
    assert g.expeditions.travel(1)
    for t in g.world.map["interactables"][:2]:
        g.world.pos.update(t["x"], t["y"] + 30)
        g.world.sync()
        g.refresh()
        g.interact()
        assert g.scene == "terminal"
        code = (ROOT / "content/authoring" / (t["challenge_id"] + ".py")).read_text()
        g.event(pg.event.Event(pg.KEYDOWN, key=pg.K_a, mod=pg.KMOD_CTRL))
        g.event(pg.event.Event(pg.TEXTINPUT, text=code))
        g.event(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN, mod=pg.KMOD_CTRL))
        end = time.monotonic() + 8
        while g.future and time.monotonic() < end:
            pg.event.pump()
            g.collect()
            g.draw()
            pg.time.delay(10)
        assert not g.future
        g.leave_terminal()
    frames = []
    for _ in range(210):
        pg.event.pump()
        start = time.perf_counter()
        g.update_field(1 / 60)
        g.draw()
        frames.append(time.perf_counter() - start)
        pg.time.delay(10)
    assert g.p["player"]["xp"] == 200
    g.event(pg.event.Event(pg.KEYDOWN, key=pg.K_r, mod=0))
    g.event(pg.event.Event(pg.KEYDOWN, key=pg.K_RIGHT, mod=0))
    g.draw()
    assert g.scene == "replay"
    g.event(pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE, mod=0))
    g.window = pg.display.set_mode((1280, 720), pg.RESIZABLE)
    for destination in (2, 3, 4, 0):
        assert g.expeditions.travel(destination)
        g.draw()
        pg.event.pump()
    pg.event.post(pg.event.Event(pg.QUIT))
    g.run()
    print(
        "PASS: native star map, five destinations, Python editing, route delivery, replay, resize, return and quit."
    )
    print(
        f"Update/render mean {sum(frames) / len(frames) * 1000:.2f} ms; max {max(frames) * 1000:.2f} ms"
    )
