from topology.link import Link
from topology.node import Node
from topology.server import Server
from topology.switch import Switch
from typing import List, Dict


class Topology:

    def __init__(self, _id: str, links: List[Link], servers: List[Server], switches: List[Switch]):
        self.__id = _id
        self.links = links
        self.nodes: List[Node] = []
        self.servers = servers
        self.servers_dict: Dict[int, Server] = {}
        for server in servers:
            self.servers_dict[server.int_id] = server
            self.nodes.append(server)
        self.switches = switches
        self.switches_dict: Dict[int, Switch] = {}
        for switch in switches:
            self.switches_dict[switch.int_id] = switch
            self.nodes.append(switch)

    @property
    def id(self):
        return self.__id

    def build(self):
        for link in self.links:
            switch_id, port_id = "", ""
            try:
                switch_id = link.dst_node_id
                port_id = link.dst_port_id
                if link.dst_port_id is not None:
                    self.switches_dict[link.dst_node_id].ports_dict[link.dst_port_id].set_in_link(link)
                else:
                    self.servers_dict[link.dst_node_id].add_in_link(link)
                switch_id = link.src_node_id
                port_id = link.src_port_id
                if link.src_port_id is not None:
                    self.switches_dict[link.src_node_id].ports_dict[link.src_port_id].set_out_link(link)
                else:
                    self.servers_dict[link.src_node_id].add_out_link(link)
            except RuntimeError:
                print("Invalid switch {} or switch port {}".format(switch_id, port_id))

    def add_server(self, server: Server) -> None:
        self.servers.append(server)

    def add_switch(self, switch: Switch) -> None:
        self.switches.append(switch)

    def add_link(self, link: Link) -> None:
        self.links.append(link)

    def get_switch_by_int_id(self, int_id: int) -> Switch:
        return self.switches_dict[int_id]
