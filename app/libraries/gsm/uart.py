from app.libraries.gsm.commands.response import Response
from pythoniq.framework.illuminate.support.facades.app import App
from machine import UART as UARTMachine


class UART(UARTMachine):
    def __init__(self, gsm):
        super().__init__(gsm.config().get('uart.id'))
        self.gsm = gsm

        self.init(baudrate=self.gsm.config().get('uart.baudRate'), bits=8, parity=None, stop=1, timeout=1000, rxbuf=2048, txbuf=2048)

        self._lastCommand: str = ''
        self._lastResponse: str = ''

    def autoBaudRate(self) -> None:
        defaultBaudRate = self.gsm.config().get('uart.defaultBaudRate')
        baudRate = self.gsm.config().get('uart.baudRate')

        if defaultBaudRate != baudRate:
            if App().storage().missing('/hardware/gsm/baudRate.txt'):
                return self.setBaudRate(baudRate, defaultBaudRate)

            oldBaudRate = int(App().storage().get('/hardware/gsm/baudRate.txt'))
            if oldBaudRate != baudRate:
                return self.setBaudRate(baudRate, oldBaudRate)

    def setBaudRate(self, baudRate: int, oldBaudRate: int = 115200) -> None:
        self.init(baudrate=oldBaudRate, bits=8, parity=None, stop=1, timeout=1000, rxbuf=2048, txbuf=2048)
        self.put('AT+IPREX=' + str(baudRate))
        self.flush()
        self.init(baudrate=baudRate, bits=8, parity=None, stop=1, timeout=1000, rxbuf=2048, txbuf=2048)

        while True:
            self.put('at')

            if self.any():
                response = self.get()
                if len(response) > 1 and response[1] == 'OK':
                    break

        App().storage().put('/hardware/gsm/baudRate.txt', str(baudRate))

    def get(self) -> list:
        response = super().read()
        response = response is not None and response or b''
        value = bytearray(response)
        for i in range(len(value)):
            if value[i] > 127:
                value[i] = 36

        self._lastResponse = value.decode('utf-8').lstrip('\x00')
        return self._lastResponse.split('\r\n')

    def put(self, value) -> int | None:
        self._lastCommand = value
        return super().write(value + "\r\n")

    def lastCommand(self) -> str:
        return self._lastCommand

    def lastResponse(self) -> str:
        return self._lastResponse

    def response(self) -> Response:
        return Response(self.lastResponse())
