import logging

LOG = logging.getLogger(__name__)


class FlowTableStatistics(object):
    def __init__(self, flow_table_statistics):
        self.__json = flow_table_statistics
        self.packets_looked_up = flow_table_statistics["packets-looked-up"]
        self.active_flows = flow_table_statistics["active-flows"]
        self.packets_matched = flow_table_statistics["packets-matched"]

    def to_string(self) -> str:
        return self.__json
