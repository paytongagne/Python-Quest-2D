import pygame as pg

from ..game.art import GOLD, INK, MINT, MUTED, PANEL, WHITE, font, label, rect, wrapped
from .code_editor import Editor


class Terminal:
    X, Y = 451, 143

    def __init__(self, ch, p):
        self.ch = ch
        self.editor = Editor(p["drafts"].get(ch["id"], ch["starter_code"]))
        self.rows = ["Ready. Run your code to check the repair."]
        if ch.get("simulation") == "route":
            grid, start, goal = ch["cases"][0]["args"]
            self.rows = [
                "MICA / LIVE RAIL",
                "Start " + str(start) + "   Dock " + str(goal),
                *["  " + " ".join(row) for row in grid],
                "Pass the trials, then press Esc to deploy your route.",
            ]
        self.scroll = 0
        self.brief_scroll = 0
        self.brief_height = 590
        self.error = None
        self.confirm = False
        self.help = 0
        self.drag = False
        self.char = font(18, True).size("M")[0]
        self.buttons = [
            (pg.Rect(445, 627, 173, 40), "RUN   Ctrl+Enter"),
            (pg.Rect(630, 627, 150, 40), "HINT   F1"),
            (pg.Rect(792, 627, 185, 40), "RETURN   Esc"),
        ]

    def hit_text(self, x, y, extend):
        ed = self.editor
        ed.pos = ed.index(
            ed.top + int((y - self.Y) // 24), ed.left + round((x - self.X) / self.char)
        )
        if not extend:
            ed.anchor = ed.pos

    def draw(self, s, p, busy):
        s.fill(INK)
        rect(s, PANEL, 14, 83, 352, 590)
        rect(s, "#12232e", 383, 83, 686, 322)
        label(s, "ASTRA    /    ENGINEERING TERMINAL", 23, 15, 15, MINT, True)
        label(s, self.ch["title"], 22, 39, 29)
        screen = s
        s = pg.Surface((366, 1800))
        s.fill(PANEL)
        label(s, "REPAIR BRIEF", 30, 99, 16, GOLD, True)
        y = wrapped(s, self.ch["story"], 30, 131, 319)
        for title, field in [
            ("FIELD NOTES", "lesson"),
            ("ASSIGNMENT", "objective"),
            ("EXAMPLE", "sample"),
        ]:
            label(s, title, 30, y + 14, 14, MINT, True)
            y = wrapped(s, self.ch[field], 30, y + 37, 316, 16, WHITE)
        if self.help:
            label(s, "PIP  /  HINT", 30, y + 12, 14, GOLD, True)
            y = wrapped(
                s,
                self.ch["hint"]
                if self.help > 1
                else (
                    "Trace the sample call by hand. Which state or result should each test produce?"
                    if self.ch["kind"] in ("function", "object")
                    else "Compare each printed character to the example, including spaces and capitals."
                ),
                30,
                y + 35,
                316,
                15,
                GOLD,
            )
        self.brief_height = y
        self.brief_scroll = max(0, min(self.brief_scroll, max(0, y - 620)))
        screen.blit(s, (14, 83), (14, 83 + self.brief_scroll, 352, 546))
        s = screen
        label(s, "F3 / F4  Scroll briefing", 30, 643, 14, MUTED, True)
        label(s, "terminal.py", 404, 98, 17, MINT, True)
        label(s, "F2  Reveal solution", 868, 100, 14, MUTED, True)
        ed = self.editor
        row, col = ed.locate()
        ed.top = min(row, max(ed.top, row - 9))
        width = (1054 - self.X) // self.char
        ed.left = min(col, max(ed.left, col - width + 1))
        lines = ed.text.split("\n")
        a, b = sorted((ed.pos, ed.anchor))
        for i, line in enumerate(lines[ed.top : ed.top + 10], ed.top):
            y = self.Y + (i - ed.top) * 24
            if i == row or self.error == i + 1:
                rect(s, "#463039" if self.error == i + 1 else "#213745", 391, y - 1, 668, 23)
            start = ed.index(i, 0)
            lo = max(ed.left, a - start)
            hi = min(len(line) + 1, b - start, ed.left + width)
            if lo < hi:
                rect(
                    s, "#426576", self.X + (lo - ed.left) * self.char, y, (hi - lo) * self.char, 22
                )
            label(s, str(i + 1), 397, y, 16, MUTED, True)
            label(
                s,
                line[ed.left : ed.left + width],
                self.X,
                y,
                18,
                MUTED if line.strip().startswith("#") else WHITE,
                True,
            )
        if pg.time.get_ticks() % 950 < 650:
            rect(s, MINT, self.X + (col - ed.left) * self.char, self.Y + (row - ed.top) * 24, 2, 21)
        rect(s, PANEL, 383, 419, 686, 190)
        label(s, "TEST CONSOLE", 402, 432, 15, MINT, True)
        label(s, "PgUp / PgDn", 926, 432, 14, MUTED, True)
        # Render wrapped feedback separately so even a long traceback can scroll.
        report = pg.Surface((643, max(145, 120 * len(self.rows) + 500)))
        report.fill(PANEL)
        y = 0
        for line in self.rows:
            y = (
                wrapped(
                    report,
                    line,
                    0,
                    y,
                    640,
                    15,
                    MINT
                    if line.startswith("PASS")
                    else GOLD
                    if line.startswith(("FAIL", "ERROR"))
                    else WHITE,
                    True,
                )
                + 4
            )
        self.scroll = max(0, min(self.scroll, y - 140))
        s.blit(report, (404, 466), (0, self.scroll, 643, 140))
        for box, name in self.buttons:
            pg.draw.rect(s, "#34574f" if box == self.buttons[0][0] else PANEL, box, border_radius=4)
            label(
                s,
                "RUNNING..." if busy and box == self.buttons[0][0] else name,
                box.x + 10,
                box.y + 10,
                15,
                WHITE,
                True,
            )
