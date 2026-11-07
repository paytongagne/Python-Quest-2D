def repair_order(dependencies):
    done=[]
    while len(done)<len(dependencies):
        ready=sorted(k for k,v in dependencies.items() if k not in done and all(p in done for p in v))
        if not ready:
            return []
        done.append(ready[0])
    return done
