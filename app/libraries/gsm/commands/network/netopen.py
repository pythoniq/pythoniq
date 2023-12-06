from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.events.network.networkOpen import NetworkOpen
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable


class NETOPEN(AbstractCommand):
    SIGNATURE: str = 'NETOPEN'
    DESCRIPTION: str = 'Start Socket Service'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + NETOPEN.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        status = value.after('+' + NETOPEN.getSignature() + ': ').value()

        if status == '0':
            print('Network opened')
            NetworkOpen.dispatch(gsm)

        next(parser.response())
