from pathlib import Path
base=Path(__file__).resolve().parents[1]/"src/python_quest_2d"
def sub(file,a,b):
    p=base/file
    s=p.read_text(encoding="utf-8")
    assert a in s,a
    p.write_text(s.replace(a,b),encoding="utf-8")
sub("core/challenges.py",'MAPS = load_content("maps")','LESSONS.update(load_content("expansion"))\nMAPS = load_content("maps") | load_content("sectors")')
sub("core/progress.py",'"schema_version": 2','"schema_version": 3')
sub("core/progress.py",'if p["player"]["zone"] not in ZONES','if p["player"]["zone"] not in (*ZONES,"hydro")')
sub("core/progress.py","            return p","""            if p["schema_version"]==2:
                backup=path.with_suffix(".pre-greenline.json")
                if not backup.exists():
                    shutil.copy2(path,backup)
                p["schema_version"]=3
            return p""")
sub("core/worker.py","import ast","""import ast
import copy
from pathlib import Path
if __name__=="__main__":
    sys_path = str(Path(__file__).resolve().parent)
    import sys
    sys.path.insert(0,sys_path)
    from route import trace
else:
    from .route import trace""")
sub("core/worker.py","    rows, successes, line = [], 0, None","    effect=None\n    rows, successes, line = [], 0, None")
sub("core/worker.py",'''                    actual = fn(*case["args"])
                    expected = case["expected"]
                    ok = match(actual, expected)
                    detail = f"{case['args']!r}: expected {expected!r}, got {actual!r}"''','''                    actual = fn(*copy.deepcopy(case["args"]))
                    if ch.get("simulation")=="route":
                        try:
                            trace(case["args"],actual)
                            ok=True
                            detail=f"Dock reached in {len(actual)} moves."
                            if i==1: effect=actual
                        except ValueError as exc:
                            ok=False
                            detail=str(exc)
                        detail+=f" Grid/start/goal: {case['args']!r}"
                    else:
                        expected = case["expected"]
                        ok = match(actual, expected)
                        detail = f"{case['args']!r}: expected {expected!r}, got {actual!r}"
                        if i==1 and ok and ch["id"]=="hydro_02":
                            effect=actual''')
sub("core/worker.py",'        "passed_count": successes,','        "effect": effect if successes==len(cases) else None,\n        "passed_count": successes,')
sub("game/world.py","from ..core.challenges import MAPS","from ..core.challenges import MAPS\nfrom .nursery import TRAM")
sub("game/world.py","        self.steps = 0","        self.steps = 0\n        self.flight=0.0\n        self.camera=pg.Vector2(max(0,min(self.pos.x-384,self.map['width']*32-768)),0)")
sub("game/world.py",'            dict(self.map["exit"], type="lift"),','            dict(self.map["exit"], type="tram" if self.zone=="hydro" else "lift"),\n            *([TRAM] if self.zone!="hydro" else self.map["sites"]),')
sub("game/art.py","s = pg.Surface((768, 576))",'s = pg.Surface((world.map["width"]*32,world.map["height"]*32))')
sub("game/art.py","    for t, (x, y) in zip(","    from .nursery import field\n    field(s,world,tick)\n    for t, (x, y) in zip(")
sub("game/art.py",'world.map["interactables"], [(276','world.map["interactables"] if world.zone!="hydro" else [], [(276')
sub("game/art.py",'    pg.draw.ellipse(s, accent, (x - 31, y - 13, 62, 26), 3)\n    label(s, "LIFT", x - 17, y - 10, 14, WHITE, True)','    if world.zone!="hydro":\n        pg.draw.ellipse(s, accent, (x - 31, y - 13, 62, 26), 3)\n        label(s, "LIFT", x - 17, y - 10, 14, WHITE, True)')
sub("game/art.py",'    return s\n'+'', '    return s\n') 
sub("game/art.py",'    pilot(s, *world.pos, world)\n    return s','    pilot(s, *world.pos, world)\n    return s.subsurface((int(world.camera.x),0,768,576))')
sub("game/art.py",'PALETTES.index(accent)','PALETTES.index(accent) if world.zone!="hydro" else 0')
app="game/app.py"
sub(app,"from .world import World","from .world import World\nfrom . import nursery\nfrom ..core.route import trace")
sub(app,"self.index = ZONES.index(self.world.zone)","self.index = 6 if self.world.zone=='hydro' else ZONES.index(self.world.zone)")
sub(app,"self.accent = PALETTES[self.index]","self.accent = '#9cdfae' if self.index==6 else PALETTES[self.index]")
sub(app,'        t = self.world.nearest()\n        if not t:', '''        if self.p.get("deployment"):
            self.notice="Mica is on the rail. Watch for the docking signal."
            return
        t = self.world.nearest()
        if not t:''')
