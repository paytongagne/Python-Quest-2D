"""Windows display smoke test using a disposable profile."""

import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import pygame as pg
from python_quest_2d.game.app import Game
from python_quest_2d.game.nursery import TRAM
from python_quest_2d.core.challenges import LESSONS

with tempfile.TemporaryDirectory() as folder:
    os.environ["PYTHONQUEST_SAVE"] = folder + "/progress.json"
    g = Game()
    assert pg.display.get_driver() == "windows"
    g.world.pos.update(TRAM["x"], TRAM["y"] + 25)
    g.interact()
    assert g.world.zone == "hydro"
    g.world.pos.update(220, 300)
    g.interact()
    assert g.term.ch["id"] == "hydro_01"
    g.term.editor.text = (ROOT / "content/authoring/hydro_01.py").read_text()
    g.submit()
    deadline = time.monotonic() + 8
    while g.future and time.monotonic() < deadline:
        pg.event.pump()
        g.collect()
        g.draw()
        pg.time.delay(10)
    assert not g.future and g.p.get("deployment")
    g.leave_terminal()
    frames = []
    for _ in range(170):
        pg.event.pump()
        start = time.perf_counter()
        g.update_field(1 / 60)
        g.draw()
        frames.append(time.perf_counter() - start)
        pg.time.delay(8)
    assert "hydro_01" in g.p["completed"]
    g.window = pg.display.set_mode((900, 600), pg.RESIZABLE)
    g.scene = "survey"
    g.draw()
    pg.event.post(pg.event.Event(pg.QUIT))
    g.run()
    print(
        "PASS Windows Greenline tram, Python route, animated docking, XP, survey, resize and quit"
    )
    print(
        f"Render/update mean {sum(frames) / len(frames) * 1000:.2f} ms; maximum {max(frames) * 1000:.2f} ms"
    )
