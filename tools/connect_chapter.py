from pathlib import Path
root=Path(__file__).resolve().parents[1]
def edit(path,a,b):
    p=root/"src/python_quest_2d"/path
    s=p.read_text(encoding="utf-8-sig")
    assert a in s,a
    p.write_text(s.replace(a,b),encoding="utf-8")
edit("core/worker.py",'ch["id"]=="hydro_02"','(ch["id"]=="hydro_02" or ch.get("simulation")=="instrument")')
edit("game/app.py",'                if t.ch["id"]=="hydro_04":\n                    self.p', '''                if t.ch.get("simulation")=="instrument":
                    if result.get("effect")!=t.ch["cases"][0]["expected"]:
                        t.rows=["Instrument result did not match its fixture."]
                        return
                    self.p.setdefault("instruments",{})[t.ch["id"]]=result["effect"]
                if t.ch["id"]=="hydro_04":
                    self.p''')
edit("game/app.py",'    def leave_terminal(self):','    def leave_terminal(self):')
edit("game/app.py",'        self.term = None\n        pg.key.stop_text_input()', '''        self.term = None
        if "hydro_16" in self.p["completed"] and not self.p["world_flags"].get("canopy_celebrated"):
            self.p["world_flags"]["canopy_celebrated"]=True
            self.scene="canopy"
            self.persist()
        pg.key.stop_text_input()''')
edit("game/app.py",'        for j in range(4):','        sector=min(3,int(self.world.pos.x//1536)) if i==6 else 0\n        for j in range(sector*4,sector*4+4):')
edit("game/app.py",' / 28 repairs',' / 40 repairs')
edit("game/app.py",' / 28, 5',' / 40, 5')
edit("game/app.py",'"GREENLINE   /   01" if i==6', 'f"GREENLINE   /   {min(4,int(self.world.pos.x//1536)+1):02}" if i==6')
edit("game/app.py",'"ending": "Astra is online.",','"ending": "Astra is online.",\n                    "canopy":"The canopy is breathing.",')
edit("game/app.py",'                        "pause": f','                        "canopy":"Mica docks the recovery relay. The fault latch clears, and water returns to the canopy.\n\nMARA: Sixteen systems back online. The maintenance network is next.\n\nEnter   Explore the restored greenhouse",\n                        "pause": f')
edit("game/nursery.py",'for bay in range(4):','for bay in range(16):')
edit("game/nursery.py",'for i in range(1,5):','for i in range(1,17):')
edit("game/nursery.py",'return BAYS[i-1]+" / "+LESSONS[key]["title"]','return f"Bay {i:02} / "+LESSONS[key]["title"]')
edit("game/nursery.py",'for i,name in enumerate(BAYS):','for i,name in enumerate(w.map["bay_names"]):')
edit("game/nursery.py",'    # MARA wears','    draw_machines(s,w,tick)\n    # MARA wears')
edit("game/nursery.py",'    scale=min(18,850//m["width"])','    page=min(3,int(w.pos.x//1536)) if w.zone=="hydro" else 0\n    offset=page*48\n    visible=48 if w.zone=="hydro" else m["width"]\n    label(s,m["sectors"][page] if w.zone=="hydro" else "Main deck",105,110,19,GOLD)\n    scale=min(18,850//visible)')
edit("game/nursery.py",'ox=(1088-scale*m["width"])//2','ox=(1088-scale*visible)//2')
edit("game/nursery.py",'for x,c in enumerate(row):','for x,c in enumerate(row[offset:offset+visible]):')
edit("game/nursery.py",'        pg.draw.circle(s,color,(int(ox+t["x"]/32*scale),int(oy+t["y"]/32*scale)),radius)','        x=t["x"]/32-offset\n        if 0<=x<visible:\n            pg.draw.circle(s,color,(int(ox+x*scale),int(oy+t["y"]/32*scale)),radius)')
edit("game/art.py",'world.map["interactables"]):','world.map["interactables"]):')
edit("game/app.py",'None:"MARA: Roots are taking. Your diagnostic lens can find the grower\'s log in the gallery."','None:"MARA: Roots are taking. Continue east through filtration, then the reservoir to canopy control."')


