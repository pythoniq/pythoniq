from app.libraries.osos.abstractOsos import AbstractOsos


class GridBox(AbstractOsos):
    @staticmethod
    def getLocalTime() -> str:
        import time
        date = time.localtime()
        return "%04d%02d%02d%02d%02d%02d" % (date[0], date[1], date[2], date[3], date[4], date[5])

    @staticmethod
    def version() -> str:
        return '1.0.6'
