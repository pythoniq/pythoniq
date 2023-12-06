from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.libraries.gsm.simcom.commands.sms.cmgs import CMGS
from pythoniq.framework.illuminate.support.facades.app import App
from app.events.gsm.sms.send import Send as Event


class SendMessage(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        CMGS.run(
            App().make('gsm'),
            event.getPhoneNumber(),
            event.getContext()
        )
