import logging

from odl.duration import Duration

LOG = logging.getLogger(__name__)


class FlowStatistics(object):
    def __init__(self, flow_statistics):
        self.__json = flow_statistics
        self.duration = Duration(flow_statistics["duration"])
        self.packet_count = flow_statistics["packet-count"]
        self.byte_count = flow_statistics["byte-count"]

    def to_string(self) -> str:
        return self.__json
