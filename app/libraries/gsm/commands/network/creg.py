from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.events.network.gsmNetworkRegistered import GsmNetworkRegistered
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable


class CREG(AbstractCommand):
    SIGNATURE: str = 'CREG'
    DESCRIPTION: str = 'Network registration'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CREG.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        data = value.after('+' + CREG.getSignature() + ': ').explode(',')
        n = data[0]
        stat = data[1]

        if stat == '1':    # registered, home network.
            GsmNetworkRegistered.dispatch(gsm)

        next(parser.response())
