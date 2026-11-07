def valid_packet(packet):
    return packet.startswith('TEL,') and 'TEMP=' in packet
