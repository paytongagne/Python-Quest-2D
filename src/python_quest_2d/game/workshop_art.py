"""Live assembly-bay projections derived from tested object snapshots."""

import math
import pygame as pg
from .art import GOLD, MINT, MUTED, WHITE, label, rect


def machines(s, w, programs, tick, openings=None):
    for i, title in enumerate(
        ("DRONE ASSEMBLY", "PROBE CALIBRATION", "CHARGE REGULATOR", "HYDRAULIC RESERVOIR")
    ):
        x = 44 + i * 512
        rect(s, "#192b36", x, 280, 420, 260)
        pg.draw.rect(s, "#607586", (x, 280, 420, 260), 2)
        rect(s, GOLD, x, 280, 420, 3)
        label(s, title, x + 16, 296, 17, GOLD, True)
        result = programs.get(f"workshop_{i + 1:02}")
        label(
            s,
            "LIVE OBJECT MODEL" if result else "OFFLINE / REPAIR CONSOLE ABOVE",
            x + 16,
            512,
            13,
            MINT if result else MUTED,
            True,
        )
        if not result:
            for j in range(6):
                rect(s, "#314652", x + 30 + j * 61, 374, 40, 30)
            continue
        state = result["state"]
        if i == 0:
            for j, drone in enumerate(state):
                dx = x + 70 + j * 180 + int(math.sin(tick / 700) * drone["power"] / 5)
                y = 390 + j * 12
                pg.draw.ellipse(s, "#10202c", (dx - 25, y + 18, 60, 12))
                pg.draw.rect(s, MINT, (dx - 20, y - 20, 48, 34), border_radius=5)
                rect(s, "#284452", dx - 13, y - 14, 34, 12)
                for wheel in (-20, 18):
                    rect(s, "#101e2a", dx + wheel, y + 8, 12, 16)
                label(s, str(drone["id"]), dx - 20, y + 40, 15, WHITE, True)
                label(s, str(drone["power"]) + "% power", dx - 20, y + 62, 13, MUTED, True)
        elif i == 1:
            for j, probe in enumerate(state):
                center = (x + 110 + j * 200, 414)
                pg.draw.circle(s, "#384e5c", center, 62)
                pg.draw.circle(s, MINT, center, 62, 2)
                angle = math.pi * (1 - min(100, max(0, probe["reading"])) / 100)
                end = (center[0] + math.cos(angle) * 49, center[1] - math.sin(angle) * 49)
                pg.draw.line(s, GOLD, center, end, 4)
                label(s, str(probe["reading"]), center[0] - 17, center[1] + 25, 19, WHITE, True)
        elif i == 2:
            for j, battery in enumerate(state):
                bx = x + 70 + j * 185
                charge = battery["battery_percent"]
                pg.draw.rect(s, MINT, (bx, 350, 90, 120), 2)
                rect(s, "#3c8b78", bx + 6, 464 - charge, 78, charge)
                rect(s, MUTED, bx + 29, 339, 32, 10)
                label(s, str(charge) + "%", bx + 21, 479, 16, WHITE, True)
            label(s, "OVERFILL INTERLOCK ACTIVE", x + 35, 326, 13, MINT, True)
        else:
            tank = state[0]
            opened = (openings or {}).get("workshop_machine_4")
            fill = min(1, max(0, (tick - opened) / 1200)) if opened is not None else 1
            height = 112 * tank["water"] / max(1, tank["capacity"]) * fill
            pg.draw.rect(s, MINT, (x + 42, 349, 122, 125), 2)
            rect(s, "#4799b3", x + 48, 468 - height, 110, height)
            for j in range(4):
                y = 459 - int((tick / 25 + j * 23) % max(1, height - 6))
                pg.draw.circle(s, "#92d0da", (x + 70 + j * 23, y), 2)
            label(s, f"Tank {tank['water']} / {tank['capacity']}", x + 192, 365, 16, WHITE, True)
            label(s, f"Supply {tank['supply']}", x + 192, 403, 16, MUTED, True)
            label(s, "TRANSFER COMPLETE", x + 192, 445, 13, MINT, True)
