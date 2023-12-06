from app.libraries.gsm.simcom.sms.sms import SMS
from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent


class Read(AbstractEvent):
    # The name and signature of the event.
    _signature = 'gsm.sms.read'

    def __init__(self, *arguments):
        super().__init__(*arguments)

        self.sms: SMS = self.getArgs()[0]

    def getSms(self) -> SMS:
        return self.sms
