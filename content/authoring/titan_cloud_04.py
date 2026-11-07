def deliver(ids, mode):
    if mode == 'at_least_once':
        return list(ids)
    return list(dict.fromkeys(ids))
