from pythoniq.framework.illuminate.mail.sentMessage import SentMessage
from pythoniq.framework.illuminate.contracts.queue.factory import Factory as QueueFactory


class Mailable:
    # Send the message using the given mailer.
    def send(self, mailer) -> SentMessage:
        pass

    # Queue the given message.
    def queue(self, queue: QueueFactory) -> any:
        pass

    # Deliver the queued message after (n) seconds.
    def later(self, delay: int, queue: QueueFactory) -> any:
        pass

    # Set the recipients of the message.
    def cc(self, address: object | list | dict | str, users: str | None = None):
        pass

    # Begin the process of mailing a mailable class instance.
    def bcc(self, address: object | list | dict | str, users: str | None = None):
        pass

    # Begin the process of mailing a mailable class instance.
    def to(self, address: object | list | dict | str, users: str | None = None):
        pass

    # Set the locale of the message.
    def locale(self, locale: str):
        pass

    # Set the name of the mailer that should be used to send the message.
    def mailer(self, mailer: str):
        pass
