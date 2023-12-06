from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent


class Closed(AbstractEvent):
    # The name and signature of the event.
    _signature = 'hardware.protection.opened'

    def __init__(self, *arguments):
        super().__init__(*arguments)

        self.rssi = 'test'

    def getRssi(self) -> str:
        return self.rssi
