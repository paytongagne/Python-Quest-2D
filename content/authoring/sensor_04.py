def first_match(values, target):
    for i, value in enumerate(values):
        if value == target:
            return i
    return -1
