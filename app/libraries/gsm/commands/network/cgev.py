from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.events.network.attached import Attached
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable


class CGEV(AbstractCommand):
    SIGNATURE: str = 'CGEV'
    DESCRIPTION: str = 'GSM Attach or Detach Event Reporting'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CGEV.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        Attached.dispatch(gsm)

        next(parser.response())
