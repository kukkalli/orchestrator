import logging
from typing import List

from utilities.list_utility import add_elements_with_type

LOG = logging.getLogger(__name__)


class FlowInstruction(object):
    def __init__(self, flow_instruction):
        self.__json = flow_instruction
        self.order = flow_instruction["order"]
        self.list_actions: List[FlowAction] = []
        add_elements_with_type(self.list_actions, flow_instruction["apply-actions"]["action"], FlowAction)

    def to_string(self) -> str:
        return self.__json


class FlowAction(object):
    def __init__(self, action):
        self.__json = action
        self.order = action["order"]
        self.output_action = OutputAction(action["output-action"])

    def to_string(self) -> str:
        return self.__json


class OutputAction(object):
    def __init__(self, output_action):
        self.__json = output_action
        self.output_node_connector = output_action["output-node-connector"]
        self.max_length = output_action["max-length"]

    def to_string(self) -> str:
        return self.__json

