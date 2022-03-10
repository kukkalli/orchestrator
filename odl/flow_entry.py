from typing import List

from odl.flow_instruction import FlowInstruction
from odl.flow_match import FlowMatch
from odl.flow_statistics import FlowStatistics
from utilities.list_utility import add_elements_with_type


class FlowEntry(object):
    def __init__(self, flow_entry):
        self.__json = flow_entry
        self.__id = flow_entry["id"]
        self.table_id = flow_entry["table_id"]
        self.flow_statistics = FlowStatistics(flow_entry["opendaylight-flow-statistics:flow-statistics"])
        self.priority = flow_entry["priority"]
        self.hard_timeout = flow_entry["hard-timeout"]
        self.match = None
        if "match" in flow_entry:
            self.match = FlowMatch(flow_entry["match"])
            print(f"FlowID{self.id} match:{self.match.to_string()}")
        self.cookie_mask = flow_entry["cookie_mask"]
        self.cookie = flow_entry["cookie"]
        self.flags = flow_entry["flags"]
        self.list_instructions: List[FlowInstruction] = []
        add_elements_with_type(self.list_instructions, flow_entry["instructions"]["instruction"], FlowInstruction)
        self.idle_timeout = flow_entry["idle-timeout"]

    @property
    def id(self):
        return self.__id

    def to_string(self) -> str:
        return self.__json
