def hot_readings(readings, limit):
    result = []
    for value in readings:
        if value > limit:
            result.append(value)
    return result
