def conflict_tick(a, b):
    for t in range(max(len(a),len(b))):
        x=a[min(t,len(a)-1)]
        y=b[min(t,len(b)-1)]
        if x==y:
            return t
        if t and x==b[min(t-1,len(b)-1)] and y==a[min(t-1,len(a)-1)]:
            return t
    return -1
