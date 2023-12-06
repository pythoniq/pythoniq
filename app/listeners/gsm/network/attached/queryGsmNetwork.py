from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.libraries.gsm.events.network.attached import Attached as Event


class QueryGsmNetwork(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        event.gsm().uart().put('AT+CREG?')
