"""Pure route contract, checked independently on both sides of the worker boundary."""

MOVES = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


def trace(args, commands):
    grid, start, goal = args
    if type(commands) is not list or len(commands) > 64:
        raise ValueError("Return a list of at most 64 movement commands.")
    x, y = start
    path = [(x, y)]
    for i, step in enumerate(commands, 1):
        if type(step) is not str or step not in MOVES:
            raise ValueError(f"Step {i}: use UP, DOWN, LEFT or RIGHT.")
        dx, dy = MOVES[step]
        x += dx
        y += dy
        if not (0 <= y < len(grid) and 0 <= x < len(grid[y])):
            raise ValueError(f"Step {i}: {step} leaves the grid at ({x}, {y}).")
        if grid[y][x] == "#":
            raise ValueError(f"Step {i}: obstruction at ({x}, {y}).")
        path.append((x, y))
    if (x, y) != tuple(goal):
        raise ValueError(f"Rover stopped at ({x}, {y}); goal is {goal}.")
    return path
