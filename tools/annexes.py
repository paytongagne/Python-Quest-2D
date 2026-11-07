"""Extend each Act I map eastward while retaining the original coordinate system."""
from pathlib import Path
import json
names=["Observation blister","Launch telemetry","Navigation alcove","Spectral lab","Cooling manifold","Memory archive"]
notes=[
"Night shift: the seed bank requested a courier fuse at 02:14. Its last delivery is still queued.",
"Launch log: no hull breach. The alert began inside the dispatch scheduler.",
"Navigation: every false alarm repeats exactly eight seconds after a pump request.",
"Spectral trace: the wet and dry trays are sharing one control address.",
"Thermal log: the pressure line must vent before another pump pulse.",
"Archive: a safe controller checks pressure before moisture. MARA left the logger on the far rail."]
from_order=("orientation","launch","control","sensor","engine","algorithm")
base=Path(__file__).resolve().parents[1]/"content/maps"
for i,zone in enumerate(from_order):
    path=base/(zone+".json")
    m=json.loads(path.read_text())
    rows=[]
    for y,row in enumerate(m["tiles"]):
        tail=" "*8
        if y in (2,8): tail="########"
        if 2<y<8: tail=".......#"
        if y==5: row=row[:-1]+"."
        rows.append(row+tail)
    m.update(width=32,tiles=rows,alcove=names[i],note=notes[i],sites=[dict(type="archive",x=938,y=180)])
    path.write_text(json.dumps(m,indent=2)+"\n")

