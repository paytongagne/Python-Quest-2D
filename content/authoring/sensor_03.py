def count_statuses(statuses):
    counts = {}
    for status in statuses:
        counts[status] = counts.get(status, 0) + 1
    return counts
