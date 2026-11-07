def transform(point, rotation, translation):
    return [sum(rotation[i][j]*point[j] for j in range(3))+translation[i] for i in range(3)]
