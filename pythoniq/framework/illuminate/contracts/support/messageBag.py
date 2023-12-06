from pythoniq.framework.illuminate.contracts.support.arrayable import Arrayable
from pythoniq.framework.illuminate.contracts.support.messageProvider import MessageProvider


class MessageBag(Arrayable):
    # Get the keys present in the message bag.
    def keys(self) -> list:
        pass

    # Add a message to the bag.
    def add(self, key: str, message: str) -> None:
        pass

    # Merge a new array of messages into the bag.
    def merge(self, messages: dict | list | MessageProvider) -> None:
        pass

    # Determine if messages exist for a given key.
    def has(self, key: str | dict | list = None) -> bool:
        pass

    # Get the first message from the bag for a given key.
    def first(self, key: str | None = None, format: str | None = None) -> str:
        pass

    # Get all of the messages from the bag for a given key.
    def get(self, key: str | None = None, format: str | None = None) -> list:
        pass

    # Get all of the messages for every key in the bag.
    def all(self, format: str | None = None) -> list:
        pass

    # Remove a message from the bag.
    def forget(self, key: str):
        pass

    # Get the raw messages in the container.
    def getMessages(self) -> dict:
        pass

    # Get the default message format.
    def getFormat(self) -> str:
        pass

    # Set the default message format.
    def setFormat(self, format: str = ':message') -> None:
        pass

    # Determine if the message bag has any messages.
    def isEmpty(self) -> bool:
        pass

    # Determine if the message bag has any messages.
    def isNotEmpty(self) -> bool:
        pass
