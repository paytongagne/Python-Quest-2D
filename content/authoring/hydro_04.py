def interlock(readings):
    if 'pressure' not in readings or 'moisture' not in readings:
        return 'HOLD'
    if readings['pressure'] >= 80:
        return 'VENT'
    return 'PUMP' if readings['moisture'] < 30 else 'HOLD'
