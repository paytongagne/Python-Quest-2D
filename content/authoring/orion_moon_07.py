def can_reach(grid, start, goal):
    stack=[tuple(start)]
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
    return False
