def recover(events):
    latched = False
    actions = []
    for e in events:
        if e == 'FAULT':
            latched = True
            action = 'VENT'
        elif e == 'RESET':
            latched = False
            action = 'HOLD'
        elif not latched and e == 'DRY':
            action = 'PUMP'
        else:
            action = 'HOLD'
        actions.append(action)
    return actions
