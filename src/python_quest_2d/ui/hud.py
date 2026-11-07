"""Shared bounded mission and communications panels."""

import pygame as pg
from ..game.art import PANEL, WHITE, MUTED, MINT, GOLD, label, rect, wrapped
from ..core.challenges import LESSONS


def fit_text(s, text, bounds, size=16, color=WHITE):
    box = pg.Rect(bounds)
    for chosen in range(size, 10, -1):
        panel = pg.Surface(box.size)
        panel.fill(PANEL)
        bottom = wrapped(panel, text, 0, 0, box.width, chosen, color)
        if bottom <= box.height:
            s.blit(panel, box)
            return bottom
    s.blit(panel, box)
    return bottom


def sidebar(g, keys):
    s = g.canvas
    rect(s, PANEL, 795, 77, 281, 576)
    label(s, "ENGINEERING RECORD", 812, 92, 13, g.accent, True)
    label(s, str(g.p["player"]["xp"]) + " XP", 812, 115, 33)
    label(s, f"{len(g.p['completed'])} / {len(LESSONS)} missions", 812, 161, 15, MUTED, True)
    rect(s, "#365060", 812, 190, 246, 4)
    rect(s, g.accent, 812, 190, 246 * len(g.p["completed"]) / len(LESSONS), 4)
    label(s, "LOCAL SYSTEMS", 812, 211, 13, g.accent, True)
    for i, key in enumerate(keys):
        y = 240 + i * 53
        done = key in g.p["completed"]
        label(s, "OK" if done else key[-2:], 812, y, 15, MINT if done else GOLD, True)
        fit_text(s, LESSONS[key]["title"], (850, y - 1, 207, 44))
    rect(s, "#365060", 812, 458, 246, 1)
    label(s, "FIELD COMMS", 812, 474, 13, g.accent, True)
    fit_text(s, g.notice, (812, 499, 246, 141))
