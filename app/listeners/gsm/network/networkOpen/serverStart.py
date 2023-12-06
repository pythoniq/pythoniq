from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.libraries.gsm.events.network.networkOpen import NetworkOpen as Event


class ServerStart(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        event.gsm().uart().put('AT+SERVERSTART=6789,0')
