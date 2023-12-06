from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.sms.sms import SMS
from pythoniq.framework.illuminate.support.str import Stringable
from app.events.gsm.sms.read import Read


class CMGRD(AbstractCommand):
    SIGNATURE: str = 'CMGRD'
    DESCRIPTION: str = 'Read message'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CMGRD.getSignature() + ':')

    @staticmethod
    def parse(parser: ResponseParserContract, value) -> str:
        data = value.after('+' + CMGRD.getSignature() + ': ')
        next(parser.response())
        sms = SMS.parser([data.value(), next(parser.response())])

        Read.dispatch(sms)

        return sms
