from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.support.facades.app import App
from app.events.gsm.sms.receive import Receive as Event


class ReadAndDeleteSms(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        App().make('gsm').uart().put('AT+CMGRD=' + event.getSmsIndex())
