from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable
from app.libraries.gsm.events.statusControl.signalQualityChanged import SignalQualityChanged


class CSQ(AbstractCommand):
    SIGNATURE: str = 'CSQ'
    DESCRIPTION: str = 'Query signal quality'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CSQ.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        data = value.after('+' + CSQ.getSignature() + ': ').explode(',')

        SignalQualityChanged.dispatch(gsm, data[0], data[1])

        next(parser.response())
