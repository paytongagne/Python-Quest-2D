"""Original landscape renderers and programs displayed as physical equipment."""

import math
import random
import pygame as pg
from .art import INK, PANEL, WHITE, MUTED, MINT, GOLD, label, rect, wrapped, pilot, terminal

COLORS = {
    "workshop": "#efba78",
    "orion_moon": "#b9abff",
    "titan_cloud": "#ffc488",
    "helix_bio": "#86e5d1",
    "aurora_ep": "#f3a3d0",
}


def landscape(w):
    from .pixel_world import landscape as paint

    return paint(w)


def board(s, key, ch, value, tick, progress=0):
    """Projection just above each console displays the actual output."""
    ox, oy = s.get_width() // 2, 70
    if ch.get("output") == "path":
        grid, start, goal = ch["cases"][0]["args"][:3]
        pitch = 36
        left = ox - len(grid[0]) * pitch // 2
        for y, row in enumerate(grid):
            for x, v in enumerate(row):
                c = "#8c5f71" if v in ("#", -1) else "#34495e"
                rect(s, c, left + x * pitch, oy + y * pitch, pitch - 2, pitch - 2)
                if type(v) is int and v >= 0:
                    label(s, v, left + x * pitch + 5, oy + y * pitch + 3, 12, GOLD, True)
        if value:
            pts = [(left + x * pitch + 17, oy + y * pitch + 17) for x, y in value]
            if len(pts) > 1:
                pg.draw.lines(s, MINT, False, pts, 2)
            index = min(int(progress), len(pts) - 1)
            nxt = min(index + 1, len(pts) - 1)
            a = pg.Vector2(pts[index])
            b = pg.Vector2(pts[nxt])
            p = a.lerp(b, progress % 1)
            pg.draw.rect(s, GOLD, (p.x - 8, p.y - 7, 16, 14), border_radius=3)
            rect(s, "#28444d", p.x - 6, p.y - 5, 12, 5)
            if key == "orion_moon_16" and index > 0:
                escort = pts[max(0, index - 1)]
                pg.draw.rect(s, MINT, (escort[0] - 7, escort[1] - 6, 14, 12), border_radius=3)
            label(
                s, f"STEP {index}/{len(pts) - 1}", left, oy + len(grid) * pitch + 5, 13, WHITE, True
            )
        else:
            label(s, "ROVER AWAITING PLAN", left, oy + len(grid) * pitch + 5, 12, GOLD, True)
    elif key == "orion_moon_01":
        pts = {"A": (ox - 70, oy + 38), "B": (ox, oy), "C": (ox + 70, oy + 38), "D": (ox, oy + 82)}
        for node, neighbors in (value or {}).items():
            for other in neighbors:
                pg.draw.line(s, MINT, pts[node], pts[other], 3)
        for name, p in pts.items():
            pg.draw.circle(s, "#887bc0", p, 12)
            label(s, name, p[0] - 5, p[1] - 9, 15, WHITE, True)
    elif key == "orion_moon_03":
        grid = ch["cases"][0]["args"][0]
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                rect(s, "#819ac5" if c == "." else "#302d4d", ox - 60 + x * 24, oy + y * 20, 21, 17)
        label(s, "POCKETS " + str(value or "?"), ox - 85, oy + 110, 14, MINT, True)
    elif key in ("orion_moon_06", "orion_moon_14") and value:
        for i, name in enumerate(value):
            x = 25 + i * 75
            rect(s, "#506b7b", x, oy + 25, 68, 35)
            label(s, str(name), x + 4, oy + 34, 13, WHITE, True)
        label(s, "DISPATCH ORDER", 25, oy - 5, 14, GOLD, True)
    elif key == "orion_moon_15" and value:
        for i, work in enumerate(value):
            x = 35 + i * 70
            rect(s, MINT, x, oy + 90 - work["bfs"] * 4, 18, work["bfs"] * 4)
            rect(s, GOLD, x + 22, oy + 90 - work["scan"] * 4, 18, work["scan"] * 4)
        label(s, "BFS / SCAN WORK COUNTS", 25, oy + 110, 13, WHITE, True)
    elif key == "orion_moon_10" and value is not None:
        paths = ch["cases"][0]["args"]
        for row, path in enumerate(paths):
            for i, (x, y) in enumerate(path):
                pg.draw.circle(s, GOLD if i == value else MINT, (45 + i * 80, oy + row * 50), 10)
                label(s, str([x, y]), 25 + i * 80, oy + row * 50 + 14, 12, WHITE, True)
        label(s, "CONFLICT TICK " + str(value), 25, oy + 110, 14, GOLD, True)
    else:
        wrapped(
            s, str(value) if value is not None else "Awaiting program", 30, oy, 280, 14, MINT, True
        )


