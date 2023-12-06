from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.libraries.gsm.events.network.networkRegistered import NetworkRegistered as Event


class ActivatePdpContext(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        event.gsm().uart().put('AT+CGACT=1,1')
