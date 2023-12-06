class TCA6408A:
    TCA6408A_INPUT_REGISTER = 0x00
    TCA6408A_OUTPUT_REGISTER = 0x01
    TCA6408A_POLARITY_INVERSION_REGISTER = 0x02
    TCA6408A_CONFIGURATION_REGISTER = 0x03

    _PINS = {
        0: {
            'low': 0xFE,
            'high': 0x01,
        },
        1: {
            'low': 0xFD,
            'high': 0x02
        },
        2: {
            'low': 0xFB,
            'high': 0x04
        },
        3: {
            'low': 0xF7,
            'high': 0x08
        },
        4: {
            'low': 0xEF,
            'high': 0x10
        },
        5: {
            'low': 0xDF,
            'high': 0x20
        },
        6: {
            'low': 0xBF,
            'high': 0x40
        },
        7: {
            'low': 0x7F,
            'high': 0x80
        },
    }

    _deviceAddress: int = None

    # i2c_id	I2C ID
    # scl		I2C scl pin
    # sda		I2C sda pin
    # freq		I2C freq
    # device_address ve reset pinini eklemiyorum, çünkü ilerleyen süreçlerde ayni hat üzerine ilave IO expender bağlanacak olur ise
    # reset pin ve device_address karmaşaya sebep olacaktır
    # reset		io expender reset pin. active low
    # device_address	device hardwared address to communicate

    def __init__(self, i2c, deviceAddress: int):
        self.i2c = i2c
        self._deviceAddress = deviceAddress

    def setAllInput(self) -> None:
        self.i2c.writeto_mem(self._deviceAddress, self.TCA6408A_CONFIGURATION_REGISTER, b'\xFF')

    def setAllOutput(self) -> None:
        self.i2c.writeto_mem(self._deviceAddress, self.TCA6408A_CONFIGURATION_REGISTER, b'\x00')

    def setPinState(self, pin, state='low') -> None:
        pin = self._PINS[pin][state]
        self._i2cUpdate(pin, state)

    def setPinsState(self, pins=0x00, state='low') -> None:
        self._i2cUpdate(pins, state)

    def setAllPinState(self, state='low') -> None:
        buf = b'\x00'
        if state == 'high':
            buf = b'\xFF'

        self.i2c.writeto_mem(self._deviceAddress, self.TCA6408A_OUTPUT_REGISTER, buf)

    def _i2cUpdate(self, pin, state='low') -> None:
        temp = self._i2cRead()

        if state == 'low':
            temp &= pin
        elif state == 'high':
            temp |= pin

        self._i2cWrite(temp)

    def _i2cRead(self) -> int:
        value = self.i2c.readfrom_mem(self._deviceAddress, self.TCA6408A_OUTPUT_REGISTER, 1)
        return int.from_bytes(value, 'big')

    def _i2cWrite(self, value) -> None:
        value = value.to_bytes(1, 'big')
        self.i2c.writeto_mem(self._deviceAddress, self.TCA6408A_OUTPUT_REGISTER, value)
