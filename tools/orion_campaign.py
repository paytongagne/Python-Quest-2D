from pathlib import Path
import json
# Reuse authoring helpers without running their content generation again.
namespace={"__file__":str(Path(__file__).with_name("author_expeditions.py"))}
source=Path(__file__).with_name("author_expeditions.py").read_text()
exec(source[:source.index('task("orion_moon",1')],namespace)
task,case,path,ROOT,put=[namespace[k] for k in ("task","case","path","ROOT","put")]
def add(n,title,story,lesson,obj,sample,sig,hint,cases,body,output="model"):
    task("orion_moon",n,title,story,lesson,obj,sample,sig,hint,cases,body,output)
# BFS fixture body is reused only as an explicit authoring reference for optimal paths.
bfs=(ROOT/"authoring/orion_moon_02.py").read_text().split("\n",1)[1].rstrip()
astar="""    import heapq
    heap=[(abs(start[0]-goal[0])+abs(start[1]-goal[1]),0,tuple(start),[start])]
    best={tuple(start):0}
    while heap:
        _,cost,(x,y),route=heapq.heappop(heap)
        if cost!=best[(x,y)]:
            continue
        if [x,y]==goal:
            return route
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            a,b=x+dx,y+dy
            if 0<=b<len(grid) and 0<=a<len(grid[b]) and grid[b][a]!='#':
                nxt=cost+1
                if nxt<best.get((a,b),float('inf')):
                    best[(a,b)]=nxt
                    heuristic=abs(a-goal[0])+abs(b-goal[1])
                    heapq.heappush(heap,(nxt+heuristic,nxt,(a,b),route+[[a,b]]))
    return []"""
add(5,"Predict a Smart Route","Mica's radio link can carry only a few search updates. Guide it toward the ice beacon.","A* prioritizes cost so far plus an admissible estimate. Manhattan distance never overestimates on a four-way unit-cost grid.","Return a shortest path of [x,y] cells including endpoints. Use a heap with Manhattan distance to practice A*. '#' blocks a cell.","Estimate from [1,2] to [4,4] is 5.","smart_route(grid, start, goal)","Heap entries can contain f, g, cell and path. Update the best g before pushing.",[
path(["...#..",".#....","...#..","......"],[0,0],[5,0],7),
path(["..."],[2,0],[0,0],2),path(["."],[0,0],[0,0],0)],astar,"path")
add(6,"Schedule Relay Maintenance","Repair drones need a stable dispatch order when two relays share a severity.","Sort by negative severity for descending priority, then by arrival for ascending time. Python's stable sort preserves input order on ties.","Jobs have id, severity and arrival. Return IDs sorted by highest severity, earliest arrival, then original order.","severity 9 leaves before severity 2.","service_order(jobs)","sorted(jobs, key=lambda j: (-j['severity'],j['arrival'])) preserves exact ties.",[
case([[{"id":"A","severity":2,"arrival":1},{"id":"B","severity":9,"arrival":4},{"id":"C","severity":9,"arrival":2}]],["C","B","A"]),
case([[]],[]),case([[{"id":"A","severity":1,"arrival":0},{"id":"B","severity":1,"arrival":0}]],["A","B"])],"""    return [j['id'] for j in sorted(jobs,key=lambda j:(-j['severity'],j['arrival']))]""")
add(7,"Signal Lost","A tunnel has collapsed. The dispatcher must report failure instead of inventing a route.","A search exhausts its frontier when there is no connection. A distinct failure result keeps downstream code from moving a rover.","Return True if a cardinal route exists between start and goal, otherwise False. '#' blocks movement.","['.#.'] from [0,0] to [2,0] -> False","can_reach(grid, start, goal)","Use a stack or queue with a visited set. Exhaustion means False.",[
case([[".#."],[0,0],[2,0]],False),case([["..."],[0,0],[2,0]],True),case([["."],[0,0],[0,0]],True),
case([["..#","##.","..."],[0,0],[2,2]],False)],"""    stack=[tuple(start)]
    seen=set(stack)
    while stack:
        x,y=stack.pop()
        if [x,y]==goal:
            return True
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            a,b=x+dx,y+dy
            if 0<=b<len(grid) and 0<=a<len(grid[b]) and grid[b][a]!='#' and (a,b) not in seen:
                seen.add((a,b))
                stack.append((a,b))
    return False""")
add(8,"Convert Moon Coordinates","A coordinate mismatch puts cargo beside its dock. Align rover-local and lunar-base frames.","A translation adds the origin to local coordinates. The inverse subtracts it. Keep the input list intact.","For each 2D point return point+origin, or point-origin when inverse is True.","points=[[1,2]], origin=[4,5], inverse=False -> [[5,7]]","change_frame(points, origin, inverse)","Choose a sign of -1 for inverse and +1 otherwise.",[
case([[[1,2],[-2,0]],[4,5],False],[[5,7],[2,5]]),case([[[5,7]],[4,5],True],[[1,2]]),case([[],[2,3],False],[])],"""    sign=-1 if inverse else 1
    return [[x+sign*origin[0],y+sign*origin[1]] for x,y in points]""")
