"""Author the filtration, reservoir and canopy sectors of the Greenline."""
from pathlib import Path
import json
base=Path(__file__).resolve().parents[1]/"content"
mapfile=base/"sectors/hydro.json"
m=json.loads(mapfile.read_text())
m["sectors"]=["Nursery","Filtration works","Reservoir","Canopy control"]
m["bay_names"]=["Dispatch rail","Seed bank","Logger vault","Pump gallery","Intake","Clarifier","Return pipe","Membrane rack","Culture lab","Manifold","Carrier rail","Valve bank","Event recorder","Watch station","Recovery rail","Canopy core"]
def mission(n,title,story,lesson,objective,sample,sig,hint,fixtures,body,robot=False):
    key=f"hydro_{n:02}"
    ch=dict(id=key,zone="hydro",sequence=n,kind="function",title=title,story=story,lesson=lesson,objective=objective,sample=sample,function_name=sig.split("(")[0],starter_code="def "+sig+":\n    pass\n",hint=hint,world_effect="relay_"+key)
    if robot:
        ch.update(simulation="route",cases=[dict(args=f) for f in fixtures])
    else:
        ch.update(simulation="instrument",cases=[dict(args=a,expected=e) for a,e in fixtures])
    (base/"expansion"/(key+".json")).write_text(json.dumps(ch,indent=2)+"\n",encoding="utf-8")
    (base/"authoring"/(key+".py")).write_text("def "+sig+":\n"+body+"\n",encoding="utf-8")
mission(5,"Clean the intake tags","Water shipments arrived with mismatched labels. Standardize the labels on the intake reader.","strip removes surrounding whitespace. upper changes letter case. Skip empty labels after cleaning.","Return nonempty tags in uppercase, preserving order and duplicates.","['  lo ', '', 'Hi'] -> ['LO', 'HI']","clean_tags(tags)","Try a loop. Store tag.strip().upper() before checking whether to append it.",[([[" ph "," saline","  ","ph"]],["PH","SALINE","PH"]),([[]],[]),([[" ","\t"," A b "]],["A B"])],"    return [tag.strip().upper() for tag in tags if tag.strip()]")
mission(6,"Catch the sediment","The clarifier needs a histogram of grain sizes to choose its filter mesh.","Count observations in a dictionary. Use get(key, 0) when you have not seen a label before.","Return counts for every label in the input. Return {} for an empty batch.","['fine','fine','coarse'] -> {'fine': 2, 'coarse': 1}","grain_counts(labels)","Initialize an empty dict; increment counts[label] from its current value.",[([["fine","silt","fine","coarse"]],{"fine":2,"silt":1,"coarse":1}),([[]],{}),([["silt"]*3],{"silt":3})],"""    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts""")
mission(7,"Climb the return pipe","Mica is below the rail switch. Lift the filter cartridge vertically, then traverse the top service rail.","Break a plan into two lists of moves. Use abs for distance and choose a direction from the sign.","Return UP to reach row zero, then LEFT or RIGHT to the goal. Coordinates are [x,y].","start=[1,2], goal=[3,0] -> UP, UP, RIGHT, RIGHT","plan_route(grid, start, goal)","Start with ['UP'] * start[1]. Use goal[0] - start[0] for the horizontal leg.",[[["....","#.##","#.##"],[1,2],[3,0]],[[".....","###.#"],[3,1],[0,0]],[["..."],[1,0],[1,0]]],"""    dx = goal[0] - start[0]
    return ['UP'] * start[1] + ['RIGHT' if dx >= 0 else 'LEFT'] * abs(dx)""",True)
mission(8,"Balance the membranes","Dirty water is backing up. Allocate a finite rinse supply across filters in order.","At each filter, take the smaller of its request and your remaining supply. Update the supply after each allocation.","Return an allocation for each nonnegative request. Never allocate more than available.","[3,5,2], supply=6 -> [3,3,0]","allocate(requests, supply)","Use min(request, supply) and subtract the allocation before the next iteration.",[([[3,5,2],6],[3,3,0]),([[0,4],0],[0,0]),([[],8],[]),([[2,3],9],[2,3])],"""    out = []
    for amount in requests:
        used = min(amount, supply)
        out.append(used)
        supply -= used
    return out""")
