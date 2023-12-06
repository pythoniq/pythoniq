from pythoniq.framework.illuminate.events.abstractEvent import AbstractEvent
from app.libraries.gsm.gsmContract import GsmContract


class Removed(AbstractEvent):
    def gsm(self) -> GsmContract:
        return self.getArgs()[0]
