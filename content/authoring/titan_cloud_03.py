def subscribers(patterns, topic):
    result = []
    parts = topic.split('/')
    for index, pattern in enumerate(patterns):
        levels = pattern.split('/')
        matched = True
        for i, name in enumerate(levels):
            if name == '#':
                break
            if i >= len(parts) or (name != '+' and name != parts[i]):
                matched = False
                break
        else:
            matched = len(levels) == len(parts)
        if matched:
            result.append(index)
    return result
