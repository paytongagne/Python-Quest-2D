"""Author the nursery sector of the Hydroponics expansion."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/"content"
def write(group,key,data):
    (root/group).mkdir(exist_ok=True)
    (root/group/(key+".json")).write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
def lesson(n,title,story,objective,lesson,sample,signature,hint,cases,solution,route=False):
    key=f"hydro_{n:02}"
    name=signature.split("(")[0]
    ch=dict(id=key,kind="function",zone="hydro",sequence=n,title=title,story=story,objective=objective,lesson=lesson,sample=sample,function_name=name,starter_code="def "+signature+":\n    pass\n",hint=hint,cases=cases,world_effect="relay_"+key)
    if route: ch["simulation"]="route"
    write("expansion",key,ch)
    (root/"authoring"/(key+".py")).write_text("def "+signature+":\n"+solution+"\n",encoding="utf-8")
def route(grid,start,goal):
    return {"args":[grid,start,goal]}
def case(args,expected):
    return dict(args=args,expected=expected)
lesson(1,"Dispatch the courier","MARA's courier, Mica, carries a fuse. Its rail runs east to the first airlock.","Return RIGHT once per column between start and goal. Coordinates are [x, y].","A route is a list of step names. Multiplying a list repeats its elements. A zero-length trip needs an empty list.","['RIGHT'] * 2","plan_route(grid, start, goal)","Subtract start[0] from goal[0] to get the number of moves.",[route(["....."],[0,0],[4,0]),route(["..."],[1,0],[2,0]),route([".."],[1,0],[1,0])],"    return ['RIGHT'] * (goal[0] - start[0])",True)
lesson(2,"Feed the seed trays","Dry roots need water. Overwatering the healthy trays would ruin the seed bank.","Return the indices of readings strictly below limit, in their original order.","enumerate pairs each value with its position. Build a list of only the positions that pass your test.","dry_trays([12, 50, 10], 20) -> [0, 2]","dry_trays(readings, limit)","Loop over enumerate(readings) and append the index when moisture < limit.",[case([[18,54,22,61],30],[0,2]),case([[],20],[]),case([[20,19,20],20],[1]),case([[0,0],1],[0,1])],"    return [i for i, moisture in enumerate(readings) if moisture < limit]")
maze=[".....","###.#","....."]
lesson(3,"Retrieve the logger","The scheduler sealed the center aisle. Mica must bring a logger around the obstruction.","Return a valid route to goal using UP, DOWN, LEFT, RIGHT. '#' blocks movement. grid[y][x] is the cell at [x,y]. Trials use open top and bottom aisles joined by one gap.","Plan three legs: move across the top to the gap in row 1, descend twice, then cross the bottom to the goal. Each test moves the gap.","grid = ['.....', '###.#', '.....']","plan_route(grid, start, goal)","Find the gap with grid[1].index('.'). Build each horizontal leg using its signed distance.",[route(maze,[0,0],[4,2]),route(["....",".###","...."],[2,0],[1,2]),route([".....","##.##","....."],[2,0],[0,2])],"""    def cross(a, b):
        return ['RIGHT' if b >= a else 'LEFT'] * abs(b-a)
    gap = grid[1].index('.')
    return cross(start[0], gap) + ['DOWN', 'DOWN'] + cross(gap, goal[0])""",True)
lesson(4,"Break the pressure cycle","Mica recovered the pressure log. The Scheduler keeps cycling the pump; install an interlock before the line bursts.","Return 'VENT' for pressure >= 80, else 'PUMP' for moisture < 30, else 'HOLD'. A missing reading must return 'HOLD'.","Check for missing keys before using them. Put the emergency condition first so pressure always takes priority over irrigation.","interlock({'pressure': 82, 'moisture': 10}) -> 'VENT'","interlock(readings)","Check both keys, then pressure, then moisture. Return HOLD if no action is needed.",[case([{"pressure":88,"moisture":4}],"VENT"),case([{"pressure":80,"moisture":30}],"VENT"),case([{"pressure":79,"moisture":29}],"PUMP"),case([{"pressure":10,"moisture":30}],"HOLD"),case([{}],"HOLD"),case([{"pressure":84}],"HOLD")],"""    if 'pressure' not in readings or 'moisture' not in readings:
        return 'HOLD'
    if readings['pressure'] >= 80:
        return 'VENT'
    return 'PUMP' if readings['moisture'] < 30 else 'HOLD'""")
w,h=48,18
grid=[["#" if x in (0,w-1) or y in (0,h-1) else "." for x in range(w)] for y in range(h)]
gates=[]
for n,x in enumerate((12,24,36),1):
    for y in range(1,h-1): grid[y][x]="#"
    grid[9][x]="."
    gates.append(dict(id=f"relay_hydro_{n:02}",x=x*32,y=288,requires_challenge=f"hydro_{n:02}"))
for x in (3,6,16,19,28,31,40,43):
    for y in (2,3,14,15): grid[y][x]="#"
write("sectors","hydro",dict(id="hydro",width=w,height=h,tile_size=32,tiles=["".join(r) for r in grid],spawn=dict(x=96,y=280),gates=gates,interactables=[dict(type="terminal",x=(x*32+16),y=272,challenge_id=f"hydro_{n:02}") for n,x in enumerate((6,17,29,40),1)],exit=dict(x=88,y=392,to_zone="orientation"),sites=[dict(type="mara",x=146,y=338),dict(type="log",x=1440,y=113)],beds=[[484,160],[564,160],[484,390],[564,390]],boards={"hydro_01":[116,147],"hydro_03":[846,133]}))

