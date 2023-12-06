class RetrievesMultipleKeys:
    # Retrieve multiple items from the cache by key.
    # Items not found in the cache will have a null value.
    def many(self, keys: list) -> dict:
        return_ = []

        items = []
        for key, value in keys.items():
            item = isinstance(key, str) and key or (isinstance(key, str) and value or None)
            items.append([item])

        for key, default in items.items():
            return_.append(self.get(key, default))

        return return_

    # Store multiple items in the cache for a given number of seconds.
    def putMany(self, values: dict, seconds: int) -> bool:
        manyResult = None

        for key, value in values.items():
            result = self.put(key, value, seconds)

            manyResult = manyResult and result or (result and manyResult)

        return manyResult or False
