class Readable:
    @staticmethod
    def hertz(num, suffix="hz"):
        for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
            if abs(num) < 1000:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1000
        return f"{num:.1f}Yi{suffix}"

    @staticmethod
    def byte(num: int, suffix="B") -> str:
        for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
            if abs(num) < 1024:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024
        return f"{num:.1f}Yi{suffix}"

    @staticmethod
    def bit(num, suffix="b"):
        for unit in ("", "k", "m", "g", "t", "p", "e", "z"):
            if abs(num) < 1024:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024
        return f"{num:.1f}Yi{suffix}"

    @staticmethod
    def percent(percent, suffix="%") -> str:
        return "{:5.2f}{}".format(percent, suffix)

    @staticmethod
    def time(seconds: int) -> str:
        days, seconds = divmod(seconds, 24 * 60 * 60)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)

        if int(days):
            return "{:0} days, {:0>2}:{:0>2}:{:0>2}".format(int(days), int(hours), int(minutes), seconds)

        return "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), seconds)
