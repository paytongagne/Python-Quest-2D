def average_reading(readings):
    if not readings:
        return 0
    return sum(readings) / len(readings)
