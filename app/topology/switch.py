from typing import List, Dict

from topology.node import Node
from topology.switch_port import SwitchPort


class Switch(Node):

    def __init__(self, _id, int_id: int):
        super().__init__(_id, int_id)

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
