"""Two-pixel art system: shared light direction, material palettes and grounded sprites."""

import math
import random
from functools import lru_cache
import pygame as pg

PALETTES = {
    "orion_moon": ("#56566c", "#5b5a70", "#66647a", "#35394e", "#9291a3", "#aec0d2"),
    "workshop": ("#333f47", "#37444b", "#47545b", "#192934", "#72818a", "#edb86b"),
    "titan_cloud": ("#344251", "#384959", "#4a5c69", "#1c2b3b", "#8296a5", "#efbd83"),
    "helix_bio": ("#36524f", "#3b5955", "#4f6c64", "#203d3e", "#8bb7a1", "#9ce9cd"),
    "aurora_ep": ("#37415c", "#3b4663", "#4b5876", "#222c48", "#8799bf", "#e7b2d9"),
}


def box(s, c, r):
    pg.draw.rect(s, c, r)


def poly(s, c, pts):
    pg.draw.polygon(s, c, pts)


@lru_cache(None)
def sprite(kind, color="#b6c8d5", phase=0):
    s = pg.Surface((64, 64), pg.SRCALPHA)
    # Feet are at (32,52); consistent southeast cast shadows.
    pg.draw.ellipse(s, (11, 22, 34, 100), (18, 48, 34, 8))
    dark = "#172c3a"
    shade = "#536b7e"
    light = "#d8e3dd"
    if kind in ("pilot", "npc"):
        step = (-1, 1, 0, 0)[phase % 4]
        box(s, dark, (24, 40, 7, 11 + step))
        box(s, dark, (34, 40, 7, 11 - step))
        box(s, shade, (24, 41, 6, 6))
        box(s, shade, (35, 41, 6, 6))
        box(s, dark, (21, 27, 24, 17))
        box(s, color, (24, 25, 17, 18))
        box(s, light, (25, 26, 4, 11))
        box(s, shade, (38, 28, 3, 12))
        box(s, color, (19, 30 + step, 4, 11))
        box(s, color, (43, 30 - step, 4, 11))
        box(s, dark, (22, 12, 22, 17))
        box(s, light, (24, 11, 18, 17))
        box(s, "#7e9eac", (40, 14, 3, 12))
        box(s, "#203e54", (25, 16, 16, 8))
        box(s, "#76d7dc", (26, 17, 11, 2))
        box(s, "#ecf6ed", (26, 14, 5, 1))
        box(s, "#e2b56f", (27, 32, 10, 5))
        box(s, dark, (29, 33, 3, 2))
    elif kind == "console":
        box(s, dark, (20, 29, 26, 23))
        box(s, shade, (22, 31, 22, 17))
        poly(s, light, [(21, 28), (40, 25), (46, 31), (25, 34)])
        box(s, dark, (21, 14, 24, 17))
        box(s, color, (23, 15, 20, 12))
        box(s, "#163e4c", (24, 16, 18, 10))
        for i in range(3):
            box(s, color, (26, 18 + i * 3, 6 + (i + phase) % 3 * 3, 1))
        box(s, "#7ee2c0", (40, 36, 2, 2))
        box(s, "#bbc7c4", (27, 36, 9, 2))
        box(s, "#344959", (25, 41, 15, 4))
    elif kind == "rover":
        for x in (18, 39):
            for y in (29, 42):
                box(s, dark, (x, y, 8, 10))
                box(s, shade, (x + 1, y + 2, 5, 2))
        poly(s, shade, [(23, 28), (38, 28), (42, 33), (42, 48), (22, 48), (22, 33)])
        box(s, color, (24, 29, 15, 15))
        box(s, light, (25, 29, 12, 3))
        box(s, dark, (27, 34, 10, 7))
        box(s, "#88dbd3", (28, 35, 8, 2))
        box(s, light, (32, 18, 2, 11))
        box(s, color, (28, 16, 10, 4))
        box(s, "#8ee8c1", (23, 45, 3, 2))
        box(s, "#edbb79", (36, 45, 3, 2))
    elif kind == "dish":
        box(s, dark, (25, 43, 22, 9))
        box(s, shade, (29, 31, 8, 17))
        poly(s, shade, [(13, 24), (19, 15), (46, 22), (47, 31), (32, 37), (20, 31)])
        poly(s, light, [(14, 22), (21, 13), (46, 21), (41, 29), (29, 31)])
        pg.draw.line(s, color, (29, 24), (39, 11), 2)
        box(s, "#eff5eb", (38, 9, 3, 3))
        box(s, color, (29, 40, 7, 3))
    elif kind == "crate":
        box(s, dark, (20, 33, 28, 20))
        box(s, shade, (21, 29, 25, 21))
        poly(s, light, [(21, 29), (29, 24), (49, 27), (46, 32)])
        poly(s, color, [(22, 32), (45, 32), (45, 49), (22, 49)])
        box(s, shade, (26, 34, 3, 14))
        box(s, shade, (38, 34, 3, 14))
        box(s, light, (30, 37, 7, 5))
    elif kind == "rack":
        box(s, dark, (21, 13, 25, 41))
        box(s, shade, (22, 12, 22, 39))
        box(s, light, (22, 12, 22, 3))
        box(s, dark, (25, 17, 16, 30))
        for y in range(19, 45, 6):
            box(s, "#4d7885", (26, y, 12, 3))
            box(s, color if (y + phase) % 3 else "#dbe6dd", (37, y, 2, 2))
        box(s, light, (22, 48, 22, 2))
    elif kind == "plant":
        poly(s, shade, [(25, 42), (43, 42), (40, 52), (28, 52)])
        box(s, "#abc6a8", (25, 41, 18, 3))
        for dx, dy in [(-7, -13), (4, -20), (10, -6), (-1, -4)]:
            pg.draw.line(s, "#4a8272", (34, 43), (34 + dx, 35 + dy), 2)
            poly(
                s,
                "#83b798",
                [(34 + dx, 35 + dy), (26 + dx, 30 + dy), (29 + dx, 24 + dy), (35 + dx, 28 + dy)],
            )
    elif kind == "shuttle":
        poly(s, dark, [(4, 44), (19, 24), (31, 14), (43, 24), (60, 44), (48, 51), (16, 51)])
        poly(s, shade, [(6, 42), (25, 32), (39, 32), (58, 42), (48, 47), (16, 47)])
        poly(s, light, [(21, 43), (22, 27), (31, 16), (41, 27), (43, 43)])
        poly(s, "#315c74", [(26, 29), (31, 22), (37, 29), (37, 36), (26, 36)])
        box(s, color, (25, 40, 15, 4))
        box(s, "#e9ba78", (13, 44, 5, 4))
        box(s, "#e9ba78", (46, 44, 5, 4))
    elif kind == "tank":
        pg.draw.ellipse(s, dark, (20, 43, 30, 10))
        box(s, shade, (21, 20, 27, 26))
        pg.draw.ellipse(s, light, (21, 14, 27, 13))
        box(s, color, (24, 24, 20, 14))
        box(s, "#305b68", (27, 25, 13, 11))
        box(s, "#91d6cd", (28, 31, 11, 4))
        box(s, light, (22, 24, 3, 19))
        pg.draw.arc(s, light, (21, 38, 27, 12), 3.1, 6.2, 2)
        box(s, shade, (45, 28, 8, 4))
        box(s, light, (51, 30, 3, 16))
    elif kind == "scope":
        pg.draw.ellipse(s, shade, (17, 39, 36, 12))
        box(s, light, (29, 31, 8, 13))
        poly(s, shade, [(16, 20), (23, 14), (48, 29), (42, 36)])
        poly(s, light, [(16, 18), (22, 12), (48, 27), (42, 33)])
        pg.draw.ellipse(s, dark, (39, 25, 12, 11))
        pg.draw.ellipse(s, color, (41, 27, 8, 7))
        box(s, color, (20, 19, 5, 5))
        box(s, light, (19, 42, 5, 8))
        box(s, light, (45, 42, 5, 8))
    elif kind == "beacon":
        box(s, shade, (29, 28, 5, 23))
        box(s, light, (29, 28, 2, 22))
        box(s, dark, (25, 24, 13, 8))
        box(s, color, (27, 25, 9, 4))
    return s


