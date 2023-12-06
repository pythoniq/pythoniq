from pythoniq.framework.illuminate.foundation.events.dispatchable import Dispatchable
from pythoniq.framework.illuminate.broadcasting.interactsWithSockets import InteractsWithSockets
from pythoniq.framework.illuminate.support.facades.app import App


class AbstractEvent(Dispatchable, InteractsWithSockets):
    # The name and signature of the event.
    _signature: str = None

    def __init__(self, *arguments):
        # Arguments to pass to the event handler.
        self._arguments: list = list(arguments)

        self.handle()

    def handle(self, *arguments):
        pass

    def getArgs(self):
        return self._arguments

    def getSignature(self) -> str:
        return self._signature

    def fire(self):
        App().event().dispatch(self)
