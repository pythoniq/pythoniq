import time


class SMS:
    _index: int = None
    _status: int = None
    _from: str = None
    _dateTime: int = None
    _message: str = None

    _stats: dict = {
        '0': 'REC UNREAD',
        '1': 'REC READ',
        '2': 'STO UNSENT',
        '3': 'STO SENT',
        '4': 'ALL',
    }

    def __init__(self, index: int, status: int, from_: str, dateTime: int, message: str) -> None:
        self._index = index
        self._status = status
        self._from = from_
        self._dateTime = dateTime
        self._message = message

    @staticmethod
    def getStatusCode(status: str) -> str:
        return [key for key, value in SMS._stats.items() if value == status][0]

    @staticmethod
    def listParser(value):
        message = value[1]

        arr = value[0].split(',')
        timeData = arr[5].rstrip('"').replace('+', ',').split(',')
        dateArray = list(map(lambda x: int(x), arr[4].lstrip('"').split('/')))
        timeArray = list(map(lambda x: int(x), timeData[0].split(':')))
        arr3 = timeData[1].split('+')

        tup = (
            int('20' + str(dateArray[0])), dateArray[1], dateArray[2],
            timeArray[0], timeArray[1], timeArray[2], 0, 0,
            int(arr3[0])
        )

        return SMS(arr[0], SMS.getStatusCode(arr[1].strip('"')), arr[2].strip('"'), time.mktime(tup), message)

    @staticmethod
    def parser(value):
        message = value[1]

        arr = value[0].replace('"', '').split(',')
        timeData = arr[4].split('+')

        dateArray = list(map(lambda x: int(x), arr[3].lstrip('"').split('/')))
        timeArray = list(map(lambda x: int(x), timeData[0].split(':')))

        tup = (
            int('20' + str(dateArray[0])), dateArray[1], dateArray[2],
            timeArray[0], timeArray[1], timeArray[2], 0, 0,
            int(timeData[1])
        )

        return SMS(0, SMS.getStatusCode(arr[0].strip('"')), arr[1].strip('"'), time.mktime(tup), message)

