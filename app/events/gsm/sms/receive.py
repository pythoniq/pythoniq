from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent


class Receive(AbstractEvent):
    # The name and signature of the event.
    _signature = 'gsm.sms.receive'

    def __init__(self, *arguments):
        super().__init__(*arguments)
        
        self.smsIndex = self.getArgs()[0]

    def getSmsIndex(self) -> str:
        return self.smsIndex
