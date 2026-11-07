"""Lay out four connected maintenance bays around a central bulkhead."""
import json
from pathlib import Path
for index,p in enumerate(sorted((Path(__file__).resolve().parents[1]/"content/maps").glob("*.json"))):
    m=json.loads(p.read_text())
    grid=[list(row) for row in m["tiles"]]
    for x in range(1,23):
        grid[9][x]="#"
    for y in range(1,17):
        grid[y][12]="#"
    for x in range(1,12):
        grid[14][x]="#"
    coords=[(12,4),(18,9),(12,12),(6,14)]
    for gate,(x,y) in zip(m["gates"],coords):
        grid[y][x]="."
        gate.update(x=x*32,y=y*32)
    for t,(x,y) in zip(m["interactables"],[(5,4),(18,4),(18,12),(6,12)]):
        t.update(x=x*32+16,y=y*32+16)
    grid[2][7+index%3]="#"
    grid[6][17+index%3]="#"
    m["tiles"]=["".join(row) for row in grid]
    m["exit"].update(x=208,y=505)
    p.write_text(json.dumps(m,indent=2)+"\n")

