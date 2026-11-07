def change_frame(points, origin, inverse):
    sign=-1 if inverse else 1
    return [[x+sign*origin[0],y+sign*origin[1]] for x,y in points]
