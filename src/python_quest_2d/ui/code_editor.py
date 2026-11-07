import pygame as pg


class Editor:
    def __init__(self, text):
        self.text = text
        self.pos = self.anchor = len(text)
        self.history = []
        self.future = []
        self.top = self.left = 0

    def snapshot(self):
        return self.text, self.pos, self.anchor

    def replace(self, new):
        a, b = sorted((self.pos, self.anchor))
        if len(self.text) + len(new) - (b - a) > 65536:
            return
        self.history.append(self.snapshot())
        self.history = self.history[-120:]
        self.future.clear()
        self.text = self.text[:a] + new + self.text[b:]
        self.pos = self.anchor = a + len(new)

    def locate(self):
        prefix = self.text[: self.pos]
        return prefix.count("\n"), len(prefix.rsplit("\n", 1)[-1])

    def index(self, row, col):
        lines = self.text.split("\n")
        row = max(0, min(row, len(lines) - 1))
        return sum(len(l) + 1 for l in lines[:row]) + min(max(0, col), len(lines[row]))

    def key(self, e):
        k = e.key
        ctrl = e.mod & pg.KMOD_CTRL
        shift = e.mod & pg.KMOD_SHIFT
        row, col = self.locate()
        if ctrl and k == pg.K_a:
            self.anchor, self.pos = 0, len(self.text)
        elif ctrl and k in (pg.K_c, pg.K_x, pg.K_v):
            a, b = sorted((self.pos, self.anchor))
            try:
                if k == pg.K_v:
                    self.replace(pg.scrap.get_text().replace("\r\n", "\n").replace("\t", "    "))
                elif a != b:
                    pg.scrap.put_text(self.text[a:b])
                    if k == pg.K_x:
                        self.replace("")
            except (pg.error, TypeError, AttributeError):
                pass
        elif ctrl and k in (pg.K_z, pg.K_y):
            src, dest = (self.history, self.future) if k == pg.K_z else (self.future, self.history)
            if src:
                dest.append(self.snapshot())
                self.text, self.pos, self.anchor = src.pop()
        elif k in (pg.K_LEFT, pg.K_RIGHT, pg.K_HOME, pg.K_END, pg.K_UP, pg.K_DOWN):
            if k in (pg.K_LEFT, pg.K_RIGHT):
                self.pos = max(0, min(len(self.text), self.pos + (1 if k == pg.K_RIGHT else -1)))
            else:
                self.pos = self.index(
                    row + (k == pg.K_DOWN) - (k == pg.K_UP),
                    0 if k == pg.K_HOME else 65536 if k == pg.K_END else col,
                )
            if not shift:
                self.anchor = self.pos
        elif k in (pg.K_BACKSPACE, pg.K_DELETE):
            if self.anchor == self.pos:
                self.anchor = max(
                    0, min(len(self.text), self.pos + (1 if k == pg.K_DELETE else -1))
                )
            self.replace("")
        elif k == pg.K_RETURN and not ctrl:
            line = self.text[self.index(row, 0) : self.pos]
            self.replace(
                "\n"
                + " "
                * (len(line) - len(line.lstrip(" ")) + (4 if line.rstrip().endswith(":") else 0))
            )
        elif k == pg.K_TAB:
            if shift:
                start = self.index(row, 0)
                count = min(4, len(self.text[start:]) - len(self.text[start:].lstrip(" ")))
                self.anchor, self.pos = start, start + count
                self.replace("")
            else:
                self.replace("    ")
