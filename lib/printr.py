oldLength = 0


def print_r(string: str = ''):
    global oldLength
    diff = oldLength - len(string)

    if diff >= 0:
        padding = " " * diff
        string = string + padding

    print(string, end="\r")

    oldLength = len(string)
