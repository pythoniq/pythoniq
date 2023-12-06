from app.libraries.gsm.commands.commandContract import CommandContract
from app.libraries.gsm.gsmContract import GsmContract


class AbstractCommand(CommandContract):
    SIGNATURE: str = None
    DESCRIPTION: str = None
    TIMEOUT: int = None
    PREFIX: str = 'AT+'
    
    _gsm: GsmContract = None
    
    def __init__(self, gsm: GsmContract):
        self._gsm = gsm

    @classmethod
    def getSignature(cls) -> str:
        return cls.SIGNATURE

    @classmethod
    def getDescription(cls) -> str:
        return cls.DESCRIPTION

    @classmethod
    def getTimeout(cls) -> int:
        return cls.TIMEOUT

    @classmethod
    def getPrefix(cls) -> str:
        return cls.PREFIX

    @classmethod
    def prefixCommand(cls) -> str:
        return cls.getPrefix() + cls.getSignature()
    
    def gsm(self) -> GsmContract:
        return self._gsm

    # The mobile equipment returns the list of parameters and value ranges set with
    # the corresponding to Write Command or by internal processes.
    def test(self) -> int | None:
        return self.gsm().uart().put(self.prefixCommand() + '=?')

    # This command returns the currently set value of the parameter or parameters.
    def read(self) -> int | None:
        return self.gsm().uart().put(self.prefixCommand() + '?')

    # This command sets the user-definable parameter values.
    def write(self, command: str) -> int | None:
        return self.gsm().uart().put(self.prefixCommand() + '=' + command)

    # The execution command reads non-variable parameters affected by internal processes in the GSM engine.
    def execute(self) -> int | None:
        return self.gsm().uart().put(self.prefixCommand())
