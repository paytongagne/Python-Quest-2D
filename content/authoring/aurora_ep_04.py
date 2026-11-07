def accepted_samples(samples):
    return [s['id'] for s in samples if s.get('contact') is True and s.get('confidence',0)>=0.8]
