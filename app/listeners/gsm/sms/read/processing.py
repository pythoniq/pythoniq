from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.readable import Readable
from app.events.gsm.sms.read import Read as Event
from app.events.gsm.sms.send import Send


class Processing(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        if event.getSms()._from != '+905459553000' and event.getSms()._from != '+905335453354':
            return

        if event.getSms()._message == 'adonis monitor':
            context = ''

            response = App().monitor().getMemory()
            percent = response["usage"] / response["total"] * 100
            context += 'Mem(' + Readable.percent(percent) + '): '
            context += Readable.byte(response["usage"]) + '(u)/'
            context += Readable.byte(response["free"]) + '(f)/'
            context += Readable.byte(response["total"]) + "(t)\n"

            response = App().monitor().getStorage()
            percent = response["usage"] / response["total"] * 100
            context += 'Storage(' + Readable.percent(percent) + '): '
            context += Readable.byte(response["usage"]) + '(u)/'
            context += Readable.byte(response["free"]) + '(f)/'
            context += Readable.byte(response["total"]) + "(t)\n"

            response = App().monitor().getUpTime()
            context += 'Uptime: ' + Readable.time(response)

            Send.dispatch(event.getSms()._from, context)
