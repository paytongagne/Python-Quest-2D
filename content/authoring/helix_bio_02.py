def timestamps(n, rate_hz):
    if n <= 0 or rate_hz <= 0:
        return []
    return [i*1000/rate_hz for i in range(n)]
