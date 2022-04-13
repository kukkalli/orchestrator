import logging
from typing import List

from utilities.list_utility import add_elements

LOG = logging.getLogger(__name__)


class GroupFeatures(object):
    def __init__(self, group_features):
        self.__json = group_features
        self.list_group_types_supported: List[str] = []
        self.list_max_groups: List[int] = []
        self.list_group_capabilities_supported: List[str] = []
        self.list_actions: List[int] = []
        add_elements(self.list_group_types_supported, group_features["group-types-supported"])
        add_elements(self.list_max_groups, group_features["max-groups"])
        add_elements(self.list_group_capabilities_supported, group_features["group-capabilities-supported"])
        add_elements(self.list_actions, group_features["actions"])

    def to_string(self) -> str:
        return self.__json
