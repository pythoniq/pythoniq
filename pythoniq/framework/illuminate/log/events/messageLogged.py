class MessageLogged:
    # The log "level".
    level: str

    # The log message.
    message: str

    # The log context.
    context: dict

    # Create a new event instance.
    def __init__(self, level: str, message: str, context: dict):
        self.level = level
        self.message = message
        self.context = context
