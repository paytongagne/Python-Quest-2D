def valve_trace(temps):
    opened = False
    trace = []
    for t in temps:
        if t >= 70:
            opened = True
        elif t <= 50:
            opened = False
        trace.append(opened)
    return trace
