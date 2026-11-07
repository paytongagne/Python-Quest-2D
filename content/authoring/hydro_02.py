def dry_trays(readings, limit):
    return [i for i, moisture in enumerate(readings) if moisture < limit]
