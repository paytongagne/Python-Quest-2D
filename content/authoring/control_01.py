def classify_temp(temp):
    if temp < 0:
        return 'COLD'
    elif temp > 35:
        return 'HOT'
    else:
        return 'SAFE'
