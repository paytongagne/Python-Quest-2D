def allocate(requests, supply):
    out = []
    for amount in requests:
        used = min(amount, supply)
        out.append(used)
        supply -= used
    return out
