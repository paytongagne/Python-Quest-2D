def bad_heuristics(heuristic, distances):
    return sorted(k for k,d in distances.items() if k not in heuristic or not 0<=heuristic[k]<=d)
