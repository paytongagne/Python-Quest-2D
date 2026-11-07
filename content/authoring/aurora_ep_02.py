def cursor_position(a, b, t):
    t=max(0,min(1,t))
    return [x+(y-x)*t for x,y in zip(a,b)]