mission(9,"Decode the cultures","Culture tubes carry a species and volume separated by a colon. A cracked label must be quarantined.","split(':') separates the two fields. Check their count before converting the volume with int.","Return [species, volume] for NAME:integer (trim fields, nonempty name, nonnegative volume). Return None for malformed labels.","' fern : 7 ' -> ['fern', 7]","decode_tube(label)","Use try/except ValueError around int. Check the number of fields and volume >= 0.",[([' fern : 7 '],['fern',7]),([':3'],None),(['fern:bad'],None),(['moss:-1'],None),(['a:b:3'],None),(['moss:0'],['moss',0])],"""    parts = label.split(':')
    if len(parts) != 2 or not parts[0].strip():
        return None
    try:
        volume = int(parts[1])
    except ValueError:
        return None
    return [parts[0].strip(), volume] if volume >= 0 else None""")
mission(10,"Reconcile the manifold","Two manifolds report water usage for overlapping crop beds. Combine their meters without losing a bed.","Start with a copy of one mapping. Add the second mapping's values to the matching totals.","Return a new dictionary with the sum per bed across both mappings.","{'A': 3} and {'A': 2,'B': 1} -> {'A': 5,'B': 1}","merge_meters(left, right)","Loop through right.items(). Add each value to totals.get(bed, 0).",[([{'A':3},{'A':2,'B':1}],{'A':5,'B':1}),([{},{}],{}),([{'C':7},{}],{'C':7}),([{}, {'D':0}],{'D':0})],"""    total = dict(left)
    for key, value in right.items():
        total[key] = total.get(key, 0) + value
    return total""")
mission(11,"Cross the carrier rail","A contamination screen divides the reservoir. Mica must pass through its only opening to deliver a test vial.","Inspect each row in the barrier column. Move vertically on the left, cross horizontally, then align with the dock on the right.","The barrier is column 2. Use its open row. Return a legal route from the left side to the right side.","'.' = traversable, '#' = wall; grid[y][x]","plan_route(grid, start, goal)","Find the y where grid[y][2] == '.'. Vertical legs may go either way.",[[["..#..",".....","..#.."],[0,2],[4,0]],[[".....","..#..","..#.."],[1,1],[3,2]],[["..#..","..#..","....."],[0,0],[4,2]]],"""    gap = next(y for y, row in enumerate(grid) if row[2] == '.')
    def vertical(a,b):
        return ['DOWN' if b >= a else 'UP'] * abs(b-a)
    return vertical(start[1],gap) + ['RIGHT']*(goal[0]-start[0]) + vertical(gap,goal[1])""",True)
mission(12,"Latch the valve bank","A valve chatters when temperature hovers near its threshold. Install a controller with memory.","Hysteresis uses two thresholds. Readings between them preserve the previous state.","Starting closed, open at >=70, close at <=50. Return a list of booleans, one per reading.","[70,60,50] -> [True,True,False]","valve_trace(temps)","Keep an opened variable between iterations; append it after handling both thresholds.",[([[40,70,60,50,65]],[False,True,True,False,False]),([[]],[]),([[60,71,69]],[False,True,True]),([[70,50]],[True,False])],"""    opened = False
    trace = []
    for t in temps:
        if t >= 70:
            opened = True
        elif t <= 50:
            opened = False
        trace.append(opened)
    return trace""")
mission(13,"Rebuild the event tape","The canopy recorder repeats consecutive events. Recover the duration of each uninterrupted state.","Run-length encoding groups adjacent equal values. Equal values separated by another state start new groups.","Return [event, count] pairs for consecutive runs.","['A','A','B','A'] -> [['A',2],['B',1],['A',1]]","pack_events(events)","If the last pair has the same label, increment its count. Otherwise append a new pair.",[([['P','P','V','P']],[['P',2],['V',1],['P',1]]),([[]],[]),([['H','H','H']],[['H',3]])],"""    runs = []
    for event in events:
        if runs and runs[-1][0] == event:
            runs[-1][1] += 1
        else:
            runs.append([event,1])
    return runs""")
