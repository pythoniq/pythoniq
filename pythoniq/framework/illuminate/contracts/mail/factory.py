from pythoniq.framework.illuminate.contracts.mail.mailer import Mailer


class Factory:
    # Get a mailer instance by name.
    def mailer(self, name: str = None) -> Mailer:
        pass
