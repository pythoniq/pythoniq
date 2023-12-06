from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent


class Closing(AbstractEvent):
    def gsm(self) -> GsmContract:
        return self.getArgs()[0]
