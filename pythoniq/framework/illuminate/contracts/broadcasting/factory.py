from pythoniq.framework.illuminate.contracts.broadcasting.broadcaster import Broadcaster


class Factory:
    # Get a broadcaster implementation by name.
    def connection(self, name: str = None) -> Broadcaster:
        pass
