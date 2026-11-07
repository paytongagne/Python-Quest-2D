def cached_distances(graph, queries):
    from collections import deque
    cache={}
    values=[]
    for start,goal in queries:
        key=tuple(sorted((start,goal)))
        if key not in cache:
            queue=deque([(start,0)])
            seen={start}
            distance=-1
            while queue:
                node,d=queue.popleft()
                if node==goal:
                    distance=d
                    break
                for nxt in graph.get(node,[]):
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt,d+1))
            cache[key]=distance
        values.append(cache[key])
    return {'distances':values,'searches':len(cache)}
