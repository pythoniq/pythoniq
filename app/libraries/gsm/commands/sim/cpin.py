from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable
from app.libraries.gsm.events.sim.ready import Ready
from app.libraries.gsm.events.sim.removed import Removed


class CPIN(AbstractCommand):
    SIGNATURE: str = 'CPIN'
    DESCRIPTION: str = 'Enter PIN'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CPIN.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        data = value.after('+' + CPIN.getSignature() + ': ')

        if data.value() == 'READY':
            Ready.dispatch(gsm, data)
        elif data.value() == 'SIM REMOVED':
            Removed.dispatch(gsm, data)

        next(parser.response())
