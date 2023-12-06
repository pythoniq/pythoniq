def value(value: any, *args: any):
    if callable(value):
        return value(*args)

    return value


# Get an item from an array or object using "dot" notation.
def data_get(target: dict, key: str | list | dict | None = None, default: any = None):
    if key is None:
        return target

    if isinstance(key, str):
        key = key.split('.')

    for segment, i in enumerate(key):
        if isinstance(target, dict):
            if segment == len(key) - 1:
                return target.get(i, default)

            if i not in target:
                return default

            target = target[i]
        elif isinstance(target, list):
            if segment == len(key) - 1:
                return target[int(i)] if i < len(target) else default

            target = target[int(i)]
        else:
            return default
