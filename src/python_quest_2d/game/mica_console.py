"""Player controls for saved Mica revisions, verified deployment and trace review."""

import pygame as pg

from ..core import program_library as library
from ..core import progress
from ..core.contracts import ContractError
from ..core.grade import grade_program
from ..ui.terminal import Terminal
from .art import GOLD, INK, MINT, MUTED, PANEL, WHITE, label, rect, wrapped
from .mica_observation import (
    MicaState,
    device_locked,
    device_state,
    prepare,
    verify,
    workshop_enabled,
)
from .mica_runner import saved_mica

STARTER = """# Name: Relay routine
def plan(observation):
    target_id = observation["objective"]["target_id"]
    target = next(d for d in observation["visible"]["devices"] if d["id"] == target_id)
    x, y = observation["robot"]["cell"]
    dx = target["cell"][0] - x
    direction = "east" if dx > 0 else "west"
    steps = max(0, abs(dx) - 1)
    return [{"type": "move", "direction": direction}] * steps + [
        {"type": "interact", "target": target_id}
    ]
"""


def nearby_device(world):
    for device in world.map.get("mica_devices", []):
        if (
            "dock" in device
            and world.pos.distance_to(tuple(32 * x + 16 for x in device["dock"])) <= 112
        ):
            return device
    return None


