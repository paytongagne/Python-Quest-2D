"""Pygame presentation and scene lifecycle."""

import math
from array import array
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import pygame as pg

from ..core.challenges import LESSONS, NAMES, ROOT, ZONES
from ..core.grade import grade
from ..core.legacy_migration import migrate
from ..core.progress import award, load, location, save, UnsupportedProfile
from ..ui.terminal import Terminal
from .art import (
    GOLD,
    INK,
    MINT,
    MUTED,
    PALETTES,
    PANEL,
    WHITE,
    draw_world,
    floor_map,
    label,
    rect,
    wrapped,
)
from .world import World
from . import nursery
from .expedition import Expeditions, PLANETS
from . import planet_art
from ..core.route import trace
from ..ui.hud import sidebar
from .presentation import Presentation

SIZE = (1088, 690)


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(SIZE, pg.RESIZABLE)
        pg.display.set_caption("Python Quest 2D | Astra Research Facility")
        self.canvas = pg.Surface(SIZE)
        self.p = load()
        self.world = World(self.p)
        self.expeditions = Expeditions(self)
        self.refresh()
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.future = None
        self.term = None
        self.scene = "world"
        self.old = Path.home() / ".python_quest_progress.json"
        if not location().exists() and self.old.exists():
            self.scene = "import"
        self.notice = (
            "PIP: Astra lost power. Approach the Bay 01 console to start repairs."
            if not self.p["completed"]
            else "PIP: Welcome back, engineer. Check the deck systems for your next repair."
        )
        self.presentation = Presentation(self)
        self.opening = {}
        self.running = True
        self.last_save = pg.time.get_ticks()
        self.snapshot = None
        self.pending_gate = None
        self.view = pg.Rect(0, 0, *SIZE)
        self.sounds = {}
        if pg.mixer.get_init():
            rate, _, channels = pg.mixer.get_init()
            for name, freq in [("open", 420), ("pass", 660), ("fail", 194)]:
                samples = array("h")
                for i in range(rate // 5):
                    val = int(
                        3200
                        * (1 - i / (rate // 5))
                        * math.sin(2 * math.pi * freq * (1 + i / rate) * i / rate)
                    )
                    samples.extend([val] * channels)
                self.sounds[name] = pg.mixer.Sound(buffer=samples)
        pg.key.set_repeat(350, 42)

    def refresh(self):
        if self.world.zone in PLANETS:
            self.index = 7
            self.accent = PLANETS[self.world.zone]["color"]
            self.bg = planet_art.landscape(self.world)
            self.world.camera.update(
                max(0, min(self.world.pos.x - 384, self.world.map["width"] * 32 - 768)),
                max(
                    0,
                    min(
                        self.world.pos.y - (480 if self.world.zone == "workshop" else 288),
                        self.world.map["height"] * 32 - 576,
                    ),
                ),
            )
            return
        self.index = 6 if self.world.zone == "hydro" else ZONES.index(self.world.zone)
        self.accent = "#9cdfae" if self.index == 6 else PALETTES[self.index]
        self.bg = floor_map(self.world, self.accent, self.index)

    def tone(self, name):
        if self.p["settings"]["sound"] and name in self.sounds:
            self.sounds[name].play()

    def persist(self):
        if self.p.get("deployment"):
            self.p["deployment"]["elapsed_steps"] = self.world.flight
        if self.term:
            self.p["drafts"][self.term.ch["id"]] = self.term.editor.text
        save(self.p)
        self.snapshot = self.state_signature()
        self.last_save = pg.time.get_ticks()

    def state_signature(self):
        return (
            self.world.zone,
            tuple(self.world.pos),
            int(self.world.flight),
            self.term.editor.text if self.term else None,
        )

    def interact(self):
        if self.p.get("deployment") or self.p.get("expedition_job"):
            self.notice = "Mica is on the rail. Watch for the docking signal."
            return
        t = self.world.nearest()
        if not t:
            return
        self.tone("open")
        if self.world.zone in PLANETS and self.expeditions.interaction(t):
            return
        if t["type"] == "terminal":
            self.term = Terminal(LESSONS[t["challenge_id"]], self.p)
            self.scene = "terminal"
            pg.key.start_text_input()
        elif t["type"] == "district":
            self.world.enter("workshop")
            self.refresh()
            self.presentation.arrive()
            self.notice = "Workshop District / Assembly bays. Follow the gold objective marker."
            self.persist()
        elif t["type"] == "tram":
            if self.world.zone == "hydro":
                self.world.enter(self.p.get("tram_origin", "orientation"))
                self.notice = "Back on the main deck. Use J for your flight log."
            else:
                self.p["tram_origin"] = self.world.zone
                self.world.enter("hydro")
                self.notice = "MARA: Meet me by the west platform. Mica needs a pilot."
            self.refresh()
            self.persist()
        elif t["type"] == "archive":
            self.p["world_flags"]["log_" + self.world.zone] = True
            self.notice = self.world.map["note"]
            self.persist()
        elif t["type"] == "log":
            self.p["world_flags"]["grower_log"] = True
            self.notice = "Field log: The Scheduler kept flushing the line after every dry reading. MARA marked this valve for salvage."
            self.persist()
        elif t["type"] == "mara":
            key = next(
                (
                    k
                    for k in ("hydro_01", "hydro_02", "hydro_03", "hydro_04")
                    if k not in self.p["completed"]
                ),
                None,
            )
            self.notice = {
                "hydro_01": "MARA: Mica is on the eastbound rail. Program the console above me to deliver a fuse.",
                "hydro_02": "MARA: Mica opened the seed bank. Check moisture before you feed the trays.",
                "hydro_03": "MARA: The logger is across a broken rail. Route Mica through the gap.",
                "hydro_04": "MARA: We've got the readings. Stop the pump from cycling; mind the steam.",
                None: "MARA: Roots are taking. Continue east through filtration, then the reservoir to canopy control.",
            }[key]
        elif t["type"] == "pip":
            self.notice = (
                "PIP: Mica's fuse is installed. MARA has more work across the greenline."
                if "hydro_01" in self.p["completed"]
                else "PIP: The west tram leads to MARA and her programmable rover. Main-deck repairs open the numbered bays."
            )
        elif t["requires_challenge"] in self.p["completed"]:
            if t["to_zone"]:
                self.world.enter(t["to_zone"])
                self.refresh()
                self.notice = "Lift docked. Find the console in Bay 01."
            else:
                self.scene = "ending"
                self.p["world_flags"]["astra_restored"] = True
            self.persist()
        else:
            self.notice = "Lift offline. Complete all four repairs on this deck."

    def submit(self):
        if self.future:
            return
        t = self.term
        k = t.ch["id"]
        self.p["attempts"][k] = self.p["attempts"].get(k, 0) + 1
        if t.ch.get("simulation") == "expedition":
            self.p.pop("expedition_job", None)
        if t.ch.get("simulation") == "route":
            self.p.pop("deployment", None)
        self.persist()
        self.future = self.pool.submit(grade, t.ch, t.editor.text)
        t.rows = ["Checking your program in a local Python interpreter..."]
        t.error = None

    def collect(self):
        if self.future and self.future.done():
            result = self.future.result()
            self.future = None
            t = self.term
            t.rows = [result["status"].replace("_", " ").upper()] + result["rows"]
            t.scroll = 0
            t.error = result.get("line")
            if result["passed"]:
                if self.expeditions.accept(t.ch, result):
                    return
                if t.ch.get("simulation") == "route":
                    try:
                        trace(t.ch["cases"][0]["args"], result.get("effect"))
                    except ValueError as exc:
                        t.rows = ["Route rejected: " + str(exc)]
                        return
                    self.p["deployment"] = dict(key=t.ch["id"], commands=result["effect"])
                    self.world.flight = 0.0
                    self.persist()
                    self.notice = "Flight plan verified. Esc to watch Mica deliver the payload."
                    t.rows[0] = self.notice
                    self.tone("open")
                    return
                if t.ch["id"] == "hydro_02":
                    trays = result.get("effect")
                    if trays != t.ch["cases"][0]["expected"]:
                        t.rows = ["Controller output did not match the tray fixtures."]
                        return
                    self.p["irrigated"] = trays
                if t.ch.get("simulation") == "instrument":
                    if result.get("effect") != t.ch["cases"][0]["expected"]:
                        t.rows = ["Instrument result did not match its fixture."]
                        return
                    self.p.setdefault("instruments", {})[t.ch["id"]] = result["effect"]
                if t.ch["id"] == "hydro_04":
                    self.p["world_flags"]["diagnostic_lens"] = True
                xp = award(self.p, t.ch["id"])
                self.pending_gate = t.ch["world_effect"] if xp else None
                self.notice = f"Repair verified. Bulkhead online. +{xp} XP"
                if t.ch["id"] == "hydro_04":
                    self.notice = f"Pump stabilized. Diagnostic lens online. +{xp} XP"
                t.rows[0] = self.notice + "   Esc to explore."
                self.tone("pass")
            else:
                self.tone("fail")

    def update_field(self, dt):
        w = self.world
        target = max(0, min(w.pos.x - 384, w.map["width"] * 32 - 768))
        w.camera.x += (target - w.camera.x) * (1 - math.exp(-10 * dt))
        self.expeditions.update(dt)
        if w.zone != "hydro":
            return
        job = self.p.get("deployment")
        if job:
            w.flight += dt * 2.2
            if w.flight >= max(1, len(job["commands"])):
                key = job["key"]
                self.p.pop("deployment")
                xp = award(self.p, key)
                self.opening[LESSONS[key]["world_effect"]] = pg.time.get_ticks()
                self.notice = f"Mica docked. Payload installed; bulkhead open. +{xp} XP"
                self.tone("pass")
        if "hydro_04" not in self.p["completed"] and nursery.HAZARD.collidepoint(w.pos):
            w.pos.update(1190, 288)
            w.sync()
            self.notice = "Steam surge! Suit recall returned you to the gallery entrance."

    def hint(self):
        t = self.term
        t.help = min(2, t.help + 1)
        if t.ch["id"] not in self.p["hinted"]:
            self.p["hinted"].append(t.ch["id"])
        self.persist()

    def reveal(self):
        t = self.term
        if self.future:
            return
        if not t.confirm:
            t.confirm = True
            t.rows = [
                "Reveal the reference solution? F2 again confirms. Your first pass will earn 25 XP. Esc cancels."
            ]
            return
        t.confirm = False
        k = t.ch["id"]
        if k not in self.p.setdefault("revealed", []):
            self.p["revealed"].append(k)
        t.editor.anchor = 0
        t.editor.pos = len(t.editor.text)
        t.editor.replace((ROOT / "content/authoring" / (k + ".py")).read_text(encoding="utf-8"))
        t.rows = ["Solution loaded. Trace its steps, then run the tests."]
        self.persist()

    def leave_terminal(self):
        if self.future:
            self.term.rows = ["Run in progress. The worker stops after three seconds."]
            return
        self.persist()
        self.scene = "world"
        self.term = None
        if "hydro_16" in self.p["completed"] and not self.p["world_flags"].get("canopy_celebrated"):
            self.p["world_flags"]["canopy_celebrated"] = True
            self.scene = "canopy"
            self.persist()
        pg.key.stop_text_input()
        if self.pending_gate:
            self.opening[self.pending_gate] = pg.time.get_ticks()
            self.pending_gate = None

    def point(self, pos):
        return (
            (pos[0] - self.view.x) * SIZE[0] / self.view.w,
            (pos[1] - self.view.y) * SIZE[1] / self.view.h,
        )

    def event(self, e):
        if e.type == pg.QUIT:
            self.running = False
            return
        if e.type == pg.KEYDOWN:
            self.presentation.arrival = None
        if self.expeditions.event(e):
            return
        if self.scene == "terminal":
            t = self.term
            if e.type == pg.TEXTINPUT and not self.future:
                t.editor.replace(e.text)
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    if t.confirm:
                        t.confirm = False
                        t.rows = ["Reveal canceled."]
                    else:
                        self.leave_terminal()
                elif e.key == pg.K_RETURN and e.mod & pg.KMOD_CTRL:
                    self.submit()
                elif e.key == pg.K_F2:
                    self.reveal()
                elif e.key in (pg.K_F3, pg.K_F4):
                    t.brief_scroll += 140 * (1 if e.key == pg.K_F4 else -1)
                elif e.key == pg.K_F1:
                    self.hint()
                elif e.key in (pg.K_PAGEUP, pg.K_PAGEDOWN):
                    t.scroll += 100 * (1 if e.key == pg.K_PAGEDOWN else -1)
                elif e.key == pg.K_s and e.mod & pg.KMOD_CTRL:
                    self.persist()
                elif not self.future:
                    t.editor.key(e)
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                x, y = self.point(e.pos)
                for (button, _), action in zip(
                    t.buttons, (self.submit, self.hint, self.leave_terminal)
                ):
                    if button.collidepoint(x, y):
                        action()
                        return
                if t.X <= x < 1060 and t.Y <= y < t.Y + 240:
                    t.hit_text(x, y, pg.key.get_mods() & pg.KMOD_SHIFT)
                    t.drag = True
            elif e.type == pg.MOUSEMOTION and t.drag:
                t.hit_text(*self.point(e.pos), True)
            elif e.type == pg.MOUSEBUTTONUP:
                t.drag = False
            elif e.type == pg.MOUSEWHEEL:
                if self.point(pg.mouse.get_pos())[0] < 366:
                    t.brief_scroll -= e.y * 45
                else:
                    t.scroll -= e.y * 45
            return
        if e.type != pg.KEYDOWN:
            return
        k = e.key
        if self.scene == "import" and k in (pg.K_y, pg.K_n):
            if k == pg.K_y:
                try:
                    migrate(self.old, self.p)
                except (ValueError, TypeError, OSError) as exc:
                    self.notice = "Import failed: " + str(exc)
            self.scene = "world"
            self.persist()
        elif self.scene == "world":
            if k == pg.K_m:
                self.scene = "survey"
            elif k == pg.K_e:
                self.interact()
            elif k == pg.K_j:
                self.scene = "journal"
            elif k == pg.K_ESCAPE:
                self.scene = "pause"
        elif self.scene == "pause" and k == pg.K_m:
            self.p["settings"]["sound"] = not self.p["settings"]["sound"]
            self.persist()
        elif self.scene == "pause" and k == pg.K_r:
            self.p["settings"]["reduced_motion"] = not self.p["settings"].get(
                "reduced_motion", False
            )
            self.persist()
        elif self.scene == "pause" and k == pg.K_q:
            self.running = False
        elif self.scene == "journal" and pg.K_1 <= k <= pg.K_6:
            z = ZONES[k - pg.K_1]
            if self.p.get("deployment"):
                self.notice = "Mica is in transit."
                return
            if z == ZONES[0] or ZONES[k - pg.K_1 - 1] + "_04" in self.p["completed"]:
                self.world.enter(z)
                self.refresh()
                self.scene = "world"
                self.persist()
        elif self.scene == "journal" and k == pg.K_8:
            if not self.expeditions.busy():
                self.world.enter("workshop")
                self.refresh()
                self.scene = "world"
                self.presentation.arrive()
                self.notice = "ION: Welcome to the Workshop. Restore the four object engineering bays in order."
                self.persist()
        elif self.scene == "journal" and k == pg.K_7:
            self.scene = "greenline_travel"
        elif self.scene == "greenline_travel" and pg.K_1 <= k <= pg.K_4:
            sector = k - pg.K_1
            if not self.p.get("deployment") and (
                sector == 0 or f"hydro_{sector * 4:02}" in self.p["completed"]
            ):
                if self.world.zone != "hydro":
                    self.p["tram_origin"] = self.world.zone
                self.world.enter("hydro")
                self.world.pos.update(sector * 1536 + 100, 280)
                self.world.sync()
                self.refresh()
                self.scene = "world"
                self.persist()
        elif self.scene == "survey" and k == pg.K_m:
            self.scene = "world"
        elif k in (pg.K_ESCAPE, pg.K_j, pg.K_RETURN):
            self.scene = "world"

    def world_screen(self):
        if self.expeditions.world_screen():
            return
        s = self.canvas
        s.fill(INK)
        i = self.index
        label(s, "A S T R A     /     RESEARCH FACILITY", 18, 11, 14, self.accent, True)
        label(s, nursery.TITLE if i == 6 else NAMES[i], 16, 33, 28)
        label(
            s,
            f"GREENLINE   /   {min(4, int(self.world.pos.x // 1536) + 1):02}"
            if i == 6
            else f"DECK   0{i + 1} / 06",
            588,
            44,
            15,
            MUTED,
            True,
        )
        s.blit(
            draw_world(
                self.world,
                self.bg,
                self.accent,
                0 if self.p["settings"].get("reduced_motion") else pg.time.get_ticks(),
                {} if self.p["settings"].get("reduced_motion") else self.opening,
            ),
            (12, 77),
        )
        sector = min(3, int(self.world.pos.x // 1536)) if i == 6 else 0
        sidebar(self, [f"{self.world.zone}_{j + 1:02}" for j in range(sector * 4, sector * 4 + 4)])
        t = self.world.nearest()
        prompt = {
            "district": "Enter Workshop District",
            "terminal": "Access console",
            "pip": "Talk to PIP",
            "lift": "Use deck lift",
            "tram": "Ride Greenline tram",
            "log": "Read field log",
            "mara": "Talk to MARA",
            "archive": "Read archive",
        }
        label(
            s, "[E] " + prompt[t["type"]] if t else "WASD / arrows   Move", 17, 660, 16, GOLD, True
        )
        label(s, "T  Worlds   J  Journal   M  Survey", 715, 660, 16, MUTED, True)

    def draw(self):
        if self.expeditions.draw_overlay(self.canvas):
            pass
        elif self.scene == "terminal":
            self.term.draw(self.canvas, self.p, self.future is not None)
        else:
            self.world_screen()
            if self.scene == "survey":
                nursery.survey(self.canvas, self.world)
            elif self.scene != "world":
                s = self.canvas
                dim = pg.Surface(SIZE, pg.SRCALPHA)
                dim.fill((5, 10, 20, 195))
                s.blit(dim, (0, 0))
                rect(s, PANEL, 180, 94, 730, 497)
                rect(s, self.accent, 180, 94, 730, 4)
                title = {
                    "journal": "Flight log",
                    "pause": "Station paused",
                    "ending": "Astra is online.",
                    "canopy": "The canopy is breathing.",
                    "greenline_travel": "Greenline stations",
                    "import": "Previous flight record found",
                }[self.scene]
                label(s, title, 214, 125, 38)
                if self.scene == "journal":
                    label(
                        s, "Press a deck number to travel or revisit a repair.", 215, 196, 18, MUTED
                    )
                    for i, z in enumerate(ZONES):
                        count = sum(f"{z}_{j:02}" in self.p["completed"] for j in range(1, 5))
                        label(s, f"{i + 1}    {NAMES[i]}", 218, 250 + i * 42, 19)
                        label(
                            s,
                            f"{count}/4"
                            if i == 0 or ZONES[i - 1] + "_04" in self.p["completed"]
                            else "LOCKED",
                            740,
                            250 + i * 42,
                            17,
                            GOLD,
                            True,
                        )
                    due = [
                        LESSONS[k]["title"]
                        for k, d in self.p["review"].items()
                        if k in LESSONS and d <= date.today().isoformat()
                    ]
                    if due:
                        wrapped(s, "Practice due: " + due[0], 216, 503, 650, 16, GOLD)
                    wrapped(
                        s,
                        "7  Greenline    8  Workshop District / Classes & machines",
                        216,
                        537,
                        660,
                        16,
                        GOLD,
                    )
                elif self.scene == "greenline_travel":
                    for i, name in enumerate(
                        ("Nursery", "Filtration works", "Reservoir", "Canopy control")
                    ):
                        unlocked = i == 0 or f"hydro_{i * 4:02}" in self.p["completed"]
                        label(
                            s,
                            f"{i + 1}   {name}" + ("" if unlocked else "   LOCKED"),
                            216,
                            235 + i * 55,
                            21,
                            WHITE if unlocked else MUTED,
                        )
                    label(s, "Esc  Return to station", 216, 528, 17, MINT, True)
                else:
                    body = {
                        "canopy": """Mica docks the recovery relay. The fault latch clears, and water returns to the canopy.

MARA: Sixteen systems back online. The maintenance network is next.

Enter   Explore the restored greenhouse""",
                        "pause": f"Esc   Resume\nM     Sound {'on' if self.p['settings']['sound'] else 'off'}\nR     Reduced motion {'on' if self.p['settings'].get('reduced_motion') else 'off'}\nQ     Save and quit",
                        "ending": "The algorithm core recognizes the pair. Across all six decks, emergency lights give way to steady power.\n\nPIP: Navigation restored, engineer. Astra is yours.\n\nEnter   Return to the facility",
                        "import": "Import completed lessons, XP and drafts from Python Quest v1? A backup is kept beside the old save.\n\nY   Import     N   Start fresh",
                    }.get(self.scene, "")
                    wrapped(s, body, 216, 231, 626, 21, WHITE)
        self.presentation.draw()
        self.view = pg.Rect(0, 0, *SIZE).fit(self.window.get_rect())
        self.window.fill(INK)
        self.window.blit(pg.transform.scale(self.canvas, self.view.size), self.view)
        pg.display.flip()

    def run(self):
        clock = pg.time.Clock()
        try:
            while self.running:
                dt = clock.tick(60) / 1000
                self.collect()
                for e in pg.event.get():
                    self.event(e)
                if self.scene == "world" and not self.presentation.arrival:
                    k = pg.key.get_pressed()
                    self.world.move(
                        int(k[pg.K_d] or k[pg.K_RIGHT]) - int(k[pg.K_a] or k[pg.K_LEFT]),
                        int(k[pg.K_s] or k[pg.K_DOWN]) - int(k[pg.K_w] or k[pg.K_UP]),
                        dt,
                    )
                    self.update_field(dt)
                if (
                    pg.time.get_ticks() - self.last_save > 750
                    and self.snapshot != self.state_signature()
                    and self.scene != "import"
                ):
                    self.persist()
                if self.scene == "replay":
                    self.expeditions.update(dt)
                self.draw()
        finally:
            try:
                if self.scene != "import":
                    self.persist()
            finally:
                self.pool.shutdown()
                pg.quit()


def main():
    try:
        Game().run()
    except UnsupportedProfile as exc:
        from .art import font

        font.cache_clear()
        # Do not start a fresh session or autosave over a future-version profile.
        pg.init()
        screen = pg.display.set_mode(SIZE)
        pg.display.set_caption("Python Quest 2D | Save protected")
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key in (pg.K_ESCAPE, pg.K_RETURN)
                ):
                    running = False
            screen.fill(INK)
            label(screen, "Save protected", 60, 70, 34, GOLD)
            wrapped(screen, str(exc), 60, 145, 950, 24, WHITE)
            label(screen, "Close this window and open the newer game version.", 60, 260, 21, MUTED)
            label(screen, "Esc / Enter  Close", 60, 600, 18, MINT, True)
            pg.display.flip()
            pg.time.wait(30)
        pg.quit()
