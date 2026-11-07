"""Executable fixtures and original environments for expedition release."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]/"content"
def put(group,key,value):
    (ROOT/group).mkdir(exist_ok=True)
    (ROOT/group/(key+".json")).write_text(json.dumps(value,indent=2)+"\n",encoding="utf-8")
def task(zone,num,title,story,lesson,objective,sample,signature,hint,cases,body,output="model"):
    key=f"{zone}_{num:02}"
    ch=dict(id=key,kind="function",zone=zone,sequence=num,title=title,story=story,lesson=lesson,objective=objective,sample=sample,function_name=signature.split("(")[0],starter_code="def "+signature+":\n    pass\n",hint=hint,cases=cases,world_effect="relay_"+key,simulation="expedition",output=output)
    put("expeditions",key,ch)
    (ROOT/"authoring"/(key+".py")).write_text("def "+signature+":\n"+body+"\n",encoding="utf-8")
def case(args,expected): return dict(args=args,expected=expected)
def path(grid,start,goal,cost): return dict(args=[grid,start,goal],cost=cost)

task("orion_moon",1,"Mark the Lunar Relay Grid","ION: Lunar dust cut the relay network. Rebuild the graph before we move the convoy.","An adjacency dictionary maps each node to its neighbors. An undirected edge is stored in both directions. Sets remove duplicates.","Return every named node mapped to its sorted neighbors. Ignore edges containing unknown nodes and self-edges. Preserve isolated nodes.","nodes=['A','B'], edges=[['A','B']] -> {'A':['B'],'B':['A']}","relay_graph(nodes, edges)","Initialize a set for each node, add both ends of valid edges, then sort each set.",[
case([["A","B","C","D"],[["A","B"],["B","C"],["A","D"]]],{"A":["B","D"],"B":["A","C"],"C":["B"],"D":["A"]}),
case([["X","Y"],[["X","X"],["X","Z"],["Y","X"],["X","Y"]]],{"X":["Y"],"Y":["X"]}),
case([[],[]],{}),case([["A"],[]],{"A":[]})],"""    graph = {node: set() for node in nodes}
    for a,b in edges:
        if a in graph and b in graph and a != b:
            graph[a].add(b)
            graph[b].add(a)
    return {key: sorted(value) for key,value in graph.items()}""")
bfs="""    from collections import deque
    queue = deque([(start,[start])])
    seen = {tuple(start)}
    while queue:
        (x,y), route = queue.popleft()
        if [x,y] == goal:
            return route
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            a,b=x+dx,y+dy
            if 0<=b<len(grid) and 0<=a<len(grid[b]) and grid[b][a]!='#' and (a,b) not in seen:
                seen.add((a,b))
                queue.append(([a,b],route+[[a,b]]))
    return []"""
task("orion_moon",2,"Find Mica a Safe Route","Mica carries the relay battery. The crater rim blocks a direct crossing.","BFS uses a queue. Mark neighbors as seen when queued, and retain the path to each cell. Equal-cost steps make the first goal path shortest.","Return a shortest list of [x,y] cells including start and goal. '#' is blocked. All fixtures have a reachable goal.","[[0,0],[1,0],[1,1]] is two moves. grid[y][x] addresses the terrain.","shortest_route(grid, start, goal)","Queue (cell,path). Append each unseen open neighbor with path + [neighbor].",[
path([".....",".###.","...#.","....."],[0,0],[4,3],7),path(["..",".."],[0,0],[1,1],2),path(["."],[0,0],[0,0],0),path([".#.","..."],[0,0],[2,0],4)],bfs,"path")
task("orion_moon",3,"Survey the Ice Tunnels","The ice has split the tunnel network into pockets. Survey every pocket before restoring radio coverage.","DFS visits one connected region with a stack. After draining it, find the next unvisited open cell. Count the size of each region.","Return sizes of all cardinally connected '.' regions, sorted largest first. '#' cells are blocked.","['.#.','.#.'] -> [2,2]","survey_regions(grid)","Maintain visited across all searches. Start a new stack at every unseen '.'.",[
case([["..#..",".##..","..###","#####","...#."]],[5,4,3,1]),
case([[]],[]),case([["###"]],[]),case([["...","..."]],[6]),case([[".#.",".#."]],[2,2])],"""    seen = set()
    sizes = []
    for y,row in enumerate(grid):
        for x,tile in enumerate(row):
            if tile != '.' or (x,y) in seen:
                continue
            stack = [(x,y)]
            seen.add((x,y))
            count = 0
            while stack:
                a,b = stack.pop()
                count += 1
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    c,d = a+dx,b+dy
                    if 0<=d<len(grid) and 0<=c<len(grid[d]) and grid[d][c]=='.' and (c,d) not in seen:
                        seen.add((c,d))
                        stack.append((c,d))
            sizes.append(count)
    return sorted(sizes,reverse=True)""")
dijkstra="""    import heapq
    heap = [(0, tuple(start), [start])]
    best = {tuple(start): 0}
    while heap:
        cost,(x,y),route = heapq.heappop(heap)
        if cost != best[(x,y)]:
            continue
        if [x,y] == goal:
            return route
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            a,b=x+dx,y+dy
            if 0<=b<len(grid) and 0<=a<len(grid[b]) and grid[b][a]>=0:
                nxt = cost + grid[b][a]
                if nxt < best.get((a,b),float('inf')):
                    best[(a,b)] = nxt
                    heapq.heappush(heap,(nxt,(a,b),route+[[a,b]]))
    return []"""
task("orion_moon",4,"Route Around High Radiation","The ridge is open, but radiation makes the direct route costly. Deliver the shield module using the cheapest safe route.","Dijkstra explores the lowest cumulative cost first using a heap. Update a cell only when its new cost improves the best known value.","Return a minimum-cost list of [x,y] cells including both endpoints. Entering a cell costs its nonnegative value. -1 is blocked. Start cost is zero.","[[1,9,1],[1,1,1]] from [0,0] to [2,0] costs 4 via the bottom row.","least_cost(grid, start, goal)","Heap entries hold total cost, cell and path. Skip outdated entries after popping.",[
path([[1,8,8,1,1],[1,1,1,1,1],[9,9,-1,2,1]],[0,0],[4,0],6),
path([[1,9,1],[1,1,1]],[0,0],[2,0],4),path([[0]],[0,0],[0,0],0),
path([[1,-1,1],[2,2,1]],[0,0],[2,0],6)],dijkstra,"path")
# Five destinations are represented by playable locations. Preview travel remains explicitly marked.
manifest=[
dict(id="astra",zone="orientation",name="Astra Research Facility",color="#73dbcc",requires=None,tag="HOME / 40 missions"),
dict(id="orion",zone="orion_moon",name="Orion Relay Moon",color="#bdadff",requires="mission_control_16",tag="CRATER EXPEDITION"),
dict(id="titan",zone="titan_cloud",name="Titan Cloudworks",color="#ffc68a",requires="orion_moon_16",tag="INGRESS EXPEDITION"),
dict(id="helix",zone="helix_bio",name="Helix Biomedical Campus",color="#85e5cf",requires="titan_cloud_16",tag="ACQUISITION EXPEDITION"),
dict(id="aurora",zone="aurora_ep",name="Aurora Mapping Observatory",color="#ef9acb",requires="helix_bio_16",tag="NAVIGATION EXPEDITION")]
put("universe","destinations",manifest)

def terrain(zone,count):
    w,h=(64,36) if zone=="orion_moon" else (34,24)
    grid=[["#" if x in (0,w-1) or y in (0,h-1) else "." for x in range(w)] for y in range(h)]
    terms=[]
    if count==4:
        for n,(x,y) in enumerate([(8,10),(38,9),(40,27),(9,27)],1):
            terms.append(dict(id=f"{zone}_{n:02}",type="terminal",challenge_id=f"{zone}_{n:02}",x=x*32+16,y=y*32+16))
        # Only one pass between each region, preserving a winding clockwise journey.
        for y in range(1,h-1): grid[y][31]="#"
        for x in range(1,w-1): grid[18][x]="#"
        holes=[(31,10),(43,18),(31,27)]
        gates=[]
        for n,(x,y) in enumerate(holes,1):
            grid[y][x]="."
            gates.append(dict(id=f"relay_{zone}_{n:02}",x=x*32,y=y*32,requires_challenge=f"{zone}_{n:02}"))
        # Crater rims remain physical obstacles with visible shaded terrain.
        for cx,cy,r in [(20,6,3),(53,10,4),(52,28,3),(18,27,3)]:
            for y in range(cy-r,cy+r+1):
                for x in range(cx-r,cx+r+1):
                    if (x-cx)**2+(y-cy)**2<=r*r:
                        grid[y][x]="#"
    else:
        terms=[dict(type="terminal",challenge_id=f"{zone}_01",x=400,y=320)]
        gates=[]
        for x in (18,23,28):
            for y in range(6,13): grid[y][x]="#"
    put("planets",zone,dict(id=zone,width=w,height=h,tile_size=32,tiles=["".join(r) for r in grid],spawn=dict(x=110,y=280),interactables=terms,gates=gates,exit=dict(type="shuttle",x=110,y=380),sites=[dict(type="scientist",x=193,y=352),dict(type="relic",x=(w-5)*32,y=(h-4)*32)]))
terrain("orion_moon",4)
for z in ("titan_cloud","helix_bio","aurora_ep"): terrain(z,1)

