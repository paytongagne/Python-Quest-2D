def parse_temp(packet):
    for part in packet.split(','):
        if part.startswith('TEMP='):
            try:
                return float(part[5:])
            except ValueError:
                return None
    return None
