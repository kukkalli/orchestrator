import logging
from typing import List, Dict

from topology.node import Node
from topology.switch_port import SwitchPort

LOG = logging.getLogger(__name__)


class Switch(Node):

    def __init__(self, int_id: int, str_id: str, name: str):
        super().__init__(int_id, str_id, name)

        self.ports: List[SwitchPort] = []
        self.ports_dict: Dict[str, SwitchPort] = {}

    def add_port(self, port: SwitchPort) -> None:
        port.switch_id = self.id
        self.ports.append(port)
        self.ports_dict[port.id] = port

    def remove_port(self, port: SwitchPort) -> None:
        self.ports.remove(port)
        del self.ports_dict[port.id]

    def get_ports(self) -> List[SwitchPort]:
        return self.ports

    def get_port_by_id(self, _id) -> SwitchPort:
        return self.ports_dict.get(_id)
