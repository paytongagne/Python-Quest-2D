"""Deck-specific equipment silhouettes. Solved bays energize their instruments."""

import math

import pygame as pg

from .art import label, rect

SYSTEMS = ("UPLINK", "THRUST", "ROUTER", "RADAR", "TURBINE", "CORE")


def draw_instrument(s, zone, x, y, color, powered, tick):
    pg.draw.ellipse(s, "#1b2e39", (x - 43, y + 9, 86, 22))
    rect(s, "#526878", x - 32, y + 11, 64, 8)
    rect(s, "#152631", x - 28, y + 14, 56, 8)
    c = color if powered else "#859ca7"
    phase = tick * 0.002 if powered else 0.8
    if zone == 0:
        # Directional antenna, struts and horn.
        pg.draw.polygon(s, "#687f8e", [(x - 9, y + 13), (x + 9, y + 13), (x + 2, y - 12)])
        pg.draw.polygon(
            s,
            "#aabac0",
            [(x - 28, y - 25), (x + 22, y - 2), (x + 9, y + 4), (x - 8, y - 1), (x - 21, y - 10)],
        )
        pg.draw.line(s, c, (x - 3, y - 11), (x + 6, y - 29), 3)
        pg.draw.circle(s, c, (x + 7, y - 30), 4)
    elif zone == 1:
        for d in (-15, 12):
            pg.draw.polygon(
                s,
                "#b1bbc2",
                [
                    (x + d, y - 30),
                    (x + d + 9, y - 17),
                    (x + d + 9, y + 6),
                    (x + d - 8, y + 6),
                    (x + d - 8, y - 17),
                ],
            )
            rect(s, "#526878", x + d - 9, y - 9, 18, 6)
            pg.draw.polygon(
                s,
                c,
                [
                    (x + d - 5, y + 6),
                    (x + d + 6, y + 6),
                    (x + d, y + 14 + int(3 * math.sin(phase))),
                ],
            )
    elif zone == 2:
        for i in range(3):
            rect(s, "#6d838e", x - 30 + i * 21, y - 28, 18, 40)
            for j in range(5):
                rect(s, "#283946", x - 28 + i * 21, y - 25 + j * 7, 14, 4)
                rect(s, c, x - 27 + i * 21, y - 24 + j * 7, 3, 2)
    elif zone == 3:
        pg.draw.circle(s, "#344c58", (x, y - 6), 26)
        for r in (8, 16, 24):
            pg.draw.circle(s, c, (x, y - 6), r, 1)
        pg.draw.line(
            s, c, (x, y - 6), (x + int(23 * math.cos(phase)), y - 6 + int(23 * math.sin(phase))), 3
        )
    elif zone == 4:
        pg.draw.circle(s, "#657c87", (x, y - 7), 26)
        pg.draw.circle(s, "#21333f", (x, y - 7), 22)
        for i in range(6):
            a = phase + i * math.pi / 3
            pts = [
                (x + int(r * math.cos(a + d)), y - 7 + int(r * math.sin(a + d)))
                for r, d in [(4, 0), (20, 0.18), (15, 0.8)]
            ]
            pg.draw.polygon(s, c, pts)
        pg.draw.circle(s, "#edf1ce", (x, y - 7), 5)
    else:
        points = [(x, y - 36), (x + 25, y - 13), (x, y + 10), (x - 25, y - 13)]
        pg.draw.polygon(s, "#3e3c58", points)
        pg.draw.lines(s, c, True, points, 2)
        pg.draw.line(s, c, (x, y - 36), (x, y + 10), 2)
        pg.draw.line(s, c, (x - 25, y - 13), (x + 25, y - 13), 1)
    label(s, SYSTEMS[zone], x - 25, y + 25, 12, c, True)
