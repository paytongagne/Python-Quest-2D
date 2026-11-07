def near_vector(a, b, tolerance):
    return tolerance>=0 and len(a)==len(b) and all(abs(x-y)<=tolerance for x,y in zip(a,b))
