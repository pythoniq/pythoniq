from pythoniq.framework.illuminate.contracts.monitor.monitor import Monitor as MonitorContract
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.readable import Readable

import machine
import gc
import time
import os


class Battery(MonitorContract):
    @staticmethod
    def start(sleep: int = 1):
        if not Monitor.isInstance:
            Monitor.init()

        if App().make("config").get("monitor.startCollect", True):
            gc.collect()

        while True:
            Monitor.render()
            time.sleep(sleep)

    @staticmethod
    def init():
        Monitor.isInstance = True

        if App().make("config").has("monitor"):
            Monitor._colors = App().make("config").get("monitor.colors")
            Monitor._format = App().make("config").get("monitor.format")
            App().make("config").forget("monitor")

        Monitor._format = Monitor._format.replace("{", "%(").replace("}", ")s")