def plan_route(grid, start, goal):
    from collections import deque
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
    return []
