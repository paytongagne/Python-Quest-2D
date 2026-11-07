"""World travel, expedition state and inspectable program replay."""

import copy
import math
import pygame as pg
from ..core.challenges import LESSONS, MAPS, ROOT
from ..core.expedition_contract import validate
from ..core.progress import award
from . import planet_art
from .art import INK, PANEL, WHITE, MUTED, MINT, GOLD, label, rect, wrapped
from ..ui.hud import sidebar, fit_text
import json

DESTINATIONS = json.loads((ROOT / "content/universe/destinations.json").read_text())
PLANETS = {d["zone"]: d for d in DESTINATIONS[1:]}
PLANETS["workshop"] = dict(
    name="Workshop District", tag="ASTRA / OBJECT ENGINEERING", color="#efba78"
)


class Expeditions:
    def __init__(self, game):
        self.g = game
        self.preview = False
        self.replay_key = None
        self.replay_step = 0
        self.playing = False

    def busy(self):
        mica = getattr(self.g, "mica_job", None)
        return bool(
            self.g.p.get("deployment")
            or self.g.p.get("expedition_job")
            or self.g.future
            or (mica is not None and mica.status == "running")
        )

    def travel(self, index):
        g = self.g
        target = DESTINATIONS[index]
        if self.busy():
            g.notice = "Finish the current delivery before boarding."
            return False
        unlocked = target["requires"] is None or target["requires"] in g.p["completed"]
        if not unlocked and not self.preview:
            requirement = LESSONS.get(target["requires"], {}).get(
                "title", target["requires"].replace("_", " ").title()
            )
            g.notice = "Route locked: complete " + requirement + ". D enables Expedition Preview."
            return False
        g.world_screen()
        g.presentation.departure = g.canvas.subsurface((12, 77, 768, 576)).copy()
        current = copy.deepcopy(g.p["player"])
        g.p.setdefault("checkpoints", {})[g.world.zone] = current
        if g.world.zone not in PLANETS or g.world.zone == "workshop":
            g.p["astra_return"] = g.world.zone
        zone = target["zone"] if index else g.p.get("astra_return", "orientation")
        saved = g.p["checkpoints"].get(zone)
        g.world.enter(zone)
        if saved:
            g.world.pos.update(saved["x"], saved["y"])
            g.world.sync()
        g.p.setdefault("visited_worlds", [])
        if target["id"] not in g.p["visited_worlds"]:
            g.p["visited_worlds"].append(target["id"])
        g.refresh()
        g.scene = "world"
        g.notice = (
            ("Expedition Preview / " if not unlocked else "")
            + target["name"]
            + ". T opens the star map."
        )
        g.presentation.arrive()
        g.persist()
        return True

    def interaction(self, t):
        g = self.g
        if t["type"] == "shuttle":
            g.scene = "starmap"
            return True
        if t["type"] == "scientist":
            g.notice = {
                "workshop": "ION: Each bay runs your real Python objects. Restore the drone blueprint, calibrate the probe, protect the battery, then refill the hydraulic tank. J opens return travel.",
                "orion_moon": "ION: Restore the graph, route Mica, survey the ice, then choose the least-cost ridge crossing. R replays your last program.",
                "titan_cloud": "ION: These are offline packets. Repair framing, validation, topic routing and delivery policy in order.",
                "helix_bio": "ION: All traces are synthetic. Fix generation, the sample clock, baseline estimates and reproducible noise.",
                "aurora_ep": "ION: A toy chamber tests geometry software. Define a sample, interpolate the cursor, transform it and filter quality.",
            }[g.world.zone]
            return True
        if t["type"] == "relic":
            g.p["world_flags"]["relic_" + g.world.zone] = True
            g.notice = "Survey archive recovered. Replay diagnostics unlocked for this expedition."
            g.persist()
            return True
        if t["type"] == "terminal":
            key = t["challenge_id"]
            n = LESSONS[key]["sequence"]
            previous = f"{g.world.zone}_{n - 1:02}"
            if n > 1 and previous not in g.p["completed"]:
                g.notice = "Restore " + LESSONS[previous]["title"] + " first."
                return True
        return False

    def accept(self, ch, result):
        if ch.get("simulation") != "expedition":
            return False
        g = self.g
        try:
            value = validate(ch, ch["cases"][0], result.get("effect"))
        except (ValueError, TypeError, KeyError) as exc:
            g.term.rows = ["World output rejected: " + str(exc)]
            return True
        g.p.setdefault("programs", {})[ch["id"]] = value
        g.p["last_replay"] = ch["id"]
        if ch["output"] == "path":
            g.p["expedition_job"] = {"key": ch["id"], "step": 0.0}
            g.term.rows[0] = "Plan verified. Esc deploys Mica. R opens step replay after docking."
        else:
            xp = award(g.p, ch["id"])
            g.pending_gate = ch["world_effect"] if xp else None
            if xp:
                g.tone("pass")
            g.term.rows[0] = f"Relay restored. +{xp} XP. Esc to see your program in the world."
        g.persist()
        return True

    def update(self, dt):
        g = self.g
        w = g.world
        target = max(
            0, min(w.pos.y - (480 if w.zone == "workshop" else 288), w.map["height"] * 32 - 576)
        )
        w.camera.y += (target - w.camera.y) * (1 - math.exp(-10 * dt))
        job = g.p.get("expedition_job")
        if job and w.zone == LESSONS[job["key"]]["zone"]:
            job["step"] += min(dt, 0.1) * 2.4
            path = g.p["programs"][job["key"]]
            if job["step"] >= max(1, len(path) if job["key"] == "orion_moon_16" else len(path) - 1):
                key = job["key"]
                g.p.pop("expedition_job")
                xp = award(g.p, key)
                if xp:
                    g.opening[LESSONS[key]["world_effect"]] = pg.time.get_ticks()
                    g.tone("pass")
                g.notice = f"Mica docked. Relay payload delivered. +{xp} XP. R replays each step."
                if key == "orion_moon_16":
                    g.p["world_flags"]["moon_convoy_rescued"] = True
                    g.scene = "convoy_complete"
                g.persist()
        if self.playing and g.scene == "replay":
            self.replay_step += dt * 2

    def event(self, e):
        g = self.g
        if g.scene == "starmap" and e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            point = g.point(e.pos)
            for i, (x, y) in enumerate(
                [(140, 204), (320, 390), (495, 220), (690, 402), (885, 200)]
            ):
                if pg.Rect(x - 85, y - 80, 170, 180).collidepoint(point):
                    self.travel(i)
                    return True
        if e.type != pg.KEYDOWN:
            return False
        k = e.key
        if g.scene == "diagnostics":
            if k in (pg.K_ESCAPE, pg.K_o):
                g.scene = "world"
            elif k == pg.K_e:
                g.scene = "world"
                g.interact()
            return True
        if g.scene == "world" and k == pg.K_o:
            nearby = g.world.nearest()
            if nearby and nearby["type"] == "terminal" and g.world.zone in PLANETS:
                self.diagnostic_key = nearby["challenge_id"]
                g.scene = "diagnostics"
            else:
                g.notice = "Approach a console, then O to inspect its diagnostics."
            return True
        if g.scene == "convoy_complete":
            if k in (pg.K_ESCAPE, pg.K_RETURN):
                g.scene = "world"
            return True
        if g.scene == "world" and k == pg.K_t:
            g.scene = "starmap"
            return True
        if g.scene == "world" and k == pg.K_r and g.p.get("last_replay"):
            if self.busy():
                g.notice = "Mica is delivering. Replay becomes available after docking."
                return True
            self.replay_key = g.p["last_replay"]
            self.replay_step = 0
            self.playing = False
            g.scene = "replay"
            return True
        if g.scene == "starmap":
            if k == pg.K_d:
                self.preview = not self.preview
                g.notice = (
                    "Preview enabled: choose any released world."
                    if self.preview
                    else "Campaign routes enabled: completed chapters unlock onward travel."
                )
            elif pg.K_1 <= k <= pg.K_5:
                self.travel(k - pg.K_1)
            elif k in (pg.K_ESCAPE, pg.K_t):
                g.scene = "world"
            return True
        if g.scene == "replay":
            if k == pg.K_RIGHT:
                self.replay_step += 1
            elif k == pg.K_LEFT:
                self.replay_step = max(0, self.replay_step - 1)
            elif k == pg.K_HOME:
                self.replay_step = 0
            elif k == pg.K_SPACE:
                self.playing = not self.playing
            elif k in (pg.K_ESCAPE, pg.K_r):
                g.scene = "world"
                self.playing = False
            return True
        if g.p.get("expedition_job") and g.scene in ("journal", "greenline_travel"):
            if pg.K_1 <= k <= pg.K_8:
                g.notice = "Mica is still delivering the relay."
                return True
        return False

    def draw_overlay(self, s):
        g = self.g
        if g.scene == "diagnostics":
            from .diagnostics import draw

            draw(s, g, self.diagnostic_key)
            return True
        if g.scene == "survey" and g.world.zone in PLANETS:
            w = g.world
            s.fill(INK)
            label(s, PLANETS[w.zone]["name"] + " / Survey", 30, 25, 30)
            m = w.map
            scale = min(12, 940 // m["width"], 440 // m["height"])
            ox = (1088 - scale * m["width"]) // 2
            oy = 112
            for y, row in enumerate(m["tiles"]):
                for x, c in enumerate(row):
                    rect(
                        s,
                        "#6f728c" if c == "#" else "#27384c",
                        ox + x * scale,
                        oy + y * scale,
                        scale - 1,
                        scale - 1,
                    )
            for t in m["interactables"]:
                px = ox + t["x"] / 32 * scale
                py = oy + t["y"] / 32 * scale
                pg.draw.circle(
                    s, MINT if t["challenge_id"] in g.p["completed"] else GOLD, (px, py), 4
                )
                label(s, t["challenge_id"][-2:], px + 5, py - 6, 12, WHITE, True)
            pg.draw.circle(s, WHITE, (ox + w.pos.x / 32 * scale, oy + w.pos.y / 32 * scale), 5)
            label(
                s,
                "White: pilot   Amber: pending repair   Green: restored",
                40,
                590,
                18,
                MUTED,
                True,
            )
            label(s, "M / Esc  Close survey", 40, 640, 18, MINT, True)
            return True
        if g.scene == "convoy_complete":
            rect(s, PANEL, 150, 130, 788, 420)
            label(s, "The convoy is home.", 190, 170, 38, MINT)
            wrapped(
                s,
                "Cargo and escort dock beneath the relay lights. Your service order, work model and weighted route survived the recovery checks.\n\nION: Titan's ingress link is responding. The next route is open.\n\nEnter  Return to the moon     T opens world travel after closing",
                190,
                247,
                695,
                22,
                WHITE,
            )
            return True
        if g.scene == "starmap":
            s.fill("#0c1323")
            for star in range(90):
                x, y = (star * 193 + 79) % 1088, (star * 97 + 11) % 490
                pg.draw.circle(s, "#344965", (x, y), 1)

            label(s, "ASTRA / INTERWORLD NAVIGATION", 35, 25, 17, MINT, True)
            label(s, "Choose a destination", 35, 60, 35)
            points = [(140, 204), (320, 390), (495, 220), (690, 402), (885, 200)]
            pg.draw.lines(s, "#4d5578", False, points, 2)
            for i, (d, p) in enumerate(zip(DESTINATIONS, points)):
                pg.draw.circle(s, d["color"], p, 32 if i else 40)
                if i == 1:
                    for dx, dy, r in [(-11, -9, 8), (14, 5, 6), (-4, 17, 5)]:
                        pg.draw.circle(s, "#8178b4", (p[0] + dx, p[1] + dy), r)
                elif i == 2:
                    for dy in (-15, 0, 15):
                        pg.draw.line(
                            s, "#cc8d71", (p[0] - 23, p[1] + dy), (p[0] + 23, p[1] + dy), 3
                        )
                elif i == 3:
                    pg.draw.arc(s, "#3d9e96", (p[0] - 25, p[1] - 26, 50, 52), 0.3, 2.7, 4)
                elif i == 4:
                    pg.draw.ellipse(s, "#c182bb", (p[0] - 51, p[1] - 14, 102, 28), 3)
                pg.draw.circle(s, "#71829d", p, 47, 1)
                label(s, str(i + 1), p[0] - 8, p[1] - 16, 25, INK, True)
                wrapped(s, d["name"], p[0] - 89, p[1] + 55, 180, 17, WHITE)
                unlocked = d["requires"] is None or d["requires"] in g.p["completed"]
                label(
                    s,
                    "READY" if unlocked else "PREVIEW" if self.preview else "LOCKED",
                    p[0] - 40,
                    p[1] - 72,
                    14,
                    GOLD,
                    True,
                )
            label(
                s,
                "D  Expedition Preview " + ("ON" if self.preview else "OFF"),
                35,
                548,
                19,
                GOLD,
                True,
            )
            wrapped(
                s,
                "Campaign travel follows each world's completion requirements. Preview access lets you play the released expedition sections now.",
                35,
                581,
                990,
                17,
                MUTED,
            )
            label(s, "Click a world / 1-5 Travel     Esc Return", 35, 646, 17, MINT, True)
            fit_text(s, g.notice, (35, 511, 1000, 31), 14, GOLD)
            return True
        if g.scene == "replay":
            s.fill(INK)
            key = self.replay_key
            ch = LESSONS[key]
            value = g.p["programs"][key]
            label(s, "PROGRAM REPLAY / " + ch["title"], 30, 24, 27)
            panel = pg.Surface((500, 350))
            panel.fill("#292c47")
            count = max(1, len(value) - 1) if ch["output"] == "path" else 1
            self.replay_step = min(self.replay_step, count)
            if key.startswith("orion_moon"):
                planet_art.board(panel, key, ch, value, 0, self.replay_step)
            else:
                wrapped(panel, str(value), 20, 35, 460, 18, MINT, True)
            s.blit(panel, (30, 105))
            if ch["output"] == "path":
                i = min(int(self.replay_step), len(value) - 1)
                grid = ch["cases"][0]["args"][0]
                cost = sum(
                    grid[y][x] if type(grid[y][x]) is int else 1 for x, y in value[1 : i + 1]
                )
                lines = [
                    f"Step {i} / {len(value) - 1}",
                    f"Cell {value[i]}",
                    f"Cost so far {cost}",
                    f"Optimal cost {ch['cases'][0]['cost']}",
                ]
            else:
                lines = ["Validated output", str(value)]
            wrapped(s, "\n\n".join(lines), 565, 120, 480, 22, WHITE)
            label(
                s,
                "Left / Right  Step    Home  Reset    Space  Play/Pause    Esc  Close",
                30,
                618,
                16,
                MINT,
                True,
            )
            label(
                s,
                "Replay reads the saved output. It grants no additional XP.",
                30,
                655,
                15,
                MUTED,
                True,
            )
            return True
        return False

    def world_screen(self):
        g = self.g
        w = g.world
        if w.zone not in PLANETS:
            return False
        s = g.canvas
        s.fill(INK)
        d = PLANETS[w.zone]
        label(
            s,
            ("FACILITY / " if w.zone == "workshop" else "EXPEDITION / ") + d["tag"],
            20,
            13,
            15,
            d["color"],
            True,
        )
        label(s, d["name"], 18, 37, 29)
        tick = 0 if g.p["settings"].get("reduced_motion") else pg.time.get_ticks()
        s.blit(
            planet_art.draw(
                w, g.bg, LESSONS, tick, {} if g.p["settings"].get("reduced_motion") else g.opening
            ),
            (12, 77),
        )
        sector = 0
        if w.zone == "workshop":
            sector = min((len(w.map["interactables"]) - 1) // 4, int(w.pos.x // 2048))
        if w.zone == "orion_moon":
            east, south = w.pos.x >= 1280, w.pos.y >= 768
            sector = (2 if east else 3) if south else (1 if east else 0)
        sidebar(g, [t["challenge_id"] for t in w.map["interactables"][sector * 4 : sector * 4 + 4]])
        near = w.nearest()
        label(
            s,
            "E  "
            + (
                {
                    "terminal": "Program / O Diagnostics",
                    "shuttle": "Board shuttle",
                    "scientist": "Talk to ION",
                    "relic": "Recover archive",
                }.get(near["type"], "Inspect")
            )
            if near
            else "WASD / arrows  Move",
            16,
            660,
            15,
            GOLD,
            True,
        )
        label(s, "T Worlds   J Log   M Map   R Replay   Esc Pause", 553, 660, 15, MUTED, True)
        return True
