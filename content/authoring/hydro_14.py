def first_surge(readings, limit):
    streak = 0
    for i, n in enumerate(readings):
        streak = streak + 1 if n >= limit else 0
        if streak == 3:
            return i - 2
    return -1
