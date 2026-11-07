def plan_route(grid, start, goal):
    gap = next(y for y, row in enumerate(grid) if row[2] == '.')
    def vertical(a,b):
        return ['DOWN' if b >= a else 'UP'] * abs(b-a)
    return vertical(start[1],gap) + ['RIGHT']*(goal[0]-start[0]) + vertical(gap,goal[1])