class MicaConsole:
    def __init__(self, game):
        self.game = game
        self.selected = 0
        self.parent = None
        self.pending = None
        self.delete_key = None
        self.message = "Save a program, then equip it on Mica."
        self.trace_index = self.step = 0
        self.compare = None

    @property
    def data(self):
        return self.game.p["program_library"]

    def revisions(self):
        return list(reversed(self.data["revisions"]))

    def open(self):
        if self.game.expeditions.busy():
            self.game.notice = "Finish or recall Mica before opening the library."
            return
        data = self.game.p.get("program_library")
        runtime = self.game.p.get("runtime_v1")
        if (
            not isinstance(data, dict)
            or data.get("schema") != 1
            or not isinstance(data.get("slots"), dict)
            or not isinstance(data.get("revisions"), dict)
            or not isinstance(data.get("traces"), list)
            or not isinstance(runtime, dict)
            or runtime.get("schema") != 1
            or not isinstance(runtime.get("device_state"), dict)
        ):
            self.game.notice = "This profile's Mica library format is unavailable in this build."
            return
        keys = self.revisions()
        equipped = self.data["slots"].get("mica")
        self.selected = keys.index(equipped) if equipped in keys else 0
        self.delete_key = None
        self.game.scene = "mica_library"

    def enable(self):
        profile = progress.extensions(self.game.p)
        profile["settings"]["mica_workshop"] = True
        progress.save(profile)
        self.game.p.update(profile)

    def edit(self, key):
        self.parent = key
        source = self.data["revisions"][key]["source"] if key else STARTER
        device = nearby_device(self.game.world)
        note = device.get("brief") if device else None
        challenge = dict(
            id="mica-library",
            title="Edit Mica program",
            kind="function",
            starter_code=source,
            story=(note + " " if note else "")
            + "Save a new revision with Ctrl+S or the Save button. Edit the first # Name: line to name your program.",
            lesson="plan(observation) returns actions. Read the robot cell, target and walls from observation to reuse your code.",
            objective="Return moves, scans, waits or a final interact with the target. Mica must stand beside the target to activate it.",
            sample='{"type": "move", "direction": "east"}',
            hint="The starter routine handles unobstructed east/west routes. For a detour, search cardinal neighbors inside visible width and height. Skip walls and stop on a tile next to the relay.",
        )
        g = self.game
        g.term = Terminal(challenge, {"drafts": {}})
        g.term.rows = ["Ctrl+S saves a revision. Esc returns to the library."]
        box, _ = g.term.buttons[0]
        g.term.buttons[0] = (box, "SAVE   Ctrl+S")
        g.scene = "terminal"
        pg.key.start_text_input()

    def save_editor(self):
        try:
            key = library.save_revision(self.game.p, self.game.term.editor.text, self.parent)
        except (ValueError, OSError) as exc:
            self.game.term.rows = [f"Save failed: {exc}"]
            return
        self.selected = self.revisions().index(key)
        self.close_editor()
        self.message = "Revision saved. Enter equips it on Mica."

    def close_editor(self):
        self.game.term = None
        self.game.scene = "mica_library"
        pg.key.stop_text_input()

    def start(self, rehearsal):
        g = self.game
        if g.expeditions.busy():
            return
        key = self.data["slots"].get("mica")
        revision = self.data["revisions"].get(key)
        device = nearby_device(g.world)
        if not revision:
            self.message = "Equip a saved revision with Enter first."
            return
        if not device:
            self.message = "Stand by a marked Mica dock in the Hangar, Workshop or Orion."
            return
        if device_locked(g.world, device):
            self.message = "Restore the Orion outpost relay to power this dock."
            return
        state = device_state(g.world, device["id"])
        if state == "online" and not rehearsal:
            self.message = "This relay is online. Try the other dock or rehearse another revision."
            return
        initial = MicaState(tuple(device["dock"]), device["energy"])
        mica = saved_mica(g.world, initial)
        try:
            pending = prepare(g.world, mica, device["id"], revision["source"])
        except ValueError as exc:
            self.message = str(exc)
            return
        self.pending = (key, mica, pending, rehearsal)
        g.future = g.pool.submit(grade_program, pending.request(), player_opt_in=True)
        self.message = "Verifying the equipped program..."

    def collect(self, report):
        key, mica, pending, rehearsal = self.pending
        self.pending = None
        if not report["passed"]:
            self.message = " ".join(report["rows"])[:340]
            return
        g = self.game
        source = self.data["revisions"].get(key, {}).get("source")
        if self.data["slots"].get("mica") != key or source is None or not nearby_device(g.world):
            self.message = "Mica's equipment or dock changed. Verify the program again."
            return
        try:
            mica = saved_mica(g.world, mica)
            result = verify(g.world, mica, pending, report, source)
            if not rehearsal and not result["proposed_intents"]:
                self.message = (
                    "The route is valid. Add an interact action to bring the relay online."
                )
                return
            library.record_verification(
                g.p, key, g.world.zone, pending.snapshot_digest, result, rehearsal=rehearsal
            )
            if rehearsal:
                self.message = f"Rehearsal saved. {len(result['trace'])} actions, {result['energy_used']} energy. R opens traces."
            else:
                job = g.deploy_mica(mica, pending, report, source, revision=key)
                g.notice = job.message + " Backspace recalls Mica."
                g.scene = "world"
        except (ValueError, OSError) as exc:
            self.message = str(exc)

    def event(self, event):
        g = self.game
        if g.scene == "world" and event.type == pg.KEYDOWN:
            if event.key == pg.K_b:
                self.open()
                return True
            if event.key == pg.K_BACKSPACE and g.mica_job and g.mica_job.status == "running":
                g.mica_job.cancel()
                g.notice = g.mica_job.message
                return True
        if g.scene not in ("mica_library", "mica_traces"):
            return False
        if event.type != pg.KEYDOWN or g.future:
            return True
        key = event.key
        if g.scene == "mica_traces":
            traces = self.data["traces"]
            if key == pg.K_ESCAPE:
                g.scene = "mica_library"
            elif traces:
                if key in (pg.K_UP, pg.K_DOWN):
                    self.trace_index = (self.trace_index + (1 if key == pg.K_DOWN else -1)) % len(
                        traces
                    )
                    self.step = 0
                elif key in (pg.K_LEFT, pg.K_RIGHT):
                    longest = len(traces[self.trace_index]["result"]["trace"])
                    if self.compare is not None:
                        longest = max(longest, len(traces[self.compare]["result"]["trace"]))
                    self.step = max(
                        0, min(longest - 1, self.step + (1 if key == pg.K_RIGHT else -1))
                    )
                elif key == pg.K_c:
                    self.compare = None if self.compare == self.trace_index else self.trace_index
            return True
        if key == pg.K_ESCAPE:
            g.scene = "world"
            return True
        try:
            if not workshop_enabled(g.p):
                if key == pg.K_RETURN:
                    self.enable()
                return True
            keys = self.revisions()
            self.selected = min(self.selected, max(0, len(keys) - 1))
            selected = keys[self.selected] if keys else None
            if key != pg.K_DELETE:
                self.delete_key = None
            if key in (pg.K_UP, pg.K_DOWN) and keys:
                self.selected = (self.selected + (1 if key == pg.K_DOWN else -1)) % len(keys)
            elif key == pg.K_n:
                self.edit(None)
            elif key == pg.K_e and selected:
                self.edit(selected)
            elif key == pg.K_RETURN and selected:
                library.equip(g.p, selected)
                self.message = "Revision equipped on Mica."
            elif key == pg.K_DELETE and selected:
                if self.delete_key == selected:
                    library.delete_revision(g.p, selected)
                    self.delete_key = None
                    self.message = "Revision deleted. Saved traces are still available."
                else:
                    self.delete_key = selected
                    self.message = "Press Delete again to remove this revision."
            elif key in (pg.K_v, pg.K_d):
                self.start(key == pg.K_v)
            elif key == pg.K_r:
                self.trace_index = max(0, len(self.data["traces"]) - 1)
                self.step = 0
                self.compare = None
                g.scene = "mica_traces"
        except (ValueError, OSError) as exc:
            self.message = str(exc)
        return True

    def draw(self, canvas):
        g = self.game
        if g.scene not in ("mica_library", "mica_traces"):
            return False
        canvas.fill(INK)
        if g.scene == "mica_traces":
            self.draw_traces(canvas)
            return True
        label(canvas, "Mica program library", 35, 36, 34, WHITE)
        if not workshop_enabled(g.p):
            wrapped(
                canvas,
                "Equip Mica with reusable Python programs. Use the marked docks in the Orientation Hangar, Workshop and Orion to test and deploy your code.",
                36,
                115,
                840,
                22,
                WHITE,
            )
            label(canvas, "Enter  Enable Mica Workshop     Esc  Return", 36, 237, 19, MINT, True)
            return True
        rect(canvas, PANEL, 32, 108, 410, 352)
        rect(canvas, PANEL, 455, 108, 600, 352)
        label(canvas, "SAVED REVISIONS", 48, 125, 16, MINT, True)
        keys = self.revisions()
        index = min(self.selected, max(0, len(keys) - 1))
        start = index // 8 * 8
        equipped = self.data["slots"].get("mica")
        for i, key in enumerate(keys[start : start + 8], start):
            r = self.data["revisions"][key]
            y = 165 + (i - start) * 33
            if i == index:
                rect(canvas, "#2d484d", 41, y - 3, 392, 31)
            label(
                canvas,
                f"{'*' if key == equipped else ' '} {r['name'][:28]} / r{r.get('revision', 1)}",
                49,
                y,
                16,
                WHITE,
                True,
            )
        if keys:
            r = self.data["revisions"][keys[index]]
            label(
                canvas,
                f"{index + 1}/{len(keys)}   {'Verified' if r.get('verified') else 'Needs verification'}   * Equipped",
                48,
                431,
                13,
                MUTED,
                True,
            )
            label(canvas, "PYTHON PREVIEW", 472, 125, 16, MINT, True)
            for i, line in enumerate(r["source"].splitlines()[:10]):
                label(canvas, line[:62], 472, 159 + i * 24, 16, WHITE, True)
        else:
            label(canvas, "Press N to create your first program.", 49, 172, 17, WHITE)
        device = nearby_device(g.world)
        text = f"DOCK  {device['name']}" if device else "DOCK  Hangar / Workshop / Orion"
        label(canvas, text, 35, 478, 16, MINT, True)
        brief = device.get("brief") if device else None
        if brief:
            wrapped(canvas, brief, 35, 502, 1000, 15, MUTED)
        wrapped(canvas, self.message, 35, 548 if brief else 515, 1000, 17, WHITE)
        label(
            canvas,
            "Up/Down Select   Enter Equip   N New   E Edit   Delete Remove",
            35,
            609,
            16,
            MUTED,
            True,
        )
        label(canvas, "V Rehearse   D Deploy   R Traces   Esc Return", 35, 644, 16, MINT, True)
        return True

    def draw_traces(self, canvas):
        traces = self.data["traces"]
        label(canvas, "Mica execution traces", 35, 36, 34, WHITE)
        if not traces:
            label(canvas, "Rehearse or deploy a program to record its trace.", 36, 120, 19, MUTED)
        else:
            current = traces[self.trace_index]
            self.trace_card(canvas, current, self.trace_index, 35)
            if self.compare is not None:
                other = traces[self.compare]
                self.trace_card(canvas, other, self.compare, 557)
                text = (
                    "Same starting snapshot"
                    if current["snapshot_digest"] == other["snapshot_digest"]
                    else "Different starting conditions"
                )
                label(canvas, text, 36, 590, 16, GOLD, True)
        label(
            canvas,
            "Up/Down Select run   Left/Right Step   C Pin comparison   Esc Library",
            35,
            644,
            16,
            MINT,
            True,
        )

    def trace_card(self, canvas, record, index, x):
        result = record["result"]
        steps = result["trace"]
        rect(canvas, PANEL, x, 112, 490, 447)
        world = record.get("world_id") or record.get("event", {}).get("world_id", "unknown")
        label(
            canvas,
            f"Run {index + 1}   {world.replace('_', ' ')}   {record.get('mode', 'deployment')}",
            x + 15,
            130,
            16,
            MINT,
            True,
        )
        label(
            canvas,
            f"{len(steps)} actions   {result['energy_used']} energy used",
            x + 15,
            172,
            17,
            WHITE,
        )
        label(
            canvas,
            f"Code {record['source_hash'][:10]}   Snapshot {record['snapshot_digest'][:10]}",
            x + 15,
            211,
            14,
            MUTED,
            True,
        )
        if not steps:
            label(canvas, "The program returned an empty plan.", x + 15, 279, 17, WHITE)
            return
        i = min(self.step, len(steps) - 1)
        step = steps[i]
        label(
            canvas,
            f"Step {i + 1}/{len(steps)}   {step['action']['type'].upper()}",
            x + 15,
            265,
            20,
            GOLD,
        )
        detail = " ".join(str(v) for k, v in step["action"].items() if k != "type")
        wrapped(canvas, detail, x + 15, 306, 455, 17, WHITE)
        cells = [steps[0]["from_cell"], *(entry["to_cell"] for entry in steps)]
        west = min(cell[0] for cell in cells)
        north = min(cell[1] for cell in cells)
        scale = min(
            24,
            408 / max(1, max(cell[0] for cell in cells) - west),
            64 / max(1, max(cell[1] for cell in cells) - north),
        )
        points = [
            (round(x + 26 + (cx - west) * scale), round(383 + (cy - north) * scale))
            for cx, cy in cells
        ]
        pg.draw.lines(canvas, "#527078", False, points, 2)
        for point in points:
            pg.draw.circle(canvas, MUTED, point, 3)
        pg.draw.circle(canvas, GOLD, points[i + 1], 6)
        label(canvas, f"{step['from_cell']}  to  {step['to_cell']}", x + 15, 459, 17, WHITE, True)
        label(canvas, f"Energy remaining  {step['energy_remaining']}", x + 15, 500, 17, MINT, True)
