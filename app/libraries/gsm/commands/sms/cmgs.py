from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable
from app.libraries.gsm.sms.sms import SMS
import time


class CMGS(AbstractCommand):
    SIGNATURE: str = 'CMGS'
    DESCRIPTION: str = 'Send message'
    TIMEOUT: int = 40000
    PREFIX: str = 'AT+'

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CMGS.getSignature() + ':')

    @staticmethod
    def parse(parser: ResponseParserContract, value) -> str:
        data = value.after('+' + CMGS.getSignature() + ': ')
        next(parser.response())
        return SMS.parser([data.value(), next(parser.response())])

    @staticmethod
    def run(gsm: GsmContract, phoneNumber: str, context: str) -> int | None:
        gsm.uart().write((CMGS.PREFIX + CMGS.getSignature() + '="' + phoneNumber + '"' + "\r").encode())
        time.sleep_ms(200)
        return gsm.uart().write((context + "\r" + chr(26)).encode())