mission(14,"Find the first surge","The scheduler erases isolated faults. Locate the first sustained pressure surge in its trace.","A running counter measures consecutive high readings. Reset it when a reading drops below the threshold.","Return the starting index of the first run of 3 readings >= limit. Return -1 if absent.","[9,2,8,9,8], limit=8 -> 2","first_surge(readings, limit)","At the third high, the run started two positions earlier.",[([[9,2,8,9,8],8],2),([[8,8,8],8],0),([[8,1,8,8],8],-1),([[],4],-1)],"""    streak = 0
    for i, n in enumerate(readings):
        streak = streak + 1 if n >= limit else 0
        if streak == 3:
            return i - 2
    return -1""")
mission(15,"Rescue the canopy relay","Recovery phase one. Mica has one final delivery through a branching rail maze. Find any path to the canopy dock.","Breadth-first search explores adjacent cells with a queue. Store each candidate's path. Track visited coordinates so a cycle cannot trap the rover.","Return legal moves from start to goal through each reachable grid. A zero-length trip returns [].","Moves: UP, DOWN, LEFT, RIGHT. grid[y][x] == '#' blocks a cell.","plan_route(grid, start, goal)","Queue (position,path); for each valid unseen neighbor, append its direction to the path.",[[["..#..",".#...","...#.","##..."],[0,0],[4,0]],[["....",".##.","...."],[3,2],[0,0]],[[".."],[1,0],[1,0]],[[".#.","...",".#."],[0,2],[2,2]]],"""    from collections import deque
    queue = deque([(tuple(start), [])])
    seen = {tuple(start)}
    while queue:
        (x,y), path = queue.popleft()
        if [x,y] == goal:
            return path
        for name,dx,dy in [('UP',0,-1),('DOWN',0,1),('LEFT',-1,0),('RIGHT',1,0)]:
            pos = x+dx, y+dy
            a,b = pos
            if 0 <= b < len(grid) and 0 <= a < len(grid[b]) and grid[b][a] != '#' and pos not in seen:
                seen.add(pos)
                queue.append((pos,path+[name]))
    return []""",True)
mission(16,"Restart the canopy","Recovery phase two. The relay is installed. Replay the scheduler tape and emit safe commands to restore the canopy.","A fault latches the system offline until RESET. A reset emits HOLD. Dry and wet readings control water only while online.","FAULT -> VENT and latch. RESET -> HOLD and clear latch. While latched emit HOLD for other events. Otherwise DRY -> PUMP; all others -> HOLD.","['FAULT','DRY','RESET','DRY'] -> ['VENT','HOLD','HOLD','PUMP']","recover(events)","Maintain a latched flag. Handle FAULT and RESET before evaluating DRY.",[([['DRY','FAULT','DRY','RESET','DRY','WET']],['PUMP','VENT','HOLD','HOLD','PUMP','HOLD']),([[]],[]),([['FAULT','FAULT','WET']],['VENT','VENT','HOLD']),([['RESET','UNKNOWN','DRY']],['HOLD','HOLD','PUMP'])],"""    latched = False
    actions = []
    for e in events:
        if e == 'FAULT':
            latched = True
            action = 'VENT'
        elif e == 'RESET':
            latched = False
            action = 'HOLD'
        elif not latched and e == 'DRY':
            action = 'PUMP'
        else:
            action = 'HOLD'
        actions.append(action)
    return actions""")
# Extend east from the initial gallery without moving any existing object.
w,h=192,18
rows=[list(r[:-1]+'.'*(w-48)+'#') for r in m["tiles"]]
rows[0]=list("#"*w)
rows[-1]=list("#"*w)
for n in range(4,16):
    x=n*12 if n>4 else 47
    y=(5,9,12)[n%3]
    for r in range(1,17): rows[r][x]='#'
    rows[y][x]='.'
    m["gates"].append(dict(id=f"relay_hydro_{n:02}",x=x*32,y=y*32,requires_challenge=f"hydro_{n:02}"))
    key=f"hydro_{n+1:02}"
    t=dict(type="terminal",x=(n*12+5)*32+16,y=(8 if n%2==0 else 10)*32+16,challenge_id=key)
    m["interactables"].append(t)
    if n+1 in (7,11,15): m["boards"][key]=[n*384+113,138]
    for cy in (3,14):
        for cx in range(2+(n%2),8,2):
            rows[cy][n*12+cx]='#'
m.update(width=w,tiles=[''.join(row) for row in rows])
mapfile.write_text(json.dumps(m,indent=2)+"\n")

