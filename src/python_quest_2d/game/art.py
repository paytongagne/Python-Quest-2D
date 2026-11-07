"""Original pixel geometry and instrumentation for the Astra facility."""

import math
import random
from functools import lru_cache

import pygame as pg

INK = "#0c1824"
PANEL = "#152736"
WHITE = "#ecf4ef"
MUTED = "#a5bdc6"
GOLD = "#ffd186"
MINT = "#6ae4bd"
PALETTES = ["#73dbcc", "#ffae72", "#92b4ff", "#81d49c", "#ed9587", "#ca9dff"]


@lru_cache(None)
def font(size, mono=False):
    return pg.font.SysFont("consolas" if mono else "segoeui", size, bold=not mono)


def label(s, text, x, y, size=16, color=WHITE, mono=False):
    s.blit(font(size, mono).render(str(text), True, color), (x, y))


def wrapped(s, message, x, y, width, size=16, color=MUTED, mono=False):
    f = font(size, mono)
    for paragraph in str(message).split("\n"):
        line = ""
        for word in paragraph.split():
            if line and f.size(line + " " + word)[0] > width:
                label(s, line, x, y, size, color, mono)
                y += size + 5
                line = ""
            while f.size(word)[0] > width:
                cut = max(1, len(word) * width // f.size(word)[0] - 1)
                label(s, word[:cut], x, y, size, color, mono)
                y += size + 5
                word = word[cut:]
            line = (line + " " + word).strip()
        label(s, line, x, y, size, color, mono)
        y += size + 5
    return y


def rect(s, c, x, y, w, h):
    if w > 0 and h > 0:
        pg.draw.rect(s, c, (int(x), int(y), int(w), int(h)))


def floor_map(world, accent, index):
    s = pg.Surface((world.map["width"] * 32, world.map["height"] * 32))
    s.fill(INK)
    for y, row in enumerate(world.map["tiles"]):
        for x, t in enumerate(row):
            X, Y = x * 32, y * 32
            if t == " ":
                rect(s, "#0d1724", X, Y, 32, 32)
                rect(s, "#698293", X + (x * 7 + y * 13) % 31, Y + (x * 13 + y * 3) % 31, 1, 1)
                continue
            if t == "#":
                rect(s, "#192735", X, Y, 32, 32)
                rect(s, "#526575", X + 1, Y + 1, 30, 18)
                rect(s, "#354858", X + 2, Y + 4, 28, 13)
                rect(s, "#263746", X + 2, Y + 20, 28, 8)
                if (x + y) % 4 == 0:
                    rect(s, accent, X + 7, Y + 22, 18, 2)
            else:
                color = ("#293d49", "#2c404c", "#2e424e")[(x * 9 + y * 7) % 3]
                rect(s, color, X + 1, Y + 1, 31, 31)
                rect(s, "#3c515c", X + 3, Y + 3, 2, 2)
                if (x + y) % 7 == 0:
                    rect(s, "#223540", X + 15, Y + 23, 11, 2)
    # Bays have recessed starboard observation ports.
    for X in (46, 433):
        rect(s, "#111c2c", X, 35, 225, 36)
        rng = random.Random(index + X)
        for _ in range(31):
            sx, sy = rng.randrange(217), rng.randrange(27)
            rect(s, "#8cabb9", X + 4 + sx, 39 + sy, 2, 1)
        for dx in (0, 74, 148, 222):
            rect(s, "#475d69", X + dx, 35, 4, 37)
        rect(s, accent, X, 70, 225, 2)
    if world.zone != "hydro":
        rect(s, "#142935", 782, 100, 198, 40)
        label(s, world.map["alcove"], 789, 110, 15, accent, True)
        rect(s, "#4d6b79", 909, 149, 57, 29)
        rect(s, "#102c39", 914, 152, 47, 19)
        pg.draw.lines(
            s,
            accent,
            False,
            [(918, 166), (925, 164), (931, 156), (940, 165), (950, 161), (957, 164)],
            2,
        )
    else:
        from .nursery import greenhouse

        greenhouse(s)
    # Painted service routes and bay markings
    for n, t in enumerate(world.map["interactables"]):
        X, Y = t["x"], t["y"]
        rect(s, "#405560", X - 34, Y + 28, 68, 2)
        for dx in range(-34, 35, 12):
            rect(s, accent, X + dx, Y + 29, 6, 2)
        label(s, f"BAY  {n + 1:02}", X - 35, Y + 35, 14, "#a7c1c4", True)
    return s


def terminal(s, x, y, color, done, tick):
    rect(s, "#182932", x - 21, y + 8, 44, 10)
    rect(s, "#697e85", x - 18, y - 24, 36, 35)
    rect(s, "#253640", x - 16, y - 23, 32, 22)
    rect(s, "#0d232b", x - 13, y - 20, 26, 15)
    for i, w in enumerate((9, 17, 12)):
        rect(s, color, x - 10, y - 17 + 4 * i, w, 2)
    rect(s, color, x - 13, y - 20 + int(tick / 160) % 14, 26, 1)
    rect(s, "#acbcc0", x - 18, y, 36, 4)
    for i in range(5):
        rect(s, "#344a55", x - 13 + i * 5, y + 5, 3, 2)
    rect(s, MINT if done else GOLD, x + 12, y + 5, 3, 3)
    if done:
        pg.draw.lines(s, MINT, False, [(x - 6, y - 31), (x - 2, y - 28), (x + 5, y - 36)], 3)


def pilot(s, x, y, world):
    from .pixel_world import character

    character(s, x, y, world)


def draw_world(world, bg, accent, tick, opening):
    s = bg.copy()
    from .instruments import draw_instrument

    index = PALETTES.index(accent) if world.zone != "hydro" else 0
    from .nursery import field

    field(s, world, tick)
    for t, (x, y) in zip(
        world.map["interactables"] if world.zone != "hydro" else [],
        [(276, 202), (659, 209), (667, 462), (295, 396)],
    ):
        draw_instrument(s, index, x, y, accent, t["challenge_id"] in world.p["completed"], tick)
    for gate in world.map["gates"]:
        x, y = gate["x"], gate["y"]
        done = gate["requires_challenge"] in world.p["completed"]
        fraction = max(0, 1 - (tick - opening.get(gate["id"], -10000)) / 650) if done else 1
        rect(s, "#172732", x, y, 32, 32)
        for i in range(4):
            rect(s, "#576975", x + i * 8, y + 2, 4, 3)
            rect(s, "#576975", x + i * 8, y + 26, 4, 3)
        for a in (0, 1):
            w = int(fraction * 15)
            rect(s, "#994e4e", x + (32 - w if a else 0), y + 4, w, 24)
        rect(s, MINT if done else GOLD, x, y + 1, 32, 2)
    for t in world.map["interactables"]:
        terminal(s, t["x"], t["y"], accent, t["challenge_id"] in world.p["completed"], tick)
    x, y = 104, 187 + int(2 * math.sin(tick / 340))
    rect(s, "#152533", x - 12, y - 9, 24, 18)
    rect(s, "#a4c8c6", x - 10, y - 9, 20, 14)
    rect(s, "#22525a", x - 8, y - 6, 16, 8)
    for i in (-5, 3):
        rect(s, MINT, x + i, y - 4, 3, 3)
    label(s, "PIP", x - 12, y + 8, 12, MINT, True)
    e = world.map["exit"]
    x, y = e["x"], e["y"]
    if world.zone != "hydro":
        pg.draw.ellipse(s, accent, (x - 31, y - 13, 62, 26), 3)
        label(s, "LIFT", x - 17, y - 10, 14, WHITE, True)
    if world.zone == "orientation":
        from .pixel_world import stamp

        stamp(s, "rack", 320, 80, "#efba78", int(tick // 200) % 4)
        label(s, "WORKSHOP", 277, 94, 14, GOLD, True)
    from .pixel_world import draw_mica_docks, stamp

    draw_mica_docks(s, world)
    if world.mica_visual is not None:
        stamp(s, "rover", *world.mica_visual, "#88e3bc")
    pilot(s, *world.pos, world)
    return s.subsurface((int(world.camera.x), 0, 768, 576))
