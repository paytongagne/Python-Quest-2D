"""Ephemeral arrival staging, focus cues and repair feedback; never changes saves."""

import math
import pygame as pg
from .art import GOLD, MINT, PANEL, WHITE, label, rect
from ..ui.hud import fit_text

INTROS = {
    "orientation": ("ASTRA RESEARCH FACILITY", "Engineering decks / home station"),
    "orion_moon": ("ORION RELAY MOON", "Low orbit insertion / lunar rover operations"),
    "titan_cloud": ("TITAN CLOUDWORKS", "Cloud descent / packet exchange infrastructure"),
    "helix_bio": ("HELIX BIOMEDICAL CAMPUS", "Research docking / synthetic signal instrumentation"),
    "aurora_ep": (
        "AURORA MAPPING OBSERVATORY",
        "Observatory approach / spatial mapping laboratory",
    ),
    "workshop": ("ASTRA / WORKSHOP DISTRICT", "Freight elevator / object engineering"),
}


class Presentation:
    def __init__(self, g):
        self.g = g
        self.seen = set(g.p["completed"])
        self.reward = None
        self.arrival = None
        self.departure = None

    def arrive(self):
        self.arrival = (pg.time.get_ticks(), INTROS.get(self.g.world.zone, INTROS["orientation"]))

    def draw(self):
        g = self.g
        now = pg.time.get_ticks()
        fresh = set(g.p["completed"]) - self.seen
        if fresh:
            self.reward = (now, sorted(fresh)[-1])
            self.seen.update(fresh)
        if g.scene != "world":
            # Keep the reward ready until the player leaves the editor.
            if self.reward:
                self.reward = (now, self.reward[1])
            return
        s = g.canvas
        reduced = g.p["settings"].get("reduced_motion")
        near = g.world.nearest()
        if near:
            x = near["x"] - g.world.camera.x + 12
            y = near["y"] - g.world.camera.y + 77
            old = s.get_clip()
            s.set_clip((12, 77, 768, 576))
            radius = 27 if reduced else 27 + int(2 * math.sin(now / 180))
            pg.draw.ellipse(s, GOLD, (x - radius, y - 14, radius * 2, 28), 2)
            label(s, "[E]", x - 13, y - 61, 14, GOLD, True)
            s.set_clip(old)
        target = next(
            (t for t in g.world.map["interactables"] if t["challenge_id"] not in g.p["completed"]),
            None,
        )
        if target:
            tx = target["x"] - g.world.camera.x + 12
            ty = target["y"] - g.world.camera.y + 77 - 60
            x = max(30, min(760, tx))
            y = max(94, min(630, ty))
            pg.draw.polygon(s, GOLD, [(x, y + 7), (x - 5, y), (x, y - 7), (x + 5, y)])
        if self.reward:
            age = (now - self.reward[0]) / 1000
            if age < 3:
                rect(s, PANEL, 30, 92, 430, 62)
                rect(s, MINT, 30, 92, 4, 62)
                label(s, "SYSTEM RESTORED", 46, 100, 13, MINT, True)
                from ..core.challenges import LESSONS

                fit_text(s, LESSONS[self.reward[1]]["title"], (46, 121, 400, 27), 18)
                if not reduced:
                    for i in range(14):
                        a = i * 2.4
                        x = 245 + math.cos(a) * age * 55
                        y = 165 + math.sin(a) * age * 20 + age * 14
                        pg.draw.circle(s, MINT, (x, y), max(1, 3 - int(age)))
            else:
                self.reward = None
        if self.arrival:
            age = (now - self.arrival[0]) / 1000
            duration = 4.2
            if age >= duration:
                self.arrival = None
                self.departure = None
                return
            title, subtitle = self.arrival[1]
            if age < 2.8 and not reduced:
                panel = pg.Surface((768, 576))
                if age < 1.2 and self.departure is not None:
                    panel.blit(self.departure, (0, 0))
                    stage = "DEPARTURE / launch clearance confirmed"
                else:
                    panel.fill("#0c1728")
                    for i in range(65):
                        x = (i * 109 + int(age * 240)) % 768
                        y = (i * 73) % 576
                        pg.draw.line(panel, "#607995", (x, y), (x + 18, y), 1)
                    stage = "IN TRANSIT / " + title
                from .pixel_world import stamp

                stamp(panel, "shuttle", 384, 430 - int(age * 95), g.accent)
                label(panel, stage, 24, 28, 17, WHITE, True)
                label(panel, "Any key skips travel", 24, 540, 14, MINT, True)
                s.blit(panel, (12, 77))
            else:
                # Reveal the world with a compact title; no obstruction of its center.
                rect(s, PANEL, 24, 91, 740, 76)
                label(s, title, 40, 100, 24, WHITE)
                label(s, subtitle, 40, 136, 15, g.accent)
