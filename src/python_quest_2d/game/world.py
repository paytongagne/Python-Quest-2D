import math

import pygame as pg

from ..core.challenges import MAPS
from .nursery import TRAM


class World:
    def __init__(self, progress):
        self.p = progress
        self.enter(progress["player"]["zone"], resume=True)

    def enter(self, zone, resume=False):
        self.zone = zone
        self.map = MAPS[zone]
        self.walls = [
            pg.Rect(x * 32, y * 32, 32, 32)
            for y, row in enumerate(self.map["tiles"])
            for x, tile in enumerate(row)
            if tile in "# "
        ]
        if zone in ("orion_moon", "workshop", "titan_cloud", "helix_bio", "aurora_ep"):
            from .pixel_world import props

            self.walls += [
                pg.Rect(int(x // 32) * 32, int(y // 32) * 32, 32, 32)
                for y, kind, x, color, phase in props(self)
            ]
        player = self.p["player"]
        player["zone"] = zone
        pos = player if resume else self.map["spawn"]
        self.pos = pg.Vector2(pos["x"], pos["y"])
        self.face = (0, 1)
        self.steps = 0
        self.moving = False
        self.flight = self.p.get("deployment", {}).get("elapsed_steps", 0.0)
        self.camera = pg.Vector2(max(0, min(self.pos.x - 384, self.map["width"] * 32 - 768)), 0)
        self.sync()

    def sync(self):
        self.p["player"].update(x=self.pos.x, y=self.pos.y)

    def move(self, dx, dy, dt):
        velocity = pg.Vector2(dx, dy)
        self.moving = bool(velocity)
        if not velocity:
            return
        velocity = velocity.normalize() * 174 * min(dt, 0.04)
        self.face = (dx, dy)
        obstacles = self.walls + [
            pg.Rect(g["x"], g["y"], 32, 32)
            for g in self.map["gates"]
            if g["requires_challenge"] not in self.p["completed"]
        ]
        obstacles += [pg.Rect(t["x"] - 15, t["y"] - 10, 30, 20) for t in self.map["interactables"]]
        for axis in (0, 1):
            old = self.pos[axis]
            self.pos[axis] += velocity[axis]
            body = pg.Rect(0, 0, 18, 16)
            body.center = self.pos
            if body.collidelist(obstacles) >= 0:
                previous = body.copy()
                previous.center = (old, self.pos.y) if axis == 0 else (self.pos.x, old)
                overlap = lambda r: sum(r.clip(o).width * r.clip(o).height for o in obstacles)
                # A legacy save inside newly placed scenery can walk out, never further in.
                if overlap(previous) == 0 or overlap(body) > overlap(previous):
                    self.pos[axis] = old
            else:
                self.steps += abs(velocity[axis])
        self.sync()

    def nearest(self):
        if self.zone in ("orion_moon", "titan_cloud", "helix_bio", "aurora_ep", "workshop"):
            things = [*self.map["interactables"], self.map["exit"], *self.map["sites"]]
            return min(
                (t for t in things if math.dist(self.pos, (t["x"], t["y"])) <= 54),
                key=lambda t: math.dist(self.pos, (t["x"], t["y"])),
                default=None,
            )
        things = [
            *self.map["interactables"],
            dict(self.map["exit"], type="tram" if self.zone == "hydro" else "lift"),
            *self.map.get("sites", []),
            *([TRAM] if self.zone != "hydro" else []),
            {"type": "pip", "x": 104, "y": 195},
        ]
        return min(
            (t for t in things if math.dist(self.pos, (t["x"], t["y"])) <= 54),
            key=lambda t: math.dist(self.pos, (t["x"], t["y"])),
            default=None,
        )
