"""Field equipment, live rover visualization, survey map and objectives."""

import math
import pygame as pg
from .art import rect, label, wrapped, PANEL, MINT, MUTED, WHITE, GOLD, INK
from ..core.challenges import LESSONS
from ..core.route import trace

TITLE = "Hydroponics Station"
BAYS = ("Dispatch rail", "Seed bank", "Logger vault", "Pump gallery")
TRAM = dict(type="tram", x=223, y=244)
HAZARD = pg.Rect(1268, 315, 110, 30)


def greenhouse(s):
    # Each bay has a glazed canopy and a pair of copper supply pipes.
    for bay in range(16):
        x = bay * 384 + 43
        rect(s, "#112b32", x, 37, 303, 42)
        for i in range(33):
            px = x + 5 + i * 9
            height = 6 + (i * 17 + bay * 7) % 27
            pg.draw.line(s, "#4d766b", (px, 74), (px + 2, 74 - height), 2)
            pg.draw.ellipse(s, "#82ad82", (px - 4, 70 - height, 8, 4))
            pg.draw.ellipse(s, "#577c6e", (px, 75 - height // 2, 7, 4))
        for dx in (0, 76, 152, 228, 300):
            rect(s, "#526e78", x + dx, 36, 3, 44)
        for y in (437, 444):
            rect(s, "#705d49", x, y, 299, 4)
            for dx in (15, 75, 155, 235):
                rect(s, "#97a49c", x + dx, y - 2, 5, 8)


def objective(p):
    for i in range(1, 17):
        key = f"hydro_{i:02}"
        if key not in p["completed"]:
            return f"Bay {i:02} / " + LESSONS[key]["title"]
    return (
        "Find the grower's field log in the pump gallery."
        if not p["world_flags"].get("grower_log")
        else "Nursery restored. Return via the west tram."
    )


def draw_tram(s, t, color):
    x, y = t["x"], t["y"]
    pg.draw.rect(s, "#192c3a", (x - 22, y - 16, 44, 31), border_radius=6)
    for i in (-11, -3, 5):
        pg.draw.lines(s, color, False, [(x + i, y - 6), (x + i + 5, y), (x + i, y + 6)], 2)
    label(s, "TRAM", x - 17, y + 19, 12, color, True)


def field(s, w, tick):
    if w.zone != "hydro":
        draw_tram(s, TRAM, GOLD)
        label(s, "FIELD LOG", 902, 188, 13, MINT, True)
        return
    draw_tram(s, w.map["exit"], MINT)
    for i, name in enumerate(w.map["bay_names"]):
        label(s, name.upper(), i * 384 + 46, 90, 16, "#aecab9", True)
    # Glass propagation racks cast a cool light on the service floor.
    fed = w.p.get("irrigated", [])
    for i, (x, y) in enumerate(w.map["beds"]):
        pg.draw.rect(s, "#172735", (x, y, 66, 53), border_radius=5)
        rect(s, "#849fa2", x + 2, y + 1, 62, 4)
        for n in range(3):
            for m in range(2):
                px, py = x + 12 + 20 * n, y + 19 + 19 * m
                color = "#70d39a" if i in fed else "#b9a06d"
                pg.draw.line(s, color, (px, py), (px, py - 8), 2)
                pg.draw.ellipse(s, color, (px - 7, py - 10, 8, 5))
                pg.draw.ellipse(s, color, (px, py - 13, 8, 5))
        label(s, "0" + str(i), x + 3, y + 54, 12, MINT, True)
    for key, origin in w.map["boards"].items():
        args = LESSONS[key]["cases"][0]["args"]
        grid, start, goal = args
        ox, oy = origin
        pitch = 28
        rect(s, "#12252f", ox - 5, oy - 5, len(grid[0]) * pitch + 9, len(grid) * pitch + 9)
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                r = pg.Rect(ox + x * pitch, oy + y * pitch, pitch - 2, pitch - 2)
                pg.draw.rect(s, "#76515a" if tile == "#" else "#35505a", r)
                if tile == "#":
                    pg.draw.line(s, GOLD, r.topleft, r.bottomright, 2)
        gx, gy = goal
        pg.draw.rect(s, GOLD, (ox + gx * pitch + 3, oy + gy * pitch + 3, 20, 20), 2)
        vx, vy = goal if key in w.p["completed"] else start
        job = w.p.get("deployment")
        if job and job["key"] == key:
            points = trace(args, job["commands"])
            idx = min(len(points) - 1, int(w.flight))
            nxt = min(idx + 1, len(points) - 1)
            frac = 0 if w.p["settings"].get("reduced_motion") else w.flight % 1
            vx, vy = [a + (b - a) * frac for a, b in zip(points[idx], points[nxt])]
        px, py = round(ox + vx * pitch + 13), round(oy + vy * pitch + 13)
        rect(s, "#182833", px - 12, py - 8, 24, 18)
        rect(s, GOLD, px - 9, py - 10, 18, 16)
        rect(s, "#194251", px - 7, py - 6, 14, 6)
        rect(s, MINT, px - 5, py - 5, 4, 2)
        label(s, "MICA", ox, oy + len(grid) * pitch + 6, 12, GOLD, True)
    draw_machines(s, w, tick)
    # MARA wears a copper work suit and a helmet lamp.
    rect(s, "#915948", 136, 317, 20, 20)
    rect(s, GOLD, 137, 302, 18, 16)
    rect(s, "#365666", 139, 307, 15, 5)
    label(s, "MARA", 128, 342, 14, GOLD, True)
    rect(s, "#92bab4", 1432, 101, 16, 22)
    rect(s, "#243744", 1435, 107, 10, 3)
    if w.p["world_flags"].get("diagnostic_lens"):
        label(s, "ARCHIVE", 1407, 129, 13, MINT, True)
    active = "hydro_04" not in w.p["completed"]
    pg.draw.rect(s, "#603e37" if active else "#294c46", HAZARD)
    for i in range(5):
        x = HAZARD.x + 8 + 20 * i
        rect(s, GOLD if active else MINT, x, HAZARD.y + 4, 4, 20)
        if active:
            pg.draw.circle(s, "#bdc8bb", (x, HAZARD.y - 3 - int((tick / 65 + i * 4) % 20)), 4, 1)
    label(s, "PRESSURE LINE", HAZARD.x, HAZARD.bottom + 5, 13, GOLD if active else MINT, True)


def draw_machines(s, w, tick):
    outputs = w.p.get("instruments", {})
    for n in range(5, 17):
        key = f"hydro_{n:02}"
        x = (n - 1) * 384 + 85
        y = 370 if n % 2 else 133
        if n in (7, 11, 15):
            continue
        rect(s, "#172c36", x, y, 216, 66)
        rect(s, "#5f8187", x, y, 216, 3)
        label(s, "LIVE  /  " + w.map["bay_names"][n - 1].upper(), x + 9, y + 10, 12, MINT, True)
        value = outputs.get(key)
        if value is None:
            label(s, "AWAITING CONTROL", x + 10, y + 32, 14, GOLD, True)
            continue
        if n in (12, 16):
            # Boolean valve states and capstone commands drive an animated actuator.
            phase = int(tick / 650) % max(1, len(value))
            action = value[phase] if value else "HOLD"
            opened = action is True or action == "PUMP"
            color = MINT if opened else GOLD if action == "VENT" else MUTED
            rect(s, color, x + 174, y + 24, 25, 25)
            rect(s, "#142731", x + 178, y + 29, 17 if opened else 6, 15)
            label(
                s,
                str(action) + "  " + str(phase + 1) + "/" + str(len(value)),
                x + 10,
                y + 33,
                14,
                color,
                True,
            )
        else:
            wrapped(s, str(value), x + 10, y + 30, 195, 12, WHITE, True)
    if "hydro_16" in w.p["completed"]:
        for x in range(5990, 6110, 24):
            pg.draw.circle(s, MINT, (x, 72), 4)


def survey(s, w):
    m = w.map
    rect(s, PANEL, 75, 48, 936, 590)
    label(s, "Deck survey", 102, 66, 32)
    page = min(3, int(w.pos.x // 1536)) if w.zone == "hydro" else 0
    offset = page * 48
    visible = 48 if w.zone == "hydro" else m["width"]
    label(
        s,
        m["sectors"][page] if w.zone == "hydro" else w.zone.replace("_", " ").title(),
        105,
        110,
        19,
        GOLD,
    )
    scale = min(18, 850 // visible)
    ox = (1088 - scale * visible) // 2
    oy = 151
    for y, row in enumerate(m["tiles"]):
        for x, c in enumerate(row[offset : offset + visible]):
            rect(
                s,
                "#5e7381" if c == "#" else "#233944",
                ox + x * scale,
                oy + y * scale,
                scale - 1,
                scale - 1,
            )

    def dot(t, color, radius):
        x = t["x"] / 32 - offset
        if 0 <= x < visible:
            pg.draw.circle(s, color, (int(ox + x * scale), int(oy + t["y"] / 32 * scale)), radius)

    for t in m["interactables"]:
        dot(t, MINT if t["challenge_id"] in w.p["completed"] else GOLD, 5)
    for gate in m["gates"]:
        if gate["requires_challenge"] not in w.p["completed"]:
            dot(gate, "#dc7d7d", 5)
    dot(
        m["exit"]
        if w.zone == "hydro"
        else (
            m["exit"] if w.zone in ("orion_moon", "titan_cloud", "helix_bio", "aurora_ep") else TRAM
        ),
        "#b79bfc",
        6,
    )
    dot(dict(x=w.pos.x, y=w.pos.y), WHITE, 6)
    label(
        s,
        "White: pilot     Amber: repair     Red: bulkhead     Violet: tram",
        105,
        514,
        16,
        MUTED,
        True,
    )
    wrapped(
        s,
        objective(w.p)
        if w.zone == "hydro"
        else "Reach the west tram near PIP to visit Hydroponics.",
        105,
        550,
        840,
        18,
        WHITE,
    )
    label(s, "M / Esc   Close survey", 105, 595, 15, MINT, True)
