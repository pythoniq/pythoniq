from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent
from app.libraries.gsm.gsmContract import GsmContract


class SignalQualityChanged(AbstractEvent):
    def gsm(self) -> GsmContract:
        return self.getArgs()[0]

    def getRssi(self) -> str:
        return self.getArgs()[1]

    def getBer(self) -> str:
        return self.getArgs()[2]
