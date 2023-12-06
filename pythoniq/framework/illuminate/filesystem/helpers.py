from pythoniq.framework.illuminate.contracts.filesystem.fileNotFoundException import FileNotFoundException
from lib.helpers import is_file

import os


def exists(path) -> bool:
    try:
        os.stat(path)
        return True
    except:
        return False


def missing(path) -> bool:
    return not exists(path)


def listDir(path) -> list[str]:
    if missing(path) or is_file(path):
        raise FileNotFoundException('Directory does not exist at path "%s".' % path)
    return os.listdir(path)


def files(path) -> list:
    items = []
    for item in listDir(path):
        if is_file(path + '/' + item):
            items.append(item)

    return items
