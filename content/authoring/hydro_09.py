def decode_tube(label):
    parts = label.split(':')
    if len(parts) != 2 or not parts[0].strip():
        return None
    try:
        volume = int(parts[1])
    except ValueError:
        return None
    return [parts[0].strip(), volume] if volume >= 0 else None
