def isEmpty(body):
    return len(body) == 0


def toNumber(string):
    try:
        return int(string)
    except ValueError:
        return float(string)
