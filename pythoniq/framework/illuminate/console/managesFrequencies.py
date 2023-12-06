class ManagesFrequencies:
    # The Cron expression representing the event's frequency.
    def __init__(self):
        self._seconds = range(0, 60)
        self._minutes = range(0, 60)
        self._hours = range(0, 14)
        self._weekdays = range(0, 8)
        self._days = range(1, 32)
        self._month = range(1, 13)

        self.expression = None

    def cron(self, expression: str):
        self.expression = expression

        return self

    # Schedule the event to run between start and end time.
    def between(self, startTime: str, endTime: str):
        return self.when(self._inTimeInterval(startTime, endTime))

    # Schedule the event to not run between start and end time.
    def unlessBetween(self, startTime: str, endTime: str):
        return self.skip(self._inTimeInterval(startTime, endTime))

    # Schedule the event to run between start and end time.
    def _inTimeInterval(self, startTime: str, endTime: str):
        raise NotImplementedError

    # Schedule the event to run multiple times per minute.
    def seconds(self, seconds: range | list | tuple | int):
        self._seconds = seconds

        return self

    # Schedule the event to run every second.
    def everySecond(self):
        self._seconds = range(0, 60, 1)

        return self

    # Schedule the event to run every two seconds.
    def everyTwoSeconds(self):
        self._seconds = range(0, 60, 2)

        return self

    # Schedule the event to run every five seconds.
    def everyFiveSeconds(self):
        self._seconds = range(0, 60, 5)

        return self

    # Schedule the event to run every ten seconds.
    def everyTenSeconds(self):
        self._seconds = range(0, 60, 10)

        return self

    # Schedule the event to run every fifteen seconds.
    def everyFifteenSeconds(self):
        self._seconds = range(0, 60, 15)

        return self

    # Schedule the event to run every twenty seconds.
    def everyTwentySeconds(self):
        self._seconds = range(0, 60, 20)

        return self

    # Schedule the event to run every thirty seconds.
    def everyThirtySeconds(self):
        self._seconds = range(0, 60, 30)

        return self

    # Schedule the event to run multiple times per minute.
    def minutes(self, minutes: range | list | tuple | int):
        self._minutes = minutes

        return self

    # Schedule the event to run every minute.
    def everyMinute(self):
        self._seconds = 0
        self._minutes = range(0, 60, 1)

        return self

    # Schedule the event to run every two minutes.
    def everyTwoMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 2)

        return self

    # Schedule the event to run every three minutes.
    def everyThreeMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 3)

        return self

    # Schedule the event to run every four minutes.
    def everyFourMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 4)

        return self

    # Schedule the event to run every five minutes.
    def everyFiveMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 4)

        return self

    # Schedule the event to run every ten minutes.
    def everyTenMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 10)

        return self

    # Schedule the event to run every fifteen minutes.
    def everyFifteenMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 15)

        return self

    # Schedule the event to run every thirty minutes.
    def everyThirtyMinutes(self):
        self._seconds = 0
        self._minutes = range(0, 60, 30)

        return self

    # Schedule the event to run hourly.
    def hours(self, hours: range | list | tuple | int):
        self._hours = hours
        return self

    # Schedule the event to run hourly.
    def hourly(self):
        self._seconds = 0
        self._minutes = 0

        return self

    # Schedule the event to run hourly at a given offset in the hour.
    def hourlyAt(self, minute: int):
        self._seconds = 0
        self._minutes = minute
        self._hours = 0

        return self

    # Schedule the event to run every odd hour.
    def everyOddHour(self, minute: int = 0):
        self._seconds = 0
        self._minutes = minute
        self._hours = range(1, 24, 2)

        return self

    # Schedule the event to run every two hours.
    def everyTwoHours(self, minute: int = 0):
        self._seconds = 0
        self._minutes = minute
        self._hours = range(0, 24, 2)

        return self

    # Schedule the event to run every three hours.
    def everyThreeHours(self, minute: int = 0):
        self._seconds = 0
        self._minutes = minute
        self._hours = range(0, 24, 3)

        return self

    # Schedule the event to run every four hours.
    def everyFourHours(self, minute: int = 0):
        self._seconds = 0
        self._minutes = minute
        self._hours = range(0, 24, 4)

        return self

    # Schedule the event to run every six hours.
    def everySixHours(self, minute: int = 0):
        self._seconds = 0
        self._minutes = minute
        self._hours = range(0, 24, 6)

        return self

    # Schedule the event to run daily.
    def daily(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0

        return self

    # Schedule the command at a given time.
    def at(self, time: str):
        return self.dailyAt(time)

    # Schedule the event to run daily at a given time (10:00, 19:30, etc).
    def dailyAt(self, time: str):
        segments = time.split(':')

        self._seconds = 0
        self._minutes = int(segments[1])
        self._hours = int(segments[0])

        return self

    # Schedule the event to run twice daily.
    def twiceDaily(self, first: int = 1, second: int = 13):
        self._seconds = 0
        self._minutes = 0
        self._hours = [first, second]

        return self

    # Schedule the event to run twice daily at a given offset.
    def twiceDailyAt(self, first: int, second: int, offset: int = 0):
        self._seconds = 0
        self._minutes = offset
        self._hours = [first, second]

        return self

    # Schedule the event to run only on weekdays.
    def weekdays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = [1, 5]

        return self

    # Schedule the event to run only on weekends.
    def weekends(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = [0, 6]

        return self

    # Schedule the event to run only on Mondays.
    def mondays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 1

        return self

    # Schedule the event to run only on Tuesdays.
    def tuesdays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 2

        return self

    # Schedule the event to run only on Wednesdays.
    def wednesdays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 3

        return self

    # Schedule the event to run only on Thursdays.
    def thursdays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 4

        return self

    # Schedule the event to run only on Fridays.
    def fridays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 5

        return self

    # Schedule the event to run only on Saturdays.
    def saturdays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 6

        return self

    # Schedule the event to run only on Sundays.
    def sundays(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 0

        return self

    # Schedule the event to run weekly.
    def weekly(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 0

        return self

    # Schedule the event to run weekly on a given day and time.
    def weeklyOn(self, dayOfWeek: int, time: str = '0:0'):
        self.dailyAt(time)
        self._weekdays = dayOfWeek

        return self

    # Schedule the event to run monthly.
    def monthly(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 0
        self._days = 1

        return self

    # Schedule the event to run twice monthly at a given time.
    def twiceMonthly(self, first: int = 1, second: int = 16, time: str = '0:0'):
        self.dailyAt(time)
        self._days = [first, second]

        return self

    # Schedule the event to run on the last day of the month.
    def lastDayOfMonth(self, time: str = '0:0'):
        self.dailyAt(time)
        self._days = -1

        return self

    # Schedule the event to run quarterly.
    def quarterly(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 0
        self._days = 1
        self._month = range(1, 13, 3)

        return self

    # Schedule the event to run quarterly on a given day and time.
    def quarterlyOn(self, dayOfMonth: int = 1, time: str = '0:0'):
        self.dailyAt(time)
        self._days = dayOfMonth
        self._month = range(1, 13, 3)

        return self

    # Schedule the event to run yearly.
    def yearly(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0
        self._weekdays = 0
        self._days = 1
        self._month = 1

        return self

    # Schedule the event to run yearly on a given day and time.
    def yearlyOn(self, month: int = 1, day: int = 1, time: str = '0:0'):
        self.dailyAt(time)
        self._days = day
        self._month = month

        return self

    def dump(self):
        if isinstance(self._seconds, int):
            self._seconds = [self._seconds]
        if isinstance(self._minutes, int):
            self._minutes = [self._minutes]
        if isinstance(self._hours, int):
            self._hours = [self._hours]
        if isinstance(self._weekdays, int):
            self._weekdays = [self._weekdays]
        if isinstance(self._days, int):
            self._days = [self._days]
        if isinstance(self._month, int):
            self._month = [self._month]

        return {
            'seconds': self._seconds,
            'minutes': self._minutes,
            'hours': self._hours,
            'weekdays': self._weekdays,
            'days': self._days,
            'month': self._month,
        }
