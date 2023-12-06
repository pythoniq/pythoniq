from app.libraries.gsm.commands.abstractCommand import AbstractCommand
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.events.network.pdpAddressSet import PdpAddressSet
from app.libraries.gsm.gsmContract import GsmContract
from pythoniq.framework.illuminate.support.str import Stringable


class CGPADDR(AbstractCommand):
    SIGNATURE: str = 'CGPADDR'
    DESCRIPTION: str = 'Show PDP address'
    TIMEOUT: int = 9000

    @staticmethod
    def match(value: Stringable) -> bool:
        return value.startsWith('+' + CGPADDR.getSignature() + ':')

    @staticmethod
    def parse(gsm: GsmContract, parser: ResponseParserContract, value) -> None:
        data = value.after('+' + CGPADDR.getSignature() + ': ').explode(',')
        cid = data[0]
        addr = data[1]

        if cid == '1':
            gsm.setIpAddress(addr)
            PdpAddressSet.dispatch(gsm)

        next(parser.response())
