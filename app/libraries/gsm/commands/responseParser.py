from app.libraries.gsm.commands.network.cereg import CEREG
from app.libraries.gsm.commands.network.cgev import CGEV
from app.libraries.gsm.commands.network.cgpaddr import CGPADDR
from app.libraries.gsm.commands.network.creg import CREG
from app.libraries.gsm.commands.network.netopen import NETOPEN
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.gsmContract import GsmContract
from app.libraries.gsm.commands.response import Response
from app.libraries.gsm.commands.sim.cpin import CPIN
# from app.libraries.gsm.commands.sms.cmgl import CMGL
# from app.libraries.gsm.commands.sms.cmgr import CMGR
# from app.libraries.gsm.commands.sms.cmgrd import CMGRD
# from app.libraries.gsm.commands.sms.cmti import CMTI
from app.libraries.gsm.commands.statusControl.csq import CSQ
from pythoniq.framework.illuminate.support.str import Str


class ResponseParser(ResponseParserContract):
    _gsm: GsmContract = None
    _response: Response = None

    def __init__(self, gsm: GsmContract):
        self._gsm = gsm

    def parse(self, response: Response) -> None:
        self._response = response
        while self._response.getIndex() < self._response.count():
            value = self._response.item()
            value = Str.of(value)

            if CPIN.match(value):
                CPIN.parse(self._gsm, self, value)

            if CSQ.match(value):
                CSQ.parse(self._gsm, self, value)

            if CGEV.match(value):
                CGEV.parse(self._gsm, self, value)

            if CREG.match(value):
                CREG.parse(self._gsm, self, value)

            if CEREG.match(value):
                CEREG.parse(self._gsm, self, value)

            if CGPADDR.match(value):
                CGPADDR.parse(self._gsm, self, value)

            if NETOPEN.match(value):
                NETOPEN.parse(self._gsm, self, value)

            # if CMGL.match(value):
            #     response = CMGL.parse(self, value)
            #     print(response)
            #
            # if CMTI.match(value):
            #     response = CMTI.parse(self, value)
            #     print(response)
            #
            # if CMGR.match(value):
            #     response = CMGR.parse(self, value)
            #     print(response)
            #
            # if CMGRD.match(value):
            #     response = CMGRD.parse(self, value)
            #     print(response)

            try:
                next(self._response)
            except StopIteration:
                break