def stamp(s, kind, x, y, color="#b6c8d5", phase=0):
    art = sprite(kind, color, phase)
    s.blit(pg.transform.scale(art, (64, 64)), (int(x) - 32, int(y) - 52))


def character(s, x, y, w):
    # Sprite pixels are built at the same scale as environment props.
    art = sprite("pilot", "#e5ac66", int(w.steps // 9) % 4 if getattr(w,'moving',False) else 0)
    if w.face[1]<0:
        art=art.copy()
        box(art,'#b8cbd0',(25,16,16,8))
        box(art,'#748e9b',(28,27,10,12))
        box(art,'#c5dad1',(29,28,8,3))
    # Match horizontal facing without resampling.
    if w.face[0] < 0:
        art = pg.transform.flip(art, True, False)
    s.blit(art, (int(x) - 32, int(y) - 52))


def landscape(w):
    """Bake richly textured terrain at a 2px grid; retain the collision map unchanged."""
    width, height = w.map["width"], w.map["height"]
    zone = w.zone
    base, alt, rim, shadow, light, accent = PALETTES[zone]
    s = pg.Surface((width * 16, height * 16))
    s.fill(base)
    rng = random.Random(zone)
    lunar = zone == "orion_moon"
    for y, row in enumerate(w.map["tiles"]):
        for x, t in enumerate(row):
            X, Y = x * 16, y * 16
            col = (
                alt
                if (math.sin(x * 0.43) + math.cos(y * 0.57) + math.sin((x + y) * 0.21)) > 0.5
                else base
            )
            box(s, col, (X, Y, 16, 16))
            if lunar:
                for _ in range(9):
                    px, py = X + rng.randrange(16), Y + rng.randrange(16)
                    box(s, rim if rng.random() > 0.4 else shadow, (px, py, 1, 1))
                if (x * 17 + y * 29) % 11 == 0 and t != "#":
                    pg.draw.arc(s, rim, (X + 2, Y + 5, 11, 5), 0, 3.1, 1)
                    pg.draw.arc(s, shadow, (X + 3, Y + 6, 9, 4), 3.1, 6.2, 1)
            else:
                if x % 2 == 0:
                    pg.draw.line(s, shadow, (X, Y), (X, Y + 15))
                if y % 2 == 0:
                    pg.draw.line(s, shadow, (X, Y), (X + 15, Y))
                box(s, rim, (X + 2, Y + 2, 1, 1))
                if (x + y) % 9 == 0:
                    for n in range(3):
                        box(s, shadow, (X + 4, Y + 7 + n * 2, 8, 1))
            if t == "#":
                if zone == "workshop" and 9 <= y <= 16 and 2 <= x % 16 <= 14:
                    # Footprints become assembly equipment, not giant display panels.
                    box(s, base, (X, Y, 16, 16))
                    for gy in range(0, 16, 4):
                        pg.draw.line(s, shadow, (X, Y + gy), (X + 15, Y + gy))
                        pg.draw.line(s, rim, (X, Y + gy + 1), (X + 15, Y + gy + 1))
                    if x % 16 in (2, 14):
                        pg.draw.line(s, accent, (X + 2, Y + 1), (X + 9, Y + 8), 2)
                    continue
                if lunar:
                    poly(
                        s,
                        shadow,
                        [
                            (X, Y + 7),
                            (X + 5, Y + 2),
                            (X + 14, Y + 4),
                            (X + 18, Y + 17),
                            (X + 2, Y + 17),
                        ],
                    )
                    poly(
                        s,
                        rim,
                        [
                            (X, Y + 4),
                            (X + 5, Y),
                            (X + 13, Y + 2),
                            (X + 16, Y + 10),
                            (X + 8, Y + 14),
                            (X, Y + 10),
                        ],
                    )
                    poly(
                        s, light, [(X + 1, Y + 4), (X + 5, Y + 1), (X + 12, Y + 3), (X + 7, Y + 5)]
                    )
                    pg.draw.line(s, base, (X + 8, Y + 6), (X + 10, Y + 12))
                else:
                    box(s, shadow, (X, Y + 8, 16, 12))
                    box(s, rim, (X, Y, 16, 12))
                    box(s, light, (X, Y, 16, 2))
                    box(s, base, (X + 2, Y + 5, 12, 6))
                    if (x + y) % 4 == 0:
                        box(s, accent, (X + 4, Y + 7, 8, 1))
    # Natural low-relief craters occupy walkable ground, never conceal terminals.
    if lunar:
        candidates = [
            (210, 100, 45, 22),
            (825, 100, 55, 24),
            (845, 480, 55, 25),
            (150, 450, 45, 22),
        ]
        for _ in range(28):
            candidates.append(
                (
                    rng.randrange(70, width * 16 - 70),
                    rng.randrange(55, height * 16 - 55),
                    rng.randrange(16, 42),
                    rng.randrange(9, 19),
                )
            )
        for cx, cy, rx, ry in candidates:
            if any(
                w.map["tiles"][y][x] != "."
                for y in range((cy - ry - 4) // 16, (cy + ry + 4) // 16 + 1)
                for x in range((cx - rx - 4) // 16, (cx + rx + 4) // 16 + 1)
            ):
                continue
            if any(
                abs(t["x"] / 2 - cx) < rx + 30 and abs(t["y"] / 2 - cy) < ry + 35
                for t in w.map["interactables"]
            ):
                continue
            pg.draw.ellipse(s, shadow, (cx - rx, cy - ry, rx * 2, ry * 2))
            pg.draw.ellipse(s, rim, (cx - rx, cy - ry - 2, rx * 2, ry * 2), 3)
            pg.draw.arc(s, light, (cx - rx, cy - ry - 3, rx * 2, ry * 2), 0.2, 2.9, 2)
            pg.draw.ellipse(s, base, (cx - rx + 6, cy - ry + 7, rx * 2 - 12, ry * 2 - 10))
        # Worn service tracks link the landing area to terminals without replacing terrain.
        for t in w.map["interactables"]:
            x, y = t["x"] // 2, t["y"] // 2
            for dy in range(20, 76, 4):
                for dx in (-5, 5):
                    box(s, rim, (x + dx, y + dy, 2, 1))
    else:
        # Inlaid conduit strips, local architecture and maintenance markings.
        for t in w.map["interactables"]:
            x, y = t["x"] // 2, t["y"] // 2
            pg.draw.lines(
                s, shadow, False, [(x - 22, y + 12), (x + 22, y + 12), (x + 22, y + 50)], 2
            )
            pg.draw.lines(s, rim, False, [(x - 22, y + 11), (x + 21, y + 11), (x + 21, y + 49)])
    if zone == "titan_cloud":
        for yy in (154, 162):
            pg.draw.line(s, shadow, (30, yy), (width * 16 - 30, yy), 3)
            for xx in range(35, width * 16 - 30, 16):
                box(s, accent, (xx, yy, 5, 1))
    elif zone == "helix_bio":
        for xx in range(55, width * 16 - 40, 70):
            box(s, shadow, (xx, 24, 42, 14))
            box(s, "#598f80", (xx + 2, 26, 38, 10))
            for k in range(8):
                box(s, "#87b99d", (xx + 4 + k * 4, 27 + (k % 2) * 3, 2, 4))
    elif zone == "aurora_ep":
        # Inlaid observatory meridians are subtle floor markings.
        for radius in (45, 66, 88):
            pg.draw.ellipse(s, rim, (300 - radius, 190 - radius // 2, radius * 2, radius), 1)
        for xx in range(36, width * 16 - 40, 64):
            box(s, shadow, (xx, 19, 44, 16))
            for j in range(9):
                box(s, light, (xx + 3 + (j * 13) % 38, 21 + (j * 7) % 11, 1, 1))
    return pg.transform.scale(s, (width * 32, height * 32))


def props(w):
    """Placed only in free space, clear of consoles, spawn, gates and walk routes."""
    result = []
    kind = {
        "orion_moon": "dish",
        "workshop": "rack",
        "titan_cloud": "rack",
        "helix_bio": "tank",
        "aurora_ep": "scope",
    }[w.zone]
    for i, t in enumerate(w.map["interactables"]):
        for dx, dy, k in [(-64, -32, kind), (64, 0, "crate")]:
            x, y = t["x"] + dx, t["y"] + dy
            cx, cy = int(x // 32), int(y // 32)
            if (
                1 <= cx < w.map["width"] - 1
                and 1 <= cy < w.map["height"] - 1
                and w.map["tiles"][cy][cx] == "."
                and all(
                    math.dist((x, y), (o["x"], o["y"])) > 50
                    for o in [w.map["exit"], *w.map["sites"]]
                )
            ):
                result.append((y, k, x, PALETTES[w.zone][-1], 0))
    return result


def draw(w, bg, lessons, tick, openings=None):
    s = bg.copy()
    accent = PALETTES[w.zone][-1]
    for gate in w.map["gates"]:
        x, y = gate["x"], gate["y"]
        done = gate["requires_challenge"] in w.p["completed"]
        box(s, "#243441", (x, y, 32, 32))
        opened=(openings or {}).get(lessons[gate['requires_challenge']]['world_effect'])
        fraction=1 if not done else max(0,1-(tick-opened)/650) if opened is not None else 0
        for i in range(4):
            box(s, "#77828b", (x + i * 8, y + 3, 6, int(26*fraction)))
        box(s, "#88e3bc" if done else "#eab978", (x + 2, y + 2, 28, 3))
    actors = props(w)
    for t in w.map["interactables"]:
        key = t["challenge_id"]
        done = key in w.p["completed"]
        actors.append(
            (t["y"], "console", t["x"], "#88e3bc" if done else accent, int(tick // 200) % 4)
        )
        if w.zone == "orion_moon":
            # The machine stays in the world; route details live in diagnostics.
            job = w.p.get("expedition_job")
            saved = w.p.get("programs", {}).get(key)
            rx, ry = t["x"] + 58, t["y"] + 74
            if job and job["key"] == key and saved:
                i = min(int(job["step"]), len(saved) - 1)
                j = min(i + 1, len(saved) - 1)
                cell = pg.Vector2(saved[i]).lerp(saved[j], job["step"] % 1)
                start = pg.Vector2(saved[0])
                delta = cell - start
                rx += delta.x * 20
                ry += delta.y * 20
            actors.append((ry, "rover", rx, accent, 0))
    e = w.map["exit"]
    actors.append((e["y"], "shuttle", e["x"], accent, 0))
    for site in w.map["sites"]:
        if site["type"] == "scientist":
            actors.append((site["y"], "npc", site["x"], accent, int(tick // 650) % 4))
        elif not w.p["world_flags"].get("relic_" + w.zone):
            actors.append((site["y"], "beacon", site["x"], "#efc274", int(tick // 200) % 4))
    if w.mica_visual is not None:
        x, y = w.mica_visual
        actors.append((y, "rover", x, "#88e3bc", 0))
    actors.append((w.pos.y, "player", w.pos.x, accent, 0))
    for y, kind, x, color, phase in sorted(actors, key=lambda a: a[0]):
        if kind == "player":
            character(s, x, y, w)
        else:
            stamp(s, kind, x, y, color, phase)
    if w.zone == "workshop":
        for i in range(len(w.map["interactables"])):
            x = i * 512 + 256
            y = 410
            # Compact physical assembly cell: rails, two pistons, central module.
            for off in (-116, 116):
                box(s, "#172a35", (x + off - 10, y - 80, 20, 150))
                for dy in range(-72, 65, 16):
                    box(s, "#778b91", (x + off - 7, y + dy, 14, 6))
            for j in range(5):
                stamp(
                    s,
                    "tank" if i % 4 == 3 else "rack",
                    x - 128 + j * 64,
                    y - 30,
                    accent,
                    int(tick // 200) % 4,
                )
            done = f"workshop_{i + 1:02}" in w.p["completed"]
            data = w.p.get("programs", {}).get(f"workshop_{i + 1:02}")
            stamp(
                s, "rover" if i % 2 == 0 else "dish", x, y + 45, "#8cdbb6" if done else "#77818d", 0
            )
            if data is not None:
                if i == 0:
                    for n, obj in enumerate(data["state"]):
                        stamp(
                            s,
                            "rover",
                            x - 55 + n * 110 + int(math.sin(tick / 650) * obj["power"] / 8),
                            y + 55,
                            accent,
                        )
                elif i == 1:
                    for n, obj in enumerate(data["state"]):
                        cx = x - 55 + n * 110
                        cy = y + 45
                        pg.draw.circle(s, "#718b90", (cx, cy), 23)
                        angle = math.pi * (1 - obj["reading"] / 100)
                        pg.draw.line(
                            s,
                            accent,
                            (cx, cy),
                            (cx + int(math.cos(angle) * 18), cy - int(math.sin(angle) * 18)),
                            3,
                        )
                elif i == 2:
                    for n, obj in enumerate(data["state"]):
                        bx = x - 65 + n * 110
                        box(s, "#b2cec6", (bx, y + 7, 30, 50))
                        box(s, "#223943", (bx + 4, y + 11, 22, 42))
                        fill = int(obj["battery_percent"] * 0.4)
                        box(s, "#85ddba", (bx + 4, y + 51 - fill, 22, fill))
                elif i == 3:
                    obj = data["state"][0]
                    fill = int(48 * obj["water"] / max(1, obj["capacity"]))
                    stamp(s, "tank", x, y + 55, accent)
                    box(s, "#77d4d3", (x - 9, y + 41 - fill // 2, 18, fill // 2))
                elif i == 4:
                    for n, report in enumerate(data):
                        stamp(
                            s,
                            "rover",
                            x - 60 + n * 120 + int(math.sin(tick / (500 + n * 300)) * 12),
                            y + 50,
                            "#8bdcc5" if report["role"] == "survey" else "#dfb67f",
                        )
                elif i == 5:
                    for n, charge in enumerate(data["charges"]):
                        box(s, "#748a92", (x - 60 + n * 95, y + 20, 36, 45))
                        box(
                            s,
                            "#85ddba",
                            (x - 56 + n * 95, y + 61 - int(charge * 0.4), 28, int(charge * 0.4)),
                        )
                elif i == 6:
                    for n, value in enumerate(data):
                        pg.draw.circle(
                            s,
                            "#ef9a77" if value == "fault" else "#88dbb4",
                            (x - 70 + n * 35, y + 42),
                            7,
                        )
                elif i == 7:
                    for n in range(data):
                        stamp(s, "crate", x - 36 + n * 55, y + 60, accent)

    return s.subsurface((int(w.camera.x), int(w.camera.y), 768, 576))
