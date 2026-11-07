def work_counts(sizes):
    result=[]
    for v,e in sizes:
        fast=v+e
        slow=v*v
        result.append({'bfs':fast,'scan':slow,'winner':'bfs' if fast<slow else 'scan' if slow<fast else 'tie'})
    return result
