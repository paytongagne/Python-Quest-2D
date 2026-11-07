def baseline(samples):
    if len(samples) < 2:
        return list(samples)
    return [samples[0]+i*(samples[-1]-samples[0])/(len(samples)-1) for i in range(len(samples))]
