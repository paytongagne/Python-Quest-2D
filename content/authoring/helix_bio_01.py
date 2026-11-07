def toy_pulse(n):
    template=[0,0.1,-0.2,1.0,-0.3,0.2,0.1,0]
    return [template[i % len(template)] for i in range(n)]
