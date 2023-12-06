from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from pythoniq.framework.illuminate.support.str import Stringable
from app.libraries.gsm.sms.sms import SMS


class CMGL(AbstractCommand):
    SIGNATURE: str = 'CMGL'
    DESCRIPTION: str = 'List SMS messages from preferred store'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CMGL.getSignature() + ':')

    @staticmethod
    def parse(parser: ResponseParserContract, value) -> str:
        data = value.after('+' + CMGL.getSignature() + ': ')
        next(parser.response())
        return SMS.listParser([data.value(), next(parser.response())])

