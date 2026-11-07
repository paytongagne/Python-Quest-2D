"""Capture actual Pygame windows at declared sizes with disposable visual fixture saves."""

import argparse, os, sys, tempfile, json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
parser.add_argument("--output", required=True)
parser.add_argument("--orion-only", action="store_true")
a = parser.parse_args()
root = Path(a.root).resolve()
out = Path(a.output).resolve()
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "src"))
import pygame as pg
from python_quest_2d.game.app import Game
from python_quest_2d.core.challenges import LESSONS

with tempfile.TemporaryDirectory() as tmp:
    os.environ["PYTHONQUEST_SAVE"] = str(Path(tmp) / "visual.json")
    g = Game()
    assert pg.display.get_driver() == "windows"
    zones = (
        ["orion_moon"]
        if a.orion_only
        else ["orientation", "orion_moon", "workshop", "titan_cloud", "helix_bio", "aurora_ep"]
    )
    rows = []
    for size in [(1280, 720), (1600, 900), (1920, 1080)]:
        g.window = pg.display.set_mode(size, pg.RESIZABLE)
        for zone in zones:
            for pos in range(2):
                g.world.enter(zone)
                t = g.world.map["interactables"][0 if pos == 0 else 3]
                g.world.pos.update(t["x"] - 80, t["y"] + 100)
                # Avoid posing inside the Workshop's fixed machinery footprint.
                if zone == "workshop":
                    g.world.pos.update(t["x"], 600)
                # Pose only in collision-free space; a camera test must not stand in a wall.
                desired=g.world.pos.copy()
                candidates=[pg.Vector2((int(desired.x)//32+dx)*32+16,(int(desired.y)//32+dy)*32+16) for dy in range(-3,4) for dx in range(-3,4)]
                obstacles=g.world.walls+[pg.Rect(t['x']-15,t['y']-10,30,20) for t in g.world.map['interactables']]
                for point in sorted(candidates,key=lambda v:v.distance_squared_to(desired)):
                    body=pg.Rect(0,0,18,16);body.center=point
                    if body.collidelist(obstacles)<0:
                        g.world.pos.update(point);break
                else:raise AssertionError('No safe visual-test position')
                g.world.sync()
                g.refresh()
                g.presentation.arrival = None
                g.presentation.reward = None
                g.scene = "world"
                g.notice = "Field survey: approach a device to program or inspect its diagnostics."
                for _ in range(3):
                    pg.event.pump()
                    g.draw()
                name = f"{zone}-{size[0]}x{size[1]}-view{pos + 1}.png"
                pg.image.save(g.window, out / name)
                rows.append(
                    dict(
                        file=name,
                        zone=zone,
                        size=size,
                        player=list(g.world.pos),
                        camera=list(g.world.camera),
                    )
                )
    (out / "manifest.json").write_text(json.dumps(rows, indent=2))
    g.pool.shutdown()
    pg.quit()
    print("Captured", len(rows), "native Windows screenshots at", out)
