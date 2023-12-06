from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.libraries.gsm.events.network.networkRegistered import NetworkRegistered as Event


class SetPdpContext(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        pass
        # @todo: APN burada mı tanımlanacak? Ona göre burası değişecek.
        # event.gsm().uart().put('AT+CGDCONT=1,"IP","internet"')
