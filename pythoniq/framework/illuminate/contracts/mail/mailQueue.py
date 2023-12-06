from pythoniq.framework.illuminate.contracts.mail.mailable import Mailable


class MailQueue:
    # Queue a new e-mail message for sending.
    def queue(self, view: Mailable | str | list | dict, queue: str | None = None) -> None:
        pass

    # Queue a new e-mail message for sending after (n) seconds.
    def later(self, delay: int, view: Mailable | str | list | dict, queue: str | None = None) -> None:
        pass
