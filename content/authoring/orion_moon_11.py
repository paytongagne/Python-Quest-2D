def reroute(grid, start, goal):
    from collections import deque
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
    return []
