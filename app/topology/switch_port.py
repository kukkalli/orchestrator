import logging

from topology.link import Link
from topology.port_state import PortState
from topology.port_stats import PortStats

LOG = logging.getLogger(__name__)


class SwitchPort:
    def __init__(self, switch_id, port):
        self.__json = port
        LOG.debug(f"port: {port}")
        self.switch_id = switch_id
        self.__id = port['id']
        self.hardware_address = port["flow-node-inventory:hardware-address"]
        self.supported = port["flow-node-inventory:supported"]
        self.peer_features = port["flow-node-inventory:peer-features"]
        self.advertised_features = port["flow-node-inventory:advertised-features"]
        self.name = port["flow-node-inventory:name"]
        self.port_number = port["flow-node-inventory:port-number"]
        self.capacity = port["flow-node-inventory:current-speed"]
        self.configuration = port["flow-node-inventory:configuration"]
        self.current_feature = port["flow-node-inventory:current-feature"]
        self.maximum_speed = port["flow-node-inventory:maximum-speed"]
        self.reason = None
        if "flow-node-inventory:reason" in port:
            self.reason = port["flow-node-inventory:reason"]
        self.port_state = PortState(port["flow-node-inventory:state"])
        self.port_stats = PortStats(port['opendaylight-port-statistics:flow-capable-node-connector-statistics'])
        self._mac: str = ""
        self.in_link: Link or None = None
        self.out_link: Link or None = None

    """
    def __init__(self, _id: str, name: str, port_number: str, switch_id: str, capacity: int,
                 port_stats: PortStats = None, port_state: PortState = None):
        self.__id = _id
        self.name = name
        self.__port_number = port_number
        self.switch_id = switch_id
        self.capacity = capacity
        self.port_state = port_state
        self.port_stats = port_stats
        self._mac: str = ""
        self.in_link: Link or None = None
        self.out_link: Link or None = None
    """

    @property
    def id(self):
        return self.__id

    def get_mac(self):
        return self._mac

    def set_mac(self, mac: str):
        self._mac = mac

    def set_in_link(self, link: Link):
        self.in_link = link

    def set_out_link(self, link: Link):
        self.out_link = link

    def get_port_state(self):
        return self.port_state

    def get_port_stats(self):
        return self.port_stats
