def count_errors(path):
    with open(path, encoding="utf-8") as log:
        return sum(line.strip().startswith("ERROR:") for line in log)
