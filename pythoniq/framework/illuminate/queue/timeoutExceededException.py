from pythoniq.framework.illuminate.queue.maxAttemptsExceededException import MaxAttemptsExceededException


class TimeoutExceededException(MaxAttemptsExceededException):
    pass
