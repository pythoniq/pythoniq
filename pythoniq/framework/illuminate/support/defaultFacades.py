class DefaultFacades:
    # The current facades.
    _facades: dict = None

    # Create a new default provider collection.
    def __init__(self, facades: dict = None) -> None:
        self._facades = facades or {
            'Storage': 'pythoniq.framework.illuminate.support.facades.storage.Storage',
        }

    #
    def merge(self, facades: dict):
        self._facades.update(facades)

        return DefaultFacades(self._facades)

    # Replace the given facades with other facades.
    def replace(self, facades: dict):
        pass

    # Disable the given facades.
    def excepting(self, facades: dict):
        pass

    # Convert the provider collection to an array.
    def toArray(self) -> dict:
        return self._facades
