from pathlib import Path
base=Path(__file__).resolve().parents[1]/"src/python_quest_2d"
def edit(name,old,new):
    path=base/name
    text=path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old,new),encoding="utf-8")

edit("ui/terminal.py","ed.top+(y-self.Y)//24","ed.top+int((y-self.Y)//24)")
edit("game/art.py","    for gate in world.map",'''    from .instruments import draw_instrument
    index=PALETTES.index(accent)
    for t,(x,y) in zip(world.map["interactables"],[(276,202),(659,209),(667,462),(295,396)]):
        draw_instrument(s,index,x,y,accent,t["challenge_id"] in world.p["completed"],tick)
    for gate in world.map''')
edit("game/app.py","from ..core.challenges import LESSONS,ZONES,NAMES","from ..core.challenges import LESSONS,ZONES,NAMES,ROOT")
edit("game/app.py","    def leave_terminal(self):",'''    def reveal(self):
        t=self.term
        if self.future:
            return
        if not t.confirm:
            t.confirm=True
            t.rows=["Reveal the reference solution? F2 again confirms. Your first pass will earn 25 XP. Esc cancels."]
            return
        t.confirm=False
        k=t.ch["id"]
        if k not in self.p.setdefault("revealed",[]):
            self.p["revealed"].append(k)
        t.editor.anchor=0
        t.editor.pos=len(t.editor.text)
        t.editor.replace((ROOT/"content/authoring"/(k+".py")).read_text(encoding="utf-8"))
        t.rows=["Solution loaded. Trace its steps, then run the tests."]
        self.persist()

    def leave_terminal(self):''')
edit("game/app.py","                    self.leave_terminal()","                    if t.confirm:\n                        t.confirm=False\n                        t.rows=['Reveal canceled.']\n                    else:\n                        self.leave_terminal()")
edit("game/app.py","                elif e.key==pg.K_F1:","                elif e.key==pg.K_F2:\n                    self.reveal()\n                elif e.key==pg.K_F1:")
edit("ui/terminal.py","self.ok=False","self.confirm=False")
edit("ui/terminal.py",'label(s,"PYTHON  /  LOCAL",892,100,14,MUTED,True)','label(s,"F2  Reveal solution",868,100,14,MUTED,True)')
edit("core/progress.py",'xp=75 if key in p["hinted"] else 100','xp=25 if key in p.get("revealed",[]) else 75 if key in p["hinted"] else 100')
edit("ui/terminal.py",'self.ch["hint"] if self.help>1 else self.ch["lesson"]','self.ch["hint"] if self.help>1 else ("Trace the sample call by hand. Which value must your function return?" if self.ch["kind"]=="function" else "Compare each printed character to the example, including spaces and capitals.")')

