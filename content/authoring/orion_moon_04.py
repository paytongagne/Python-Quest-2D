def least_cost(grid, start, goal):
    import heapq
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
    return []
