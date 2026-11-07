def service_order(jobs):
    return [j['id'] for j in sorted(jobs,key=lambda j:(-j['severity'],j['arrival']))]
