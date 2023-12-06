from pythoniq.framework.illuminate.contracts.monitor.monitor import Monitor as MonitorContract
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.readable import Readable

import machine
import gc
import time
import os


class Monitor(MonitorContract):
    isInstance = False
    _colors: dict = {
        # green
        "0": "\033[92m",
        "10": "\033[92m",
        "20": "\033[92m",
        "30": "\033[92m",

        # blue
        "40": "\033[94m",
        "50": "\033[94m",

        # orange
        "60": "\033[93m",
        "70": "\033[93m",

        # red
        "80": "\033[91m",
        "90": "\033[91m",
        "100": "\033[91m",
    }
    _data: dict = {
        "storage.usage.bar": "",
        "storage.usage.percent": "",
        "storage.usage": "",
        "storage.free": "",
        "storage.total": "",
        "memory.usage.bar": "",
        "memory.usage.percent": "",
        "memory.usage": "",
        "memory.free": "",
        "memory.total": "",
        "uptime": "",
    }
    _format: str = (
            "Freq: {cpu.freq}" +
            " ||| " +
            "Storage[{storage.usage.bar}]({storage.usage.percent}) " +
            "{storage.usage}(u)/{storage.free}(f)/{storage.total}(t)" +
            " ||| " +
            "Mem[{memory.usage.bar}]({memory.usage.percent}) " +
            "{memory.usage}(u)/{memory.free}(f)/{memory.total}(t)" +
            " ||| " +
            "Uptime: {uptime}" +
            "  "
    )

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

    @staticmethod
    def render() -> None:
        response = Monitor.getCPU()
        Monitor._data["cpu.freq"] = Readable.hertz(response["freq"])

        response = Monitor.getStorage()
        percent = response["usage"] / response["total"] * 100
        Monitor._data["storage.usage.bar"] = Monitor.usagePipe(percent)
        Monitor._data["storage.usage.percent"] = Readable.percent(percent)
        Monitor._data["storage.usage"] = Readable.byte(response["usage"])
        Monitor._data["storage.free"] = Readable.byte(response["free"])
        Monitor._data["storage.total"] = Readable.byte(response["total"])

        response = Monitor.getMemory()
        percent = response["usage"] / response["total"] * 100
        Monitor._data["memory.usage.bar"] = Monitor.usagePipe(percent)
        Monitor._data["memory.usage.percent"] = Readable.percent(percent)
        Monitor._data["memory.usage"] = Readable.byte(response["usage"])
        Monitor._data["memory.free"] = Readable.byte(response["free"])
        Monitor._data["memory.total"] = Readable.byte(response["total"])

        response = Monitor.getUpTime()
        Monitor._data["uptime"] = Readable.time(response)

        try:
            print(Monitor._format % Monitor._data, end="\r")
        except Exception as e:
            Monitor.init()
            try:
                Monitor.render()
            except Exception as e:
                print("Monitor.render() error: ", e)

    @staticmethod
    def getCPU() -> dict:
        return {
            "freq": machine.freq(),
        }

    @staticmethod
    def getStorage() -> dict:
        diskStats = os.statvfs(App().basePath())
        total = diskStats[0] * diskStats[2]
        free = diskStats[0] * diskStats[3]

        return {
            "total": diskStats[0] * diskStats[2],
            "free": diskStats[0] * diskStats[3],
            "usage": total - free,
        }

    @staticmethod
    def getMemory() -> dict:
        total = gc.mem_alloc() + gc.mem_free()
        usage = gc.mem_alloc()

        return {
            "total": total,
            "free": gc.mem_free(),
            "usage": usage,
        }

    @staticmethod
    def getUpTime() -> int:
        return time.time() - App().startedAt()

    @staticmethod
    def usagePipe(percent) -> str:
        pipe = ""
        for i in range(0, 100, 10):
            if percent >= i:
                pipe += Monitor.getPercentToColor(str(i)) + "|" + "\033[0m"
            else:
                pipe += " "

        return pipe

    @staticmethod
    def getPercentToColor(percent) -> str:
        if percent in Monitor._colors:
            return Monitor._colors[percent]

        return ""
