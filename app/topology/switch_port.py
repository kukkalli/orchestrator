import logging

from topology.link import Link
from topology.port_stats import PortStats

LOG = logging.getLogger(__name__)


class SwitchPort:
    def __init__(self, _id: str, name: str, port_number: str, switch_id: str, capacity: int,
                 port_stats: PortStats = None):
        self.__id = _id
        self.name = name
        self.__port_number = port_number
        self.switch_id = switch_id
        self.capacity = capacity
        self.port_stats = port_stats
        self._mac: str = ""
        self.in_link: Link or None = None
        self.out_link: Link or None = None

    @property
    def id(self):
        return self.__id

    @property
    def port_number(self):
        return self.__port_number

    def get_mac(self):
        return self._mac

    def set_mac(self, mac: str):
        self._mac = mac

    def set_in_link(self, link: Link):
        self.in_link = link

    def set_out_link(self, link: Link):
        self.out_link = link
