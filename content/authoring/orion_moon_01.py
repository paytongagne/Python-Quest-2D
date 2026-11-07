def relay_graph(nodes, edges):
    graph = {node: set() for node in nodes}
    for a,b in edges:
        if a in graph and b in graph and a != b:
            graph[a].add(b)
            graph[b].add(a)
    return {key: sorted(value) for key,value in graph.items()}
