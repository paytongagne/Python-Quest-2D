def pack_events(events):
    runs = []
    for event in events:
        if runs and runs[-1][0] == event:
            runs[-1][1] += 1
        else:
            runs.append([event,1])
    return runs
