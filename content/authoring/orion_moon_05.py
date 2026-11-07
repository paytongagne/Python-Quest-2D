def smart_route(grid, start, goal):
    import heapq
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
    return []
