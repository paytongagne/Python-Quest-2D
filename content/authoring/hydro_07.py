def plan_route(grid, start, goal):
    dx = goal[0] - start[0]
    return ['UP'] * start[1] + ['RIGHT' if dx >= 0 else 'LEFT'] * abs(dx)
