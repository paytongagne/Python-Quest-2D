"""Render-safe expedition outputs, independently checked in worker and game."""

import math


def primitive(value, depth=0):
    if depth > 8:
        return False
    if type(value) in (str, int, float, bool, type(None)):
        return len(str(value)) < 1000 and (type(value) is not float or math.isfinite(value))
    if type(value) is list:
        return len(value) <= 512 and all(primitive(v, depth + 1) for v in value)
    if type(value) is dict:
        return len(value) <= 128 and all(
            type(k) is str and primitive(v, depth + 1) for k, v in value.items()
        )
    return False


def same(a, b):
    if type(b) in (int, float):
        return type(a) in (int, float) and abs(a - b) < 1e-9
    if type(a) is not type(b):
        return False
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if type(b) is dict:
        return a.keys() == b.keys() and all(same(a[k], v) for k, v in b.items())
    return a == b


def validate(ch, case, result):
    if not primitive(result):
        raise ValueError(
            "Return bounded JSON values: lists, dictionaries, strings or finite numbers."
        )
    if ch.get("output") == "path":
        grid, start, goal = case["args"][:3]
        if type(result) is not list or not result or len(result) > 128:
            raise ValueError("Return up to 128 [x,y] coordinates including start and goal.")
        if result[0] != start or result[-1] != goal:
            raise ValueError(f"Path must start at {start} and end at {goal}.")
        cost = 0
        for i, point in enumerate(result):
            if type(point) is not list or len(point) != 2 or any(type(v) is not int for v in point):
                raise ValueError(f"Step {i}: expected [integer x, integer y].")
            x, y = point
            if (
                not (0 <= y < len(grid) and 0 <= x < len(grid[y]))
                or grid[y][x] == "#"
                or grid[y][x] == -1
            ):
                raise ValueError(f"Step {i}: {point} is blocked or outside the map.")
            if i:
                px, py = result[i - 1]
                if abs(x - px) + abs(y - py) != 1:
                    raise ValueError(
                        f"Step {i}: move one cardinal cell, from {result[i - 1]} to {point}."
                    )
                cost += grid[y][x] if type(grid[y][x]) is int else 1
        if cost != case["cost"]:
            raise ValueError(f"Path cost is {cost}; optimal cost is {case['cost']}.")
        return result
    if not same(result, case["expected"]):
        raise ValueError(f"Expected {case['expected']!r}; got {result!r}")
    return result
