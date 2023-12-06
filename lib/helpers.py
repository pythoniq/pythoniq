import os, time, math, random


def end(dictionary: dict | list) -> any:
    if not len(dictionary):
        return

    if isinstance(dictionary, dict):
        return sorted(dictionary.keys())[-1]
    elif isinstance(dictionary, list):
        return dictionary[-1]


def is_file(path: str) -> bool:
    try:
        return (os.stat(path)[0] & 0x4000) == 0
    except:
        return False


def is_dir(path: str) -> bool:
    try:
        return (os.stat(path)[0] & 0x4000) != 0
    except:
        return False


def uniqid(prefix: str = '', more_entropy: bool = False):
    m = time.time()
    sec = math.floor(m)
    usec = math.floor(1000000 * (m - sec))
    if more_entropy:
        lcg = random.random()
        the_uniqid = "%08x%05x%.8F" % (sec, usec, lcg * 10)
    else:
        the_uniqid = '%8x%05x' % (sec, usec)

    the_uniqid = prefix + the_uniqid
    return the_uniqid

