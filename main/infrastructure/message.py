from enum import Enum

from main import messages


class MessageCategory(Enum):
    INFO = 'INFO'
    ERROR = 'ERROR'
    VALIDATION = 'VALIDATION'
    WARNING = 'WARNING'


class Message(object):
    def __init__(self, category=None, target=None, key=None, args=None):
        self.category = category
        self.target = target
        self.key = key
        self.args = args if args else []

    @property
    def content(self) -> str:
        message = messages[self.key]
        return message.format(*self.args)
