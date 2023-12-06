from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from pythoniq.framework.illuminate.support.str import Stringable
from app.libraries.gsm.sms.sms import SMS


class CMGD(AbstractCommand):
    SIGNATURE: str = 'CMGD'
    DESCRIPTION: str = 'Delete message'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CMGD.getSignature() + ':')

    @staticmethod
    def parse(parser: ResponseParserContract, value) -> str:
        data = value.after('+' + CMGD.getSignature() + ': ')
        next(parser.response())
        return SMS.parser([data.value(), next(parser.response())])

