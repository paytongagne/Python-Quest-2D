def survey_regions(grid):
    seen = set()
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
    return sorted(sizes,reverse=True)
