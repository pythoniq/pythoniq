from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent


class Send(AbstractEvent):
    # The name and signature of the event.
    _signature = 'gsm.sms.send'

    def __init__(self, *arguments):
        super().__init__(*arguments)

        self.phoneNumber: str = self.getArgs()[0]
        self.context: str = self.getArgs()[1]

    def getPhoneNumber(self) -> str:
        return self.phoneNumber

    def getContext(self) -> str:
        return self.context
