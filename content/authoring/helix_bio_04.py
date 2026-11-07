def inject_noise(samples, seed, amplitude):
    return [round(v+(((seed+i*17)%101)/50-1)*amplitude,6) for i,v in enumerate(samples)]