sub(app,'        elif t["type"] == "pip":\n            self.notice = "PIP: Each repair opens a bulkhead. Follow the bay numbers to the lift."','''        elif t["type"]=="tram":
            if self.world.zone=="hydro":
                self.world.enter(self.p.get("tram_origin","orientation"))
                self.notice="Back on the main deck. Use J for your flight log."
            else:
                self.p["tram_origin"]=self.world.zone
                self.world.enter("hydro")
                self.notice="MARA: Meet me by the west platform. Mica needs a pilot."
            self.refresh()
            self.persist()
        elif t["type"]=="log":
            self.p["world_flags"]["grower_log"]=True
            self.notice="Field log: The Scheduler kept flushing the line after every dry reading. MARA marked this valve for salvage."
            self.persist()
        elif t["type"]=="mara":
            key=next((k for k in ("hydro_01","hydro_02","hydro_03","hydro_04") if k not in self.p["completed"]),None)
            self.notice={"hydro_01":"MARA: Mica is on the eastbound rail. Program the console above me to deliver a fuse.",
              "hydro_02":"MARA: Mica opened the seed bank. Check moisture before you feed the trays.",
              "hydro_03":"MARA: The logger is across a broken rail. Route Mica through the gap.",
              "hydro_04":"MARA: We've got the readings. Stop the pump from cycling; mind the steam.",
              None:"MARA: Roots are taking. Your diagnostic lens can find the grower's log in the gallery."}[key]
        elif t["type"] == "pip":
            self.notice = ("PIP: Mica's fuse is installed. MARA has more work across the greenline." if "hydro_01" in self.p["completed"] else "PIP: The west tram leads to MARA and her programmable rover. Main-deck repairs open the numbered bays.")''')
sub(app,'                xp = award(self.p, t.ch["id"])','''                if t.ch.get("simulation")=="route":
                    try:
                        trace(t.ch["cases"][0]["args"],result.get("effect"))
                    except ValueError as exc:
                        t.rows=["Route rejected: "+str(exc)]
                        return
                    self.p["deployment"]=dict(key=t.ch["id"],commands=result["effect"])
                    self.world.flight=0.0
                    self.persist()
                    self.notice="Flight plan verified. Esc to watch Mica deliver the payload."
                    t.rows[0]=self.notice
                    self.tone("open")
                    return
                if t.ch["id"]=="hydro_02":
                    trays=result.get("effect")
                    if trays!=t.ch["cases"][0]["expected"]:
                        t.rows=["Controller output did not match the tray fixtures."]
                        return
                    self.p["irrigated"]=trays
                if t.ch["id"]=="hydro_04":
                    self.p["world_flags"]["diagnostic_lens"]=True
                xp = award(self.p, t.ch["id"])''')
sub(app,'                t.rows[0] = self.notice +','                if t.ch["id"]=="hydro_04":\n                    self.notice=f"Pump stabilized. Diagnostic lens online. +{xp} XP"\n                t.rows[0] = self.notice +')
sub(app,'    def hint(self):','''    def update_field(self,dt):
        w=self.world
        target=max(0,min(w.pos.x-384,w.map["width"]*32-768))
        w.camera.x+=(target-w.camera.x)*(1-math.exp(-10*dt))
        if w.zone!="hydro": return
        job=self.p.get("deployment")
        if job:
            w.flight+=dt*2.2
            if w.flight>=max(1,len(job["commands"])):
                key=job["key"]
                self.p.pop("deployment")
                xp=award(self.p,key)
                self.opening[LESSONS[key]["world_effect"]]=pg.time.get_ticks()
                self.notice=f"Mica docked. Payload installed; bulkhead open. +{xp} XP"
                self.tone("pass")
        if "hydro_04" not in self.p["completed"] and nursery.HAZARD.collidepoint(w.pos):
            w.pos.update(1190,288)
            w.sync()
            self.notice="Steam surge! Suit recall returned you to the gallery entrance."

    def hint(self):''')
sub(app,'        elif self.scene == "world":\n            if k == pg.K_e:', '        elif self.scene == "world":\n            if k==pg.K_m:\n                self.scene="survey"\n            elif k == pg.K_e:')
sub(app,'        elif k in (pg.K_ESCAPE, pg.K_j, pg.K_RETURN):','        elif self.scene=="survey" and k==pg.K_m:\n            self.scene="world"\n        elif k in (pg.K_ESCAPE, pg.K_j, pg.K_RETURN):')
sub(app,'            if z == ZONES[0] or','            if self.p.get("deployment"):\n                self.notice="Mica is in transit."\n                return\n            if z == ZONES[0] or')
sub(app,'label(s, NAMES[i],','label(s, nursery.TITLE if i==6 else NAMES[i],')
sub(app,'f"DECK   0{i + 1} / 06"','"GREENLINE   /   01" if i==6 else f"DECK   0{i + 1} / 06"')
sub(app,' / 24 repairs',' / 28 repairs')
sub(app,'/ 24, 5','/ 28, 5')
sub(app,'{"terminal": "Access console", "pip": "Talk to PIP", "lift": "Use deck lift"}','{"terminal":"Access console","pip":"Talk to PIP","lift":"Use deck lift","tram":"Ride Greenline tram","log":"Read field log","mara":"Talk to MARA"}')
sub(app,'label(s, "J   Flight log      Esc   Pause", 754','label(s, "J  Journal   M  Survey   Esc  Pause", 715')
sub(app,'            if self.scene != "world":','            if self.scene=="survey":\n                nursery.survey(self.canvas,self.world)\n            elif self.scene != "world":')
sub(app,'                    label(s, "Esc   Return to station", 216, 548, 16, MUTED, True)','                    wrapped(s,"Greenline: "+nursery.objective(self.p),216,537,660,16,GOLD)')
sub(app,'                if (\n                    pg.time','                    self.update_field(dt)\n                if (\n                    pg.time')

