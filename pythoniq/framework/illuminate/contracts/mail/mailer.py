from pythoniq.framework.illuminate.mail.pendingMail import PendingMail
from pythoniq.framework.illuminate.mail.sentMessage import SentMessage


class Mailer:
    # Begin the process of mailing a mailable class instance.
    def to(self, users: any) -> PendingMail:
        pass

    # Begin the process of mailing a mailable class instance.
    def bcc(self, users: any) -> PendingMail:
        pass

    # Send a new message with only a raw text part.
    def raw(self, text: str, callback: any) -> SentMessage | None:
        pass

    # Send a new message using a view.
    def send(self, view: str | list, data: dict, callback: callable | str | None) -> int:
        pass
