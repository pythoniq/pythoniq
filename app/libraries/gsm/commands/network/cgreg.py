from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.events.network.networkNotRegistered import NetworkNotRegistered
from app.libraries.gsm.events.network.networkRegistered import NetworkRegistered
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable


class CGREG(AbstractCommand):
    SIGNATURE: str = 'CGREG'
    DESCRIPTION: str = 'Network registration status'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CGREG.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        data = value.after('+' + CGREG.getSignature() + ': ').explode(',')
        n = data[0]
        stat = data[1]

        if stat == '1':    # registered, home network.
            NetworkRegistered.dispatch(gsm)
        else:
            NetworkNotRegistered.dispatch(gsm)

        next(parser.response())
