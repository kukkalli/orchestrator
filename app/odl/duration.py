import logging

LOG = logging.getLogger(__name__)


class Duration(object):
    def __init__(self, duration):
        self.__json = duration
        self.nanosecond = duration["nanosecond"]
        self.second = duration["second"]

    def to_string(self) -> str:
        return self.__json
