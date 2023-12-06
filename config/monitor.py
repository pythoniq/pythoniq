def config():
    return {
        "colors": {
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
        },
        "format":
            # "Freq: {cpu.freq}"
            # " ||| "
            "Storage[{storage.usage.bar}]({storage.usage.percent}) "
            "{storage.usage}(u)/{storage.free}(f)/{storage.total}(t)"
            " ||| "
            "Mem[{memory.usage.bar}]({memory.usage.percent}) "
            "{memory.usage}(u)/{memory.free}(f)/{memory.total}(t)"
            " ||| "
            "Uptime: {uptime}"
            "  ",
        "startCollect": True,
    }

