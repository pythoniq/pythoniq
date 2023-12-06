from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.events.gsm.sms.receive import Receive
from pythoniq.framework.illuminate.support.str import Stringable


class CMTI(AbstractCommand):
    SIGNATURE: str = 'CMTI'
    DESCRIPTION: str = 'New Message Indication'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CMTI.getSignature() + ':')

    @staticmethod
    def parse(parser: ResponseParserContract, value) -> None:
        data = value.after('+' + CMTI.getSignature() + ': ').after(',').value()

        Receive.dispatch(data)

        next(parser.response())