add(9,"Avoid Precision Drift","Ridge sensors disagree by tiny fractions. Set an explicit tolerance policy.","Absolute tolerance compares the difference to a bound. Different vector lengths cannot be equal. Negative tolerances are invalid.","Return True only if lengths match, tolerance >=0 and every coordinate difference <= tolerance.","[1,2] vs [1.1,2], tolerance=.2 -> True","near_vector(a, b, tolerance)","Check shape first, then all(abs(x-y)<=tolerance).",[
case([[1,2],[1.1,2],.2],True),case([[0],[1],1],True),case([[1],[1,2],1],False),case([[],[],-1],False),case([[],[],0],True)],"""    return tolerance>=0 and len(a)==len(b) and all(abs(x-y)<=tolerance for x,y in zip(a,b))""")
add(10,"Prevent Rover Collision","Two rovers share a single service lane. Check their schedules before launch.","A conflict is a shared cell at a tick or an edge swap between ticks. After its final step, a rover stays at its last cell.","Return the first conflict tick, or -1. Both paths are nonempty. Include tick 0. Compare through the longer path.","[[0,0],[1,0]] and [[1,0],[0,0]] -> 1 (swap)","conflict_tick(a, b)","Extend each path by holding its final cell. Check equal positions and swapped previous positions.",[
case([[[0,0],[1,0]],[[1,0],[0,0]]],1),case([[[0,0]],[[2,0],[1,0],[0,0]]],2),
case([[[0,0]],[[0,0]]],0),case([[[0,0],[1,0]],[[0,1],[1,1]]],-1)],"""    for t in range(max(len(a),len(b))):
        x=a[min(t,len(a)-1)]
        y=b[min(t,len(b)-1)]
        if x==y:
            return t
        if t and x==b[min(t-1,len(b)-1)] and y==a[min(t-1,len(a)-1)]:
            return t
    return -1""")
add(11,"Reroute After a Landslide","A boulder now blocks yesterday's corridor. The displayed map includes the new obstruction.","Route planning must use the current obstacle map. An earlier valid path may now hit a wall.","Return a shortest path on the updated grid, including endpoints. '#' includes newly fallen rocks. All goals are reachable.","A blocked top aisle may require a lower detour.","reroute(grid, start, goal)","Run a fresh BFS on the supplied grid. Avoid caching a path across changed maps.",[
path([".#...","...#.","....."],[0,0],[4,0],8),
path(["..#","..."],[0,0],[2,1],3),path(["."],[0,0],[0,0],0)],bfs,"path")
add(12,"Keep Heuristics Honest","ION found a heuristic that promises a short route through a solid crater.","An admissible heuristic never exceeds the true remaining cost and never goes negative. Supplied distances are trusted fixtures.","Return sorted node IDs whose heuristic is negative, greater than its true distance, or missing. Ignore heuristic entries outside distances.","h={'A':4}, distances={'A':3,'B':0} -> ['A','B']","bad_heuristics(heuristic, distances)","Iterate the distance dictionary and test each estimate against [0, distance].",[
case([{"A":4},{"A":3,"B":0}],["A","B"]),case([{"A":0,"B":2},{"A":0,"B":3}],[]),case([{"A":-1},{"A":4}],["A"]),case([{},{}],[])],"""    return sorted(k for k,d in distances.items() if k not in heuristic or not 0<=heuristic[k]<=d)""")
add(13,"Cache Crater Distances","Convoy queries repeat. Reuse results without confusing two directions of a route.","Memoization stores a result by its inputs. For this undirected graph, a pair can be canonicalized as a sorted tuple.","Return {'distances': list, 'searches': number of distinct unordered pairs}. Distances count edges or -1 if unreachable.","Queries [['A','B'],['B','A']] need one search.","cached_distances(graph, queries)","Use BFS per new sorted pair. Store -1 too so impossible routes are cached.",[
case([{"A":["B"],"B":["A","C"],"C":["B"],"D":[]},[["A","C"],["C","A"],["A","D"],["A","A"]]],{"distances":[2,2,-1,0],"searches":3}),
case([{},[]],{"distances":[],"searches":0}),case([{"X":[]},[["X","X"],["X","X"]]],{"distances":[0,0],"searches":1})],"""    from collections import deque
    cache={}
    values=[]
    for start,goal in queries:
        key=tuple(sorted((start,goal)))
        if key not in cache:
            queue=deque([(start,0)])
            seen={start}
            distance=-1
            while queue:
                node,d=queue.popleft()
                if node==goal:
                    distance=d
                    break
                for nxt in graph.get(node,[]):
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt,d+1))
            cache[key]=distance
        values.append(cache[key])
    return {'distances':values,'searches':len(cache)}""")
