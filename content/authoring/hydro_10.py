def merge_meters(left, right):
    total = dict(left)
    for key, value in right.items():
        total[key] = total.get(key, 0) + value
    return total