def draw(w, bg, lessons, tick, openings=None):
    from .pixel_world import draw as paint

    return paint(w, bg, lessons, tick, openings)


def display(s, w, programs, tick):
    zone = w.zone
    rect(s, "#111e30", 450, 260, 540, 290)
    if zone == "titan_cloud":
        model = programs.get("titan_cloud_01", {})
        messages = model.get("messages", [])
        label(s, "OFFLINE PACKET EXCHANGE", 470, 272, 17, GOLD, True)
        for i, packet in enumerate(messages):
            x = 470 + int((tick / 12 + i * 110) % 370)
            y = 325 + i % 3 * 40
            pg.draw.rect(s, "#80684f", (x, y, 70, 28), border_radius=5)
            label(s, repr(packet), x + 7, y + 5, 14, WHITE, True)
        label(s, "PENDING " + repr(model.get("pending", "")), 470, 450, 14, MUTED, True)
        lanes = programs.get("titan_cloud_03", [])
        for i in range(3):
            rect(s, MINT if i in lanes else "#415168", 955, 280 + i * 60, 30, 40)
        if "titan_cloud_02" in programs:
            label(
                s,
                "FRAME " + ("VALID" if not programs["titan_cloud_02"] else "QUARANTINE"),
                470,
                500,
                16,
                MINT,
                True,
            )
        if "titan_cloud_04" in programs:
            label(s, "DELIVERED " + repr(programs["titan_cloud_04"]), 470, 525, 16, GOLD, True)
    elif zone == "helix_bio":
        label(s, "TOY ECG / SYNTHETIC TEST UNITS", 468, 273, 16, MINT, True)
        samples = programs.get("helix_bio_04") or programs.get("helix_bio_01", [])
        if samples:
            pts = [
                (470 + i * 450 / max(1, len(samples) - 1), 370 - v * 60)
                for i, v in enumerate(samples)
            ]
            pg.draw.lines(s, MINT, False, pts, 2)
            cursor = 470 + int(tick / 15) % 450
            pg.draw.line(s, "#477b80", (cursor, 308), (cursor, 425))
        label(s, "DISPLAY TEST / NO PATIENT DATA", 468, 457, 14, MUTED, True)
        if "helix_bio_02" in programs:
            label(s, "CLOCK ms " + str(programs["helix_bio_02"]), 460, 510, 14, MINT, True)
        if "helix_bio_03" in programs:
            baseline = programs["helix_bio_03"]
            pts = [(470 + i * 210, 438 - v * 4) for i, v in enumerate(baseline)]
            pg.draw.lines(s, GOLD, False, pts, 2)
    elif zone == "aurora_ep":
        label(s, "TOY CHAMBER / SYNTHETIC GEOMETRY", 466, 272, 15, "#f3a3d0", True)
        center = pg.Vector2(700, 375)
        angle = tick / 2500

        def project(p):
            x, y, z = p
            return center + pg.Vector2(
                (x * math.cos(angle) + z * math.sin(angle)) * 64,
                y * -48 + (z * math.cos(angle) - x * math.sin(angle)) * 20,
            )

        for latitude in (-0.65, 0, 0.65):
            radius = math.sqrt(1 - latitude * latitude) * 2
            points = [
                project(
                    [
                        radius * math.cos(i * math.pi / 24),
                        latitude * 2,
                        radius * math.sin(i * math.pi / 24),
                    ]
                )
                for i in range(49)
            ]
            pg.draw.lines(s, "#7e6aab", False, points, 1)
        point = (
            programs.get("aurora_ep_03")
            or programs.get("aurora_ep_02")
            or programs.get("aurora_ep_01", {}).get("position")
        )
        if point:
            pos = project(point)
            pg.draw.line(s, GOLD, (650, 450), pos, 3)
            pg.draw.circle(s, WHITE, pos, 6)
        label(s, "CURSOR " + str(point or "awaiting samples"), 468, 458, 13, MUTED, True)
        for i, name in enumerate(("A", "B", "C")):
            pos = project([math.cos(i * 2) * 1.8, math.sin(i * 2), math.sin(i * 2) * 1.8])
            accepted = name in programs.get("aurora_ep_04", [])
            pg.draw.circle(s, MINT if accepted else "#82617b", pos, 5)
            label(s, name, pos.x + 8, pos.y - 6, 12, WHITE, True)
        if "aurora_ep_04" in programs:
            label(s, "ACCEPTED " + str(programs["aurora_ep_04"]), 470, 510, 14, MINT, True)
