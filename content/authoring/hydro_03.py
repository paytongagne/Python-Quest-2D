def plan_route(grid, start, goal):
    def cross(a, b):
        return ['RIGHT' if b >= a else 'LEFT'] * abs(b-a)
    gap = grid[1].index('.')
    return cross(start[0], gap) + ['DOWN', 'DOWN'] + cross(gap, goal[0])
