from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.events.hardware.protectionCover.opened import Opened as Event
from app.events.gsm.sms.send import Send


class Alarm(ShouldQueue, InteractsWithQueue):
    def handle(self, event: Event):
        Send.dispatch('+905459553000', 'Koruma kapagi acildi!')

        Send.dispatch('+905335453354', 'Koruma kapagi acildi!')
