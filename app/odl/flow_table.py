import logging
from typing import List, Dict

from odl.flow_entry import FlowEntry
from odl.table_statistics import FlowTableStatistics
from utilities.list_utility import add_elements_with_type

LOG = logging.getLogger(__name__)


class FlowTable(object):
    def __init__(self, table):
        self.__json = table
        self.__id = table["id"]
        self.statistics = FlowTableStatistics(table["opendaylight-flow-table-statistics:flow-table-statistics"])
        self.list_flows: List[FlowEntry] = []
        self.dict_flows_by_match: Dict[str, FlowEntry] = {}
        self.dict_flows_by_id: Dict[str, FlowEntry] = {}
        if "flow" in table:
            add_elements_with_type(self.list_flows, table["flow"], FlowEntry)
        for flow in self.list_flows:
            self.dict_flows_by_id[flow.id] = flow
            if flow.match:
                key: str = ""
                if flow.match.ipv4_source:
                    ip = flow.match.ipv4_source.split("/")
                    key = key + "s:" + ip[0]
                if flow.match.ipv4_destination:
                    if len(key) > 0:
                        key = key + "_"
                    ip = flow.match.ipv4_destination.split("/")
                    key = key + "d:" + ip[0]
                if len(key) > 0:
                    self.dict_flows_by_match[key] = flow

    @property
    def id(self):
        return self.__id

    def to_string(self) -> str:
        return self.__json

    def get_flow_by_src_ip_dest_ip(self, src_ip: str, dst_ip: str):
        key: str = ""
        if len(src_ip) > 0:
            src_ip = src_ip.split("/")
            key = "s:" + src_ip[0]
        if len(dst_ip) > 0:
            if len(key) > 0:
                key = key + "_"
            dst_ip = dst_ip.split("/")
            key = key + "d:" + dst_ip[0]
        return self.dict_flows_by_match[key]

    def get_flow_by_id(self, flow_id):
        return self.dict_flows_by_id[flow_id]