add(14,"Restore Relay Dependencies","Convoy phase one. Power, radio and launch services must start in dependency order.","Topological sorting repeatedly chooses a node with no remaining prerequisites. A cycle leaves no eligible node.","Input maps each service to its prerequisite list. Return lexicographically smallest available service at each step, or [] if cyclic. All prerequisites are named services.","{'radio':['power'],'power':[]} -> ['power','radio']","repair_order(dependencies)","Keep a completed set. Sort the services whose prerequisites are all completed.",[
case([{"radio":["power"],"power":[],"launch":["radio"],"scan":["power"]}],["power","radio","launch","scan"]),
case([{"A":["B"],"B":["A"]}],[]),case([{}],[]),case([{"Z":[],"A":[]}],["A","Z"])],"""    done=[]
    while len(done)<len(dependencies):
        ready=sorted(k for k,v in dependencies.items() if k not in done and all(p in done for p in v))
        if not ready:
            return []
        done.append(ready[0])
    return done""")
add(15,"Benchmark Rover Strategies","Convoy phase two. Compare deterministic work counts before choosing a search strategy.","Count modeled operations instead of wall-clock time. A sparse BFS model touches V vertices and E edges; a repeated full scan costs V squared.","For each [vertices, edges] return {'bfs': V+E, 'scan': V*V, 'winner': 'bfs'/'scan'/'tie'}. Inputs are nonnegative.","[4,3] -> bfs=7, scan=16, winner='bfs'","work_counts(sizes)","Compute both counts and compare. These are stated workload models, not timing measurements.",[
case([[[4,3],[1,0],[0,0],[2,5]]],[{"bfs":7,"scan":16,"winner":"bfs"},{"bfs":1,"scan":1,"winner":"tie"},{"bfs":0,"scan":0,"winner":"tie"},{"bfs":7,"scan":4,"winner":"scan"}]),
case([[]],[])],"""    result=[]
    for v,e in sizes:
        fast=v+e
        slow=v*v
        result.append({'bfs':fast,'scan':slow,'winner':'bfs' if fast<slow else 'scan' if slow<fast else 'tie'})
    return result""")
# Final phase two deliveries share identical terrain, so reuse the path validator separately.
add(16,"Boss: Rescue the Moon Convoy","Convoy phase three. Deliver the cargo rover through the reopened corridor after the support relays come online.","The rescue keeps each prior repair as a checkpoint. A minimum-cost route conserves the convoy's shared shield reserve.","Return the least-cost cargo path including endpoints. Cell values are traversal costs; -1 blocks a cell. Start costs zero.","The escort follows the cleared path one step behind cargo.","rescue_convoy(grid, start, goal)","Use the weighted route algorithm from the ridge. Compare alternative detours before committing.",[
path([[1,8,8,1,1],[1,-1,1,1,1],[1,1,1,-1,1],[5,5,1,1,1]],[0,0],[4,0],8),
path([[1,5,1],[1,1,1]],[0,0],[2,0],4),path([[1]],[0,0],[0,0],0)],
(ROOT/"authoring/orion_moon_04.py").read_text().split("\n",1)[1].rstrip(),"path")
m=json.loads((ROOT/"planets/orion_moon.json").read_text())
w,h=80,48
grid=[['#' if x in (0,w-1) or y in (0,h-1) else '.' for x in range(w)] for y in range(h)]
for y in range(1,h-1):grid[y][39]='#'
for x in range(1,w-1):grid[24][x]='#'
gates=[]
for n,(x,y) in zip((4,8,12),[(39,12),(60,24),(39,36)]):
    grid[y][x]='.'
    gates.append(dict(id=f"relay_orion_moon_{n:02}",x=x*32,y=y*32,requires_challenge=f"orion_moon_{n:02}"))
terms=[]
for sector,(ox,oy) in enumerate([(0,0),(40,0),(40,24),(0,24)]):
    for j,(x,y) in enumerate([(8,10),(28,10),(28,21),(8,21)]):
        n=sector*4+j+1
        terms.append(dict(type="terminal",challenge_id=f"orion_moon_{n:02}",x=(ox+x)*32+16,y=(oy+y)*32+16))
    for cx,cy,r in [(ox+18,oy+5,3),(ox+19,oy+17,3)]:
        for y in range(cy-r,cy+r+1):
            for x in range(cx-r,cx+r+1):
                if (x-cx)**2+(y-cy)**2<=r*r:grid[y][x]='#'
m.update(width=w,height=h,tiles=[''.join(r) for r in grid],interactables=terms,gates=gates)
m["sites"][1].update(x=1120,y=1376)
put("planets","orion_moon",m)


