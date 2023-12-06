class InvalidPayloadException(Exception):
    # The value that failed to decode.
    value: str = None

    # Create a new exception instance.
    def __init__(self, value: str):
        self.value = value
