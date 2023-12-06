from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.support.facades.app import App
from app.libraries.gsm.events.network.networkOpen import NetworkOpen as Event


class NetworkLedOn(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        App().make('ioExpander.led').setPinState(5, 'high')
