from typing import List
from utilities.list_utility import add_elements


class SwitchFeatures(object):
    def __init__(self, switch_features):
        self.__json = switch_features
        self.max_tables = switch_features["max_tables"]
        self.list_capabilities: List[str] = []
        self.max_buffers = switch_features["max_buffers"]
        add_elements(self.list_capabilities, switch_features["capabilities"])

    def to_string(self) -> str:
        return self.__json
