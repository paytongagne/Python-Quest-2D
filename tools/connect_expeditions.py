from pathlib import Path
root=Path(__file__).resolve().parents[1]/"src/python_quest_2d"
def edit(name,a,b):
    p=root/name;s=p.read_text(encoding="utf-8")
    assert a in s,a
    p.write_text(s.replace(a,b),encoding="utf-8")
edit("core/challenges.py",'LESSONS.update(load_content("expansion"))','LESSONS.update(load_content("expansion"))\nLESSONS.update(load_content("expeditions"))')
edit("core/challenges.py",'load_content("maps") | load_content("sectors")','load_content("maps") | load_content("sectors") | load_content("planets")')
edit("core/progress.py","from .challenges import LESSONS, ZONES","from .challenges import LESSONS, ZONES, MAPS")
edit("core/progress.py",'"schema_version": 3','"schema_version": 4')
edit("core/progress.py",'not in (*ZONES, "hydro")','not in MAPS')
edit("core/progress.py",'            return p','''            if p["schema_version"]==3:
                backup=path.with_suffix(".pre-expedition.json")
                if not backup.exists():
                    shutil.copy2(path,backup)
                p["schema_version"]=4
            return p''')
edit("core/worker.py",'    from route import trace','    from route import trace\n    from expedition_contract import validate')
edit("core/worker.py",'    from .route import trace','    from .route import trace\n    from .expedition_contract import validate')
edit("core/worker.py",'                    if ch.get("simulation") == "route":','''                    if ch.get("simulation")=="expedition":
                        try:
                            validated=validate(ch,case,actual)
                            ok=True
                            detail=f"Validated {str(actual)[:300]}"
                            if i==1:
                                effect=validated
                        except ValueError as exc:
                            ok=False
                            detail=str(exc)
                    elif ch.get("simulation") == "route":''')
edit("game/world.py",'        things = [','''        if self.zone in ("orion_moon","titan_cloud","helix_bio","aurora_ep"):
            things=[*self.map["interactables"],self.map["exit"],*self.map["sites"]]
            return min((t for t in things if math.dist(self.pos,(t["x"],t["y"]))<=54),
                       key=lambda t:math.dist(self.pos,(t["x"],t["y"])),default=None)
        things = [''')
app="game/app.py"
edit(app,'from . import nursery','from . import nursery\nfrom .expedition import Expeditions, PLANETS\nfrom . import planet_art')
edit(app,'        self.world = World(self.p)','        self.world = World(self.p)\n        self.expeditions=Expeditions(self)')
edit(app,'    def refresh(self):','''    def refresh(self):
        if self.world.zone in PLANETS:
            self.index=7
            self.accent=PLANETS[self.world.zone]["color"]
            self.bg=planet_art.landscape(self.world)
            return''')
edit(app,'        if self.p.get("deployment"):\n            self.notice','        if self.p.get("deployment") or self.p.get("expedition_job"):\n            self.notice')
edit(app,'        self.tone("open")\n        if t["type"]','        self.tone("open")\n        if self.world.zone in PLANETS and self.expeditions.interaction(t):\n            return\n        if t["type"]')
edit(app,'        if t.ch.get("simulation") == "route":\n            self.p.pop','        if t.ch.get("simulation")=="expedition":\n            self.p.pop("expedition_job",None)\n        if t.ch.get("simulation") == "route":\n            self.p.pop')
edit(app,'            if result["passed"]:\n                if t.ch','            if result["passed"]:\n                if self.expeditions.accept(t.ch,result):\n                    return\n                if t.ch')
edit(app,'        if w.zone != "hydro":','        self.expeditions.update(dt)\n        if w.zone != "hydro":')
edit(app,'        if self.scene == "terminal":\n            t = self.term','        if self.expeditions.event(e):\n            return\n        if self.scene == "terminal":\n            t = self.term')
edit(app,'    def world_screen(self):','    def world_screen(self):\n        if self.expeditions.world_screen():\n            return')
edit(app,' / 40 repairs',' / {len(LESSONS)} repairs')
edit(app,' / 40, 5',' / len(LESSONS), 5')
edit(app,'        if self.scene == "terminal":\n            self.term.draw','        if self.expeditions.draw_overlay(self.canvas):\n            pass\n        elif self.scene == "terminal":\n            self.term.draw')
edit(app,'label(s, "J  Journal   M  Survey   Esc  Pause", 715','label(s, "T  Worlds   J  Journal   M  Survey", 715')
edit(app,'                self.draw()\n        finally:','                if self.scene=="replay":\n                    self.expeditions.update(dt)\n                self.draw()\n        finally:')
edit("game/nursery.py",'else "Main deck",','else w.zone.replace("_"," ").title(),')
edit("game/nursery.py",'else TRAM,','else (m["exit"] if w.zone in ("orion_moon","titan_cloud","helix_bio","aurora_ep") else TRAM),')
edit("game/planet_art.py",'    pilot(s,*w.pos,w)\n','')
edit("game/planet_art.py",'    return s.subsurface','    pilot(s,*w.pos,w)\n    return s.subsurface')

