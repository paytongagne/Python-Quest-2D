"""Open the real Windows SDL window, resize it and complete the first repair."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pygame as pg
from python_quest_2d.game.app import Game


def smoke():
    with tempfile.TemporaryDirectory() as folder:
        os.environ["PYTHONQUEST_SAVE"] = folder + "/progress.json"
        g = Game()
        assert pg.display.get_driver() == "windows"
        g.window = pg.display.set_mode((900, 600), pg.RESIZABLE)
        g.world.move(1, 0, 0.035)
        for _ in range(9):
            g.world.move(1, 1, 0.035)
        g.event(pg.event.Event(pg.KEYDOWN, key=pg.K_e, mod=0))
        assert g.term
        g.event(pg.event.Event(pg.TEXTINPUT, text="print('System online')"))
        g.submit()
        for _ in range(500):
            pg.event.pump()
            g.collect()
            g.draw()
            if not g.future:
                break
            pg.time.delay(10)
        assert g.p["player"]["xp"] == 100
        g.leave_terminal()
        pg.event.post(pg.event.Event(pg.QUIT))
        g.run()
        print("PASS: Windows display, 900x600 resize, terminal, worker, XP, quit")


if __name__ == "__main__":
    smoke()
