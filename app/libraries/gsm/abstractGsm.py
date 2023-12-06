from app.libraries.gsm.commands.response import Response
from app.libraries.gsm.commands.responseParser import ResponseParser
from app.libraries.gsm.commands.responseParserContract import ResponseParserContract
from app.libraries.gsm.uart import UART
from pythoniq.framework.illuminate.contracts.config.repository import Repository as ConfigContract
from pythoniq.framework.illuminate.config.repository import Repository as Config
from app.libraries.gsm.gsmContract import GsmContract
from app.libraries.gsm.events.hardware.opening import Opening
from app.libraries.gsm.events.hardware.opened import Opened
from app.libraries.gsm.events.hardware.closing import Closing
from app.libraries.gsm.events.hardware.closed import Closed
from app.libraries.gsm.events.hardware.powerOpening import PowerOpening
from app.libraries.gsm.events.hardware.powerOpened import PowerOpened
from app.libraries.gsm.events.hardware.powerClosing import PowerClosing
from app.libraries.gsm.events.hardware.powerClosed import PowerClosed
from app.libraries.gsm.events.hardware.simCardInserted import SimCardInserted
from app.libraries.gsm.events.hardware.simCardRemoved import SimCardRemoved
from app.libraries.gsm.events.hardware.activating import Activating
from app.libraries.gsm.events.hardware.activated import Activated
from app.libraries.gsm.events.hardware.deActivating import DeActivating
from app.libraries.gsm.events.hardware.deActivated import DeActivated
from app.libraries.gsm.pin import Pin
import time


class AbstractGsm(GsmContract):
    _config: ConfigContract = None

    # Create a new gsm instance.
    def __init__(self, config: dict):
        self._status: int = 0
        self._simCardStatus: int = 0

        self._config = Config(config)
        self._pin: Pin = Pin()
        self._pinInit()

        self._uart: UART = UART(self)
        self._parser = ResponseParser(self)

    def config(self) -> ConfigContract:
        return self._config

    def _pinInit(self) -> None:
        self.pin().set('regulator', self.config().get('regulator'), Pin.OUT)
        self.pin().set('power', self.config().get('powerKey'), Pin.OUT)
        self.pin().set('status', self.config().get('status'), Pin.IN, Pin.PULL_DOWN)
        self.pin().set('simDetect', self.config().get('simDetect'), Pin.IN, Pin.PULL_DOWN)

    def pin(self, name: str = None) -> dict | Pin:
        if name is not None:
            return self._pin.get(name)

        return self._pin

    def on(self) -> None:
        Opening.dispatch(self)
        self.powerOn()
        self.active()
        Opened.dispatch(self)

        self.pin().irq('simDetect', handler=self._simCardStatusChange, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    def off(self) -> None:
        self.pin().irq('simDetect', handler=None, trigger=0)

        Closing.dispatch(self)
        self.deActive()
        self.powerOff()
        Closed.dispatch(self)

    def restart(self) -> None:
        self.off()
        time.sleep_ms(100)
        self.on()

    def powerOn(self) -> None:
        PowerOpening.dispatch(self)
        self.pin().get('regulator').on()
        PowerOpened.dispatch(self)

    def powerOff(self) -> None:
        PowerClosing.dispatch(self)
        self.pin().get('regulator').off()
        PowerClosed.dispatch(self)

    def active(self) -> None:
        Activating.dispatch(self)
        self.pin().get('power').on()
        time.sleep_ms(100)
        self.pin().get('power').off()
        time.sleep_ms(50)
        self.pin().get('power').on()

        while self.pin().get('status').value() == 1:
            pass

        self.pin().irq('status', handler=self._statusChange, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    def deActive(self) -> None:
        DeActivating.dispatch(self)
        self.pin().get('power').off()
        DeActivated.dispatch(self)

        self.pin().irq('status', handler=None, trigger=0)

    def _statusChange(self, pin) -> None:
        if pin.value() != self._status:
            self._status = pin.value()

            if self._status == 1:
                Activated.dispatch(self)

    def _simCardStatusChange(self, pin) -> None:
        if pin.value() != self._simCardStatus:
            self._simCardStatus = pin.value()

            if self._simCardStatus == 0:
                SimCardInserted.dispatch(self)
            else:
                SimCardRemoved.dispatch(self)

    def uart(self) -> UART:
        return self._uart

    def check(self) -> None:
        if self.uart().any():
            self.uart().get()
            response = self.uart().lastResponse()

            print(response)

            response = Response(response)

            self.parser().parse(response)

    def parser(self) -> ResponseParserContract:
        return self._parser

    def setIpAddress(self, ip: str) -> None:
        self.config().set('apn.ip', ip)
