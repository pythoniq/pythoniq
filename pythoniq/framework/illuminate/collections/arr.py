from pythoniq.framework.illuminate.collections.helpers import value, data_get
from pythoniq.framework.illuminate.support.traits.macroable import Macroable


class Arr(Macroable):
    # Determine whether the given value is array accessible.
    @staticmethod
    def accessible(value) -> bool:
        return isinstance(value, (dict, Arr))

    # Add an element to an array using "dot" notation if it doesn't exist.
    @staticmethod
    def add(array: dict, key: str, value: any) -> dict:
        if Arr.get(array, key) is None:
            Arr.set(array, key, value)

        return array

    # Collapse an array of arrays into a single array.
    # @todo: implement Collection
    @staticmethod
    def collapse(array: list) -> list:
        results = []

        for values in array:
            if not isinstance(values, list):
                continue

            results = results + values

        return results

    # Cross join the given arrays, returning all possible permutations.
    @staticmethod
    def crossJoin(*arrays: list) -> list:
        results = [[]]

        for index, array in enumerate(arrays):
            if not isinstance(array, list):
                continue

            current = []

            for result in results:
                for item in array:
                    current.append(result + [item])

            results = current

        return results

    # Divide an array into two arrays. One with keys and the other with values.
    @staticmethod
    def divide(array: dict) -> list:
        return [list(array.keys()), list(array.values())]

    # Flatten a multi-dimensional associative array with dots.
    @staticmethod
    def dot(array: dict, prepend: str = '') -> dict:
        results = {}

        for key, value in array.items():
            if isinstance(value, dict):
                results.update(Arr.dot(value, prepend + key + '.'))
            else:
                results[prepend + key] = value

        return results

    # Convert a flatten "dot" notation array into an expanded array.
    @staticmethod
    def undot(array: dict) -> dict:
        results = {}

        for key, value in array.items():
            Arr.set(results, key, value)

        return results

    # Get all of the given array except for a specified array of keys.
    @staticmethod
    def except_(array: dict, keys: list) -> dict:
        Arr.forget(array, keys)

        return array

    # Determine if the given key exists in the provided array.
    @staticmethod
    def exists(array: dict, key: str) -> bool:
        if isinstance(array, dict):
            return key in array.keys()

        return key in array

    # Return the first element in an list or dict passing a given truth test.
    @staticmethod
    def first(array: list | dict, callback: callable = None, default: any = None) -> any:
        if isinstance(array, dict):
            for key, value in array.items():
                if callback(value, key):
                    return value
        elif isinstance(array, (list, tuple)):
            key = 0
            for value in array:
                key += 1
                if callback(value, key):
                    return value

        return default

    # Return the last element in an array passing a given truth test.
    @staticmethod
    def last(array: list | dict, callback: callable = None, default: any = None) -> any:
        if isinstance(array, dict):
            for key in reversed(array):
                if callback(array[key], key):
                    return array[key]
        elif isinstance(array, (list, tuple)):
            key = len(array)
            for value in reversed(array):
                key -= 1
                if callback(value, key):
                    return value

        return

    # Flatten a multi-dimensional array into a single level.
    # @todo: implement Collection
    @staticmethod
    def flatten(array: dict, depth: int = -1) -> list:
        results = []

        if isinstance(array, dict):
            for value in array.values():
                if isinstance(value, (list, tuple, dict)):
                    results = results + Arr.flatten(value, depth - 1)
                else:
                    results.append(value)
        elif isinstance(array, (list, tuple)):
            for value in array:
                if isinstance(value, (list, tuple, dict)):
                    results = results + Arr.flatten(value, depth - 1)
                else:
                    results.append(value)

        return results

    # Remove one or many array items from a given array using "dot" notation.
    @staticmethod
    def forget(array: dict, keys: str | list) -> dict:
        original = array

        keys = keys if isinstance(keys, list) else [keys]

        if len(keys) == 0:
            return array

        for key in keys:
            if Arr.exists(array, key):
                del array[key]
                continue

            parts = key.split('.')

            while len(parts) > 1:
                part = parts.pop(0)

                if Arr.exists(array, part):
                    array = array[part]
                    continue

                break

            if len(parts) == 1:
                part = parts.pop(0)

                if Arr.exists(array, part):
                    del array[part]

        return original

    # Get an item from an array using "dot" notation.
    @staticmethod
    def get(array: dict, key: str, default: any = None) -> any:
        if not Arr.accessible(array):
            return value(default)

        if key is None:
            return array

        if Arr.exists(array, key):
            return array[key]

        if '.' not in key:
            return value(default)

        for segment in key.split('.'):
            if Arr.accessible(array) and Arr.exists(array, segment):
                array = array[segment]
            else:
                return value(default)

        return array

    # Check if an item or items exist in an array using "dot" notation.
    @staticmethod
    def has(array: dict, key: str | list) -> bool:
        keys = key if isinstance(key, list) else [key]

        if not array or keys == []:
            return False

        for key in keys:
            subKeyArray = array

            if Arr.exists(array, key):
                continue

            for segment in key.split('.'):
                if Arr.accessible(subKeyArray) and Arr.exists(subKeyArray, segment):
                    subKeyArray = subKeyArray[segment]
                else:
                    return False

        return True

    # Determine if any of the keys exist in an array using "dot" notation.
    @staticmethod
    def hasAny(array: dict, keys: str | list) -> bool:
        if len(keys) == 0:
            return False

        keys = keys if isinstance(keys, list) else [keys]

        if not array:
            return False

        if keys == {}:
            return False

        for key in keys:
            if Arr.has(array, key):
                return True

        return False

    # Determines if an array is associative.
    # An array is "associative" if it doesn't have sequential numerical keys beginning with zero.
    @staticmethod
    def isAssoc(array: list | tuple | dict) -> bool:
        if isinstance(array, dict):
            return True
        else:
            return False

    # Determines if an array is a list.
    # An array is a "list" if all array keys are sequential integers starting from 0 with no gaps in between.
    @staticmethod
    def isList(array: list | tuple | dict) -> bool:
        if isinstance(array, (list, tuple)):
            return True
        else:
            return False

    # Join all items using a string. The final items can use a separate glue string.
    @staticmethod
    def join(array: list, glue: str = ',', finalGlue: str = None) -> str:
        if finalGlue is None:
            return glue.join(array)

        if len(array) <= 2:
            return finalGlue.join(array)

        return finalGlue.join([glue.join(array[:-1]), array[-1]])

    # Key an associative array by a field or using a callback.
    # @todo: implement Collection
    @staticmethod
    def keyBy(array: list, key: str) -> dict:
        results = {}

        for item in array:
            if key in item:
                results[item[key]] = item

        return results

    # Prepend the key names of an associative array.
    # @todo: implement Collection
    @staticmethod
    def prependKeysWith(array: dict, prefix: str) -> dict:
        results = {}

        for key, value in array.items():
            results[prefix + key] = value

        return results

    # Get a subset of the items from the given array.
    @staticmethod
    def only(array: dict, keys: str | list) -> dict:
        if isinstance(keys, str):
            keys = keys.split(',')

        return {key: value for key, value in array.items() if key in keys}

    # Pluck an array of values from an array.
    @staticmethod
    def pluck(array: list[dict], value: str, key: str = None) -> list | dict:
        [value, key] = Arr.explodePluckParameters(value, key)

        if key is None:
            results = []
            for item in array:
                results.append(data_get(item, value))

            return results

        results = {}
        for item in array:
            results[data_get(item, key)] = data_get(item, value)

        return results

    # Explode the "value" and "key" arguments passed to "pluck".
    @staticmethod
    def explodePluckParameters(value: str | list, key: str | list | None = None) -> tuple:
        if isinstance(value, str):
            value = value.split('.')

        if isinstance(list, str):
            key = key.split('.')

        return value, key

    # Run a map over each of the items in the array.
    @staticmethod
    def map(array: dict | list | tuple, callback: callable) -> dict | list | tuple:
        if isinstance(array, dict):
            keys = array.keys()

            for key in keys:
                array[key] = callback(array[key], key)

            return array
        elif isinstance(array, (list, tuple)):
            for key, value in enumerate(array):
                array[key] = callback(value, key)

            return array

    # Run an associative map over each of the items.
    # The callback should return an associative array with a single key/value pair.
    @staticmethod
    def mapWithKeys(array: list[dict], callback: callable) -> dict:
        result = {}

        for key, value in enumerate(array):
            assoc = callback(value, key)

            for assocKey, assocValue in assoc.items():
                result[assocKey] = assocValue

        return result

    # Push an item onto the beginning of an array.
    @staticmethod
    def prepend(array: list | dict, value: any, key: any = None) -> list:
        if isinstance(array, list):
            array.insert(0, value)

            return array

        if isinstance(array, dict):
            if key is None:
                array = {value: array}
            else:
                array[key] = value

            return array

    # Get a value from the array, and remove it.
    @staticmethod
    def pull(array: list | dict, key: str | list, default: any = None) -> any:
        value = Arr.get(array, key, default)

        Arr.forget(array, key)

        return value

    # Convert the array into a query string.
    @staticmethod
    def query(array: dict) -> str:
        for key, value in array.items():
            if isinstance(value, (list, tuple)):
                array[key] = ','.join(value)
            elif isinstance(value, dict):
                array[key] = Arr.query(value)

        return '&'.join([key + '=' + value for key, value in array.items()])

    # Get one or a specified number of random values from an array.
    @staticmethod
    def random(array: list, number: int | None = None) -> any:
        requested = number if number is not None else 1

        count = len(array)

        if requested > count:
            raise ValueError(
                'You requested ' + str(requested) + ' items, but there are only ' + str(count) + ' items available.')

        import random
        if number is None:
            return array[random.randint(0, count - 1)]

    # Set an array item to a given value using "dot" notation.
    # If no key is given to the method, the entire array will be replaced.
    @staticmethod
    def set(array: dict, key: str | int | None, value: any) -> dict:
        original = array

        if key is None:
            return array

        keys = key.split('.')

        while len(keys) > 1:
            if len(keys) == 1:
                break

            key = keys.pop(0)

            if key not in array:
                array[key] = {}

            array = array[key]

        array[keys.pop(0)] = value

        return original

    # Shuffle the given array and return the result.
    @staticmethod
    def shuffle(array, seed: int = None) -> list:
        import random
        if seed is not None:
            random.seed(seed)

        random.shuffle(array)

        return array

    # Sort the array using the given callback or "dot" notation.
    # @todo: implement Collection
    @staticmethod
    def sort(array: list | dict, callback: callable = None) -> list:
        if isinstance(array, dict):
            if callback is None:
                callback = lambda item: item

            return sorted(array.items(), key=lambda item: callback(item[1]))
        elif isinstance(array, (list, tuple)):
            if callback is None:
                callback = lambda item: item

            return sorted(array, key=callback)

    # Sort the array in descending order using the given callback or "dot" notation.
    # @todo: implement Collection
    @staticmethod
    def sortDesc(array: list | dict, callback: callable = None) -> list:
        return Arr.sort(array, callback)[::-1]

    # Recursively sort an array by keys and values.
    @staticmethod
    def sortRecursive(array: dict | list, descending: bool = False) -> dict | list:
        raise NotImplementedError

    # Recursively sort an array by keys and values in descending order.
    @staticmethod
    def sortRecursiveDesc(array: dict | list) -> dict | list:
        return Arr.sortRecursive(array, True)

    # Filter the array using the given callback.
    @staticmethod
    def where(array: dict | list, callback: callable) -> dict:
        result = {}
        if isinstance(array, dict):
            for key, value in array.items():
                if callback(value, key):
                    result[key] = value

            return result
        elif isinstance(array, (list, tuple)):
            for key, value in enumerate(array):
                if callback(value, key):
                    result[key] = value

            return result

    # Filter the array using the given callback.
    @staticmethod
    def whereNotNull(array: dict | list) -> dict:
        return Arr.where(array, lambda value, key: value is not None)

    # If the given value is not an array and not null, wrap it in one.
    @staticmethod
    def wrap(value: any) -> list:
        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]
